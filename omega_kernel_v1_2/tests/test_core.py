from omega import Omega, OmegaDeadStateError


def test_numeric_attractor_reaches_ten_and_stabilizes():
    omega = Omega(
        transition=lambda s: [s - 1, s, s + 1, s + 2],
        invariant=lambda s: 0 <= s <= 10,
        utility=lambda s: -abs(10 - s),
        tiebreak=lambda s: s,
    )
    results = omega.run(0, 8)
    selected = [r.selected_state for r in results]
    assert selected[:5] == [2, 4, 6, 8, 10]
    assert selected[-1] == 10


def test_tiebreak_prefers_lower_score_when_utility_ties():
    omega = Omega(
        transition=lambda s: [1, 2],
        invariant=lambda s: True,
        utility=lambda s: 1.0,
        tiebreak=lambda s: float(s),
    )
    assert omega.step(0).selected_state == 1


def test_run_rejects_negative_steps():
    omega = Omega(lambda s: [s], lambda s: True, lambda s: 0.0)
    try:
        omega.run(0, -1)
    except ValueError as exc:
        assert "steps" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_dead_state_raises():
    omega = Omega(lambda s: [s + 1], lambda s: False, lambda s: 0.0)
    try:
        omega.step(0)
    except OmegaDeadStateError as exc:
        assert "dead state" in str(exc)
    else:
        raise AssertionError("Expected OmegaDeadStateError")
