# neurarrow

> *Work In Progress*

Specifications for storing neuroscience data using the [Apache Arrow](https://arrow.apache.org/) data model,
and models compatible with it (e.g. [Apache Parquet](https://parquet.apache.org/)).

## Versioning

This specification utilises [semantic versioning](https://semver.org/).

Before version `1.0.0`, all minor changes may be break compatibility.
Otherwise,

- Patch versions are used for non-substantive changes to the text of the specification.
- Minor versions are used for additions which do not break backward compatibility, i.e.
  - A v1.2 parser should be able to read all v1.1 files
  - A v1.1 parser may be able to partially read v1.2 files
- Major versions are used for changes which break compatibility, i.e.
  - A v1.x parser may not be able to read a v2.y file and vice versa.

## Prior art

These software packages manage columnar neuroscience data:

- [navis](https://navis.readthedocs.io/en/latest/)
  - This specification was originally based on
- [CATMAID](https://catmaid.org)
- [natverse](https://natverse.org/)

These file formats describe columnar neuroscience data:

- [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html) and [SWCplus](https://neuroinformatics.nl/swcPlus/)
