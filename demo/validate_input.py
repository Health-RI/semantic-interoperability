#!/usr/bin/env python3
"""Validate mapping input CSV files.

Expected files:
- input.csv: mapping rows to validate
- prefix.csv: prefix declarations used to validate CURIEs

The script defaults to semicolon-delimited CSV files and emits a readable
validation report. It exits with status code 0 when validation passes and 1
when validation errors are found.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EXPECTED_INPUT_COLUMNS = [
    "type",
    "mapping",
    "subject_id",
    "subject_label",
    "predicate_id",
    "predicate_modifier",
    "object_id",
    "object_label",
    "replaces",
    "aligns",
    "implements",
]

EXPECTED_PREFIX_COLUMNS = ["prefix", "url"]
ALLOWED_TYPES = {"standard", "model"}
ALLOWED_PREDICATES = {
    "hriv:hasExactMeaning",
    "hriv:hasBroaderMeaningThan",
    "hriv:hasNarrowerMeaningThan",
}
ALLOWED_PREDICATE_MODIFIER = {"", "Not"}
IMPLEMENTS_ALLOWED_SOURCE_TYPE = "model"
IMPLEMENTS_ALLOWED_TARGET_TYPE = "standard"
ALIGNS_ALLOWED_SOURCE_TYPE = "standard"
ALIGNS_ALLOWED_TARGET_TYPE = "standard"

# Conservative CURIE validation:
# - prefix starts with a letter, then letters/digits/._-
# - local part must be non-empty and may contain common CURIE-safe chars
CURIE_RE = re.compile(
    r"^(?P<prefix>[A-Za-z][A-Za-z0-9._-]*):(?P<local>[A-Za-z0-9._~/%#?&=+\-]+)$"
)

# RDF langString-style validation.
#
# In the source CSV, labels are written like:
#   "Label"@en
#   "Self-identified Gender"@en-US
#
# When parsed by Python's csv module, such values are typically read as:
#   Label@en
#   Self-identified Gender@en-US
#
# Therefore the validator accepts both representations.
RAW_LANGSTRING_RE = re.compile(
    r'^"(?:[^"\\]|\\.)*"@[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$'
)
PARSED_LANGSTRING_RE = re.compile(r"^.+@[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")


@dataclass(frozen=True)
class ValidationError:
    message: str
    row_number: int | None = None
    column: str | None = None

    def render(self) -> str:
        location_parts: list[str] = []
        if self.row_number is not None:
            location_parts.append(f"row {self.row_number}")
        if self.column is not None:
            location_parts.append(f"column '{self.column}'")
        if location_parts:
            return f"- {' / '.join(location_parts)}: {self.message}"
        return f"- {self.message}"


class ValidationContext:
    def __init__(self) -> None:
        self.errors: list[ValidationError] = []

    def add(
        self, message: str, row_number: int | None = None, column: str | None = None
    ) -> None:
        self.errors.append(
            ValidationError(message=message, row_number=row_number, column=column)
        )

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate input.csv against the mapping constraints."
    )
    parser.add_argument(
        "--input",
        default="input.csv",
        help="Path to the input CSV file (default: input.csv)",
    )
    parser.add_argument(
        "--prefix",
        default="prefix.csv",
        help="Path to the prefix CSV file (default: prefix.csv)",
    )
    parser.add_argument(
        "--delimiter",
        default=";",
        help="CSV delimiter used by both files (default: ';')",
    )
    return parser.parse_args()


def read_csv_rows(path: Path, delimiter: str) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file '{path}' is missing a header row.")
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                normalized[key.strip()] = (value or "").strip()
            rows.append(normalized)
        return [name.strip() for name in reader.fieldnames], rows


def validate_prefix_file(
    path: Path, delimiter: str, ctx: ValidationContext
) -> dict[str, str]:
    if not path.exists():
        ctx.add(f"Prefix file '{path}' was not found.")
        return {}

    try:
        fieldnames, rows = read_csv_rows(path, delimiter)
    except Exception as exc:  # pragma: no cover - defensive error path
        ctx.add(f"Could not read prefix file '{path}': {exc}")
        return {}

    if fieldnames != EXPECTED_PREFIX_COLUMNS:
        ctx.add(
            f"Prefix file must have exactly these columns in this order: {EXPECTED_PREFIX_COLUMNS}. Found: {fieldnames}."
        )

    prefixes: dict[str, str] = {}
    for index, row in enumerate(rows, start=2):
        prefix = row.get("prefix", "")
        url = row.get("url", "")

        if not prefix:
            ctx.add("Prefix must not be empty.", row_number=index, column="prefix")
            continue
        if ":" in prefix:
            ctx.add("Prefix must not contain ':'.", row_number=index, column="prefix")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9._-]*", prefix):
            ctx.add(
                "Prefix must start with a letter and contain only letters, digits, '.', '_' or '-'.",
                row_number=index,
                column="prefix",
            )
        if not url:
            ctx.add("URL must not be empty.", row_number=index, column="url")
        if prefix in prefixes:
            ctx.add(
                "Prefix is duplicated in prefix.csv.", row_number=index, column="prefix"
            )
            continue

        prefixes[prefix] = url

    return prefixes


def validate_curie(
    value: str,
    prefixes: dict[str, str],
    ctx: ValidationContext,
    row_number: int,
    column: str,
) -> None:
    if not value:
        ctx.add("Value must not be empty.", row_number=row_number, column=column)
        return

    match = CURIE_RE.fullmatch(value)
    if not match:
        ctx.add(
            "Value must be a valid CURIE in the form prefix:localPart.",
            row_number=row_number,
            column=column,
        )
        return

    prefix = match.group("prefix")
    if prefix not in prefixes:
        ctx.add(
            f"CURIE prefix '{prefix}' is not declared in prefix.csv.",
            row_number=row_number,
            column=column,
        )


def validate_optional_curie(
    value: str,
    prefixes: dict[str, str],
    ctx: ValidationContext,
    row_number: int,
    column: str,
) -> None:
    if not value:
        return
    validate_curie(value, prefixes, ctx, row_number, column)


def validate_langstring(
    value: str, ctx: ValidationContext, row_number: int, column: str
) -> None:
    if not value:
        ctx.add("Value must not be empty.", row_number=row_number, column=column)
        return

    if not (
        RAW_LANGSTRING_RE.fullmatch(value) or PARSED_LANGSTRING_RE.fullmatch(value)
    ):
        ctx.add(
            'Value must be a langstring like "Label"@en or "Label"@en-US.',
            row_number=row_number,
            column=column,
        )


def validate_input_file(
    path: Path, delimiter: str, prefixes: dict[str, str], ctx: ValidationContext
) -> None:
    if not path.exists():
        ctx.add(f"Input file '{path}' was not found.")
        return

    try:
        fieldnames, rows = read_csv_rows(path, delimiter)
    except Exception as exc:  # pragma: no cover - defensive error path
        ctx.add(f"Could not read input file '{path}': {exc}")
        return

    if fieldnames != EXPECTED_INPUT_COLUMNS:
        ctx.add(
            f"Input file must have exactly these columns in this order: {EXPECTED_INPUT_COLUMNS}. Found: {fieldnames}."
        )

    mappings_seen: dict[str, int] = {}
    mappings_by_type: dict[str, set[str]] = {
        allowed_type: set() for allowed_type in ALLOWED_TYPES
    }
    replaces_references: list[tuple[int, str]] = []
    subject_ids_by_type: dict[str, set[str]] = {
        allowed_type: set() for allowed_type in ALLOWED_TYPES
    }
    aligns_references: list[tuple[int, str]] = []
    implements_references: list[tuple[int, str, str]] = []

    for row_number, row in enumerate(rows, start=2):
        mapping_type = row.get("type", "")
        mapping = row.get("mapping", "")
        subject_id = row.get("subject_id", "")
        subject_label = row.get("subject_label", "")
        predicate_id = row.get("predicate_id", "")
        predicate_modifier = row.get("predicate_modifier", "")
        object_id = row.get("object_id", "")
        object_label = row.get("object_label", "")
        replaces = row.get("replaces", "")
        aligns = row.get("aligns", "")
        implements = row.get("implements", "")

        if mapping_type not in ALLOWED_TYPES:
            ctx.add(
                f"Value must be one of {sorted(ALLOWED_TYPES)}.",
                row_number=row_number,
                column="type",
            )

        validate_curie(mapping, prefixes, ctx, row_number, "mapping")
        validate_curie(subject_id, prefixes, ctx, row_number, "subject_id")
        validate_langstring(subject_label, ctx, row_number, "subject_label")

        if predicate_id not in ALLOWED_PREDICATES:
            ctx.add(
                f"Value must be one of {sorted(ALLOWED_PREDICATES)}.",
                row_number=row_number,
                column="predicate_id",
            )
        else:
            validate_curie(predicate_id, prefixes, ctx, row_number, "predicate_id")

        if predicate_modifier not in ALLOWED_PREDICATE_MODIFIER:
            ctx.add(
                "Value must be empty or 'Not'.",
                row_number=row_number,
                column="predicate_modifier",
            )

        validate_curie(object_id, prefixes, ctx, row_number, "object_id")
        validate_langstring(object_label, ctx, row_number, "object_label")
        validate_optional_curie(replaces, prefixes, ctx, row_number, "replaces")
        validate_optional_curie(aligns, prefixes, ctx, row_number, "aligns")
        validate_optional_curie(implements, prefixes, ctx, row_number, "implements")

        if mapping:
            if mapping in mappings_seen:
                ctx.add(
                    f"Duplicate mapping CURIE already defined at row {mappings_seen[mapping]}.",
                    row_number=row_number,
                    column="mapping",
                )
            else:
                mappings_seen[mapping] = row_number
                if mapping_type in ALLOWED_TYPES:
                    mappings_by_type[mapping_type].add(mapping)

        if replaces:
            replaces_references.append((row_number, replaces))
            if replaces == mapping and mapping:
                ctx.add(
                    "A mapping cannot replace itself.",
                    row_number=row_number,
                    column="replaces",
                )

        if mapping_type in ALLOWED_TYPES and subject_id:
            subject_ids_by_type[mapping_type].add(subject_id)

        if aligns:
            if mapping_type != ALIGNS_ALLOWED_SOURCE_TYPE:
                ctx.add(
                    f"Only rows with type '{ALIGNS_ALLOWED_SOURCE_TYPE}' may have a value in this column.",
                    row_number=row_number,
                    column="aligns",
                )
            aligns_references.append((row_number, aligns))

        if implements:
            if mapping_type != IMPLEMENTS_ALLOWED_SOURCE_TYPE:
                ctx.add(
                    f"Only rows with type '{IMPLEMENTS_ALLOWED_SOURCE_TYPE}' may have a value in this column.",
                    row_number=row_number,
                    column="implements",
                )
            implements_references.append((row_number, implements, subject_id))

    for row_number, replaces in replaces_references:
        if replaces not in mappings_seen:
            ctx.add(
                "Value must reference a mapping CURIE that exists in the same input.csv file.",
                row_number=row_number,
                column="replaces",
            )

    allowed_aligns_targets = mappings_by_type[ALIGNS_ALLOWED_TARGET_TYPE]
    for row_number, aligns in aligns_references:
        if aligns not in allowed_aligns_targets:
            ctx.add(
                (
                    f"Value must reference a mapping CURIE that exists in a row with type "
                    f"'{ALIGNS_ALLOWED_TARGET_TYPE}'."
                ),
                row_number=row_number,
                column="aligns",
            )

    allowed_implements_targets = subject_ids_by_type[IMPLEMENTS_ALLOWED_TARGET_TYPE]
    for row_number, implements, subject_id in implements_references:
        if implements not in allowed_implements_targets:
            ctx.add(
                (
                    f"Value must reference a subject_id that exists in another row with type "
                    f"'{IMPLEMENTS_ALLOWED_TARGET_TYPE}'."
                ),
                row_number=row_number,
                column="implements",
            )
        elif implements == subject_id:
            ctx.add(
                (
                    "Value must reference a subject_id from another row, not the same subject_id "
                    "as the current row."
                ),
                row_number=row_number,
                column="implements",
            )


def render_summary(errors: Iterable[ValidationError]) -> str:
    return "\n".join(error.render() for error in errors)


def main() -> int:
    args = parse_args()
    ctx = ValidationContext()

    prefix_path = Path(args.prefix)
    input_path = Path(args.input)

    prefixes = validate_prefix_file(prefix_path, args.delimiter, ctx)
    validate_input_file(input_path, args.delimiter, prefixes, ctx)

    if ctx.ok:
        print("Validation passed: no errors found.")
        return 0

    print(f"Validation failed: {len(ctx.errors)} error(s) found.")
    print(render_summary(ctx.errors))
    return 1


if __name__ == "__main__":
    sys.exit(main())
