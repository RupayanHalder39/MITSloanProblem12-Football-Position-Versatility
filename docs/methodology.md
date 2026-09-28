# Methodology

## Analytical unit

The study uses `Player × Match × Dominant Position Family`. Halftime-aware formation-segment timing
is aggregated within each match before one dominant role family is assigned. The primary cohort
requires role purity of at least 70%, at least 600 clean minutes, and at least eight qualifying
matches in each compared role.

## Role families and tactical distance

The analysed outfield families are CB, FB, WB, DM, CM, AM, W, and ST. The conservative frozen graph
uses these undirected edges:

`CB–FB`, `CB–DM`, `FB–WB`, `WB–W`, `DM–CM`, `CM–AM`, `AM–W`, `AM–ST`, `W–ST`.

Tactical distance is the unweighted shortest-path edge count. Distance 1 is adjacent; larger values
are cross-family. Pitch locations in Figure 1 are schematic and do not enter the calculation.

## Performance profiles

Player-match totals are normalized per 90 and standardized within role-family reference groups.
They are aggregated into Attack, Progression, Possession, and Defense scores. For a given player and
role pair, each category difference is Role A minus Role B. Profile divergence is the Euclidean norm
of the four differences.

## Typology and robustness

The frozen workflow distinguishes stable advantage, context-dependent trade-off, positional
neutrality, and insufficient evidence using profile magnitude and stability evidence. Robustness
checks include alternative role graphs, exclusion of disputed transition classifications,
leave-one-player-out analysis, leave-one-transition-out analysis, threshold sensitivity, and
season/context checks.

The public release preserves frozen aggregate results rather than recalculating headline values
without the restricted source data.
