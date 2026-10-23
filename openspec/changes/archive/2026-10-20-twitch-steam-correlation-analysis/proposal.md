# Proposal

## Why

`SBD/steam_notebook.ipynb` only answers questions from Steam's own concurrent-player data. `Mejoras/csv/twitch_games_monthly_historical.csv` now provides monthly Twitch viewership (`AverageViewers`, `PeakViewers`, `HoursWatched`, `HoursStreamed`, `AverageChannels`, `PeakChannels`) for the exact same 10 games and an almost-matching time span (2015/2018–2026 vs. the notebook's 2007/2018–2026). This lets the notebook answer questions a single-platform view cannot: whether a game's Steam playerbase and Twitch audience move together, which moves first, and whether the two platforms tell the same long-term story about a game's health.

## What Changes

- Add a Twitch monthly dataset to the notebook's canonical load/cleaning path (new sibling frame to `diario_juego`, joined on `(Game, Month)`), following the existing cleaning conventions (`;` separator, BOM handling, numeric/datetime coercion) instead of introducing a second ad hoc loader.
- Add four new analysis questions to the "Analisis" section, each as its own self-sufficient subsection (markdown question + code cell(s)), reusing the existing shared helpers (`configurar`, `tabla`, `formato_porcentaje`, `barras`) and the self-sufficient-cell convention used by the stability/retention questions:
  1. **Correlación jugadores-espectadores**: per-game Pearson correlation between monthly-resampled `Players` and `AverageViewers`, ranked table + scatter/annotated plot.
  2. **Quién se mueve primero (adelanto/retraso) y momentos virales**: per-game cross-correlation of the two series at lags of -3..+3 months to classify each game as Twitch-leads / Steam-leads / synced / no relationship, plus a generalized "biggest month-over-month jump" event table (using Among Us' September 2020 spike as the worked example before generalizing to all 10 games).
  3. **Trayectorias de ciclo de vida divergentes**: compare each game's recent-years trend slope for `Players` vs. `AverageViewers`, flagging games where the two series disagree in direction (declining on one platform while flat/growing on the other).
  4. **Estacionalidad compartida vs. patrones propios**: month-of-year averages for both series per game, to distinguish shared calendar-driven seasonality from idiosyncratic cycles (e.g. Rust's wipe-driven pattern) that may only be visible on one platform.
- Scope is strictly limited to `twitch_games_monthly_historical.csv`; `twitch_top_games_365d.csv` and `twitch_streamer_broadcasts_combined.csv` are explicitly out of scope and must not be loaded or referenced.
- Document, in the new load cell and/or a markdown note, the two known data caveats: `Counter-Strike 2`'s Twitch series starts in 2015 (carried over from the CS:GO-era directory page, predating CS2 itself) and `Among Us` has genuine `0`-viewer months before September 2020 (needs a division-by-zero guard in the correlation/lead-lag calculations).

## Capabilities

### New Capabilities
- `twitch-steam-correlation-analysis`: the notebook's ability to load the Twitch monthly dataset alongside the Steam dataset and answer cross-platform correlation, lead/lag, lifecycle-divergence, and seasonality questions.

### Modified Capabilities
(none — the existing `steam-notebook-cleanup` capability's requirements, such as the canonical single load/cleaning path and shared presentation helpers, are followed, not changed)

## Impact

- Affected: `SBD/steam_notebook.ipynb` (new load cell(s) and four new analysis subsections appended to section 5).
- New input file read: `Mejoras/csv/twitch_games_monthly_historical.csv` (the notebook will need this path reachable relative to `SBD/`, e.g. via a relative path or a copy alongside `steam_data.csv` — to be settled in design).
- No existing cells, questions, or conclusions in the notebook are altered.
- No new dependencies beyond pandas/matplotlib already in use.
