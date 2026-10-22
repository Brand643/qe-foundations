"""qe_foundations/ingestion/loader.py  -  TASK 6 (about 30 min)

Ties everything together:
    file -> reader (format) -> validate_record (rules) -> IngestionReport

Error POLICY (the heart of the milestone):
    SourceError            -> the whole file is unusable -> let it propagate (raise)
    RecordValidationError  -> one record is bad          -> COLLECT it and carry on

Already done for you: the IngestionReport and BatchResult classes' constructors
and the READERS lookup table. You write the TODOs.
"""

import csv
from pathlib import Path

from .contexts import LoadSession
from .exceptions import (
    DuplicateIdError,
    RecordValidationError,
    SourceError,
    SourceNotFoundError,
    UnsupportedFormatError,
)
from .readers import read_csv_records, read_json_records, read_xml_records
from .validation import validate_record

# Which reader handles which file extension (always compare lower-case suffixes).
READERS = {
    ".csv": read_csv_records,
    ".json": read_json_records,
    ".xml": read_xml_records,
}


class IngestionReport:
    """Result of loading ONE file: the valid records AND every rejected one."""

    def __init__(self, source, rows_seen=0):
        self.source = source
        self.rows_seen = rows_seen
        self.valid = []       # clean dicts returned by validate_record
        self.rejected = []    # RecordValidationError instances

    def summary(self):
        """Return a one-line summary of the file's results."""
        return f"{Path(self.source).name}: {self.rows_seen} rows seen, {len(self.valid)} valid, {len(self.rejected)} rejected"

    def rejected_rows(self):
        """Return rejected records as dictionaries, ordered by row."""
        return [
            {
                "source": Path(self.source).name,
                "row": error.row,
                "field": error.field,
                "reason": str(error),
            }
            for error in sorted(self.rejected, key=lambda error: error.row)
        ]

    def check_invariants(self):
        """Assert statements"""
        assert (len(self.valid) + len(self.rejected) == self.rows_seen), "Valid and rejected counts must equal rows seen"

        valid_ids = [record["id"] for record in self.valid]
        assert len(valid_ids) == len(set(valid_ids)), "Valid records must have unique IDs"

        assert all(isinstance(error, RecordValidationError) for error in self.rejected), "Every rejected item must be a RecordValidationError"

class BatchResult:
    """Result of loading a whole folder."""

    def __init__(self):
        self.reports = []           # IngestionReport, one per file that could be read
        self.failed_sources = []    # SourceError instances, one per unusable file

    def totals(self):
        """Summarize successful files and rejected records across the batch."""
        return {
            "files_ok": len(self.reports),
            "files_failed": len(self.failed_sources),
            "valid": sum(len(report.valid) for report in self.reports),
            "rejected": sum(len(report.rejected) for report in self.reports),
        }


def load_test_cases(path):
    """Load one test-data file and collect invalid records."""
    path = Path(path)

    with LoadSession(path):
        suffix = path.suffix.lower()
        reader = READERS.get(suffix)

        if reader is None:
            raise UnsupportedFormatError(path, path.suffix)

        raw_records = reader(path)
        report = IngestionReport(path.name, rows_seen=len(raw_records))
        seen_ids = set()

        for row_number, raw in enumerate(raw_records, start=1):
            try:
                record = validate_record(row_number, raw)

                if record["id"] in seen_ids:
                    raise DuplicateIdError(row_number, record["id"])

                seen_ids.add(record["id"])
                report.valid.append(record)

            except RecordValidationError as error:
                report.rejected.append(error)

        report.check_invariants()
        return report


def load_directory(folder):
    """Load every file directly inside a folder."""
    folder = Path(folder)

    if not folder.is_dir():
        raise SourceNotFoundError(folder)

    batch = BatchResult()

    for path in sorted(folder.iterdir(), key=lambda item: item.name):
        if not path.is_file():
            continue

        try:
            report = load_test_cases(path)
        except SourceError as error:
            batch.failed_sources.append(error)
        else:
            batch.reports.append(report)

    return batch


def write_rejected_csv(report, out_path):
    """Write rejected records to a CSV file and return its Path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["source", "row", "field", "reason"]

    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report.rejected_rows())

    return out_path
