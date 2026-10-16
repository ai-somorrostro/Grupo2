# Proposal

## Why

The "¿Cuál es el juego más estable?" answer in `SBD/steam_notebook.ipynb` is the only best-vs-worst question shown as a horizontal bar chart of all games, while the neighbouring questions (notably retention) answer the same shape of question with a two-line comparison plot. Readers cannot visually grasp what "stable" means over time.

## What Changes

- Replace the horizontal bar chart in the stability cell (cell 28) with a line chart comparing the most stable game vs the least stable game over time, following the retention-plot pattern (cell 26).
- Normalize each line to its own daily mean (100 = own average) so stability — not absolute size — is what the eye compares.
- Keep the existing stability table, metric (relative variation = std/mean × 100), ranking, and printed conclusion unchanged (Dota 2 most stable).
- Reuse the shared `configurar()` figure helper, `figsize=(12, 6)`, `linewidth=1.8`, and legend conventions from the retention plot.

## Capabilities

### New Capabilities

(none — presentation change within an existing capability)

### Modified Capabilities

- `steam-notebook-cleanup`: the stability question's presentation changes from a bar chart of all games to a normalized best-vs-worst line comparison; the stability ranking requirement (led by Dota 2) and shared-presentation-logic requirement now cover this line pattern. No analytical answer changes.

## Impact

- Affected: `SBD/steam_notebook.ipynb`, stability cell only (cell 28; optionally a self-sufficient follow-up plot cell mirroring the retention table/plot split of cells 25–26).
- No data, CSV, cleaning path, or other question cells affected.
- No new dependencies; matplotlib/pandas already in use.
