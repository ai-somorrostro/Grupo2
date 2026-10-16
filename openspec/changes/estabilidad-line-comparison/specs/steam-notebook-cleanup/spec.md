# Spec Delta

## ADDED Requirements

### Requirement: Stability best-vs-worst line comparison
The notebook SHALL answer "¿Cuál es el juego más estable?" with a line chart comparing the most stable game against the least stable game over time, where each line is normalized to its own daily mean (100 = own average), instead of a bar chart of all games.

#### Scenario: Two normalized lines shown
- **WHEN** a user runs the stability question cell(s) top-to-bottom
- **THEN** a single figure shows exactly two lines — one for the game with the lowest relative variation and one for the game with the highest — plotted over `Fecha` with values expressed as percentage of each game's own daily mean

#### Scenario: Stability ranking and conclusion unchanged
- **WHEN** the stability analysis executes
- **THEN** the comparison table, the relative-variation metric (std/mean × 100), and the printed conclusion still identify the same most stable game (Dota 2) within rounding as before the chart change

#### Scenario: Consistent with retention-plot conventions
- **WHEN** a reviewer compares the stability line chart with the retention comparison chart
- **THEN** both use the shared figure setup (titles, axis labels, grid, layout via the shared helper), a comparable figure size, one linewidth style for both series, and a legend identifying each game
