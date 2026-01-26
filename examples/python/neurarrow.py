# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyarrow",
# ]
# ///
from __future__ import annotations
import pyarrow as pa

from typing import Any, Callable, Optional


ID = pa.uint64()
REAL = pa.float64()

SPACE_UNITS: set[str] = {
    "angstrom",
    "attometer",
    "centimeter",
    "decimeter",
    "dekameter",
    "exameter",
    "femtometer",
    "foot",
    "gigameter",
    "hectometer",
    "inch",
    "kilometer",
    "megameter",
    "meter",
    "micrometer",
    "mile",
    "millimeter",
    "nanometer",
    "parsec",
    "petameter",
    "picometer",
    "terameter",
    "yard",
    "yoctometer",
    "yottameter",
    "zeptometer",
    "zettameter",
}

Fields = list[pa.field]

MetaValue = bytes
MetaValidator = Callable[[bytes, MetaValue], None]


class ValidationError(Exception):
    pass


def check_unit(b: bytes, valid: set[str]):
    decoded = b.decode()
    if decoded not in valid:
        raise ValidationError(f"Unit '{decoded}' not in valid set: {valid}")


def check_dtype(b: bytes, fn: Callable[[bytes], Any]):
    fn(b)


def check_version(b: MetaValue, max_ver: Optional[tuple[int, int]] = None):
    maj_b, min_b = b.split(b".")
    major = int(maj_b)
    minor = int(min_b)
    if max_ver is not None:
        assert (major, minor) < max_ver


class ArrowWrapper:
    _req_fields: Fields
    _opt_fields: Fields
    _der_fields: Fields

    _req_meta: dict[bytes, Optional[MetaValidator]]
    _opt_meta: dict[bytes, Optional[MetaValidator]]

    def __init__(self, table: pa.Table, strict: Optional[bool] = False) -> None:
        if strict is not None:
            self._validate_fields(table.schema, strict)
            self._validate_meta(table.schema, strict)
        self.table: pa.Table = table

    @property
    def metadata(self):
        return self.table.schema.metadata

    def prefixed_metadata(self, prefix: bytes | str):
        if isinstance(prefix, str):
            prefix = prefix.encode("utf-8")

        yield from (
            (k, v)
            for k, v in self.table.schema.metadata.items()
            if k.startswith(prefix)
        )

    @classmethod
    def _validate_fields(cls, schema: pa.Schema, strict=False):
        schema_dict = dict()
        for fname in schema.names:
            idxs = schema.get_all_field_indices(fname)
            if len(idxs) > 1:
                raise ValidationError("Duplicate field names")
            schema_dict[fname] = schema.field(idxs[0])

        all_fields = set()

        for field in cls._req_fields:
            try:
                expected = schema_dict[field.name]
            except KeyError:
                raise ValidationError(f"Required field does not exist: '{field.name}'")

            all_fields.add(field)

            if not field.equals(expected):
                raise ValidationError(f"Field mismatch: got {field} but expected {expected}")

        for field in cls._opt_fields + cls._der_fields:
            all_fields.add(field)
            try:
                expected = schema_dict[field.name]
            except KeyError:
                continue

            all_fields.add(field)

            if not field.equals(expected):
                raise ValidationError(f"Field mismatch: got {field} but expected {expected}")

        if strict:
            diff = set(schema_dict) - all_fields

            raise ValidationError(f"Got unexpected fields: {diff}")

    @classmethod
    def _validate_meta(cls, schema: pa.Schema, strict=False):
        req_present = set()

        for k, v in schema.metadata.items():
            prefix, *_ = k.split(b":", 1)

            try:
                vali = cls._req_meta[prefix]
                req_present.add(vali)
            except KeyError:
                pass

            try:
                vali = cls._opt_meta[prefix]
            except KeyError:
                if strict:
                    raise ValidationError(f"Got unexpected metadata prefix '{prefix}'")
                vali = None

            if vali is not None:
                vali(k, v)


class Skeletons(ArrowWrapper):
    _req_fields = [
        pa.field("sample_id", ID, False),
        pa.field("parent_id", ID, True),
        pa.field("fragment_id", ID, False),
        pa.field("x", REAL, False),
        pa.field("y", REAL, False),
        pa.field("z", REAL, False),
    ]
    _opt_fields = [
        pa.field("radius", REAL, True),
    ]
    _der_fields = [
        pa.field("child_ids", pa.list_(ID), False),
        pa.field("n_children", pa.uint32(), False),
        pa.field("strahler", pa.uint32(), False),
    ]

    _req_meta = {
        b"version": lambda _, b: check_version(b),
        b"context": None,
        b"unit": lambda _, b: check_unit(b, SPACE_UNITS),
    }
    _opt_meta = {
        b"space": None,
        b"attr": None,
    }


class Dotprops(ArrowWrapper):
    _req_fields = [
        pa.field("sample_id", ID, False),
        pa.field("fragment_id", ID, False),
        pa.field("x", REAL, False),
        pa.field("y", REAL, False),
        pa.field("z", REAL, False),
        pa.field("tangent_x", REAL, False),
        pa.field("tangent_y", REAL, False),
        pa.field("tangent_z", REAL, False),
    ]
    _opt_fields = [
        pa.field("colinearity", REAL, False),
    ]
    _der_fields = []

    _req_meta = {
        b"version": lambda _, b: check_version(b),
        b"context": None,
        b"unit": lambda _, b: check_unit(b, SPACE_UNITS),
        b"neighborhood_size": lambda _, b: check_dtype(b, int),
    }
    _opt_meta = {
        b"space": None,
        b"attr": None,
    }


class Connections(ArrowWrapper):
    _req_fields = [
        pa.field("connection_id", ID, False),
        pa.field("src_sample_id", ID, False),
        pa.field("tgt_sample_id", ID, False),
        pa.field("type", pa.dictionary(pa.uint16(), pa.utf8()), False),
    ]
    _opt_fields = []
    _der_fields = []

    _req_meta = {
        b"version": lambda _, b: check_version(b),
        b"context": None,
    }
    _opt_meta = {
        b"attr": None,
    }


def example_skeleton() -> Skeletons:
    return Skeletons(pa.table([
            # sample_id
            [0, 1, 2, 3],
            # parent_id
            [None, 0, 1, 1],
            # fragment_id
            [0, 0, 0, 0],
            # x
            [0, 1, 2, 2],
            # y
            [0, 0, 0, 1],
            # z
            [0, 0, 0, 0],
        ],
        schema=pa.schema(
            Skeletons._req_fields,
            metadata={"version": "0.1", "unit": "nanometer"},
        ),
    ))
