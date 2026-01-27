# Point clouds

Point clouds are generic points in 3D space.
Multiple point clouds (fragments) can be stored in one table.

## Parent schemas

None

## Schema metadata

These metadata keys are defined in addition to those defined by any parent schemas.

### Required schema metadata

These keys MUST exist in the schema's metadata.

#### `version`

- encoding: UTF-8 string

The version of the neurarrow specification used to write the data.

#### `context`

- encoding: UTF-8 string

The identifier for the context shared by all elements in this file, and possibly other files too; see [Contexts](../conventions.md#contexts).

### Optional schema metadata

These keys MAY exist in the schema's metadata.

#### `attr:*`

- encoding: various

Unstructured arbitrary attributes beneath the `attr:` prefix.
Nested attributes MAY be stored in a flat representation with `:` separators,
e.g. `attr:parent:child:key = value`.
Values are RECOMMENDED to be UTF-8 encoded strings.
However, storing a structure in a serialised form like JSON or MsgPack is also acceptable.

## Fields

These fields are defined in addition to those defined by any parent classes.

### Required fields

These fields MUST exist in the file.

- None

### Optional fields

These fields MAY exist in the file.

#### `attr`

- data type: map with variable-length string keys and variable-length byte values
- nullable: yes

Arbitrary attributes set on a per-row basis.
Keys SHOULD NOT use the `attr:` prefix.
Values are RECOMMENDED to be UTF-8 encoded strings.

#### `attr:*`

- data type: various
- nullable: various

Arbitrary fields beneath the `attr:` prefix.

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other fields,
and MAY be invalidated if the source fields are updated.

- None
