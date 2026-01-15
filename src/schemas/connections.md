# Connections

Connections are relationships between skeleton nodes other than morphological continuity.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- `version`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `unit`: : as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- `context`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)

### Optional schema metadata

These metadata MAY exist at the schema level.

- `space`: as described in [Conventions](../conventions.md#neurarrow-specific-metadata)
- Arbitrary attributes and extension metadata MAY be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections

## Fields

### Required fields

These fields MUST exist in the file.

#### `connection_id`

- data type: uint64
- nullable: no

An ID for this connection, which MUST be unique within the context.

### `src_sample_id`

- data type: uint64
- nullable: no

An ID for the skeleton sample at the start of this edge.
MUST exist as a `sample_id` in an accessible skeleton table.

If the edge is directed, the logical direction of the connection is from `src` to `tgt`.
If the edge is undirected, the samples are interchangeable.

### `tgt_sample_id`

- data type: uint64
- nullable: no

An ID for the skeleton sample end of this edge.
MUST exist as a `sample_id` in an accessible skeleton table.

If the edge is directed, the logical direction of the connection is from `src` to `tgt`.
If the edge is undirected, the samples are interchangeable.

### `type`

- data type: dict of string
- nullable: no

The type of this connection.
Acceptable values in this specification are

- `synapse` (directed): a chemical synapse where the `src` sample is presynaptic and the `tgt` sample is postsynaptic
- `gap_junction` (undirected): an electrical synapse

Extensions MAY add additional connection types,
which MUST be prefixed by the extension name and a colon `com.example.my_extension:my_type`.

### Optional fields

These fields MAY exist in the file.

Arbitrary attribute and extension fields MAY be added as described in the [Attributes](../conventions.md#attributes) and [Extensions](../conventions.md#extensions) sections.

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other data.

#### `src_fragment_id`

- data type: uint64
- nullable: yes

The ID of the skeleton to which the source sample belongs.
MUST be the fragment ID associated with the sample ID in the skeleton table of this context.

Note that while sample IDs are stable,
the fragment to which they belong may not be as the data evolves.

#### `tgt_fragment_id`

- data type: uint64
- nullable: yes

The ID of the skeleton to which the target sample belongs.
MUST be the fragment ID associated with the sample ID in the skeleton table of this context.

Note that while sample IDs are stable,
the fragment to which they belong may not be as the data evolves.
