# Public Release Audit — MIT Sloan Problem 12

## Scope

- Source project: private `bestPerformancePosition` research workspace, treated as read-only during release assembly.
- Presentation reference: the complete Problem 6 public-release README.
- Release repository: `MITSloanProblem12-Football-Position-Versatility`.
- Remote: `https://github.com/RupayanHalder39/MITSloanProblem12-Football-Position-Versatility.git`.

## Final paper

The supplied final two-page A4 PDF was inspected before copying. It contains the approved title,
white-background tactical-role Figure 1, frozen three-archetype Figure 2, no visible reviewer
comments, and the real repository URL. The source PDF was not modified.

Public copy: `paper/Problem12_Position_as_a_Variable_Not_a_Label.pdf`.

## Included artifacts

- README, citation metadata, scoped MIT software/documentation licence, and release documentation.
- Final abstract PDF.
- Approved white Figure 1 in PNG and SVG form.
- Frozen Figure 2 in PNG form.
- Aggregate frozen results, taxonomy robustness table, and leave-one-transition summary.
- Public-safe core-method and Figure 1 generation scripts.
- Author photograph and SoccerSolver logo supplied expressly for repository presentation.

## Excluded artifacts

- Raw SoccerSolver SQL exports and all row-level source data.
- Processed CSV rows, SQLite databases, formation segments, validation rows, and caches.
- Private correspondence, reviewer exports, internal handoff notes, temporary files, backups, and notebooks.
- Source videos, broadcast frames, tracking data, event data, and copyrighted club/player photographs.
- Local environment files, credentials, tokens, cookies, archives, logs, and machine-specific paths.
- The superseded dark Figure 1 and development-only figure candidates.

## Data redistribution decision

No redistribution licence for the SoccerSolver source or row-level derivatives was found. Those
materials are not published. Only aggregate results already disclosed by the paper and public-safe
summaries are included. Reproducibility is therefore partial, not full.

## Scientific verification

- 23,627 player-match observations; 120 outfield players; 159 comparisons.
- Primary eligibility: 70% purity, 600 clean minutes, eight matches per role.
- Typology: 16 stable advantage, 36 trade-off, 40 neutrality, 67 insufficient evidence.
- Baseline cross-minus-adjacent: +0.1873, 95% CI [0.0583, 0.3285], d=0.8939.
- Authoritative distance-only result: ρ=0.1547, permutation p=0.0488.
- Consensus-only result: +0.1854, 95% CI [0.0565, 0.3241].
- No leave-one-player or leave-one-transition check reversed direction.
- The stale internal ρ≈0.215 value is not presented as a final result.

## Figure verification

Figure 1 uses the frozen conservative role graph and labels pitch placement schematic and distance
non-metric. Figure 2 retains the frozen three-player encoding. Both repository paths are relative.
The original robustness plot is not presented as the abstract hero figure.

## README template comparison

The README follows the Problem 6 family: research-first hierarchy, data and target/method
explanation, main findings, paired figures, reproduction, limitations, researcher profile, contact,
SoccerSolver collaboration, citation, and licence. No Problem 6 scientific claims or numbers were
copied.

## Safety checks

- Secret/privacy scan: passed before staging; no credentials, API keys, tokens, private keys, cookies, or environment files found.
- Copyright/media scan: generated figures plus explicitly supplied author photograph/logo only.
- Restricted-data scan: passed before staging; no raw/row-level data, SQL, SQLite, Parquet, database, model, or archive files included.
- Symlink and portability scan: passed before staging; no symlinks or machine-specific path dependencies included.
- Large-file scan: passed before staging; no file exceeds 5 MB and Git LFS is not required.

## Publication record

- Initial release commit: pending.
- Final repository HEAD: pending.
- Push verification: pending.
