# Design

## Context

See proposal.md Why. Current state: `BDA/` contains only `steam_data.csv` (2.9M, `;`-separated, quoted, UTF-8 BOM, 62,267 rows, columns Game/DateTime/Players/Average Players, ~76% empty Average Players, 10 games, dates 2007-09-19 to 2026-10-05). No notebook, no specs exist. Constraint from request: notebook lives in `BDA/`, pandas for exploration with matplotlib allowed for one quick check; keep it superficial.

## Goals / Non-Goals

**Goals:**
- One runnable notebook at `BDA/steam_notebook.ipynb` that reproduces the same first-look outputs for everyone.
- Correct parsing on first run (separator, encoding, header) without editing the CSV.
- Surface warts (object dtypes, empty Average Players, wide date range) without fixing them.

**Non-Goals:**
- No type coercion strategy, no cleaning/filling, no date parsing beyond display of min/max.
- No styling, no multi-figure EDA, no reusable modules or tests.
- No dependency or environment changes beyond assuming pandas + matplotlib + Jupyter kernel exist.

## Decisions

- **Location `BDA/steam_notebook.ipynb` over repo root:** keeps data + exploration co-located, short relative path (`steam_data.csv`); alternative root-level notebook rejected because the dataset lives in `BDA/` and the request explicitly scopes it there.
- **pandas for all tabular inspection, matplotlib for at most one quick check:** matches the updated request (pandas-only relaxed to allow one plot); alternative pure-pandas rejected because a single players-over-time or per-game count plot catches parse errors faster than text alone, and a full plotting section rejected as out of scope.
- **Explicit `sep=';'` + `encoding='utf-8-sig'` on load:** observed BOM + semicolons break default `read_csv`; alternative of default load + cleanup cells rejected as it would display a single mangled column on first run.
- **Cell order: imports -> load -> shape/columns -> info/dtypes -> missing -> describe -> head/tail -> games/date glimpse -> one quick matplotlib check:** linear narrative from "did it load?" to "what does it look like?"; no functions, no widgets, outputs inline.
- **Show missingness raw (`isna().sum()`) and leave Average Players empty:** superficial goal means reporting, not deciding treatment; alternative of drop/fill rejected as analysis, not exploration.

## Risks / Trade-offs

- [Risk] Notebook outputs contain absolute paths or environment-specific kernel metadata -> Mitigation: use relative path `steam_data.csv` (same dir) and default kernel, clear outputs only if review asks.
- [Risk] Dates/numbers load as objects and confuse readers -> Mitigation: display dtypes via `info()` as-is; do not coerce, note the observation in markdown.
- [Risk] Scope creep into full EDA -> Mitigation: cap at ~7 short cells + 1 plot; reviewers reject extra sections.
- [Trade-off] Single quick plot adds matplotlib dependency vs pure-pandas simplicity — accepted because the request explicitly allows it and it aids sanity-checking.

## Migration Plan

Not applicable — new file only, no deployment. Rollback is deleting `BDA/steam_notebook.ipynb`.

## Open Questions

None — remaining choices (exact plot type, head N) are cosmetic and do not change specs or tasks.
