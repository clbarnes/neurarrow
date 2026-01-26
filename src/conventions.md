# Conventions

Unless there is a very good reason not to, fields and metadata keys SHOULD use `snake_case` names.

Names MUST use UTF-8 encodings.

## Data types

### Primitives

We use arrow's nomenclature for primitives.

Real values SHOULD be stored as a float64 field, or as a base-10 decimal ASCII string (e.g. `3.14`) in a metadata value.
Integer IDs SHOULD be stored as uint64 field, or as a base-10 ASCII string (e.g. `123`) in a metadata value.

## Attributes

Here, attributes are defined as arbitrary unstructured data and metadata.

Consider defining an [extension](./extensions.md) to make your additional data discoverable and re-usable.

### Attribute arrow metadata

Schema metadata and field metadata MAY contain unstructured arbitrary attributes,
whose keys MUST be prefixed by `attr:`.
Nested attributes MAY be encoded with `:`-separated elements
(e.g. `attr:parent_container:child_field`),
although storing a structure in a serialised form like JSON or MsgPack is also acceptable.

### Attribute fields

Arbitrary attribute fields MAY be added to any schema.
The name of the field MUST be prefixed by `attr:`.

Additionally, all schemas MAY have an `attr` field,
which MUST be a nullable map from variable-length string keys to variable-length bytes values.
The values are RECOMMENDED to be UTF-8 encoded strings.
These keys SHOULD NOT have an `attr:` prefix.

## Neurarrow-specific metadata

The below are common metadata keys found throughout the specification.

### `version`

The version of the neurarrow specification used to write the data, as a UTF-8 encoded string.
See the [Versioning section](./introduction.md#versioning).

### `unit`

A UTF-8 encoded string which is the full name of a unit according to UDUNITS-2, or empty for arbitrary units (e.g. voxels with unknown resolution).

- spatial
  - angstrom, attometer, centimeter, decimeter, dekameter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter

### `context`

A single logical dataset may span multiple on-disk tables,
either due to partitioning of a single logical table,
or where tables of multiple types refer to each other.
Different datasets may repeat IDs (e.g. for low integers).
The `context` is an arbitrary UTF-8 string identifying a shared context in which all IDs MUST be unique;
strictly it is the `(context, ID)` pair which is _globally_ unique.

It is RECOMMENDED that the `context` be an IRI or UUID to ensure uniqueness.

### `space`

An arbitrary UTF-8 string identifying the space from which spatial data are taken (e.g. animals, transforms).
Data sets from different spaces SHOULD NOT be spatially overlaid without transformation,
but datasets from different contexts which exist in the same space MAY be compared directly.

It is RECOMMENDED that the `space` be an IRI or UUID to ensure uniqueness.

## Schemas

Schemas have metadata, containing:

- _required_ keys which MUST exist
- _optional_ keys which MAY exist
- _attribute_ keys
- _extension_ keys

Metadata keys MUST be UTF-8 encoded strings.
Metadata values SHOULD be UTF-8 encoded strings.

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

Fields have metadata, containing:

- _required_ keys which MUST exist
- _optional_ keys which MAY exist

Metadata keys MUST be UTF-8 encoded strings.
Metadata values SHOULD be UTF-8 encoded strings.

Field metadata MAY contain arbitrary attributes as described in the [Attributes section](#attributes).

Field metadata MAY contain extension metadata as described in the [Extensions section](./extensions.md#extension-metadata).

## Storage

Individual tables SHOULD be stored as:

- [Feather](https://github.com/wesm/feather) v2
  - Also known as Arrow IPC
  - Best for inter-process communication or memory mapped I/O applications
  - Extension `.feather`
- [Parquet](https://parquet.apache.org/)
  - Best for longer-term, more space-efficient storage
  - Extension `.parquet`
- [Hive partitioned](https://duckdb.org/docs/stable/data/partitioning/hive_partitioning) parquet
  - Parquet files split into chunks in directories based on a particular column's value
  - Best for very large datasets, particularly in high-latency environments like cloud storage
  - Paths like `.../fragment_id=123/*.skeleton.parquet`
  - Note that modifying schema and field metadata on hive-partitioned data can mean updating a lot of files

The extension SHOULD be prefixed with the name of the file schema, like `brain.skeletons.parquet` or `cns.connections.feather`.
