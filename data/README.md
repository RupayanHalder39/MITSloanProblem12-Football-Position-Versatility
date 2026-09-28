# Data availability

## Source used

The analysis used an internal SoccerSolver export containing formation-segment timing and
player-match statistics. No public redistribution licence for that row-level source was found in
the project documentation.

## What is not included

This repository does not contain the source SQL export, databases, raw or processed player-match
rows, formation segments, event data, tracking data, private club data, or source credentials.
The exclusion applies to derived row-level tables as well as the original export.

## What is included

`results/` contains frozen aggregate results needed to verify the public claims: cohort counts,
typology counts, the role graph, taxonomy-level estimates, leave-one-transition summaries, and the
three examples already disclosed in the paper.

## Authorized reconstruction

An authorized researcher would need a legally obtained source export with compatible formation,
appearance, substitution, and player-match statistic fields. The source must remain outside this
repository. The public code demonstrates the central role-graph, distance, profile-divergence, and
classification logic, but cannot reconstruct the full study without those restricted rows.
