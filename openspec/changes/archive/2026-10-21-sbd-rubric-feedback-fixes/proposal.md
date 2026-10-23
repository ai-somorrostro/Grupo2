# Proposal

## Why

The SBD evaluation of `SBD/steam_notebook.ipynb` scored four of five criteria down for gaps that predate the Twitch integration work (archived 2026-10-20): record validation is superficial (shape/dtypes/nulls only, no duplicate/range/frequency checks), the Steam-Twitch join exists but its granularity choice, join keys, and post-join coverage are never argued for in the notebook, there is no justification anywhere for the pandas/matplotlib tool choice despite the team using polars elsewhere in the repo, and the notebook has no closing synthesis that the Informe can cite — so the report's conclusions (e.g. the Nov/Dec selling-window recommendation) float free of notebook evidence. Fixing these closes four of the five rubric gaps without touching the plot-by-plot interpretation work, which is deliberately deferred to a separate change.

## What Changes

- Add real data validation to the notebook's "Valores null y descripcion" section: exact and `(Game, DateTime)` duplicate checks, negative/zero `Players` checks, a reported count of rows dropped by the existing `dropna(subset=["Game","DateTime","Players"])` step (currently silent, ~1,615 rows / 2.6%), per-game observed date spans (surfacing that Counter-Strike 2's span starts in 2011, 12 years before CS2's release, mirroring the lineage caveat already documented for the Twitch dataset), and a note on the daily-to-hourly sampling-density change across the dataset's history, each closed with a short markdown conclusion of what was found and what was decided.
- Add a markdown justification for the Steam-Twitch join already implemented in the archived `twitch-steam-correlation-analysis` work: why `(Game, Month)` is the chosen granularity (Steam is daily/hourly, Twitch is monthly), a per-game coverage table (matched vs. Steam-only vs. Twitch-only months, derived from the existing `meses_solo_steam`/`meses_solo_twitch` counts that are computed but never narrated), and an explicit note on whether a second source (release dates, pricing) was considered and why it was or wasn't added.
- Add a new "Herramientas" notebook section justifying pandas + matplotlib for this dataset (~62k rows, single-machine batch EDA) against polars (used elsewhere in the repo, e.g. `BDA/Notebook datos influx.ipynb`) and against seaborn/plotly, naming concrete advantages and limitations of each rather than asserting the choice.
- Add a closing "Conclusiones" section summarizing every analysis (the 10 original questions plus the 4 Twitch questions) with the evidence that backs each one, so `SBD/Informe Steam.pdf` has a single notebook section it can cite, and so any analysis the report omits is at least listed here.
- Correct the stale `BDA/steam_notebook.ipynb` path in `openspec/specs/steam-notebook-cleanup/spec.md` to `SBD/steam_notebook.ipynb`, matching where the notebook has actually lived since the cleanup and Twitch changes.

Explicitly out of scope: per-plot "lectura de la gráfica" markdown, the single-indicator conclusions audit (including the mes/`diario_juego` sampling-bias fix behind the Nov/Dec claim), and any edit to `SBD/Informe Steam.pdf` itself. These are deferred to a separate change already scoped in a prior conversation.

## Capabilities

### New Capabilities
- `notebook-methodology-and-conclusions`: tooling justification (pandas/matplotlib vs. polars/seaborn/plotly) and a closing conclusions section summarizing every analytical question with its supporting evidence, for the report to cite.

### Modified Capabilities
- `steam-notebook-cleanup`: add a data-validation requirement (duplicates, ranges, dropped-row counts, per-game date spans, sampling-frequency note) to the existing first-look section, and correct the notebook's documented file path from `BDA/` to `SBD/`.
- `twitch-steam-correlation-analysis`: add a requirement that the existing join's granularity choice and per-game coverage are narrated in markdown, not just computed silently.

## Impact

- Affected file: `SBD/steam_notebook.ipynb` only (new cells in the first-look section, new markdown narrating the existing join output, two new sections near the end). No changes to `SBD/steam_data.csv`, `Mejoras/csv/twitch_games_monthly_historical.csv`, or `SBD/Informe Steam.pdf`.
- No new dependencies; the tooling section documents the pandas-vs-polars decision rather than introducing polars.
- Touches two existing specs (`steam-notebook-cleanup`, `twitch-steam-correlation-analysis`) via delta files, and introduces one new spec (`notebook-methodology-and-conclusions`).
- Sequencing: should land independently of the deferred plot-explanations change, but both will touch the same notebook file, so whichever lands second should rebase/re-run after the first.
