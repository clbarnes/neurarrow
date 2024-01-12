# Skeletonised cells

Cells are often described in skeletonised form, as a rooted tree graph.
The root SHOULD be the cell body.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: `{major}.{minor}` version of neurarrow spec
- `unit`: full name of a spatial unit according to UDUNITS-2, or empty for arbitrary units (e.g. voxels with unknown resolution)
  - angstrom, attometer, centimeter, decimeter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter

### Optional schema metadata

- `space`: an arbitrary value identifying the space from which these data were taken (e.g. animals, transforms). Two data sets from different spaces SHOULD NOT be compared directly.
- Individual fragments MAY have arbitrary metadata set with keys like `frag:{fragment_id}:{key}`, e.g. `frag:619:name`.
- Arbitrary metadata MAY be set under keys starting with `attr:`, e.g. `attr:acquisition_date`.

## Fields

### Required fields

These fields MUST exist in the file.

#### `sample_id`

- data type: `uint64`
- nullable: no

A unique ID for a single node in the tree.

#### `parent_id`

- data type: `uint64`
- nullable: yes
  - for exactly one sample per tree, which is the root; conventionally the cell body

The ID of the parent node for this sample.
MUST be defined elsewhere in the file.

#### `fragment_id`

- data type: `uint64`
- nullable: no

A unique ID for a single tree in the file.
This MAY represent a whole cell or only part of one.
This MUST NOT be used to represent a relationship between two disconnected trees.

#### `x`, `y`, `z`

- data type: `float64`
- nullable: no

The location of the sample in 3D, in the units given in the schema metadata.

### Optional fields

These fields MAY exist in the file.

#### `radius`

- data type: `float64`
- nullable: yes
  - where radius is not known

An approximation of the radius of the cell around this sample, in the units given in the schema metadata.

#### `labels`

- data type: `list[string]`
- nullable: no

Arbitrary text labels to apply to a sample.

#### `connectors`

- data type: `map[dictionary[string] -> list[uint64]]`
- nullable: no

Any connectors associated with the node.
The key of the map is the type of relationship;
the value is a list of related connector IDs.

Valid relationships are:

- `"presynaptic_to"` (the skeleton sample is presynaptic to a connector of type `"synapse"`)
- `"postsynaptic_to"` (the skeleton sample is postsynaptic to a connector of type `"synapse"`)
- `"gapjunction_with"` (the skeleton sample is associated with a connector of type `"gapjunction"`)

The type of the connector may restrict which relationships are valid.

### Derived fields

These columns MUST be calculable from other fields present in the file.
They are included primarily for IPC usage rather than storage,
to avoid having to recalculate the same values in different applications.

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
