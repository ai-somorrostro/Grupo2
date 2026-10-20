# twitch-steam-correlation-analysis Specification

## Purpose

Lets the Steam exploration notebook answer cross-platform questions by relating each game's Steam concurrent-player history to its Twitch monthly viewership, covering correlation, lead/lag, lifecycle divergence, and seasonality.

## Requirements

### Requirement: Twitch monthly dataset joined to Steam data
The notebook SHALL load `Mejoras/csv/twitch_games_monthly_historical.csv` through a canonical preparation path (semicolon separator, BOM/whitespace handling, numeric and datetime coercion) and make it joinable with the existing `diario_juego` Steam frame on `(Game, Month)`, without altering the existing Steam load/cleaning cells.

#### Scenario: Monthly Twitch frame available for all ten games
- **WHEN** the notebook's Twitch load cell runs
- **THEN** it produces a cleaned monthly frame covering all 10 games present in `steam_data.csv`, with `AverageViewers`, `PeakViewers`, `HoursWatched`, `HoursStreamed`, `AverageChannels`, and `PeakChannels` coerced to numeric and `DateTime`/`Month` coerced to a comparable period/timestamp type

#### Scenario: Join produces one row per game-month with both signals
- **WHEN** the Steam daily frame is resampled to monthly and joined with the Twitch monthly frame on `(Game, Month)`
- **THEN** the resulting frame has, for each matched game-month, both a Steam players aggregate and the Twitch `AverageViewers`/`PeakViewers` values, with unmatched months left as missing rather than dropped or coerced to zero

#### Scenario: Weaker Twitch datasets excluded
- **WHEN** a reviewer inspects the new load cell(s) and analysis cells
- **THEN** neither `twitch_top_games_365d.csv` nor `twitch_streamer_broadcasts_combined.csv` is read or referenced anywhere in the notebook

### Requirement: Player-viewer correlation question
The notebook SHALL answer, per game, whether monthly Steam players and monthly Twitch average viewers move together, reporting a correlation coefficient per game ranked from strongest to weakest relationship, with an accompanying visualization.

#### Scenario: Correlation table and plot
- **WHEN** the correlation cell runs on the joined monthly frame
- **THEN** it displays a table with one row per game showing its Pearson correlation coefficient between `Players` and `AverageViewers`, sorted by strength, and renders a plot (e.g. per-game scatter or annotated comparison) built through the notebook's shared `configurar`/plotting helpers

#### Scenario: Insufficient overlapping months handled
- **WHEN** a game has fewer than 2 overlapping game-months between the Steam and Twitch frames
- **THEN** that game is excluded from the correlation ranking with no uncaught exception, and the notebook states which games were excluded and why

### Requirement: Lead-lag and viral-moment analysis
The notebook SHALL determine, per game, whether Twitch viewership changes tend to precede or follow Steam player-count changes, and SHALL identify each game's largest month-over-month viewership jump together with whether a comparable Steam player jump occurs in the same or an adjacent month.

#### Scenario: Cross-correlation classification per game
- **WHEN** the lead-lag cell computes cross-correlation between the two monthly series at lags from -3 to +3 months per game
- **THEN** it classifies each game into one of "Twitch leads", "Steam leads", "synced", or "no clear relationship", and displays the classifications in a table

#### Scenario: Among Us worked example precedes generalization
- **WHEN** the lead-lag/viral section is read top to bottom
- **THEN** it first walks through Among Us' September 2020 viewership spike as a named, concrete example of the lag computation before presenting the generalized per-game results

#### Scenario: Viral-moment event table for all ten games
- **WHEN** the viral-moment cell runs
- **THEN** it produces a table with one row per game showing its largest month-over-month `AverageViewers` percentage jump, the corresponding month, and the Steam `Players` percentage change in that same or an adjacent month, so each game can be read as "matched by a Steam spike" or "Twitch-only moment"

### Requirement: Divergent lifecycle trajectories
The notebook SHALL compare each game's recent-years trend direction on Steam against its trend direction on Twitch, flagging games where the two trends disagree.

#### Scenario: Per-game trend slopes computed on both signals
- **WHEN** the lifecycle cell runs
- **THEN** it computes a trend slope (or equivalent direction indicator) over the same recent-years window for both `Players` and `AverageViewers`, per game

#### Scenario: Divergent games flagged
- **WHEN** a game's Steam trend direction and Twitch trend direction disagree (one rising while the other is flat or falling, or vice versa)
- **THEN** that game is flagged as divergent in the output table, and the notebook explicitly calls out the Counter-Strike 2 Twitch-history-predates-CS2 caveat if that game appears in the divergent set

### Requirement: Shared seasonality vs. idiosyncratic patterns
The notebook SHALL compare month-of-year averages of Steam players and Twitch viewers per game to distinguish games that share a calendar-driven pattern across both platforms from games whose pattern appears on only one platform or follows a non-calendar cycle.

#### Scenario: Month-of-year comparison per game and signal
- **WHEN** the seasonality cell runs
- **THEN** it computes, per game, the average `Players` and average `AverageViewers` grouped by calendar month (Jan-Dec) across all available years, and visualizes both signals for comparison

#### Scenario: Idiosyncratic pattern noted
- **WHEN** a game's within-year pattern does not align between the two platforms, or does not follow a plausible calendar-driven explanation
- **THEN** the notebook's accompanying text notes this as an idiosyncratic (non-seasonal) pattern rather than presenting it as shared seasonality

### Requirement: Known data caveats are guarded and documented
The notebook SHALL guard against the known data-quality issues in the Twitch monthly dataset and document them where they affect a question's interpretation.

#### Scenario: Division-by-zero guarded for Among Us
- **WHEN** any ratio or percentage-change computation involving `AverageViewers` encounters a zero value (true for Among Us before September 2020)
- **THEN** the computation does not raise an exception or silently produce `inf`/`NaN` propagated into a displayed conclusion; the affected rows are excluded or explicitly marked

#### Scenario: Counter-Strike 2 lineage caveat surfaced
- **WHEN** the notebook presents any question whose output is affected by Counter-Strike 2's Twitch history starting in 2015 (years before the CS2 release, carried over from the CS:GO-era directory page)
- **THEN** that section includes a note clarifying the data reflects the Counter-Strike franchise's Twitch directory page lineage, not literal CS2-only history
