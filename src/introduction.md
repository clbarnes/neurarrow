# Introduction

Specifications for storing and transmitting neuronal morphology and connectivity data
using the [Apache Arrow](https://arrow.apache.org/) data model,
and models compatible with it (e.g. [Apache Parquet](https://parquet.apache.org/)).

## About Apache Arrow

From [arrow.apache.org](https://arrow.apache.org/):

> Apache Arrow defines a language-independent columnar memory format for flat and nested data,
> organized for efficient analytic operations on modern hardware like CPUs and GPUs.
> The Arrow memory format also supports zero-copy reads for lightning-fast data access without serialization overhead.

Using Apache Arrow gives neurarrow implementors access to a large ecosystem of existing software libraries across languages,
as well as the ability to exchange that data between language runtimes and processes with minimal serialisation cost.

The use of standard binary formats such as parquet also allows the data to be read now and in the future
without neurarrow-specific implementations.

## Prior art

These software packages manage tabular neuroscience data:

- [navis](https://navis.readthedocs.io/en/latest/)
  - The neurarrow specification was originally based on navis' [parquet IO](https://github.com/navis-org/navis/blob/master/navis/io/pq_io.md)
- [CATMAID](https://catmaid.org)
- [natverse](https://natverse.org/)

These file formats describe tabular neuroscience data:

- [SWC](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html)
  (and [SWCplus](https://neuroinformatics.nl/swcPlus/))

These specifications build on Apache Arrow with domain-specific schemas:

- [geoarrow](https://geoarrow.org/) and [geoparquet](https://github.com/opengeospatial/geoparquet/)

## Links

Development happens [on github](https://github.com/clbarnes/neurarrow),
and the rendered specification is at <https://clbarnes.github.io/neurarrow/>.
