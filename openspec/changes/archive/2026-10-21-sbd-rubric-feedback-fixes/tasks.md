# Tasks

## 1. First-look record validation

- [x] 1.1 Add a duplicate-check cell after the existing null/describe cell reporting exact row duplicate count and `(Game, DateTime)` duplicate count (expect 0 for both against current data); verify by running the cell and confirming both counts print even though they are 0
- [x] 1.2 Add a range-check cell reporting the count of rows with negative or zero `Players`; verify by running the cell and confirming the count prints (expect 0 against current data)
- [x] 1.3 Add a dropped-row cell reporting how many rows the canonical `dropna(subset=["Game","DateTime","Players"])` step removes and what share of the total that is; verify by running the cell and confirming it reports ~1,615 rows (~2.6%) against current data
- [x] 1.4 Add a per-game date-span cell reporting each game's first and last observed date, with a markdown note that Counter-Strike 2's span (observed starting 2011) predates the game's 2023 release and reflects the franchise directory page, mirroring the Twitch-side caveat already documented in the archived Twitch change; verify by running the cell and confirming all 10 games are listed with their spans
- [x] 1.5 Add a markdown note documenting that recent history is recorded at a finer (hourly) grain than older (daily) history for at least the affected games, flagged as a caveat for any cell that averages across time without first aggregating to `diario_juego`'s consistent daily grain; verify by reading the rendered markdown
- [x] 1.6 Add a short markdown conclusion after each validation cell above (1.1-1.5) stating what was found and what was decided; verify by reading each rendered conclusion

## 2. Twitch join narration

- [x] 2.1 Add a markdown cell before or after the existing Twitch join cell (`mensual_juego`) explaining why `(Game, Month)` was chosen as the join granularity given Steam's daily/hourly data and Twitch's monthly data; verify by reading the rendered markdown
- [x] 2.2 Add a per-game coverage cell deriving, from the existing `meses_solo_steam`/`meses_solo_twitch` masks, a table of matched/Steam-only/Twitch-only month counts per game; verify by running the cell and confirming all 10 games appear with three counts each that sum to that game's total row count in `mensual_juego`
- [x] 2.3 Add a markdown note stating whether a second source (e.g. release dates, pricing) was considered for integration and why it was or was not added; verify by reading the rendered markdown

## 3. Tools justification section

- [x] 3.1 Add a new "Herramientas" markdown+code section (placed after the first-look section, before "5. Analisis") comparing pandas against polars for this dataset's size (~62k rows) and the batch, single-machine EDA performed here, citing polars' use in `BDA/Notebook datos influx.ipynb` as the team's own point of comparison, with at least one concrete advantage and one limitation stated for each; verify by reading the rendered section and confirming both an advantage and a limitation are stated for pandas relative to polars
- [x] 3.2 In the same section, justify matplotlib over at least one alternative (seaborn or plotly) with a concrete advantage and limitation of each; verify by reading the rendered section

## 4. Closing conclusions section

- [x] 4.1 Add a final "Conclusiones" section that synthesizes the analysis across questions into cross-cutting themes (building on the per-question conclusions already present in markdown next to each question's plot), without contradicting any individual question's own conclusion; verify by reading the rendered section and confirming it groups related findings (e.g. popularity having multiple dimensions, the Steam-Twitch relationship not being uniform) and states the whole-analysis caveats (differing Steam/Twitch resolutions, uneven coverage, incomplete recent period, no causation/generalization claimed)
- [x] 4.2 Confirm the closing section's treatment of the "¿Cuales son los meses con mayor y menor cantidad de jugadores?" theme is consistent with its own inline conclusion (that it rests on a single, cross-game-pooled indicator affected by the sampling-grain change, not a settled finding); verify by reading both the inline conclusion and the closing section's reference to it

## 5. Spec and docs correction

- [x] 5.1 Correct the notebook path reference from `BDA/steam_notebook.ipynb` to `SBD/steam_notebook.ipynb` wherever it appears in `openspec/specs/steam-notebook-cleanup/spec.md` (handled via this change's spec delta at archive time); verify by confirming the delta's MODIFIED requirement reflects the corrected path

## 6. Full notebook verification

- [x] 6.1 Re-execute `SBD/steam_notebook.ipynb` top-to-bottom with `SBD/steam_data.csv` and `Mejoras/csv/twitch_games_monthly_historical.csv` present, confirm every existing cell's output and conclusion is unchanged (per the cleanup spec's "Preserved analytical answers" requirement), confirm all new cells from groups 1-4 run without error, and save the notebook so outputs are updated — done: 0 errors across all 89 cells, dropped-row count (1,615/2.6%), sampling-grain cutoff (2026-09-05), and preserved answers (PUBG peak, Project Zomboid retention, Dota 2 stability 35.71%, 2025 top year) all confirmed against the executed notebook
