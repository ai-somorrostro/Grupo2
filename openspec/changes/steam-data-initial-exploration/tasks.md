# Tasks

## 1. Notebook scaffolding

- [x] 1.1 Create `BDA/steam_notebook.ipynb` with imports (pandas, matplotlib) and CSV load using relative path plus correct separator/encoding, and verify the notebook opens and the load cell shows ~62k rows x 4 columns
- [x] 1.2 Add shape/structure cells (shape, columns/dtypes, info summary) and verify outputs display rows/columns and non-null counts when run top-to-bottom

## 2. Superficial inspection

- [x] 2.1 Add missing-values and describe cells and verify per-column missing counts (including largely-empty Average Players) and describe output render
- [x] 2.2 Add data glimpse cells (head, tail, distinct games with count, DateTime min/max) and verify head/tail samples, 10 games, and observed date range appear in outputs
- [x] 2.3 Add one quick matplotlib sanity-check plot (e.g. rows per game or players over time) and verify the figure renders without extra analysis cells

## 3. Final check

- [x] 3.1 Restart kernel and run all cells top-to-bottom and verify no errors and no out-of-scope cleaning/modeling content remains
