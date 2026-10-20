# Tasks

## 1. Twitch data load and join

- [x] 1.1 Add a canonical load cell for `Mejoras/csv/twitch_games_monthly_historical.csv` (relative path per design D1) producing `twitch_mensual`: strip column-name whitespace, coerce `AverageViewers`/`PeakViewers`/`HoursWatched`/`HoursStreamed`/`AverageChannels`/`PeakChannels` to numeric, coerce `DateTime` and derive a `Mes` period column; verify by running the cell and confirming `twitch_mensual["Game"].nunique() == 10` and no `KeyError` on the stripped column names
- [x] 1.2 Add a join cell producing `mensual_juego`: resample `diario_juego` to monthly mean `Players` per `(Game, Mes)` and outer-merge with `twitch_mensual` on `(Game, Mes)`; verify by printing `mensual_juego.shape` and confirming rows exist where `AverageViewers` is `NaN` but `Players` is not (and vice versa), proving the outer join keeps unmatched months visible
- [x] 1.3 Add a markdown note alongside the load cells documenting the Counter-Strike 2 Twitch-history-predates-CS2 caveat and the Among Us pre-September-2020 zero-viewer caveat; verify by reading the rendered markdown cell

## 2. Correlation question

- [x] 2.1 Add the "¿Existe correlación entre jugadores de Steam y espectadores de Twitch?" markdown subsection and a self-sufficient code cell computing per-game Pearson correlation (`Players` vs `AverageViewers`) from `mensual_juego`, excluding games with fewer than 2 paired observations and printing which games (if any) were excluded; verify by running the cell and confirming the displayed table is sorted by correlation strength and lists exactly the 10 games minus any stated exclusions
- [x] 2.2 Add the accompanying plot (scatter or annotated comparison) using `configurar`/existing plotting conventions; verify by confirming the figure renders without error and every plotted game has a visible label/legend entry

## 3. Lead-lag and viral-moment question

- [x] 3.1 Add the "¿Quién se mueve primero: Twitch o Steam?" markdown subsection introducing the Among Us September 2020 worked example (state the concrete lag found for that game) before the generalized table; verify by reading the cell output and confirming it names Among Us and a computed lag value
- [x] 3.2 Implement the shift-and-correlate lag function (lags -3..+3, pick best `|r|`, classify "Twitch leads"/"Steam leads"/"synced"/"no clear relationship" against a visible threshold constant per design D4) and apply it to all 10 games in one table; verify by running the cell and confirming all 10 games appear with a classification and the chosen threshold constant is visible in the cell source
- [x] 3.3 Add the viral-moment event table (largest month-over-month `AverageViewers` jump per game, its month, and the `Players` percentage change in that month ±1) per design D5, guarding division-by-zero for Among Us' zero-viewer months per the caveats requirement; verify by running the cell, confirming all 10 games appear, and confirming no `inf`/exception appears in the Among Us row

## 4. Divergent lifecycle trajectories question

- [x] 4.1 Add the "¿Divergen las trayectorias de Steam y Twitch?" markdown subsection and a self-sufficient code cell computing a trend slope (via `numpy.polyfit` degree 1, per design D6) for both `Players` and `AverageViewers` over the same trailing-years window per game, with a visible named window-length constant and a minimum-coverage guard; verify by running the cell and confirming a slope sign is produced for both signals for every game that meets the coverage guard, and excluded games (if any) are stated
- [x] 4.2 Flag and display games whose two slope signs disagree, including the Counter-Strike 2 lineage caveat note if that game is in the flagged set; verify by confirming the output table marks divergent games distinctly (e.g. a boolean/label column) and, if CS2 is flagged, the caveat text is shown in the same cell's output

## 5. Seasonality question

- [x] 5.1 Add the "¿Comparten los juegos un patrón estacional?" markdown subsection and a self-sufficient code cell computing month-of-year averages (Jan-Dec) for both `Players` and `AverageViewers` per game, reusing the existing `mes_promedio`-style grouping pattern; verify by running the cell and confirming a 12-value profile exists per game per signal
- [x] 5.2 Add a comparison visualization per game (e.g. both signals normalized to their own mean, plotted together) and accompanying text noting which games show shared calendar-driven seasonality vs. an idiosyncratic/non-calendar pattern (e.g. Rust); verify by confirming the figure renders for the games discussed and the text explicitly names at least one shared-seasonality game and one idiosyncratic-pattern game

## 6. Full notebook verification and docs

- [x] 6.1 Update `README.md`'s Steam analysis instructions to note the repo's `SBD/`+`Mejoras/` sibling-directory layout must be preserved for the new relative-path load to resolve; verify by reading the updated section
- [x] 6.2 Re-execute `SBD/steam_notebook.ipynb` top-to-bottom with `SBD/steam_data.csv` and `Mejoras/csv/twitch_games_monthly_historical.csv` present in their designed locations, confirm every cell (existing and new) runs without error, all four new questions produce output, and no existing question's cell, output, or conclusion changed; then save the notebook so outputs are updated
