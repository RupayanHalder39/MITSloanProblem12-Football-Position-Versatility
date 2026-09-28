# Reproducibility

## Public verification

Run from the repository root:

```bash
python scripts/verify_release.py
```

This checks the frozen public constants, conservative role graph, required files, figure hashes,
and the absence of the stale ρ≈0.215 value from headline materials.

To rebuild the white tactical-role figure:

```bash
python -m pip install -r requirements.txt
python src/build_figure1.py
```

The script reads `results/frozen_results.json` and writes the PNG/SVG/PDF Figure 1 files.

## Reproducibility boundary

The repository supports verification of published aggregate results and reproduction of Figure 1.
Full end-to-end reconstruction is not possible without authorized row-level SoccerSolver data. No
restricted data are fetched automatically, and the public release does not imply redistribution
permission.
