# Spec Delta

## Purpose

Gives the notebook a place to justify its tool choices against alternatives used elsewhere in the project, and a closing section that synthesizes the analysis across questions so the written report has one cross-cutting narrative to cite.

## ADDED Requirements

### Requirement: Tool choice justification
The notebook SHALL include a section justifying its use of pandas and matplotlib for this dataset, naming at least one concrete alternative already used elsewhere in the project (polars) and at least one plotting alternative (e.g. seaborn or plotly), with stated advantages and limitations of each relative to this dataset's size and the analysis performed, rather than asserting the choice without comparison.

#### Scenario: Pandas vs. polars comparison stated
- **WHEN** a reader reaches the tools section
- **THEN** it states at least one concrete advantage and one concrete limitation of pandas relative to polars for a dataset of this size (~62k rows) and shape, in the context of the batch, single-machine exploratory analysis performed here

#### Scenario: Plotting library comparison stated
- **WHEN** a reader reaches the tools section
- **THEN** it states why matplotlib was used over at least one alternative visualization library, with at least one concrete advantage and one limitation

### Requirement: Closing conclusions section
The notebook SHALL include a final section that synthesizes the analysis across questions, building on the per-question conclusions already stated in markdown next to each question's plot (the original Steam-only questions and the Twitch cross-platform questions), so a reader gets a cross-cutting narrative rather than a restated list, and so the written report has a single section to cite for the overall picture.

#### Scenario: Synthesis connects findings across questions
- **WHEN** a reader reaches the closing conclusions section
- **THEN** it groups related per-question findings into cross-cutting themes (e.g. popularity having multiple distinct dimensions, the Steam-Twitch relationship not being uniform across games) rather than repeating each question's conclusion in isolation, and does not contradict any individual question's own inline conclusion

#### Scenario: Scope and limitations stated
- **WHEN** the closing section characterizes what the analysis does and does not support
- **THEN** it states the caveats that qualify the whole analysis: that Steam and Twitch data have different temporal resolutions, that coverage between the two sources is uneven, that the most recent period is incomplete, and that observed co-movement (e.g. Twitch spikes aligning with Steam spikes) does not establish causation or generalize beyond the 10 analyzed games
