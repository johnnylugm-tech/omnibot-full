"""[FR-20] EscalationManagerV2 — SLA Priority Levels.

Acceptance criteria:
  - EscalationRequest frozen dataclass: conversation_id, reason, priority
  - EscalationReason enum: out_of_scope, low_confidence, emotion_trigger
  - SLA_BY_PRIORITY configurable dict: {0: 30, 1: 15, 2: 5}
  - create(request) looks up SLA_BY_PRIORITY, computes sla_deadline, writes to DB, returns id
  - assign(escalation_id, agent_id) sets assigned_agent + picked_at
  - resolve(escalation_id) sets resolved_at
  - get_sla_breaches() queries resolved_at IS NULL AND sla_deadline < NOW()

Citations: SRS.md:170-186, SAD.md:454-477
"""

from __future__ import annotations

import datetime
from contextlib import asynccontextmanager
from typing import Any, Optional

import pytest

from omnibot.escalation.v2 import (
    EscalationManagerV2,
    EscalationReason,
    EscalationRequest,
    SLA_BY_PRIORITY,
)


# ── Mock helpers ────────────────────────────────────────────────────────────────

class MockConnection:
    """Mock async database connection."""

    def __init__(
        self,
        fetchrow_result: Optional[dict[str, Any]] = None,
        fetch_result: Optional[list[dict[str, Any]]] = None,
    ):
        self._fetchrow_result = fetchrow_result
        self._fetch_result = fetch_result or []
        self.last_sql: str = ""
        self.last_params: list[Any] = []

    async def fetchrow(self, sql: str, *args: Any) -> Optional[dict[str, Any]]:
        self.last_sql = sql
        self.last_params = list(args)
        return self._fetchrow_result

    async def fetch(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        self.last_sql = sql
        self.last_params = list(args)
        return self._fetch_result

    async def execute(self, sql: str, *args: Any) -> str:
        self.last_sql = sql
        self.last_params = list(args)
        return "UPDATE 1"


class MockPool:
    """Mock async database pool that yields MockConnection."""

    def __init__(
        self,
        fetchrow_result: Optional[dict[str, Any]] = None,
        fetch_result: Optional[list[dict[str, Any]]] = None,
    ):
        self._conn = MockConnection(fetchrow_result, fetch_result)

    @asynccontextmanager
    async def acquire(self):
        yield self._conn

    @property
    def connection(self) -> MockConnection:
        return self._conn


# ── Dataclass / Enum ───────────────────────────────────────────────────────────

def test_escalation_request_is_frozen():
    """EscalationRequest is a frozen dataclass — cannot be mutated."""
    req = EscalationRequest(
        conversation_id=42,
        reason=EscalationReason.OUT_OF_SCOPE,
        priority=1,
    )
    with pytest.raises(Exception):
        req.priority = 2  # type: ignore[misc]


def test_escalation_request_fields():
    """EscalationRequest has conversation_id, reason (enum), priority (int)."""
    req = EscalationRequest(
        conversation_id=99,
        reason=EscalationReason.EMOTION_TRIGGER,
        priority=2,
    )
    assert req.conversation_id == 99
    assert req.reason == EscalationReason.EMOTION_TRIGGER
    assert req.priority == 2


def test_escalation_reason_values():
    """EscalationReason has three string values."""
    assert EscalationReason.OUT_OF_SCOPE.value == "out_of_scope"
    assert EscalationReason.LOW_CONFIDENCE.value == "low_confidence"
    assert EscalationReason.EMOTION_TRIGGER.value == "emotion_trigger"


def test_sla_by_priority_default():
    """SLA_BY_PRIORITY default is {0: 30, 1: 15, 2: 5}."""
    assert SLA_BY_PRIORITY == {0: 30, 1: 15, 2: 5}


# ── create ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_returns_escalation_id():
    """create() inserts into DB and returns the new id."""
    pool = MockPool(fetchrow_result={"id": 7})
    mgr = EscalationManagerV2(db_pool=pool)
    req = EscalationRequest(
        conversation_id=10,
        reason=EscalationReason.LOW_CONFIDENCE,
        priority=0,
    )
    eid = await mgr.create(req)
    assert eid == 7


@pytest.mark.asyncio
async def test_create_computes_sla_deadline():
    """create() computes sla_deadline = NOW + SLA_BY_PRIORITY[priority]."""
    pool = MockPool(fetchrow_result={"id": 1})
    mgr = EscalationManagerV2(db_pool=pool)
    req = EscalationRequest(
        conversation_id=42,
        reason=EscalationReason.OUT_OF_SCOPE,
        priority=2,  # urgent -> 5 minutes
    )
    await mgr.create(req)

    sql = pool.connection.last_sql
    assert "INSERT INTO escalation_queue" in sql
    assert "sla_deadline" in sql
    sla_param = pool.connection.last_params[3]
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = sla_param - now
    assert datetime.timedelta(minutes=4, seconds=30) <= delta <= datetime.timedelta(minutes=5, seconds=30)


@pytest.mark.asyncio
async def test_create_uses_reason_enum_value():
    """create() stores reason as the enum string value, not the enum object."""
    pool = MockPool(fetchrow_result={"id": 1})
    mgr = EscalationManagerV2(db_pool=pool)
    req = EscalationRequest(
        conversation_id=10,
        reason=EscalationReason.EMOTION_TRIGGER,
        priority=2,
    )
    await mgr.create(req)
    assert pool.connection.last_params[1] == "emotion_trigger"


@pytest.mark.asyncio
async def test_create_invalid_priority_raises():
    """create() with priority not in SLA_BY_PRIORITY raises ValueError."""
    pool = MockPool(fetchrow_result={"id": 1})
    mgr = EscalationManagerV2(db_pool=pool)
    req = EscalationRequest(
        conversation_id=10,
        reason=EscalationReason.LOW_CONFIDENCE,
        priority=99,
    )
    with pytest.raises(ValueError):
        await mgr.create(req)


# ── assign ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_assign_sets_agent_and_picked_at():
    """assign() updates assigned_agent and picked_at."""
    pool = MockPool(fetchrow_result={"id": 5})
    mgr = EscalationManagerV2(db_pool=pool)
    await mgr.assign(5, "agent_42")

    sql = pool.connection.last_sql
    assert "UPDATE escalation_queue" in sql
    assert "assigned_agent" in sql
    assert "picked_at" in sql
    assert pool.connection.last_params == ["agent_42", 5]


@pytest.mark.asyncio
async def test_assign_nonexistent_raises():
    """assign() on non-existent id raises KeyError."""
    pool = MockPool(fetchrow_result=None)
    mgr = EscalationManagerV2(db_pool=pool)
    with pytest.raises(KeyError):
        await mgr.assign(999, "agent_1")


# ── resolve ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_resolve_sets_resolved_at():
    """resolve() updates resolved_at."""
    pool = MockPool(fetchrow_result={"id": 5})
    mgr = EscalationManagerV2(db_pool=pool)
    await mgr.resolve(5)

    sql = pool.connection.last_sql
    assert "UPDATE escalation_queue" in sql
    assert "resolved_at" in sql
    assert pool.connection.last_params == [5]


@pytest.mark.asyncio
async def test_resolve_nonexistent_raises():
    """resolve() on non-existent id raises KeyError."""
    pool = MockPool(fetchrow_result=None)
    mgr = EscalationManagerV2(db_pool=pool)
    with pytest.raises(KeyError):
        await mgr.resolve(999)


# ── get_sla_breaches ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_sla_breaches_returns_breached_only():
    """get_sla_breaches() returns unresolved items past sla_deadline."""
    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(minutes=10)

    breached_rows = [
        {
            "id": 3, "conversation_id": 10, "reason": "out_of_scope",
            "priority": 2, "sla_deadline": past,
            "assigned_agent": None, "picked_at": None,
            "resolved_at": None, "created_at": past,
        },
        {
            "id": 1, "conversation_id": 7, "reason": "low_confidence",
            "priority": 0, "sla_deadline": past,
            "assigned_agent": None, "picked_at": None,
            "resolved_at": None, "created_at": past,
        },
    ]

    pool = MockPool(fetch_result=breached_rows)
    mgr = EscalationManagerV2(db_pool=pool)
    result = await mgr.get_sla_breaches()

    assert len(result) == 2
    assert result[0]["priority"] == 2
    assert result[1]["priority"] == 0


@pytest.mark.asyncio
async def test_get_sla_breaches_query_structure():
    """get_sla_breaches() SQL filters unresolved + past deadline, orders by priority DESC."""
    pool = MockPool(fetch_result=[])
    mgr = EscalationManagerV2(db_pool=pool)
    await mgr.get_sla_breaches()

    sql = pool.connection.last_sql
    assert "resolved_at IS NULL" in sql
    assert "sla_deadline < NOW()" in sql
    assert "ORDER BY priority DESC" in sql


# ── SLA_BY_PRIORITY configurability ────────────────────────────────────────────

@pytest.mark.asyncio
async def test_sla_by_priority_configurable():
    """SLA_BY_PRIORITY dict can be modified at runtime and create() uses it."""
    original = SLA_BY_PRIORITY.copy()
    try:
        SLA_BY_PRIORITY[0] = 60
        SLA_BY_PRIORITY[3] = 10
        assert SLA_BY_PRIORITY[0] == 60
        assert SLA_BY_PRIORITY[3] == 10

        pool = MockPool(fetchrow_result={"id": 1})
        mgr = EscalationManagerV2(db_pool=pool)
        req = EscalationRequest(
            conversation_id=10,
            reason=EscalationReason.LOW_CONFIDENCE,
            priority=0,
        )
        await mgr.create(req)

        sla_param = pool.connection.last_params[3]
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = sla_param - now
        assert datetime.timedelta(minutes=59, seconds=30) <= delta <= datetime.timedelta(minutes=60, seconds=30)
    finally:
        SLA_BY_PRIORITY.clear()
        SLA_BY_PRIORITY.update(original)


# ── Full lifecycle ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_full_lifecycle():
    """Full lifecycle: create -> assign -> resolve with mocked DB."""
    pool = MockPool(fetchrow_result={"id": 1})
    mgr = EscalationManagerV2(db_pool=pool)

    req = EscalationRequest(
        conversation_id=100,
        reason=EscalationReason.LOW_CONFIDENCE,
        priority=1,
    )
    eid = await mgr.create(req)
    assert eid == 1
    assert "INSERT" in pool.connection.last_sql

    await mgr.assign(eid, "agent_7")
    assert "assigned_agent" in pool.connection.last_sql
    assert pool.connection.last_params == ["agent_7", 1]

    await mgr.resolve(eid)
    assert "resolved_at" in pool.connection.last_sql
    assert pool.connection.last_params == [1]
