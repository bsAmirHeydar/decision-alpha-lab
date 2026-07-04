# Remaining Questions v3 Split

This folder stores each remaining NDS experience-capture question in its own folder.

It is a safe overlay and does not delete or overwrite previous answer records.

## Structure

```text
docs/experience_capture/questions/remaining_v3_split/<QUESTION_CODE>/
  question_fa.md
  question_en.md
  manifest.json
```

## Answer Capture Workflow

When Amir answers one question, create a separate professional English answer record under:

```text
docs/experience_capture/answers/<QUESTION_CODE>/
  question_en.md
  answer_raw_en.md
  answer_normalized_en.md
  notes_en.md
  manifest.json
  images/
```

Do not merge answers together.  
Do not overwrite previous answer folders.  
Do not delete prior captured records.
