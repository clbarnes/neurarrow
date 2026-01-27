# Dotprops

Dotprops are point clouds used in [NBLAST](http://flybrain.mrc-lmb.cam.ac.uk/si/nblast/www/) and related calculations.

## Parent schemas

- [Point clouds](./pointclouds.md)

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

#### `neighborhood_size`

- encoding: ASCII base-10 unsigned integer

How many nearest neighbors were used to calculate the tangent vector (referred to as `k` in literature).

### Optional schema metadata

These metadata MAY exist at the schema level.

- None

## Fields

These fields are defined in addition to those defined by any parent classes.

### Required fields

These fields MUST exist in the file.

### `tangent_x`, `tangent_y`, `tangent_z`

- data type: float64
- nullable: no

The normalised tangent vector of the neighborhood around the point in 3D, in the units given in the schema metadata.

### Optional fields

These fields MAY exist in the file.

### `colinearity`

- data type: float64
- nullable: no

A value between 0 and 1 representing how colinear the points in the neighborhood are (referred to as `α` / `alpha` in literature).
