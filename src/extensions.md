# Extensions

Neurarrow is designed to be extensible to support different use cases.

## Naming extensions

Extensions MUST have unique names,
and SHOULD ensure this by incorporating the web domain of the controlling entity in reverse DNS format
(`com.example.my_extension`).

## Extension metadata

Where an extension is in use for a particular schema,
the version of the extension MUST be included in the schema metadata under a key which is the extension name, a colon, and the literal string `version`.
The value MUST be a UTF-8 encoded string conforming to the [PEP-440](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers) specification.
Extension authors MAY use whatever versioning scheme they prefer
(e.g. [semantic](https://semver.org/), [effort](https://jacobtomlinson.dev/effver/), [calendar](https://calver.org/))
and document it separately.

Extensions MAY add schema or field metadata.
These MUST have keys prefixed by the UTF-8 encoded extension name and a colon
(`com.example.my_extension:my_key`).

Extension authors SHOULD document all required and optional metadata keys and the format of their values.

## Extension fields

Extensions MAY add new fields to any schema.
These MUST have names prefixed by the extension name and a colon
(`com.example.my_extension.my_field`).

Extension authors SHOULD document all required, optional, and derived fields.

## Extension example

- The owner of `https://example.com` develops an extension to represent spatially transformed skeletons
- Their extension is named `com.example.transform`
- The schema metadata of tables using this extension includes `com.example.transform:version` and `com.example.transform:uuid`
- The skeletons schema now includes `com.example.transform:original_xyz`, a `struct{x:float64, y:float64, z:float64}` field

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

Ideally, extension documentation should be based on a public version-controlled repository
(e.g. [codeberg](https://codeberg.org), [gitlab](https://gitlab.com), [github](https://github.com)),
and listed below.
Raise an issue, submit a PR, or contact the neurarrow developers to get your extension listed.

## Known extensions

If you publish a neurarrow extension, please list it here.

| Name | Description | Status | URL |
| ---- | ----------- | ------ | --- |

## Wishlist

The below are examples of tabular neuromorphology data which could be defined as extensions of neurarrow.

- [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html)
  (and [SWCplus](https://neuroinformatics.nl/swcPlus/))
  - define a schema metadata field for the SWC header
  - add an i64 field to the skeletons schema for the sample type
- [navis](https://navis-org.github.io/navis/) uses a SWC-like [pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
  for its [TreeNeuron](https://navis-org.github.io/navis/reference/navis/#navis.TreeNeuron),
  as well as a pandas-based [Dotprops](https://navis-org.github.io/navis/reference/navis/#navis.Dotprops)
  - standardise schema metadata fields
  - add derived fields for caching purposes
  - navis uses a connector table which has its own point; this could be an extension of the connections schema or a new schema
