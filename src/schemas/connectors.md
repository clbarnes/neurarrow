# Connectors

Connectors are features used to represent a relationship between two skeleton nodes at a specific location.
For example, a chemical synapse may be represented as a connector.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: `{major}.{minor}` version of neurarrow spec
- `unit`: full name of a spatial unit according to UDUNITS-2, or empty for arbitrary units (e.g. voxels with unknown resolution)
  - angstrom, attometer, centimeter, decimeter, exameter, femtometer, foot, gigameter, hectometer, inch, kilometer, megameter, meter, micrometer, mile, millimeter, nanometer, parsec, petameter, picometer, terameter, yard, yoctometer, yottameter, zeptometer, zettameter

### Optional schema metadata

- `space`: an arbitrary value identifying the space from which these data were taken (e.g. animals, transforms). Two data sets from different spaces SHOULD NOT be compared directly.
- Individual connectors MAY have arbitrary metadata set with keys like `conn:{fragment_id}:{key}`, e.g. `conn:619:name`.
- Arbitrary metadata MAY be set under keys starting with `attr:`, e.g. `attr:acquisition_date`.

## Fields

### Required fields

These fields MUST exist in the file.

#### `id`

- data type: `uint64`
- nullable: no

A unique ID for a single connector.

#### `x`, `y`, `z`

- data type: `float64`
- nullable: no

The location of the sample in 3D, in the units given in the schema metadata.

#### `type`

- data type: `dictionary[string]`
- nullable: no

What type of connector this is.

Valid types are

- `"synapse"`
- `"gapjunction"`

The type of a connector may restrict what kind of relationships skeleton samples may have with it.
