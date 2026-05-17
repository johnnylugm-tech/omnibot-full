"""[FR-18] Intent Router + Dialogue State Tracker (DST) — 7-state FSM.

ConversationState enum, DialogueSlot frozen dataclass, and DialogueState
with immutable state transitions and slot-filling support.

Citations: SRS.md:110-133, SAD.md:363-399
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ConversationState(str, Enum):
    IDLE = "IDLE"
    INTENT_DETECTED = "INTENT_DETECTED"
    SLOT_FILLING = "SLOT_FILLING"
    AWAITING_CONFIRMATION = "AWAITING_CONFIRMATION"
    PROCESSING = "PROCESSING"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"


@dataclass(frozen=True)
class DialogueSlot:
    name: str
    value: Any | None = None
    required: bool = False
    prompt: str = ""


_ALLOWED_TRANSITIONS = frozenset({
    (ConversationState.IDLE, ConversationState.INTENT_DETECTED),
    (ConversationState.INTENT_DETECTED, ConversationState.PROCESSING),
    (ConversationState.INTENT_DETECTED, ConversationState.SLOT_FILLING),
    (ConversationState.SLOT_FILLING, ConversationState.AWAITING_CONFIRMATION),
    (ConversationState.SLOT_FILLING, ConversationState.ESCALATED),
    (ConversationState.AWAITING_CONFIRMATION, ConversationState.PROCESSING),
    (ConversationState.AWAITING_CONFIRMATION, ConversationState.SLOT_FILLING),
    (ConversationState.PROCESSING, ConversationState.RESOLVED),
    (ConversationState.PROCESSING, ConversationState.ESCALATED),
    (ConversationState.ESCALATED, ConversationState.RESOLVED),
})


@dataclass(frozen=True)
class DialogueState:
    conversation_id: str
    current_state: ConversationState = ConversationState.IDLE
    primary_intent: str | None = None
    sub_intents: list[str] = field(default_factory=list)
    slots: dict[str, DialogueSlot] = field(default_factory=dict)
    turn_count: int = 0
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def transition(self, new_state: ConversationState) -> DialogueState:
        if (self.current_state, new_state) not in _ALLOWED_TRANSITIONS:
            raise ValueError(
                f"Invalid transition: {self.current_state.value} -> {new_state.value}"
            )
        return DialogueState(
            conversation_id=self.conversation_id,
            current_state=new_state,
            primary_intent=self.primary_intent,
            sub_intents=list(self.sub_intents),
            slots=dict(self.slots),
            turn_count=self.turn_count + 1,
            last_updated=datetime.now(timezone.utc),
        )

    def missing_slots(self) -> list[DialogueSlot]:
        return [s for s in self.slots.values() if s.required and s.value is None]
