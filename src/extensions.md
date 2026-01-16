# Extensions

## Known extensions

If you publish a neurarrow extension, please list it here.

| Name | Description | URL |
| ---- | ----------- | --- |

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
