#!/usr/bin/env python3
"""Verify the curated public release without requiring restricted source data."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HASHES = {
    "paper/Problem12_Position_as_a_Variable_Not_a_Label.pdf": "77c1221cb1416d48bc41ca12d08b523058e47ea5f14914ead690d80528339ae5",
    "figures/figure1_tactical_role_distance.png": "e5d7a04a96e62e883b43b4460dd9be29a824f1b3e8ba7062632612b92990d309",
    "figures/figure1_tactical_role_distance.svg": "705b79d89081692493aee538e8b72e54af7a917667f0cb1c028a466d9c6b48f8",
    "figures/figure2_versatility_archetypes.png": "1f06be45defd647f0306d3e192a61c2d374ea1cb1e45ee734a1047e15d09516b",
    "assets/RupayanHalder.jpeg": "64e529e780c9e33f5b6408c0ee700fccfbe586c8348ae526643683aecd5fe168",
    "assets/SoccerSolverLogo.png": "726f16865cf5f1bd11c937c8034fb72232a485f4c1882d4dc323f0912ea051f5",
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def close(actual: float, expected: float, tolerance: float = 1e-9) -> bool:
    return math.isclose(float(actual), expected, rel_tol=0.0, abs_tol=tolerance)


def graph_distances(nodes, edges):
    graph = {node: set() for node in nodes}
    for left, right in edges:
        graph[left].add(right); graph[right].add(left)
    distances = {}
    for start in nodes:
        queue = deque([(start, 0)]); seen = {start}
        while queue:
            node, distance = queue.popleft(); distances[(start, node)] = distance
            for neighbor in graph[node] - seen:
                seen.add(neighbor); queue.append((neighbor, distance + 1))
    return distances


def main() -> int:
    required = [
        "README.md", "LICENSE", "CITATION.cff", "data/README.md",
        "docs/methodology.md", "docs/reproducibility.md", "docs/PUBLIC_RELEASE_AUDIT.md",
        "results/frozen_results.json", "src/problem12_methods.py", "src/build_figure1.py",
        *EXPECTED_HASHES,
    ]
    for relative in required:
        check((ROOT / relative).is_file(), f"Missing required file: {relative}")

    frozen = json.loads((ROOT / "results/frozen_results.json").read_text(encoding="utf-8"))
    cohort = frozen["cohort"]
    check(frozen["problem"] == 12, "Wrong problem number")
    check(cohort["player_match_observations"] == 23627, "Observation count changed")
    check(cohort["eligible_players"] == 120, "Player count changed")
    check(cohort["eligible_role_comparisons"] == 159, "Comparison count changed")
    check(close(cohort["role_purity_threshold"], 0.70), "Purity threshold changed")
    check(cohort["minimum_clean_minutes_per_role"] == 600, "Minutes threshold changed")
    check(cohort["minimum_qualifying_matches_per_role"] == 8, "Match threshold changed")

    baseline = frozen["baseline_cross_minus_adjacent"]
    check(close(baseline["estimate"], 0.1873), "Baseline estimate changed")
    check(close(baseline["ci_lower"], 0.0583), "Baseline lower CI changed")
    check(close(baseline["ci_upper"], 0.3285), "Baseline upper CI changed")
    check(close(baseline["cohens_d"], 0.8939), "Cohen's d changed")
    distance = frozen["distance_only"]
    check(close(distance["spearman_rho"], 0.1547), "Authoritative rho changed")
    check(close(distance["permutation_p"], 0.0488), "Permutation p changed")
    consensus = frozen["consensus_only"]
    check(close(consensus["estimate"], 0.1854), "Consensus-only estimate changed")
    check(close(consensus["ci_lower"], 0.0565), "Consensus lower CI changed")
    check(close(consensus["ci_upper"], 0.3241), "Consensus upper CI changed")
    check(sum(item["count"] for item in frozen["typology"].values()) == 159, "Typology counts do not sum to 159")

    nodes = frozen["role_graph"]["nodes"]
    edges = [tuple(edge) for edge in frozen["role_graph"]["conservative_edges"]]
    check(nodes == ["CB", "FB", "WB", "DM", "CM", "AM", "W", "ST"], "Role nodes changed")
    graph = graph_distances(nodes, edges)
    check(set(graph.values()) == {0, 1, 2, 3, 4}, "Unexpected graph distances")
    check(graph[("DM", "CM")] == 1 and graph[("FB", "ST")] == 3, "Figure example distances changed")

    for relative, expected in EXPECTED_HASHES.items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        check(actual == expected, f"Hash mismatch: {relative}")

    pdf_bytes = (ROOT / "paper/Problem12_Position_as_a_Variable_Not_a_Label.pdf").read_bytes()
    check(pdf_bytes.startswith(b"%PDF"), "Paper is not a PDF")
    check(len(re.findall(rb"/Type\s*/Page\b", pdf_bytes)) == 2, "Paper is not two pages")

    headline_text = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in ["README.md", "results/frozen_results.json"])
    check("0.1547" in headline_text and "0.0488" in headline_text, "Authoritative distance result missing")
    check("0.215" not in headline_text, "Stale rho found in headline material")
    local_home_marker = "/" + "Users/"
    local_file_scheme = "file:" + "//"
    check(local_home_marker not in headline_text and local_file_scheme not in headline_text, "Local absolute path found")

    print("PASS: Problem 12 public release verified")
    print("Headline: rho=0.1547, permutation p=0.0488, 159 role comparisons")
    print("Reproducibility: partial; restricted row-level data are intentionally absent")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
