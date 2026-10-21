# Spec Delta

## MODIFIED Requirements

### Requirement: Single notebook narrative
The notebook SHALL remain a single file at `SBD/steam_notebook.ipynb` covering both the first-look and the analysis sections, runnable top-to-bottom without splitting into multiple notebooks.

#### Scenario: Run all cells in order
- **WHEN** a user opens `SBD/steam_notebook.ipynb` with `SBD/steam_data.csv` present and runs all cells in order
- **THEN** all cells execute without error and produce the first-look outputs plus the answers to the existing analytical questions

#### Scenario: No split files
- **WHEN** a reviewer lists notebook files for this exploration
- **THEN** there is exactly one exploration notebook and no sibling analysis notebook carrying part of the questions

## ADDED Requirements

### Requirement: Record validation in the first-look section
The notebook's first-look section SHALL validate the loaded records beyond shape/dtypes/null-counts: exact row duplicates, `(Game, DateTime)` duplicates, implausible `Players` values (negative or zero), the count of rows dropped by the canonical cleaning path's `dropna`, each game's observed first and last date, and a note on whether the per-row sampling grain changes across each game's history (daily-only vs. mixed daily/hourly). Each check SHALL end with a short markdown conclusion stating what was found and what, if anything, was decided as a result.

#### Scenario: Duplicate checks reported
- **WHEN** the first-look validation cell(s) run
- **THEN** the output states the count of exact duplicate rows and the count of `(Game, DateTime)` duplicate rows, even when both counts are zero

#### Scenario: Range checks reported
- **WHEN** the first-look validation cell(s) run
- **THEN** the output states the count of rows with a negative or zero `Players` value, even when that count is zero

#### Scenario: Dropped-row count surfaced
- **WHEN** the canonical cleaning path removes rows via `dropna(subset=["Game", "DateTime", "Players"])`
- **THEN** the first-look section states how many rows were dropped and what share of the total that represents

#### Scenario: Per-game date span and lineage caveat
- **WHEN** the first-look section reports per-game observed date spans
- **THEN** it lists each game's first and last recorded date, and if a game's span begins before that game's real-world release date (as is the case for Counter-Strike 2, whose span starts in 2011), the output notes that the data reflects a franchise directory page rather than literal release-to-date history

#### Scenario: Sampling-grain change noted
- **WHEN** the first-look section documents dataset structure
- **THEN** it states, for at least the games affected, that recent history is recorded at a finer (hourly) grain than older history (daily), as a documented caveat for any downstream cell that averages across time without first aggregating to a consistent grain
