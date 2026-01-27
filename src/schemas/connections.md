# Connections

Connections are relationships between point cloud samples other than morphological continuity.

## Schema metadata

### Required schema metadata

These metadata MUST exist at the schema level.

- None

### Optional schema metadata

These metadata MAY exist at the schema level.

- None

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

An ID for the point cloud sample at the start of this edge.
MUST exist as a `sample_id` in an accessible skeleton table.

If the edge is directed, the logical direction of the connection is from `src` to `tgt`.
If the edge is undirected, the samples are interchangeable.

### `tgt_sample_id`

- data type: uint64
- nullable: no

An ID for the point cloud sample end of this edge.
MUST exist as a `sample_id` in an accessible skeleton table.

If the edge is directed, the logical direction of the connection is from `src` to `tgt`.
If the edge is undirected, the samples are interchangeable.

### `type`

- data type: dictionary with index type uint16 and value type variable-length string
- nullable: no

The type of this connection.
Acceptable values in this specification are

- `synapse` (directed): a chemical synapse where the `src` sample is presynaptic and the `tgt` sample is postsynaptic
- `gap_junction` (undirected): an electrical synapse

Undirected connection types SHOULD NOT be repeated to represent both directions
(i.e. if `1 =gap_junction=> 2` is defined, do not explicitly define `2 =gap_junction=> 1`).

Extensions MAY add additional connection types,
which MUST be prefixed by the extension name and a colon, e.g. `com.example.my_extension:my_type`.

### Optional fields

These fields MAY exist in the file.

- None

### Derived fields

These fields MAY exist in the file, but MUST be calculable from other data.

#### `src_fragment_id`

- data type: uint64
- nullable: yes

The ID of the skeleton to which the source sample belongs.
MUST be the fragment ID associated with the sample ID in the skeleton table of this context.

Note that while sample IDs SHOULD be stable,
the fragment to which they belong MAY not be if the data evolves.

#### `tgt_fragment_id`

- data type: uint64
- nullable: yes

The ID of the skeleton to which the target sample belongs.
MUST be the fragment ID associated with the sample ID in the skeleton table of this context.

Note that while sample IDs SHOULD be stable,
the fragment to which they belong MAY not be if the data evolves.
