# Design

## Context

See `proposal.md` (Why) and `specs/steam-notebook-cleanup/spec.md` for motivation and behavior.
Current state in `SBD/steam_notebook.ipynb`:

- Cell 28 computes per-game mean/std of daily `Players` from `diario_juego`, derives relative variation (std/mean × 100), prints the Dota 2 conclusion, shows the full ranking table, and calls `barras(..., horizontal=True)`.
- Cell 26 (retention plot) is the pattern to mirror: recompute via `calcular_retencion(diario_juego)`, take `iloc[0]` / `iloc[-1]`, `plt.plot(Fecha, % of own peak)` per game, `configurar(...)`, legend, `figsize=(12, 6)`, `linewidth=1.8`.
- Shared helpers live in cell 7 (`configurar`, `tabla`, `barras`); all question cells consume the canonical `diario_juego` frame from cell 5.

## Goals / Non-Goals

**Goals:**

- Make stability visible over time with the same visual language as the retention comparison.
- Keep the metric, ranking, table, and printed text byte-equivalent in meaning (only the figure changes).

**Non-Goals:**

- No change to the variation formula, cleaning path, or any other question cell.
- No new helpers, files, or dependencies.

## Decisions

### 1. Normalize to % of each game's own daily mean

Plot `Players / mean(Players) × 100` per game over `Fecha` (100 = own average), rather than raw player counts.

- *Why:* raw scales differ by an order of magnitude across games (plus historic peaks), so absolute lines would flatten the stable game into invisibility — the exact problem the retention plot solved by normalizing to % of own peak.
- *Alternative considered (raw counts):* rejected — illegible scale clash, contradicts the spec's "values expressed as percentage of each game's own daily mean".
- *Alternative considered (z-score):* rejected — harder for notebook readers to interpret than "100 = my average".

### 2. Best (`iloc[0]`) vs worst (`iloc[-1]`) from the already-sorted table

Reuse the sorted `estabilidad_tabla` ordering; no new selection logic.

- *Why:* symmetric with retention (`iloc[0]` / `iloc[-1]`), zero new semantics, automatically tracks data changes.
- *Alternative considered (best vs second-best):* rejected in explore — worst-case contrast tells the stability story most honestly; outlier concern is mitigated because both series are mean-normalized.

### 3. Placement: new self-sufficient plot cell after the table cell (mirror cells 25–26)

Keep cell 28 as table + conclusion (minus the `barras(...)` call) and add a following plot cell that recomputes from `diario_juego` instead of reusing cell-28 locals.

- *Why:* matches the existing retention split and the `steam-notebook-cleanup` "explicit per-cell inputs without hidden coupling" requirement — plot cell must run correctly in order without depending on cell-28 variable names.
- *Alternative considered (inline replace inside cell 28):* viable fallback, but couples plot to table-cell locals and breaks the established table/plot split pattern.

### 4. Reuse `configurar()` with retention-style labels

Title like "Estabilidad: juego más y menos estable", xlabel "Fecha", ylabel "Jugadores como porcentaje de su promedio (%)", plus legend and `tight_layout()`.

- *Why:* satisfies the shared-presentation-logic requirement with no new boilerplate.

## Risks / Trade-offs

- [Daily noise over a multi-year span] → Accept: retention plot already sets the precedent of plotting raw daily series; readability is preserved because normalization centers both lines on 100. A rolling average is deliberately NOT added (would hide the very variability being shown).
- [Least-stable game could have a short history] → Mitigation: both lines share the same `Fecha` axis; a shorter line is still honest. If review shows an unrepresentative outlier, revisit best-vs-second-best as a follow-up change.
- [Notebook outputs are committed artifacts] → Re-executed notebook must be saved so the rendered figure updates; tasks cover this.
