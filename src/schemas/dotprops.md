# Dotprops

Dotprops are point clouds used in [NBLAST](http://flybrain.mrc-lmb.cam.ac.uk/si/nblast/www/) and related calculations.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: `{major}.{minor}` version of the neurarrow spec
- `unit`: full name of a spatial unit according to UDUNITS-2, or empty for arbitrary units (e.g. voxels with unknown resolution)
  - angstrom, attometer, centimeter, decimeter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter
- `neighborhood_size`: how many nearest neighbors were used to calculate the tangent vector (often referred to as `k`), as a base-10 representation of an unsigned integer.

### Optional schema metadata

These metadata MAY exist at the schema level.

- `space`: an arbitrary value identifying the space from which these data were taken (e.g. animals, transforms). Two data sets from different spaces SHOULD NOT be compared directly.
- Arbitrary metadata MAY be set under keys starting with `attr:`, e.g. `attr:acquisition_date`.

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

### `colinearity`

- data type: float64
- nullable: no

A value between 0 and 1 representing how colinear the points in the neighborhood are (often referred to as `α` / `alpha`).
