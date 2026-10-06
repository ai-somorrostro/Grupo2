# steam-notebook-cleanup Specification

## Purpose

Keep the Steam exploration as one maintainable, reproducible notebook whose first-look and analytical answers stay equivalent while duplicated cleaning, plotting, and coupling logic is removed.

## Requirements

### Requirement: Single notebook narrative
The notebook SHALL remain a single file at `BDA/steam_notebook.ipynb` covering both the first-look and the analysis sections, runnable top-to-bottom without splitting into multiple notebooks.

#### Scenario: Run all cells in order
- **WHEN** a user opens `BDA/steam_notebook.ipynb` with `BDA/steam_data.csv` present and runs all cells in order
- **THEN** all cells execute without error and produce the first-look outputs plus the answers to the existing analytical questions

#### Scenario: No split files
- **WHEN** a reviewer lists notebook files for this exploration
- **THEN** there is exactly one exploration notebook and no sibling analysis notebook carrying part of the questions

### Requirement: Canonical load and cleaning path
The notebook SHALL define exactly one canonical data-preparation path (CSV load with `;` separator and BOM handling, datetime coercion, numeric coercion, daily-grain derivation) that all question cells reuse instead of repeating per-cell cleaning copies.

#### Scenario: No per-cell cleaning copies
- **WHEN** a reviewer inspects the question cells (mes, hora, pico, retencion, estable, ano, popularidad, crecimiento, patrones, tendencia)
- **THEN** none of them re-implements CSV parsing, datetime/numeric coercion, null-dropping, or daily averaging from scratch; they consume the canonical prepared frames

#### Scenario: Coherent datetime handling
- **WHEN** the notebook prepares `DateTime`
- **THEN** parsing (including `errors="coerce"` behavior) is defined once and later cells do not re-parse with divergent options or mutate the raw frame in conflicting ways

### Requirement: Shared presentation logic
The notebook SHALL reuse shared logic for repeated presentation patterns (figure setup with titles/labels/grid/layout, Styler number/date formatting, max/min summary printing) instead of duplicating the full boilerplate in every question cell.

#### Scenario: Plot boilerplate deduplicated
- **WHEN** a reviewer compares the plotting cells across questions
- **THEN** figure creation, labeling, grid, and layout calls go through the shared path rather than ten independent copies of the same settings

#### Scenario: Table formatting deduplicated
- **WHEN** the notebook displays styled comparison tables
- **THEN** number and date formatting is applied through the shared formatting path with consistent output across questions

### Requirement: Parameterized hourly analysis
The notebook SHALL answer the hourly seasonality question through a single parameterized analysis over a date window, covering both the full-history view and the recent-window view (post early-September 2026), instead of two near-identical duplicated cells.

#### Scenario: Both hourly views from one path
- **WHEN** the notebook computes average players per hour
- **THEN** the full-history result and the recent-window result are produced by the same logic with different window parameters, and the markdown caveat about the `00:00` daily-row artifact is retained

### Requirement: Explicit per-cell inputs without hidden coupling
Each analytical cell SHALL build or receive its inputs explicitly so it does not depend on same-named variables with different content or on variables created as side effects of another question cell.

#### Scenario: Retention plot is self-sufficient
- **WHEN** a user runs the retention comparison cell and the retention plot cell in order (or re-runs them after a kernel restart in order)
- **THEN** the plot cell obtains its comparison frame and per-game histories explicitly rather than relying on leftover variables from the prior cell, and no two cells assign different contents to the same shared variable name

### Requirement: Consolidated first-look with correct date handling
The notebook SHALL present a consolidated first-look (shape/columns/dtypes/info, missing counts, descriptives, head/tail samples, distinct games, observed date range) where the date range is computed from parsed datetimes rather than raw strings.

#### Scenario: Date range from parsed datetimes
- **WHEN** the notebook reports the observed date range
- **THEN** the min and max values are derived from the datetime-parsed column and match the dataset span (2007-09-19 through 2026-10-05 or equivalent after coercion)

#### Scenario: No redundant glimpse cells
- **WHEN** a reviewer reads the first-look section
- **THEN** columns/dtypes/info, missing/describe, and head/tail/glimpse each appear once without separate cells repeating the same inspection

### Requirement: Average Players column preserved and documented
The notebook SHALL keep the `Average Players` column, surface its coverage (counts/non-null share), and document that current analytical questions use `Players` while `Average Players` is retained without filling or dropping.

#### Scenario: Coverage visible
- **WHEN** the notebook is executed
- **THEN** outputs show the per-column missing counts including the largely-empty `Average Players` column and a note stating it is preserved as-is

### Requirement: Preserved analytical answers
The cleaned notebook SHALL preserve the existing analytical answers within rounding: monthly and hourly peaks, per-game maxima led by PUBG, retention ranking led by Project Zomboid, stability ranking led by Dota 2, yearly ranking led by 2025, current top-three popularity, year-over-year growers, multi-game monthly co-movements, and the recent median-growth trend conclusion.

#### Scenario: Answers equivalent after cleanup
- **WHEN** the cleaned notebook is executed top-to-bottom
- **THEN** each question prints the same conclusion (game names, peak periods, rankings, and growth signs) as before the cleanup, differing at most in formatting or rounding presentation
