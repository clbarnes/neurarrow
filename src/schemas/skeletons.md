# Skeletonised cells

Cells are often described in skeletonised form, as a rooted tree graph.
The root SHOULD be the cell body.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `unit`: : as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `context`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)

### Optional schema metadata

- `space`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- Individual fragments MAY have arbitrary metadata set with keys like `frag:{fragment_id}:{key}`, e.g. `frag:619:name`.
- Arbitrary attributes and extension metadata can be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections

## Fields

### Required fields

These fields MUST exist in the file.

#### `sample_id`

- data type: `uint64`
- nullable: no

An ID for a single node in the tree, which MUST be unique within the `context`.

#### `parent_id`

- data type: `uint64`
- nullable: yes
  - exactly one sample per fragment MUST be null, which MUST the root; conventionally the cell body or nearest node to it

The ID of the parent node for this sample.
MUST be defined elsewhere in the file.

#### `fragment_id`

- data type: `uint64`
- nullable: no

An ID which MUST be unique to a single tree in the dataset.
All samples sharing a `fragment_id` MUST form a connected (undirected) tree graph.
This MAY represent a whole cell or only part of one.
This MUST NOT be used to represent a relationship between two morphologically disconnected cells.

#### `x`, `y`, `z`

- data type: `float64`
- nullable: no

The location of the sample in 3D, in the units given in the schema metadata.

### Optional fields

These fields MAY exist in the file.

Arbitrary attribute and extension fields MAY be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections.

#### `radius`

- data type: `float64`
- nullable: yes
  - where radius is not known

An approximation of the radius of the cell around this sample, in the units given in the schema metadata.

### Derived fields

#### `child_ids`

- data type: `list[uint64]`
- nullable: no

The IDs of samples which have this sample as a parent.

#### `n_children`

- data type: `uint32`
- nullable: no

How many child nodes a particular sample has.

#### `strahler`

- data type: `uint32`
- nullable: no

The [Strahler number](https://en.wikipedia.org/wiki/Strahler_number) of this sample.
