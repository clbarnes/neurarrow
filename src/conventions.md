# Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Versioning

This specification utilises [semantic versioning](https://semver.org/).

Before version `1.0.0`, all minor changes may be break compatibility.
Otherwise,

- Patch versions are used for non-substantive or bug-fix changes to the text of the specification.
- Minor versions are used for additions which do not break backward compatibility, i.e.
  - A v1.2 parser SHOULD be able to read all v1.1 files
  - A v1.1 parser MAY be able to partially read v1.2 files
- Major versions are used for changes which break compatibility, i.e.
  - A v1.x parser MAY not be able to read a v2.y file
  - A v2.x parser MAY not be able to read a v1.y file

[Extensions](./extensions.md) MAY use other versioning schemes.

All version strings MUST conform to the [PEP-440 version specifier specification](https://packaging.python.org/en/latest/specifications/version-specifiers/).

## Naming

Unless there is a very good reason not to, fields and metadata keys SHOULD use `snake_case` names.

## Data types

### Primitives

This specification uses arrow's nomenclature for primitives.
Note that strings MUST be in UTF-8 encoding.

Real values SHOULD be stored as a float64 field, or as a decimal string (e.g. `3.14`) in a metadata value.
Integer IDs SHOULD be stored as uint64 field, or as a decimal string (e.g. `123`) in a custom metadata value.

## Attributes

Here, attributes are defined as arbitrary unstructured data and metadata.

Consider defining an [extension](./extensions.md) to make your additional data discoverable and re-usable.

### Attribute arrow metadata

Schema metadata and field metadata MAY contain unstructured arbitrary attributes,
whose keys MUST be prefixed by `attr:`.
Nested attributes MAY be encoded with `:`-separated elements
(e.g. `attr:parent_container:child_field`),
although storing a structure in a serialised form like JSON is also acceptable.

### Attribute fields

Arbitrary attribute fields MAY be added to any schema.
The name of the field MUST be prefixed by `attr:`.

Additionally, all schemas MAY have an `attr` field,
which MUST be a nullable map from variable-length string keys to variable-length bytes values.
These keys SHOULD NOT have an `attr:` prefix.

## Neurarrow-specific metadata

### Contexts

A single logical dataset may span multiple on-disk tables,
either due to partitioning of a single logical table,
or where tables of multiple types refer to each other.
Different datasets may repeat IDs (e.g. for low integers).
The context identifier is an arbitrary UTF-8 string identifying a shared context in which all IDs MUST be unique;
strictly it is the `(context, ID)` pair which is _globally_ unique.

It is RECOMMENDED that the identifier be an IRI or (hex-encoded) UUID to ensure uniqueness.

### Spaces

Samples taken from two spatial experiments MAY have the same coordinates,
but these may not actually be in the same physical location.
Spatial datasets are routinely transformed from one "space" to another for comparison.
It is important to track which space a dataset belongs to,
to know whether it can be compared to another.

The space identifier is an arbitrary UTF-8 string identifying the space from which spatial data are taken (e.g. animals, transforms).
Data sets from different spaces SHOULD NOT be spatially overlaid without transformation.

It is RECOMMENDED that the identifier be an IRI or UUID to ensure uniqueness.

Data from two [contexts](conventions.md#Contexts) MAY share the same space
(e.g. after transforming one experiment's data to another's space).
Data from one context MUST share a space.

## Schemas

Schemas have metadata, containing:

- _required_ keys which MUST exist
- _optional_ keys which MAY exist
- _attribute_ keys
- _extension_ keys

Metadata keys and values MUST be strings, but MAY encode non-string data
(e.g. numbers in decimal representation).

Schema metadata MAY contain arbitrary attributes;
their keys MUST be prefixed by `attr:` as described in the [Attributes section](#attributes).

Schema metadata MAY contain extension metadata;
their keys MUST be prefixed by the unique name of the extension as described in [Extensions](./extensions.md#extension-metadata).

### Schema fields

Schemas have fields (a.k.a. columns) described in this specification:

- _required_ fields which MUST exist
- _optional_ fields which MAY exist
- _derived_ fields which MAY exist, but MUST be calculable from other fields in the same context
  - derived fields MAY be invalidated if the fields they depend on are updated
- _extension_ fields whose name MUST be prefixed by the extension's unique name as described in [Extensions](./extensions.md#extension-fields)
- _attribute_ fields which MAY exist and whose name MUST be prefixed with `attr:` as described in [Attributes](#attribute-fields)
  - the `attr` field described in [Attributes](#attribute-fields) is also an _attribute_ field

In Arrow, fields can have metadata.
This feature is currently unused by neurarrow, but MAY be in future.
Writers and extensions SHOULD NOT add or rely on field metadata.

## Inheritance

Certain ("child") schemas _inherit_ from another ("parent") schema.
This means that the child schema:

- MUST have all of the parents' _required_ fields and metadata
- MAY have all of the parents' _optional_ and _derived_ fields and metadata

Child schemas MAY inherit from more than one parent schema.

The [Base](./schemas/base.md) and [Spatial](./schemas/spatial.md) schemas are provided as _abstract_ schemas.
They SHOULD NOT be written as files themselves,
but define a parent schema other (_concrete_) schemas MAY inherit from.

## Storage

Individual tables SHOULD be stored as:

- [Arrow IPC File format](https://arrow.apache.org/docs/format/Columnar.html#format-ipc)
  - Also known as [Feather format](https://arrow.apache.org/docs/python/feather.html)
  - Best for inter-process communication or memory mapped I/O applications
  - Extension `.arrow`
- [Parquet](https://parquet.apache.org/)
  - Best for longer-term, potentially more space-efficient storage
  - Extension `.parquet`
- [Hive partitioned](https://duckdb.org/docs/stable/data/partitioning/hive_partitioning) parquet
  - Parquet files split into chunks in directories based on a particular column's value
  - Best for very large datasets, particularly in high-latency environments like cloud storage
  - Paths like `.../fragment_id=123/*.skeleton.parquet`
  - Note that modifying schema and field metadata on hive-partitioned data can mean updating a lot of files

The extension SHOULD be prefixed with the name of the file schema, like `brain.skeletons.parquet` or `cns.connections.feather`.

> **WARNING**
>
> Parquet does not directly support `uint64` data (used for IDs in neurarrow).
> Large `uint64` values are usually mapped to the negative range of parquet's `int64` data type,
> and then parsed back to `uint64` when read back into arrow.
