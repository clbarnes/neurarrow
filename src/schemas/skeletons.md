# Skeletonised cells

Cells are often described in skeletonised form, as a rooted tree graph.
The root SHOULD be the cell body.

## Parent schemas

This schema inherits all fields and metadata from the following schemas:

- [Point clouds](./pointclouds.md)

## Schema metadata

These metadata keys are defined in addition to those defined by any parent schemas.

### Required schema metadata

These metadata MUST exist in the schema's metadata.

- None

### Optional schema metadata

These metadata MAY exist in the schema's metadata.

- None

## Fields

These fields are defined in addition to those defined by any parent classes.

### Required fields

These fields MUST exist in the file.

#### `parent_id`

- data type: `uint64`
- nullable: yes
  - exactly one sample per fragment MUST be null, which MUST the root; conventionally the cell body or nearest node to it

The ID of the parent node for this sample.
MUST be defined elsewhere in the file.

### Optional fields

These fields MAY exist in the file.

#### `radius`

- data type: `float64`
- nullable: yes
  - where radius is not known

An approximation of the radius of the cell around this sample, in the units given in the schema metadata.

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other fields,
and MAY be invalidated if the source fields are updated.

#### `child_ids`

- data type: `list[uint64]`
- nullable: yes

The IDs of samples which have this sample as a parent.

#### `n_children`

- data type: `uint32`
- nullable: yes

How many child nodes a particular sample has.

#### `strahler`

- data type: `uint32`
- nullable: yes

The [Strahler number](https://en.wikipedia.org/wiki/Strahler_number) of this sample.
