# Proposal

## Why

The `BDA/steam_notebook.ipynb` notebook grew from a ~7-cell first look into a 38-cell single narrative (first look + 10 analytical questions) with copy-pasted cleaning, plotting, and formatting logic. Fixes are now high-risk: a parse change in one cell is easily missed in six others, and hidden cross-cell variables break re-runs.

## What Changes

- Restructure `BDA/steam_notebook.ipynb` as a single notebook covering both first-look and analysis, preserving all current analytical answers.
- Introduce one canonical load+parse step and one canonical cleaning step (datetime coercion, numeric coercion, `Fecha` daily grain, daily-averaged frame) used by all question cells; remove per-cell cleaning copies (fixes A, B, C).
- Introduce small shared helpers for repeated plotting boilerplate, Styler formatting, and idxmax/idxmin summaries (fixes D).
- Parameterize the hourly analysis by date window instead of two near-identical cells (fixes E).
- Remove hidden cross-cell coupling (rebuild `comparacion`/`historiales` explicitly per cell; stop reusing `promedios_diarios` with different content) (fixes F).
- Consolidate first-look overlap (columns/dtypes/info, missing/describe, head/tail/glimpse) and fix string-based date min/max to use parsed datetimes (fixes G).
- Keep and document the `Average Players` column (surface coverage, state it is not used by current questions); do not drop or fill it.

## Capabilities

### New Capabilities

- `steam-notebook-cleanup`: maintainable single-notebook structure for the Steam exploration — canonical cleaning path, shared helpers, explicit per-cell inputs, preserved analytical outputs, documented `Average Players` handling.

### Modified Capabilities

- None (no main specs exist; prior `steam-data-exploration` delta described the original first-look only and is not modified here).

## Impact

- Affected: `BDA/steam_notebook.ipynb` only; read-only use of `BDA/steam_data.csv`. No CSV changes, no dependency changes (pandas + matplotlib + Jupyter kernel assumed).
- Outputs must remain equivalent: same 10 question answers (mes/hora/pico/retencion/estable/ano/popularidad/crecimiento/patrones/tendencia) within rounding, same plots semantically.
- No API, production code, or environment config impacted.
