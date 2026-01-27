# Point clouds

Point clouds are generic points in 3D space.
Multiple point clouds (fragments) can be stored in one table.

## Parent schemas

This schema inherits all fields and metadata from the following schemas:

- [Base](./base.md)

## Schema metadata

These metadata keys are defined in addition to those defined by any parent schemas.

### Required schema metadata

These metadata MUST exist in the schema's metadata.

#### `unit`

- encoding: UTF-8 string

Empty for arbitrary units (e.g. voxels with unknown resolution),
or the full name of a spatial unit according to UDUNITS-2 as below:

> angstrom, attometer, centimeter, decimeter, dekameter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter

### Optional schema metadata

These metadata MAY exist in the schema's metadata.

#### `space`

- encoding: UTF-8 string

Unique identifier for the [space](../conventions.md#spaces) in which the data exists.

## Fields

These fields are defined in addition to those defined by any parent classes.

### Required fields

These fields MUST exist in the file.

### Optional fields

These fields MAY exist in the file.

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other fields,
and MAY be invalidated if the source fields are updated.
