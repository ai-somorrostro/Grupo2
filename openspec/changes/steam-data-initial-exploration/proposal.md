# Proposal

## Why

The team has a `BDA/steam_data.csv` dataset (~62k rows, 10 games) with no shared, reproducible first look. A minimal notebook gives everyone the same basic facts (shape, columns, missing data, value ranges) before any deeper analysis.

## What Changes

- Add `BDA/steam_notebook.ipynb` as an initial, superficial exploration notebook.
- Notebook loads the CSV with correct parsing (`;` separator, BOM handling) and shows basic shape/info/data only.
- Allow `pandas` for all exploration plus `matplotlib` for one quick visual sanity check only.
- No cleaning, no feature engineering, no modeling, no refactoring of existing code.

## Capabilities

### New Capabilities

- `steam-data-exploration`: initial superficial exploration of the Steam dataset via a checked-in notebook (load, shape, info, missing values, basic glimpse, one quick matplotlib check).

### Modified Capabilities

- None.

## Impact

- Affected: new file `BDA/steam_notebook.ipynb` only; read-only use of `BDA/steam_data.csv`.
- Dependencies: Python kernel with `pandas` and `matplotlib` available; no new package installs or config changes in this change.
- No API, production code, or existing behavior impacted.
