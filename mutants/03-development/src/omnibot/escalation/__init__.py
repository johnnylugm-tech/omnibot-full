"""[FR-08] Basic Escalation Manager — No SLA.

In-memory escalation queue: create, assign, resolve.
Phase 1 stores sla_deadline as NULL (activated Phase 2).

Citations: SRS.md FR-08 section, SAD.md 2.4.1 EscalationService
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁEscalationManagerǁ__init____mutmut_orig(self) -> None:
        """Initialize in-memory escalation queue with auto-incrementing IDs."""
        self._records: Dict[int, EscalationRecord] = {}
        self._next_id: int = 1

    def xǁEscalationManagerǁ__init____mutmut_1(self) -> None:
        """Initialize in-memory escalation queue with auto-incrementing IDs."""
        self._records: Dict[int, EscalationRecord] = None
        self._next_id: int = 1

    def xǁEscalationManagerǁ__init____mutmut_2(self) -> None:
        """Initialize in-memory escalation queue with auto-incrementing IDs."""
        self._records: Dict[int, EscalationRecord] = {}
        self._next_id: int = None

    def xǁEscalationManagerǁ__init____mutmut_3(self) -> None:
        """Initialize in-memory escalation queue with auto-incrementing IDs."""
        self._records: Dict[int, EscalationRecord] = {}
        self._next_id: int = 2
    
    xǁEscalationManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEscalationManagerǁ__init____mutmut_1': xǁEscalationManagerǁ__init____mutmut_1, 
        'xǁEscalationManagerǁ__init____mutmut_2': xǁEscalationManagerǁ__init____mutmut_2, 
        'xǁEscalationManagerǁ__init____mutmut_3': xǁEscalationManagerǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEscalationManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁEscalationManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁEscalationManagerǁ__init____mutmut_orig)
    xǁEscalationManagerǁ__init____mutmut_orig.__name__ = 'xǁEscalationManagerǁ__init__'

    def xǁEscalationManagerǁcreate__mutmut_orig(self, conversation_id: str, reason: str) -> int:
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

    def xǁEscalationManagerǁcreate__mutmut_1(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = None
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_2(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=None,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_3(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=None,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_4(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=None,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_5(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=None,
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_6(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_7(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_8(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_9(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_10(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(None),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_11(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = None
        eid = self._next_id
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_12(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = None
        self._next_id += 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_13(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id = 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_14(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id -= 1
        return eid

    def xǁEscalationManagerǁcreate__mutmut_15(self, conversation_id: str, reason: str) -> int:
        """Create a new escalation record. Returns escalation_id."""
        record = EscalationRecord(
            escalation_id=self._next_id,
            conversation_id=conversation_id,
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )
        self._records[self._next_id] = record
        eid = self._next_id
        self._next_id += 2
        return eid
    
    xǁEscalationManagerǁcreate__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEscalationManagerǁcreate__mutmut_1': xǁEscalationManagerǁcreate__mutmut_1, 
        'xǁEscalationManagerǁcreate__mutmut_2': xǁEscalationManagerǁcreate__mutmut_2, 
        'xǁEscalationManagerǁcreate__mutmut_3': xǁEscalationManagerǁcreate__mutmut_3, 
        'xǁEscalationManagerǁcreate__mutmut_4': xǁEscalationManagerǁcreate__mutmut_4, 
        'xǁEscalationManagerǁcreate__mutmut_5': xǁEscalationManagerǁcreate__mutmut_5, 
        'xǁEscalationManagerǁcreate__mutmut_6': xǁEscalationManagerǁcreate__mutmut_6, 
        'xǁEscalationManagerǁcreate__mutmut_7': xǁEscalationManagerǁcreate__mutmut_7, 
        'xǁEscalationManagerǁcreate__mutmut_8': xǁEscalationManagerǁcreate__mutmut_8, 
        'xǁEscalationManagerǁcreate__mutmut_9': xǁEscalationManagerǁcreate__mutmut_9, 
        'xǁEscalationManagerǁcreate__mutmut_10': xǁEscalationManagerǁcreate__mutmut_10, 
        'xǁEscalationManagerǁcreate__mutmut_11': xǁEscalationManagerǁcreate__mutmut_11, 
        'xǁEscalationManagerǁcreate__mutmut_12': xǁEscalationManagerǁcreate__mutmut_12, 
        'xǁEscalationManagerǁcreate__mutmut_13': xǁEscalationManagerǁcreate__mutmut_13, 
        'xǁEscalationManagerǁcreate__mutmut_14': xǁEscalationManagerǁcreate__mutmut_14, 
        'xǁEscalationManagerǁcreate__mutmut_15': xǁEscalationManagerǁcreate__mutmut_15
    }
    
    def create(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEscalationManagerǁcreate__mutmut_orig"), object.__getattribute__(self, "xǁEscalationManagerǁcreate__mutmut_mutants"), args, kwargs, self)
        return result 
    
    create.__signature__ = _mutmut_signature(xǁEscalationManagerǁcreate__mutmut_orig)
    xǁEscalationManagerǁcreate__mutmut_orig.__name__ = 'xǁEscalationManagerǁcreate'

    def xǁEscalationManagerǁassign__mutmut_orig(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_1(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = None
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_2(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(None)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_3(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is not None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_4(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(None)
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_5(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = None
        record.picked_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁassign__mutmut_6(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = None

    def xǁEscalationManagerǁassign__mutmut_7(self, escalation_id: int, agent_id: str) -> None:
        """Assign an agent to the escalation."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.assigned_agent = agent_id
        record.picked_at = datetime.now(None)
    
    xǁEscalationManagerǁassign__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEscalationManagerǁassign__mutmut_1': xǁEscalationManagerǁassign__mutmut_1, 
        'xǁEscalationManagerǁassign__mutmut_2': xǁEscalationManagerǁassign__mutmut_2, 
        'xǁEscalationManagerǁassign__mutmut_3': xǁEscalationManagerǁassign__mutmut_3, 
        'xǁEscalationManagerǁassign__mutmut_4': xǁEscalationManagerǁassign__mutmut_4, 
        'xǁEscalationManagerǁassign__mutmut_5': xǁEscalationManagerǁassign__mutmut_5, 
        'xǁEscalationManagerǁassign__mutmut_6': xǁEscalationManagerǁassign__mutmut_6, 
        'xǁEscalationManagerǁassign__mutmut_7': xǁEscalationManagerǁassign__mutmut_7
    }
    
    def assign(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEscalationManagerǁassign__mutmut_orig"), object.__getattribute__(self, "xǁEscalationManagerǁassign__mutmut_mutants"), args, kwargs, self)
        return result 
    
    assign.__signature__ = _mutmut_signature(xǁEscalationManagerǁassign__mutmut_orig)
    xǁEscalationManagerǁassign__mutmut_orig.__name__ = 'xǁEscalationManagerǁassign'

    def xǁEscalationManagerǁresolve__mutmut_orig(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁresolve__mutmut_1(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = None
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁresolve__mutmut_2(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(None)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁresolve__mutmut_3(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is not None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁresolve__mutmut_4(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(None)
        record.resolved_at = datetime.now(timezone.utc)

    def xǁEscalationManagerǁresolve__mutmut_5(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = None

    def xǁEscalationManagerǁresolve__mutmut_6(self, escalation_id: int) -> None:
        """Mark escalation as resolved."""
        record = self._records.get(escalation_id)
        if record is None:
            raise KeyError(f"Escalation {escalation_id} not found")
        record.resolved_at = datetime.now(None)
    
    xǁEscalationManagerǁresolve__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEscalationManagerǁresolve__mutmut_1': xǁEscalationManagerǁresolve__mutmut_1, 
        'xǁEscalationManagerǁresolve__mutmut_2': xǁEscalationManagerǁresolve__mutmut_2, 
        'xǁEscalationManagerǁresolve__mutmut_3': xǁEscalationManagerǁresolve__mutmut_3, 
        'xǁEscalationManagerǁresolve__mutmut_4': xǁEscalationManagerǁresolve__mutmut_4, 
        'xǁEscalationManagerǁresolve__mutmut_5': xǁEscalationManagerǁresolve__mutmut_5, 
        'xǁEscalationManagerǁresolve__mutmut_6': xǁEscalationManagerǁresolve__mutmut_6
    }
    
    def resolve(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEscalationManagerǁresolve__mutmut_orig"), object.__getattribute__(self, "xǁEscalationManagerǁresolve__mutmut_mutants"), args, kwargs, self)
        return result 
    
    resolve.__signature__ = _mutmut_signature(xǁEscalationManagerǁresolve__mutmut_orig)
    xǁEscalationManagerǁresolve__mutmut_orig.__name__ = 'xǁEscalationManagerǁresolve'

    def xǁEscalationManagerǁget__mutmut_orig(self, escalation_id: int) -> Optional[EscalationRecord]:
        """Retrieve an escalation record by ID."""
        return self._records.get(escalation_id)

    def xǁEscalationManagerǁget__mutmut_1(self, escalation_id: int) -> Optional[EscalationRecord]:
        """Retrieve an escalation record by ID."""
        return self._records.get(None)
    
    xǁEscalationManagerǁget__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEscalationManagerǁget__mutmut_1': xǁEscalationManagerǁget__mutmut_1
    }
    
    def get(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEscalationManagerǁget__mutmut_orig"), object.__getattribute__(self, "xǁEscalationManagerǁget__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get.__signature__ = _mutmut_signature(xǁEscalationManagerǁget__mutmut_orig)
    xǁEscalationManagerǁget__mutmut_orig.__name__ = 'xǁEscalationManagerǁget'
