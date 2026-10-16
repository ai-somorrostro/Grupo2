# Tasks

## 1. Canonical preparation and helpers

- [x] 1.1 Add canonical load+preparation cells (BOM/`;` load, datetime + numeric coercion, `Fecha` daily grain, daily-averaged frame, `Año/Mes/Dia/Hora` once) and verify all question cells can import them without their own parsing code
- [x] 1.2 Add in-notebook helpers for figures, Styler formatting, and max/min summaries and verify one existing plot and one styled table render identically through them
- [x] 1.3 Freeze raw/prepared frames as read-only (copies per question, no in-place mutation) and verify no question cell assigns to the canonical frames

## 2. First-look consolidation and Average Players note

- [x] 2.1 Consolidate first-look into structure/quality/glimpse cells and verify shape, columns/dtypes/info, missing counts, describe, head, tail, game list, and date range each appear once
- [x] 2.2 Fix date min/max to use parsed datetimes and verify the reported span matches the dataset (2007-09-19 through 2026-10-05 or coerced equivalent)
- [x] 2.3 Document `Average Players` coverage (missing counts/non-null share plus preserved-as-is note) and verify the column is neither dropped nor filled

## 3. Question-cell deduplication

- [x] 3.1 Replace per-cell cleaning copies with the canonical frames (retencion, estable, anual, popularidad, crecimiento, patrones, tendencia) and verify no divergent `to_datetime`/`to_numeric`/`dropna` options remain
- [x] 3.2 Parameterize the hourly analysis by date window (full history + recent window from 2026-09-05) and verify both hourly results plus the `00:00`-artifact markdown are retained
- [x] 3.3 Remove hidden coupling (explicit rebuild of retention comparison/histories in the plot cell; distinct variable names per question, no reused `promedios_diarios` content) and verify each analytical cell is self-sufficient in run-all order
- [x] 3.4 Route remaining plots and styled tables through the shared helpers and verify all 10 question conclusions (mes/hora/pico/retencion/estable/ano/popularidad/crecimiento/patrones/tendencia) match pre-cleanup within rounding

## 4. Final check

- [x] 4.1 Restart kernel and run all cells top-to-bottom and verify no errors, exactly one notebook file changed, and all question answers and plot semantics are equivalent to before
