# Design

## Context

See proposal.md Why. Current state: `BDA/steam_notebook.ipynb` (38 cells, ~2728 lines with outputs) mixes first-look and 10 analytical questions in one file. Each question cell re-implements `df.copy()` + `to_datetime` (sometimes without `errors="coerce"`) + `to_numeric` + `dropna` + `floor("D")` + `groupby(["Game","Fecha"]).mean()` with small drifts; `df` itself is half-mutated by an early `to_datetime` + `Año/Mes/Dia/Hora` cell that later cells ignore. Plotting (`figure`/`bar`/`title`/`grid`/`tight_layout`/`show`) and Styler formatting repeat ~8-10 times; the hourly question exists as two ~90% identical cells; the retention plot cell depends on leftover `comparacion`/`historiales` variables; `promedios_diarios` is reused under one name with different content; date min/max runs on raw strings. Constraint: user requires a single notebook, keep `Average Players`, preserve all analytical answers.

## Goals / Non-Goals

**Goals:**
- One canonical preparation path defined early and reused by every question.
- Small in-notebook helpers for plots, tables, and max/min summaries (no new `.py` module, keeps single-file constraint).
- Each question cell self-sufficient with distinct variable names; hourly analysis parameterized by window.
- First-look consolidated; date range from parsed datetimes; `Average Players` coverage documented.

**Non-Goals:**
- No new analytical questions, no new plots beyond equivalents, no change to CSV or dependencies.
- No extraction to shared library, no test harness, no output-stripping or re-execution tooling beyond manual restart-and-run-all.
- No reinterpretation of results (e.g., redefining retention/stability metrics); equivalence is the bar.

## Decisions

- **Canonical cells near the top: load cell + preparation cell + helpers cell.** Load keeps `sep=";"` + `encoding="utf-8-sig"`; preparation coerces `DateTime` (with `errors="coerce"`) and `Players`, drops rows missing `Game`/`DateTime`/`Players`, derives `Fecha = floor("D")` plus `Año/Mes/Dia/Hora` once, and builds the daily-averaged frame used downstream. Alternative of a separate `utils.py` rejected: user requires a single notebook; helpers live in early cells instead.
- **Raw frame stays read-only after preparation.** Question cells work from copies of the prepared frames and never mutate the canonical frames in place. Alternative of continued in-place mutation rejected: it caused the current half-clean `df` state.
- **Helpers cover three patterns only: bar/line figure wrapper, Styler format wrapper, max/min summary printer.** Narrow scope keeps the diff reviewable; full chart-library abstraction rejected as over-engineering for ~10 plots.
- **Hourly analysis as one function of `(frame, start, end)` called twice** (full history + recent window from `2026-09-05`), keeping the existing `00:00`-artifact markdown. Alternative of deleting the full-history view rejected: the artifact caveat needs both views to make sense.
- **Distinct result variable names per question** (e.g., retention vs stability vs growth frames get their own names) and explicit rebuild of comparison frames inside the plot cell. Alternative of execution-order comments only rejected: comments don't survive out-of-order runs.
- **First-look consolidation: one structure cell (shape/columns/dtypes/info), one quality cell (missing + describe + `Average Players` note), one glimpse cell (head + tail + games + parsed date range).** `describe(include="all")` kept for equivalence; date min/max switched to parsed datetimes (safe because ISO strings sort identically, but parsing is the correct contract).
- **`Average Players`: report `isna().sum()` / non-null share, add one markdown line stating it is preserved as-is and unused by current questions.** Drop/fill/impute explicitly rejected per user decision.

## Risks / Trade-offs

- [Risk] Coercion unification (`errors="coerce"` everywhere) slightly changes row counts vs cells that previously parsed strictly -> Mitigation: verify each question's conclusion (names, rankings, signs) matches pre-cleanup; accept row-count deltas only if conclusions hold.
- [Risk] Helper abstraction hides per-plot tweaks (figsizes 11x5 vs 12x6 vs 13x10, scatter vs barh) -> Mitigation: helpers take size/kind/labels as parameters; keep call sites explicit.
- [Risk] Large base64 plot outputs make diffs noisy -> Mitigation: review with `nbdiff`-style cell-source focus or clear outputs before final diff; re-run-all at the end to regenerate.
- [Risk] `2026-09-05` cutoff meaning is still a guess (frequency shift) -> Mitigation: keep the literal value and existing caveat text unchanged; do not reinterpret.
- [Trade-off] In-notebook helpers slightly enlarge early cells vs a module import — accepted to honor the single-notebook constraint.

## Migration Plan

Not applicable — single-file notebook edit, no deployment. Rollback is `git checkout -- BDA/steam_notebook.ipynb`. Verification is restart-kernel + run-all + conclusion-equivalence check against the spec's preserved-answers requirement.

## Open Questions

- None that change specs, approach, or tasks. Cosmetic choices (exact helper names, first-look cell titles, figure sizes) are settled during implementation.
