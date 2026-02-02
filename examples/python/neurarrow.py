#!/usr/bin/env -S uv run --script
#
# Rough implementation of the neurarrow specification using PyArrow.
#
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyarrow",
#     "pyarrow-stubs",
#     "parver",
# ]
# ///
from __future__ import annotations
from abc import ABC, abstractmethod
import pyarrow as pa
from parver import Version

from typing import Any, Callable, Optional, Self, Sequence


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

Fields = list[pa.Field]


MetaValidator = Callable[[str, str], None]
"""Function taking custom_metadata key and value and raising ValidationError on failure."""


class ValidationError(Exception):
    pass


def check_unit(v: str, valid: set[str]):
    if v not in valid:
        raise ValidationError(f"Unit '{v}' not in valid set: {valid}")


def ensure_str(b: bytes | str) -> str:
    if isinstance(b, bytes):
        try:
            return b.decode("utf-8")
        except UnicodeDecodeError:
            raise ValidationError(f"Got non-UTF-8 bytes: {b}")
    elif isinstance(b, str):
        return b
    raise ValidationError(f"Expected bytes or str, got {type(b)}")


def check_dtype(v: str, fn: Callable[[str], Any]):
    fn(v)


def check_version(v: str, max_ver: Optional[Version] = None):
    ver = Version.parse(v)
    if max_ver is not None:
        assert ver < max_ver


class ArrowWrapper(ABC):
    def __init__(self, table: pa.Table, strict: Optional[bool] = False) -> None:
        """Wrap the given `pyarrow.Table` in this class.

        If `strict` is `None`, do not validate the fields and metadata keys.
        If `False`, validate existing fields and metadata keys, but allow extras.
        If `True`, additionally validate that there are no extra fields or metadata keys.
        """
        if strict is not None:
            self._validate_fields(table.schema, strict)
            self._validate_meta(table.schema, strict)
        self.table = table

    @classmethod
    def from_map(
        cls,
        data: dict[str, Sequence[Any] | pa.Array[Any]],
        metadata: dict[str, str],
        strict: Optional[bool] = False,
    ) -> Self:
        """Create an instance from a data dictionary and metadata dictionary."""
        mx = cls.max_schema()
        fields = []
        for k, v in data.items():
            field = mx.get(k)
            if field is None:
                field = pa.field(k, pa.infer_type(v, None), True)
            fields.append(field)
        schema = pa.schema(
            fields,
            metadata=metadata,  # type: ignore
        )
        table = pa.table(data, schema=schema)
        return cls(table, strict)

    @classmethod
    def max_schema(cls) -> dict[str, pa.Field]:
        """Get the maximal schema including all required, optional, and derived fields."""
        return {
            f.name: f
            for f in cls.required_fields()
            + cls.optional_fields()
            + cls.derived_fields()
        }

    @classmethod
    @abstractmethod
    def required_fields(cls) -> Fields:
        pass

    @classmethod
    @abstractmethod
    def optional_fields(cls) -> Fields:
        pass

    @classmethod
    @abstractmethod
    def derived_fields(cls) -> Fields:
        pass

    @classmethod
    @abstractmethod
    def required_metadata(cls) -> dict[str, MetaValidator | None]:
        pass

    @classmethod
    @abstractmethod
    def optional_metadata(cls) -> dict[str, MetaValidator | None]:
        pass

    @property
    def metadata(self):
        return self.table.schema.metadata

    def prefixed_metadata(self, prefix: str):
        pref = prefix.encode("utf-8")
        yield from (
            (k, v) for k, v in self.table.schema.metadata.items() if k.startswith(pref)
        )

    @classmethod
    def _validate_fields(cls, schema: pa.Schema, strict=False):
        """`strict` disallows extra fields."""
        schema_dict: dict[str, pa.Field] = dict()
        for fname in schema.names:
            idxs = schema.get_all_field_indices(fname)
            if len(idxs) > 1:
                raise ValidationError("Duplicate field names")
            schema_dict[fname] = schema.field(idxs[0])

        all_fields = set()

        for field in cls.required_fields():
            try:
                expected = schema_dict[field.name]
            except KeyError:
                raise ValidationError(f"Required field does not exist: '{field.name}'")

            all_fields.add(field.name)

            if not field.equals(expected):
                raise ValidationError(
                    f"Field mismatch: got {field} but expected {expected}"
                )

        for field in cls.optional_fields() + cls.derived_fields():
            try:
                expected = schema_dict[field.name]
            except KeyError:
                continue

            all_fields.add(field.name)

            if not field.equals(expected):
                raise ValidationError(
                    f"Field mismatch: got {field} but expected {expected}"
                )

        if strict:
            diff = set(n for n in schema_dict if not n.startswith("attr:")) - all_fields
            if diff:
                raise ValidationError(f"Got unexpected fields: {diff}")

    @classmethod
    def _validate_meta(cls, schema: pa.Schema, strict=False):
        """`strict` disallows extra metadata keys."""
        req_meta = cls.required_metadata()
        opt_meta = cls.optional_metadata()
        for k, v in schema.metadata.items():
            k = ensure_str(k)
            v = ensure_str(v)
            prefix = k.split(":", 1)[0]
            if prefix == "attr":
                continue

            # TODO: validation for prefixed metadata
            validator = req_meta.get(k)
            if validator is None:
                validator = opt_meta.get(k)
            if validator is not None:
                validator(k, v)

            if strict and k not in req_meta and k not in opt_meta:
                raise ValidationError(f"Got unexpected metadata key '{k}'")


class Base(ArrowWrapper, ABC):
    @classmethod
    def required_fields(cls) -> Fields:
        return []

    @classmethod
    def optional_fields(cls) -> Fields:
        return [pa.field("attr", pa.map_(pa.utf8(), pa.utf8()), True)]

    @classmethod
    def derived_fields(cls) -> Fields:
        return []

    @classmethod
    def required_metadata(cls) -> dict[str, MetaValidator | None]:
        return {
            "version": lambda _, b: check_version(b),
            "context": None,
        }

    @classmethod
    def optional_metadata(cls) -> dict[str, MetaValidator | None]:
        return {}


class Spatial(Base, ABC):
    @classmethod
    def required_metadata(cls) -> dict[str, MetaValidator | None]:
        return super().required_metadata() | {
            "unit": lambda _, b: check_unit(b, SPACE_UNITS),
        }

    @classmethod
    def optional_metadata(cls) -> dict[str, MetaValidator | None]:
        return super().optional_metadata() | {
            "space": None,
        }


class PointClouds(Spatial):
    @classmethod
    def required_fields(cls) -> Fields:
        return super().required_fields() + [
            pa.field("sample_id", ID, False),
            pa.field("fragment_id", ID, False),
            pa.field("x", REAL, False),
            pa.field("y", REAL, False),
            pa.field("z", REAL, False),
        ]

    # TODO: fragment attributes?


class Skeletons(PointClouds):
    @classmethod
    def required_fields(cls) -> Fields:
        return super().required_fields() + [
            pa.field("parent_id", ID, True),
        ]

    @classmethod
    def optional_fields(cls) -> Fields:
        return super().optional_fields() + [
            pa.field("radius", REAL, True),
        ]

    @classmethod
    def derived_fields(cls) -> Fields:
        return super().derived_fields() + [
            pa.field("child_ids", pa.list_(ID), True),
            pa.field("n_children", pa.uint32(), True),
            pa.field("strahler", pa.uint32(), True),
        ]


class Dotprops(PointClouds):
    @classmethod
    def required_fields(cls) -> Fields:
        return super().required_fields() + [
            pa.field("tangent_x", REAL, False),
            pa.field("tangent_y", REAL, False),
            pa.field("tangent_z", REAL, False),
        ]

    @classmethod
    def optional_fields(cls) -> Fields:
        return super().optional_fields() + [
            pa.field("colinearity", REAL, False),
        ]

    @classmethod
    def required_metadata(cls) -> dict[str, MetaValidator | None]:
        return super().required_metadata() | {
            "neighborhood_size": lambda _, b: check_dtype(b, int),
        }


class Connections(Base):
    @classmethod
    def required_fields(cls) -> Fields:
        return super().required_fields() + [
            pa.field("connection_id", ID, False),
            pa.field("src_sample_id", ID, False),
            pa.field("tgt_sample_id", ID, False),
            pa.field("type", pa.dictionary(pa.uint16(), pa.utf8()), False),
        ]

    @classmethod
    def derived_fields(cls) -> Fields:
        return super().derived_fields() + [
            pa.field("src_fragment_id", ID, False),
            pa.field("tgt_fragment_id", ID, False),
        ]


def example_skeleton() -> Skeletons:
    return Skeletons.from_map(
        {
            "sample_id": [0, 1, 2, 3],
            "parent_id": [None, 0, 1, 1],
            "fragment_id": [0, 0, 0, 0],
            "x": [0, 1, 2, 2],
            "y": [0, 0, 0, 1],
            "z": [0, 0, 0, 0],
            "radius": [1.0, None, None, 0.5],
        },
        metadata={"version": "0.1", "unit": "nanometer"},
        strict=True,
    )


if __name__ == "__main__":
    skel = example_skeleton()
    print(skel.table)
