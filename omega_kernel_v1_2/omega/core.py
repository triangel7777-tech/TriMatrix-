"""Core Ω transition kernel.

Formal law:
    S[t+1] = argmax_{s' in T(S[t]), I(s')=True} (U(s'), -tau(s'))
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, List, Optional, TypeVar

S = TypeVar("S")


@dataclass(frozen=True)
class OmegaResult(Generic[S]):
    """Evidence payload for one Ω transition."""

    step_index: int
    previous_state: S
    candidates: List[S]
    valid_candidates: List[S]
    selected_state: S
    selected_utility: float
    selected_tiebreak: float


class OmegaDeadStateError(RuntimeError):
    """Raised when no valid next state exists."""


class Omega(Generic[S]):
    """Auditable constrained future-state selection kernel."""

    def __init__(
        self,
        transition: Callable[[S], Iterable[S]],
        invariant: Callable[[S], bool],
        utility: Callable[[S], float],
        tiebreak: Optional[Callable[[S], float]] = None,
    ) -> None:
        self.transition = transition
        self.invariant = invariant
        self.utility = utility
        self.tiebreak = tiebreak or (lambda _s: 0.0)
        self._step_counter = 0

    def candidates(self, state: S) -> List[S]:
        return list(self.transition(state))

    def valid_candidates(self, state: S) -> List[S]:
        return [candidate for candidate in self.candidates(state) if self.invariant(candidate)]

    def select(self, valid_candidates: List[S]) -> S:
        if not valid_candidates:
            raise OmegaDeadStateError("No valid next state exists. Ω entered a dead state.")
        return max(valid_candidates, key=lambda s: (self.utility(s), -self.tiebreak(s)))

    def step(self, state: S) -> OmegaResult[S]:
        candidates = self.candidates(state)
        valid = [candidate for candidate in candidates if self.invariant(candidate)]
        selected = self.select(valid)
        result = OmegaResult(
            step_index=self._step_counter,
            previous_state=state,
            candidates=candidates,
            valid_candidates=valid,
            selected_state=selected,
            selected_utility=float(self.utility(selected)),
            selected_tiebreak=float(self.tiebreak(selected)),
        )
        self._step_counter += 1
        return result

    def run(self, initial_state: S, steps: int) -> List[OmegaResult[S]]:
        if steps < 0:
            raise ValueError("steps must be non-negative")
        state = initial_state
        trajectory: List[OmegaResult[S]] = []
        for _ in range(steps):
            result = self.step(state)
            trajectory.append(result)
            state = result.selected_state
        return trajectory
