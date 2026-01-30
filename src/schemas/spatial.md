# Spatial (abstract)

This abstract schema defines metadata and fields available to all neurarrow types containing spatial data.

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

> yoctometer, zeptometer, attometer, femtometer, picometer, nanometer, angstrom, micrometer, millimeter, centimeter, inch, decimeter, foot, yard, meter, dekameter, hectometer, kilometer, mile, megameter, gigameter, terameter, petameter, parsec, exameter, zettameter, yottameter

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
