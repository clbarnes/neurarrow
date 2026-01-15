# Dotprops

Dotprops are point clouds used in [NBLAST](http://flybrain.mrc-lmb.cam.ac.uk/si/nblast/www/) and related calculations.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `unit`: : as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `context`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `neighborhood_size`: how many nearest neighbors were used to calculate the tangent vector (referred to as `k` in literature),
  as a base-10 representation of an unsigned integer.

### Optional schema metadata

These metadata MAY exist at the schema level.

- `space`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- Arbitrary attributes and extension metadata MAY be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections

## Fields

### Required fields

These fields MUST exist in the file.

#### `sample_id`

- data type: uint64
- nullable: no

An ID for this point, which MUST be unique within the table.

#### `fragment_id`

- data type: uint64
- nullable: no

The ID of the point cloud to which the sample belongs.

#### `x`, `y`, `z`

- data type: float64
- nullable: no

The location of the point in 3D, in the units given in the schema metadata.

### `tangent_x`, `tangent_y`, `tangent_z`

- data type: float64
- nullable: no

The normalised tangent vector of the neighborhood around the point in 3D, in the units given in the schema metadata.

### Optional fields

These fields MAY exist in the file.

Arbitrary attribute and extension fields MAY be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections.

### `colinearity`

- data type: float64
- nullable: no

A value between 0 and 1 representing how colinear the points in the neighborhood are (referred to as `α` / `alpha` in literature).
