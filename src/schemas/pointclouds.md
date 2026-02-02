# Point clouds

Point clouds are generic points in 3D space.
Multiple point clouds (fragments) can be stored in one table.

## Parent schemas

This schema inherits all fields and metadata from the following schemas:

- [Spatial](./spatial.md)

## Schema metadata

These metadata keys are defined in addition to those defined by any parent schemas.

### Required schema metadata

These metadata MUST exist in the schema's metadata.

- None

### Optional schema metadata

These metadata MAY exist in the schema's metadata.

#### `frag:*:*`

- encoding: various

Individual fragments MAY have arbitrary metadata set with keys like `frag:{fragment_id}:{key}`, e.g. `frag:619:name`.

## Fields

These fields are defined in addition to those defined by any parent classes.

### Required fields

These fields MUST exist in the file.

#### `sample_id`

- data type: uint64
- nullable: no

An ID for this point, which MUST be unique within the context.

#### `fragment_id`

- data type: uint64
- nullable: no

The ID of the point cloud to which the sample belongs.

#### `x`, `y`, `z`

- data type: float64
- nullable: no

The location of the point in 3D, in the units given in the schema metadata.

### Optional fields

These fields MAY exist in the file.

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other fields,
and MAY be invalidated if the source fields are updated.
