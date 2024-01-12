# Conventions

Unless there is a very good reason not to, fields and metadata keys MUST use `snake_case` names.

Names MUST use UTF-8 encodings.

## Data types

### Primitives

We use arrow's nomenclature for primitives.

Real values SHOULD be stored as float64.
Integer IDs SHOULD be stored as uint64.

## Neurarrow-specific metadata

### unit

A UTF-8 encoded string which is the full name of a unit according to UDUNITS-2, or empty for arbitrary units (e.g. voxels with unknown resolution).

- spatial
  - angstrom, attometer, centimeter, decimeter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter

### space

An arbitrary byte string (e.g. name or UUID) identifying the space from which spatial data are taken (e.g. animals, transforms).
Data sets from different spaces SHOULD NOT be compared directly.

### attr

Arbitrary metadata MAY be stored on schemas and fields under keys prefixed by `attr:`.
Unstructured arbitrary metadata MAY be stored in serialized form,
in which case the serialization used SHOULD be given like `attr:{MIME type}`, e.g. `{"attr:application/json": {\"a\": 1, \"b\": [2, 3]}}`

## Schemas

Schemas have metadata:

- required keys which MUST exist
- optional keys which MAY exist

Metadata keys MUST be UTF-8 encoded strings.
Metadata values SHOULD be UTF-8 encoded strings.

Nested metadata MAY be encoded with `:`-separated names.
For example, a JSON-like struct `{"a": {"b": "1", "c": "2"}}` MAY be encoded as `{"a:b": "1", "a:c": "2"}`.

Arbitrary schema metadata MAY be stored under keys with the `attr:` prefix.
Schema metadata which is not part of the specification SHOULD NOT be stored outside of this namespace.

Unstructured arbitrary schema metadata MAY be stored in a serialized form, e.g. `{"attr:json": "{\"a\": 1, \"b\": [2, 3, 4]}"}`.

Schemas have fields:

- required fields which MUST exist
- optional fields which MAY exist
- derived fields with MAY exist, but MUST be calculable from other fields in the same schema
  - if the derived field depends on any non-required fields to be calculated, it SHOULD list their names as a comma-separated, lexicographically-sorted list under the field metadata key `depends`, e.g. `{"depends": "field1,field2"}`.

Arbitrary field metadata may be stored under keys with the `attr:` prefix.
Field metadata which is not part of the specification SHOULD NOT be stored outside of this namespace.

## Storage

Individual tables should be stored as:

- [Feather](https://github.com/wesm/feather)
  - Best for inter-process communication or memory mapped I/O applications
  - Extension `.feather`
- [Parquet](https://parquet.apache.org/)
  - Best for longer-term, more space-efficient storage
  - Extension `.parquet`

It is RECOMMENDED that if multiple tables need to be stored together, an uncompressed [tar](https://en.wikipedia.org/wiki/Tar_(computing)) archive should be used.
Both formats above support compression internally which is better suited for the task and still allows efficient access, where a compressed archive (`.zip`, `.tar.gz`, `.7z`) does not.

The extension SHOULD be prefixed with the name of the file schema, like `brain.skeletons.parquet` or `cns.connectors.feather`.
