# Ingestion module - design notes (Week 2, Day 2)

Answer in your own words, 2-4 sentences each.

## 1. Exceptions or assertions?

In `validate_record` I raise exceptions for a negative duration, but in
`IngestionReport.check_invariants` I use `assert`. Why is each the right tool there?

In validate_record, I use exceptions because the input data comes from external files and may contain invalid values, such as a negative duration. In IngestionReport.check_invariants, I use assertions because they check that my own code maintains correct internal conditions, such as ensuring every row is either valid or rejected. Exceptions allow the program to handle bad input, while assertions help detect programming mistakes.

## 2. Stop or collect?

Why is a malformed JSON file a `SourceError` that stops loading, while a record with
a bad status is a `RecordValidationError` that is collected? Who benefits from this split?

A malformed JSON file is a SourceError because the file cannot be read correctly, so the loader cannot reliably process its records. A record with a bad status is a RecordValidationError because the problem is limited to one record, allowing the loader to reject it and continue processing the others. This split benefits users because one unusable file does not stop an entire batch, and valid records can still be processed.

## 3. What did the context managers buy you?

Name two things that `open_source` / `LoadSession` do for the caller that you would otherwise
have to remember to do at every call site.

open_source ensures that files are closed properly, even when an error occurs, and translates file-reading problems into meaningful custom exceptions. LoadSession automatically records the elapsed time and whether loading completed or failed. This saves the caller from having to manage file cleanup and timing manually every time a file is loaded.

## 4. Your hardest bad-input case

Which sample file or record took you longest to handle, and what was the cause?

The hardest case for me was handling invalid records, such as a test case with a negative duration or an invalid status. I had to make sure the program rejected the bad record and recorded the reason without stopping the processing of other records. This helped me understand how validation and custom exceptions work together.
