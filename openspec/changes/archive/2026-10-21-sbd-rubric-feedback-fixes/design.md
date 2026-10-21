# Design

## Context

`SBD/steam_notebook.ipynb` (57 cells) already follows the conventions set by `steam-notebook-cleanup`: a canonical cleaning cell (`df` -> `df_limpio` -> `diario_juego`), shared helpers (`barras`, `configurar`, `tabla`, `max_min`, `formato_porcentaje`), and self-sufficient question cells. The archived `twitch-steam-correlation-analysis` change added a canonical Twitch load (`twitch_mensual`, cell 7) and an outer join (`mensual_juego`, cell 8) that already prints `mensual_juego.shape` and dataset-wide Steam-only/Twitch-only month counts, but narrates none of it.

Manual validation against `SBD/steam_data.csv` (62,267 rows, 10 games) found: 0 exact duplicates, 0 `(Game, DateTime)` duplicates, 0 negative/zero `Players`, 1,615 rows (2.6%) with empty `Players` silently dropped by the existing `dropna`, and Counter-Strike 2's span starting 2011-11-30 (predates CS2's 2023 release — same franchise-directory-page lineage already documented for the Twitch dataset). These are the concrete numbers this change's validation cells should surface; this design does not require re-deriving them differently, just presenting them in the notebook.

No PDF text could be extracted in the exploration session; the specific wording of the Informe's Nov/Dec claim is not verified here. See proposal.md - Why.

## Goals / Non-Goals

**Goals:**
- Add duplicate/range/dropped-row/date-span/sampling-grain validation to the first-look section.
- Narrate the existing Twitch join's granularity choice and per-game coverage.
- Add a tools-justification section and a closing conclusions section.
- Fix the stale `BDA/` path reference in `steam-notebook-cleanup`'s spec.

**Non-Goals:**
- Per-plot "lectura de la gráfica" markdown for the 10 original + 4 Twitch question plots (deferred change).
- The single-indicator conclusions audit, including the `mes` cell's use of raw `df` instead of `diario_juego` behind the Nov/Dec claim (deferred change; the closing conclusions section added here should describe that conclusion's evidence as-is today, without correcting the underlying computation).
- Any edit to `SBD/Informe Steam.pdf`.
- Adding polars or any new dependency — the tools section documents the pandas choice, it does not switch to or add polars.
- Re-deriving or re-arguing the Twitch join's correctness; this only adds narration around the already-implemented, already-archived join.

## Decisions

- **Validation lives in the existing first-look section, not a new one.** The cleanup spec already defines "Consolidated first-look" as one section covering shape/dtypes/nulls/describe/head-tail/date-range; adding duplicate/range/span checks there keeps one first-look narrative instead of a second, competing "validation" section. Alternative considered: a standalone "Validación" section between first-look and analysis — rejected because it would duplicate the existing null/describe cells' framing and fragment first-look coverage across two places.
- **Narrate the join, don't re-architect it.** The join itself (outer merge on `(Game, Month)`, `validate="one_to_one"`) is already implemented and archived; this change only adds markdown and a per-game coverage table derived from the existing `meses_solo_steam`/`meses_solo_twitch` boolean masks (cell 8). Alternative considered: recompute coverage with a fresh groupby — rejected, reusing the existing masks keeps this change additive and avoids touching the join cell's logic, consistent with the cleanup spec's "no hidden coupling" requirement (new narration cells should read `mensual_juego`'s output, not duplicate its computation).
- **Tools section states a reasoned comparison, no benchmark required.** The rubric asks for justification of advantages/limitations, not a timing experiment. Alternative considered: adding a small polars equivalent-code or timing comparison — left as an explicit open question below since it changes scope (introduces a polars import) and the user has not confirmed it's wanted.
- **Closing conclusions section is a synthesis, not a rewrite.** It restates each question's existing conclusion with a pointer to its supporting cell/output; it does not correct the `mes` cell's computation (that's the deferred change's job) but it does need to describe that conclusion honestly as single-indicator today, since this change's own validation work does not touch that specific cell's logic.
- **Path fix is bundled into the validation delta, not a separate capability.** Correcting `BDA/` to `SBD/` in `steam-notebook-cleanup`'s "Single notebook narrative" requirement is a one-line spec correction with no notebook-code impact; bundling it with this change's validation work (which already touches that spec file) avoids a near-empty standalone change.

## Risks / Trade-offs

- [Risk] The closing conclusions section could read as silently endorsing the `mes` cell's sampling-biased conclusion since this change doesn't fix it. → Mitigation: the conclusions section entry for that question should note it rests on a single, cross-game-pooled indicator (consistent with what the deferred change will later correct), rather than presenting it as settled.
- [Risk] Per-game coverage table for the Twitch join may reveal very weak coverage for some games (e.g. Counter-Strike 2's pre-2023 years), which could invite scope creep into re-litigating the join's validity. → Mitigation: this change documents coverage as observed; any reaction to weak coverage (e.g. excluding a game, adding a second source) is a separate decision not forced by this change.
- [Risk] Editing `steam-notebook-cleanup`'s spec while `estabilidad-line-comparison` (in-progress, touches the same notebook file) is still open could create merge friction. → Mitigation: this is a planning-only artifact change for now; sequencing against that change is an implementation-time concern, not a spec-level one.

## Open Questions

- Should the tools-justification section include a small polars equivalent-code or timing comparison for one representative operation, or is a reasoned prose comparison sufficient? Left open since it would introduce a polars import if answered "yes."
- Is a second integration source (release dates, pricing) worth adding now, or should the notebook simply state that Twitch is sufficient for the current questions? Left open per proposal.md; this change only requires the notebook to state the decision, not what the decision is.
