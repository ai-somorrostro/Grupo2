# Spec Delta

## Purpose

Provide a shared, reproducible first look at the Steam player dataset so the team agrees on its basic shape, contents, and data-quality warts before deeper analysis.

## ADDED Requirements

### Requirement: Notebook location and scope
The exploration SHALL be delivered as a single checked-in notebook at `BDA/steam_notebook.ipynb` limited to superficial inspection of `BDA/steam_data.csv`.

#### Scenario: Notebook opens and runs top-to-bottom
- **WHEN** a user opens `BDA/steam_notebook.ipynb` with `BDA/steam_data.csv` present and runs all cells in order
- **THEN** all cells execute without error and produce visible outputs for shape, info, and data glimpse

#### Scenario: No out-of-scope analysis present
- **WHEN** a reviewer inspects the notebook contents
- **THEN** there is no data cleaning, feature engineering, modeling, or multi-plot deep-dive — only loading plus basic inspection and at most one quick matplotlib check

### Requirement: Correct CSV loading
The notebook SHALL load the dataset so rows, columns, and values match the source file, handling its `;` separator and BOM/quoting.

#### Scenario: Row and column fidelity
- **WHEN** the notebook loads `BDA/steam_data.csv`
- **THEN** the resulting frame exposes the 4 source columns (Game, DateTime, Players, Average Players) and approximately 62k data rows

### Requirement: Basic shape and structure visibility
The notebook SHALL display the frame's shape, column list with types, and pandas info summary.

#### Scenario: Shape and info visible
- **WHEN** the notebook is executed
- **THEN** outputs show the (rows, columns) shape, column names/dtypes, and the `info()` summary including non-null counts

### Requirement: Data glimpse
The notebook SHALL show head and tail samples plus distinct games and the observed date range.

#### Scenario: Glimpse outputs present
- **WHEN** the notebook is executed
- **THEN** outputs include a head sample, a tail sample, the list/count of distinct games, and the min/max of DateTime

### Requirement: Missing values and basic descriptives
The notebook SHALL surface missing-value counts and basic descriptive statistics for numeric content.

#### Scenario: Missing and descriptives visible
- **WHEN** the notebook is executed
- **THEN** outputs show per-column missing counts (including the largely-empty Average Players column) and a `describe()` summary
