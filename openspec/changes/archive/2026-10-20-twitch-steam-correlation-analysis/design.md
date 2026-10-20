# Design

## Context

`SBD/steam_notebook.ipynb` is run with its working directory set to `SBD/` (per the repo README) and loads `steam_data.csv` with a relative path. The new input, `Mejoras/csv/twitch_games_monthly_historical.csv`, lives in a sibling directory. The notebook's existing conventions (see `steam-notebook-cleanup` spec and the cells it governs) are: one canonical load/cleaning cell per dataset, a canonical daily/monthly aggregate frame reused by question cells, shared helpers `barras`, `configurar`, `tabla`, `formato_porcentaje`, `max_min`, and a "self-sufficient cell" pattern for cells that also render a plot (they recompute from the canonical frame rather than reaching into a previous cell's locals). Only `pandas` and `matplotlib.pyplot` are currently imported; there is no `numpy`, `scipy`, or `statsmodels` import today.

## Goals / Non-Goals

**Goals:**
- Load the Twitch monthly CSV through one canonical cell, consistent with how `steam_data.csv` is loaded, without duplicating the file into `SBD/`.
- Produce one joined monthly frame (`mensual_juego`, Steam+Twitch) that all four new question cells reuse, mirroring how `diario_juego` is shared today.
- Implement correlation, lead-lag, trend-slope, and seasonality logic with only `pandas`/`numpy` (numpy is already a transitive pandas dependency; adding `import numpy as np` is acceptable, no new package to install), avoiding `scipy`/`statsmodels` to keep the `pip install jupyter pandas matplotlib` instructions in the README still sufficient — or else the README needs an update.
- Keep every new cell runnable top-to-bottom alongside the existing ones, per the "single notebook narrative" requirement.

**Non-Goals:**
- No change to `twitch_top_games_365d.csv` or `twitch_streamer_broadcasts_combined.csv` handling — they stay unused.
- No change to any existing Steam-only question, helper, or conclusion.
- No generalized statistics library/helper framework — only what the four questions need.
- No change to `BDA/` or `PIA/` folders.

## Decisions

### D1: Reference the Twitch CSV via a relative path, do not copy it into `SBD/`
Load with `pd.read_csv("../Mejoras/csv/twitch_games_monthly_historical.csv", sep=";", encoding="utf-8-sig")`, relying on the fixed sibling-directory layout (`SBD/` and `Mejoras/` are both direct children of the repo root).
- **Alternative considered**: copy/duplicate the CSV into `SBD/` next to `steam_data.csv`. Rejected: creates a second source of truth that can silently go stale if `Mejoras/csv/...` is refreshed, and the dataset is small enough that path traversal is simpler than a sync step.
- **Consequence**: the README's "cómo iniciar" instructions for the Steam analysis gain one line noting the repo's directory layout must be preserved (the `Mejoras/` sibling must exist) — this is a documentation task, not a behavior change, and does not touch the `PIA`/`BDA` sections.

### D2: One load/cleaning cell producing `twitch_mensual`, one join cell producing `mensual_juego`
`twitch_mensual`: read the CSV, strip column name whitespace (source file has leading spaces like `" Game"`), coerce `AverageViewers`/`PeakViewers`/`HoursWatched`/`HoursStreamed`/`AverageChannels`/`PeakChannels` to numeric, coerce `DateTime` to datetime and derive a `Mes` (`Period[M]`) column, matching the `Fecha`/`Año`/`Mes` derivation style already used for Steam data.
`mensual_juego`: resample `diario_juego` to monthly mean `Players` per `(Game, Mes)`, then `merge` with `twitch_mensual` on `(Game, Mes)` using an outer join so months present on only one side stay visible as `NaN` rather than being silently dropped (matches the spec's "unmatched months left as missing" scenario).
- **Alternative considered**: inner join only. Rejected: would hide exactly the coverage gaps (e.g. Among Us pre-Aug-2015 Twitch data, CS2 pre-Nov-2018 Steam data) that the caveats requirement asks to surface.

### D3: Correlation question uses `pandas.Series.corr()` (Pearson, pairwise-complete), gated by a minimum-overlap guard
Per game, compute `mensual_juego.groupby("Game").apply(lambda g: g["Players"].corr(g["AverageViewers"]))`. Before including a game in the ranked table, require at least 2 non-null paired observations (pandas returns `NaN` below that threshold on its own, but the spec requires an explicit stated exclusion list rather than a silent `NaN` row).

### D4: Lead-lag via manual shift-and-correlate (no `statsmodels.tsa.stattools.ccf`)
For lags -3..+3, shift one series relative to the other within each game's monthly frame and recompute `corr()` at each lag; pick the lag with the highest absolute correlation. Classify: `lag == 0` and `|r) >= threshold` → "synced"; `lag < 0` (Twitch change precedes Steam change) → "Twitch leads"; `lag > 0` → "Steam leads"; best `|r|` below threshold at every lag → "no clear relationship". Threshold choice (e.g. `|r| >= 0.3`) is recorded in the cell as a visible constant, not hidden magic.
- **Alternative considered**: `statsmodels` cross-correlation function. Rejected per Goals (no new dependency / README stays accurate).

### D5: Viral-moment table reuses the lag machinery's inputs, not a new frame
Per game: `AverageViewers.pct_change()` to find the single largest month-over-month jump and its month; look up `Players.pct_change()` in that same month and the two adjacent months (±1) for the "comparable Steam jump" column. Among Us is used as the worked example first (its known Sept 2020 jump), then the same computation runs for all 10 games in a generalized loop/groupby — not a special-cased branch.

### D6: Lifecycle trend slope via `numpy.polyfit` degree-1 fit over the recent-years window
For each game and each signal (`Players`, `AverageViewers`), fit a line against month-index over the same trailing window (e.g. last 3 calendar years that both series cover) and take the slope's sign as the trend direction. A game is "divergent" when the two signs differ. Window length is defined as a named constant in the cell, reusing the "at least N months of coverage" guard style already used by the existing growth/trend question cells (e.g. the `>= 300 days` completeness guard in the current yearly-trend cell).
- **Alternative considered**: compare only first-vs-last value. Rejected: too sensitive to single-month noise/outliers (e.g. Among Us' 2020 spike would dominate a 2-point comparison); a fitted slope over a multi-year window is more robust and mirrors the "mediana de los juegos" robustness choice already used in the existing yearly-trend question.

### D7: Seasonality reuses the existing month-of-year grouping pattern
Mirror the existing `mes_promedio = df.groupby("Mes")["Players"].mean()` pattern (used for the hour/month question) applied per-game to both `Players` and `AverageViewers`, then compare the two profiles (e.g. normalized to each series' own mean, plotted side by side per game) rather than inventing a new seasonality metric.

## Risks / Trade-offs

- **[Risk] Relative path `../Mejoras/csv/...` breaks if someone runs the notebook with a different working directory than `SBD/`.** → Mitigation: match the existing `steam_data.csv` convention exactly (same relative-path assumption, same README section) so the failure mode and fix are identical to the one Steam users already know ("si el notebook no encuentra el CSV, ejecútalo desde `SBD/`").
- **[Risk] Column name whitespace in the Twitch CSV (e.g. `" Game"`, `" Month"`) silently produces `KeyError`s if not stripped.** → Mitigation: strip column names and string-typed cell values immediately after `read_csv`, before any other cell references them, inside the single canonical load cell (D2).
- **[Risk] Short/partial overlap windows (Among Us pre-2020, any game's final partial month) could distort correlation, lag, or slope results.** → Mitigation: explicit minimum-overlap and completeness guards per question (D3, D6), and the merge keeping mismatched months as `NaN` rather than zero-filled (D2) so guards can detect them.
- **[Trade-off] Hand-rolled lag/slope math (D4, D6) instead of `statsmodels`/`scipy` is more code than calling a library function, but keeps the project's stated dependency list (`jupyter pandas matplotlib`) accurate — judged worth it for a student/teaching notebook where the README promise of "just these three packages" matters more than concise code.**

## Open Questions

None — the questions above (join strategy, library choice, caveat handling, path layout) are resolved as decisions; nothing here would change the specs or task breakdown if answered differently later.
