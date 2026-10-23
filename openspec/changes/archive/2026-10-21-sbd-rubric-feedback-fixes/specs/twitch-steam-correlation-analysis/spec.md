# Spec Delta

## ADDED Requirements

### Requirement: Join rationale and coverage narrated in markdown
The notebook SHALL explain, in markdown adjacent to the Twitch load and join cells, why `(Game, Month)` is the chosen join granularity given Steam's daily/hourly data and Twitch's monthly data, and SHALL present a per-game coverage summary (months matched in both sources, Steam-only months, Twitch-only months) derived from the join's own output rather than leaving those counts unnarrated.

#### Scenario: Granularity choice explained
- **WHEN** a reader reaches the Twitch load/join cells
- **THEN** a markdown cell states why Steam data is aggregated to monthly before joining and why Twitch data (already monthly) is not disaggregated, with reference to the underlying sampling frequencies of each source

#### Scenario: Per-game coverage table shown
- **WHEN** the join cell's existing Steam-only/Twitch-only month counts are computed
- **THEN** the notebook displays those counts broken down per game (not only as dataset-wide totals), so a reader can see which games have weak overlap between the two sources

#### Scenario: Second-source consideration documented
- **WHEN** a reader reaches the Twitch integration section
- **THEN** a markdown note states whether any other source besides Twitch (e.g. release dates, pricing) was considered for integration and why it was or was not added
