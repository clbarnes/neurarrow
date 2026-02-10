# Extensions

Neurarrow is designed to be extensible to support different use cases.

## Naming extensions

Extensions MUST have unique names,
and SHOULD ensure this by incorporating the web domain of the controlling entity in reverse DNS format,
like `com.example.my_extension`.

## Extension metadata

All metadata keys associated with an extension MUST be prefixed with the unique name of the extension and a colon,
like `com.example.my_extension:my_key`.
Extensions MAY add any number of required or optional keys.

All extensions MUST define a `version` metadata key,
whose value MUST be a string conforming to the [PEP-440](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers) specification.
Extension authors MAY use whatever versioning scheme they prefer
(e.g. [semantic](https://semver.org/), [effort](https://jacobtomlinson.dev/effver/), [calendar](https://calver.org/))
and document it separately.

The extension version is _required_ in all files using the extension,
so that readers can check whether an extension is in use by checking for the existence of this key.

Extension authors SHOULD document all required and optional metadata keys and the format of their values.

## Extension fields

Extensions MAY add new fields to any schema.
These MUST have names prefixed by the extension name and a colon
(`com.example.my_extension:my_field`).

Extension authors SHOULD document all required, optional, and derived fields.

## Extension example

> This section is not normative.

- The owner of `https://example.com` develops an extension to represent spatially transformed skeletons
- Their extension is named `com.example.transform`
- The schema metadata of tables using this extension includes `com.example.transform:version` and `com.example.transform:uuid`
- The skeletons schema now includes `com.example.transform:original_xyz`, a `struct{x:float64, y:float64, z:float64}` field

## Extension by inheritance

> This section is not normative.

Rather than extending an existing schema, new schemas MAY be created which [inherit](./conventions.md#inheritance) from another.
This is NOT RECOMMENDED, unless a new type of data is being represented.
Data from extension A and extension B can both exist in the same table if they extend the same schema,
but child schema X and child schema Y can only be composed by creating a third child schema Z which inherits from both.

For example, meshes can be represented as a table of vertices and a table of polygons referencing those vertices.
The vertex table can re-use the [point cloud](./schemas/pointclouds.md) schema,
possibly with an extension encoding features like vertex normals.
The polygon table could then create a new schema inheriting from [base](./schemas/base.md) because there is no similar schema already.

## Developing extensions

> This section is non-normative.

Extensions should have a single concern, to facilitate modularity and re-use.
For example, rather than defining a single general "metadata we like to keep track of in our lab" extension,
with multiple fields for different purposes, consider multiple extensions.

Your extension documentation should list

- which schemas it affects
- any added fields
  - include their data types
  - include whether they are required by the extension, optional
    - if they are derived, include how to calculate them
- any added schema or field metadata keys
  - include how to interpret their value
- which version(s) of neurarrow it targets
- whether it depends on any other extensions
  - if so, which version(s)
- any known implementations

Ideally, extension documentation should be based on a public version-controlled repository
(e.g. [codeberg](https://codeberg.org), [gitlab](https://gitlab.com), [github](https://github.com)),
and listed below.
Raise an issue, submit a PR, or contact the neurarrow developers to get your extension listed.

[gh:clbarnes/neurarrow-ext](https://github.com/clbarnes/neurarrow-ext/) has some examples of extensions, as well as a template for defining your own.

## Known extensions

If you publish a neurarrow extension, please list it here.

| Name | Description | Status | URL |
| ---- | ----------- | ------ | --- |
| `net.clbarnes.swc` | Interoperability with the SWC skeleton format | Experimental | <https://github.com/clbarnes/neurarrow-ext/blob/main/extensions/swc.md> |
| `net.clbarnes.connector` | Point annotations associated with connections | Experimental | <https://github.com/clbarnes/neurarrow-ext/blob/main/extensions/connector.md> |

## Wishlist

The below are examples of tabular neuromorphology data which could be defined as extensions of neurarrow.

- [navis](https://navis-org.github.io/navis/) uses a SWC-like [pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
  for its [TreeNeuron](https://navis-org.github.io/navis/reference/navis/#navis.TreeNeuron) morphology, and more dataframes for connectivity and [Dotprops](https://navis-org.github.io/navis/reference/navis/#navis.Dotprops)
  - standardise schema metadata fields
  - add derived fields for caching purposes
  - navis uses a connector table which has its own location; this could be an extension of the connections schema or a new schema
