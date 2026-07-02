# Experience Capture

This folder stores Amir's trading experience capture system.

It has two main sides:

- `questions/` contains the English Markdown questionnaire split by section.
- `answers/` contains captured answers, normalized interpretations, images, notes, and manifests for each question code.

The goal is to convert raw human trading experience into:

- hard rules
- features
- labels
- tests
- AI model contracts
- execution policies
- backtest requirements

## Main questionnaire

Start here:

- `questions/README.md`
- `questions/QUESTIONNAIRE_INDEX_EN.md`

## Answer convention

For each question code, store the answer under:

- `answers/<QUESTION_CODE>/answer_raw_en.md`
- `answers/<QUESTION_CODE>/answer_normalized_en.md`
- `answers/<QUESTION_CODE>/notes_en.md`
- `answers/<QUESTION_CODE>/images/`
- `answers/<QUESTION_CODE>/manifest.json`

## Existing answer example

- `answers/BASE-01/`
