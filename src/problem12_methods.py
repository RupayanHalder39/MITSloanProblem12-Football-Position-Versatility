"""Public-safe core calculations for MIT Sloan Problem 12.

These functions demonstrate the frozen role graph, tactical distance, profile
divergence, and typology decision logic. They do not load restricted source rows.
"""

from __future__ import annotations

import math
from collections import deque
from collections.abc import Iterable, Mapping, Sequence


ROLES = ("CB", "FB", "WB", "DM", "CM", "AM", "W", "ST")
BASELINE_EDGES = (
    ("CB", "FB"), ("CB", "DM"), ("FB", "WB"), ("FB", "CM"),
    ("WB", "W"), ("DM", "CM"), ("CM", "AM"), ("CM", "W"),
    ("AM", "W"), ("AM", "ST"), ("W", "ST"),
)
CONSERVATIVE_EDGES = (
    ("CB", "FB"), ("CB", "DM"), ("FB", "WB"), ("WB", "W"),
    ("DM", "CM"), ("CM", "AM"), ("AM", "W"), ("AM", "ST"),
    ("W", "ST"),
)
SCORE_NAMES = ("attack", "progression", "possession", "defense")


def build_graph(edges: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    graph = {role: set() for role in ROLES}
    for left, right in edges:
        if left not in graph or right not in graph:
            raise ValueError(f"Unknown role in edge: {left!r}, {right!r}")
        graph[left].add(right)
        graph[right].add(left)
    return graph


def shortest_path_distance(role_a: str, role_b: str, *, edges=CONSERVATIVE_EDGES) -> int:
    """Return unweighted role-graph distance; this is not distance in metres."""
    graph = build_graph(edges)
    if role_a not in graph or role_b not in graph:
        raise ValueError("Both roles must belong to the frozen outfield taxonomy")
    queue = deque([(role_a, 0)])
    visited = {role_a}
    while queue:
        role, distance = queue.popleft()
        if role == role_b:
            return distance
        for neighbor in graph[role] - visited:
            visited.add(neighbor)
            queue.append((neighbor, distance + 1))
    raise ValueError(f"Disconnected roles: {role_a}, {role_b}")


def profile_differences(role_a_scores: Mapping[str, float], role_b_scores: Mapping[str, float]) -> dict[str, float]:
    """Calculate Role A minus Role B for the four standardized dimensions."""
    missing = [name for name in SCORE_NAMES if name not in role_a_scores or name not in role_b_scores]
    if missing:
        raise ValueError(f"Missing profile dimensions: {missing}")
    return {name: float(role_a_scores[name]) - float(role_b_scores[name]) for name in SCORE_NAMES}


def profile_divergence(differences: Mapping[str, float] | Sequence[float]) -> float:
    """Euclidean divergence across Attack, Progression, Possession, and Defense."""
    values = [float(differences[name]) for name in SCORE_NAMES] if isinstance(differences, Mapping) else [float(value) for value in differences]
    if len(values) != 4:
        raise ValueError("Exactly four standardized score differences are required")
    return math.sqrt(sum(value * value for value in values))


def classify_typology(
    differences: Mapping[str, float],
    *,
    profile_value: float,
    neutral_threshold: float,
    meaningful_threshold: float,
    significant_dimensions: int,
    matches_role_a: int,
    matches_role_b: int,
    stable_flags: int,
    context_adjusted_stability: str,
    minimum_matches: int = 8,
) -> str:
    """Mirror the frozen Phase 4 typology decision order for one comparison."""
    meaningful = [value for value in differences.values() if abs(value) >= meaningful_threshold]
    positive = any(value > 0 for value in meaningful)
    negative = any(value < 0 for value in meaningful)
    if profile_value <= neutral_threshold and significant_dimensions <= 1:
        return "POSITIONALLY_NEUTRAL"
    if matches_role_a < minimum_matches or matches_role_b < minimum_matches or significant_dimensions == 0 or context_adjusted_stability == "inconsistent":
        return "INSUFFICIENT_EVIDENCE"
    if positive and negative and stable_flags >= 2:
        return "CONTEXT_DEPENDENT_TRADEOFF"
    if meaningful and len({math.copysign(1, value) for value in meaningful}) <= 1 and significant_dimensions >= 2 and stable_flags >= 2:
        return "STABLE_POSITIONAL_ADVANTAGE"
    if profile_value <= neutral_threshold:
        return "POSITIONALLY_NEUTRAL"
    return "INSUFFICIENT_EVIDENCE"
