# Tasks

## 1. Stability plot rework

- [x] 1.1 Remove the `barras(..., horizontal=True)` call from the stability cell (cell 28), keeping the metric, ranking table, and printed Dota 2 conclusion untouched, and verify the cell source no longer references `barras`
- [x] 1.2 Add a self-sufficient plot cell after the stability table cell that recomputes the sorted variation table from `diario_juego`, selects `iloc[0]` (most stable) and `iloc[-1]` (least stable), and plots each game's daily `Players` as percentage of its own mean over `Fecha` with `figsize=(12, 6)` and `linewidth=1.8`, and verify both series render with a legend via `configurar()` labels
- [ ] 1.3 Re-execute the notebook top-to-bottom with `SBD/steam_data.csv` present, confirm all cells run without error, the stability conclusion still names Dota 2 with ~35.71 % variation, and the new figure shows exactly two mean-normalized lines, then save the notebook so outputs are updated
