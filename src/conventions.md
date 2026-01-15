# Conventions

Unless there is a very good reason not to, fields and metadata keys SHOULD use `snake_case` names.

Names MUST use UTF-8 encodings.

## Data types

### Primitives

We use arrow's nomenclature for primitives.

Real values SHOULD be stored as a float64 field, or as a base-10 decimal ASCII string (e.g. `3.14`) in an attribute.
Integer IDs SHOULD be stored as uint64 field, or as a base-10 ASCII string (e.g. `123`) in an attribute.

## Additional data

Neuroarrow is designed with the flexibility to accommodate both unstructured attributes
and data structured according to some well-described extension.

### Attributes

Unstructured attributes are generally prefixed by `attr:`.
Nested attributes MAY be encoded with `:`-separated names,
(e.g. `attr:parent_container:child_field`),
although storing a structure in a serialised form like JSON or MsgPack is also acceptable.

### Extensions

Extensions SHOULD have unique names,
and SHOULD ensure this by incorporating the web domain of the controlling entity in reverse DNS format.
For example, an extension for spatial transforms defined by the owner of `https://example.com`
MAY be called `com.example.transforms`.
All data (metadata or fields) structured according to this extension would have names prefixed by `com.example.transforms:`.

Nested extension metadata SHOULD be encoded with `:`-separated names
(e.g. `com.example.transforms:method:arguments`),
although storing a structure in a serialised form like JSON or MsgPack is also acceptable.

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
The `context` is an arbitrary UTF-8 string (e.g. IRI or hexadecimal UUID) identifying a shared context in which all IDs must be unique;
it is the `context, ID` pair which is _globally_ unique.

### `space`

An arbitrary UTF-8 string (e.g. IRI or hexadecimal UUID) identifying the space from which spatial data are taken (e.g. animals, transforms).
Data sets from different spaces SHOULD NOT be compared directly,
but datasets from different contexts which exist in the same space MAY be compared.

### Arbitrary attributes

Arbitrary attributes MAY be stored under keys prefixed by `attr:`,
as described in the [Attributes section](#attributes).

### Extension metadata

Metadata controlled by extensions MUST be prefixed by their unique name,
as described in the [Extensions section](#extensions).

## Schemas

Schemas have metadata, containing:

- _required_ keys which MUST exist
- _optional_ keys which MAY exist

Metadata keys MUST be UTF-8 encoded strings.
Metadata values SHOULD be UTF-8 encoded strings.

Schema metadata MAY contain arbitrary attributes;
their keys MUST be prefixed by `attr:` as described in the [Attributes section](#attributes).

Schema metadata MAY contain extension metadata;
their keys MUST be prefixed by the unique name of the extension as described in the [Extensions section](#extensions).

### Fields

Schemas have fields (a.k.a. columns) described in this specification:

- _required_ fields which MUST exist
- _optional_ fields which MAY exist
- _derived_ fields which MAY exist, but MUST be calculable from other fields in the same context
  - derived fields MAY be invalidated if the fields they depend on are updated
- _extension_ fields whose name MUST be prefixed by the extension's unique name as described in [Extensions](#extensions)
  - these fields MAY be specified by that extension as _required_, _optional_, or _derived_
- _attribute_ fields which MAY exist and whose name MUST be prefixed with `attr:` as described in [Extensions](#extensions)
  - additionally, attributes MAY be defined for individual records (rows) using a field called `attr`,
    which MUST be nullable
    and MUST be of type `map`
    whose keys MUST be variable-length UTF-8 strings (which do not need the `attrs:` prefix) and
    whose values MUST be variable-length byte strings,
    which SHOULD contain encoded UTF-8 strings

Fields have metadata, containing:

- _required_ keys which MUST exist
- _optional_ keys which MAY exist

Metadata keys MUST be UTF-8 encoded strings.
Metadata values SHOULD be UTF-8 encoded strings.

Field metadata MAY contain arbitrary attributes;
their keys MUST be prefixed by `attr:` as described in the [Attributes section](#attributes).

Field metadata MAY contain extension metadata;
their keys MUST be prefixed by the unique name of the extension as described in the [Extensions section](#extensions).

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

The extension SHOULD be prefixed with the name of the file schema, like `brain.skeletons.parquet` or `cns.connectors.feather`.
