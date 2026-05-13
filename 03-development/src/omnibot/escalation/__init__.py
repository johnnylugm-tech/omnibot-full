"""[FR-08] Basic Escalation Manager — No SLA.

In-memory escalation queue: create, assign, resolve.
Phase 1 stores sla_deadline as NULL (activated Phase 2).

Citations: SRS.md FR-08 section, SAD.md 2.4.1 EscalationService
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass
class EscalationRecord:
    """Single escalation queue entry.

    Citations: SRS.md FR-08, SAD.md 2.4.1
    """
    escalation_id: int
    conversation_id: str
    reason: str
    created_at: datetime
    assigned_agent: Optional[str] = None
    picked_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    sla_deadline: Optional[datetime] = None


class EscalationManager:
    """In-memory escalation queue with create/assign/resolve lifecycle.

    Citations: SAD.md 2.4.1 EscalationService
    """

    def __init__(self) -> None:
        self._records: Dict[int, EscalationRecord] = {}
        self._next_id: int = 1

    def create(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def assign(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def resolve(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(timezone.utc)

    def get(self, escalation_id: int) -> Optional[EscalationRecord]:
        """Retrieve an escalation record by ID."""
        return self._records.get(escalation_id)
