# Chemical Reaction Compound Atom-to-atom Mapping
![Static Badge](https://img.shields.io/badge/ncsw__chemistry-v.2024.06.1-%237A93DC?logo=github&style=flat)
![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)
![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)

A chemical reaction can be defined as a transformation of one set of chemical compounds to another. The correct mapping of the rearrangement of chemical
compound atoms during the transformation is essential for capturing the essence of a chemical reaction. This task, widely known as atom-to-atom mapping, has
proven quite challenging. Nevertheless, novel approaches are being published frequently. The main goal of this repository is to curate existing open-source
chemical reaction compound atom-to-atom mapping libraries.


## Installation
A minimal virtual environment can be created using [Conda](https://docs.conda.io/en/latest) as follows:

```shell
conda env create -f environment.yaml

conda activate atom-to-atom-mapping
```

The package can be locally installed using [pip](https://pip.pypa.io/en/stable) as follows:

```shell
pip install --no-build-isolation -e .
```


## Atom-to-atom Mapping Libraries
The following chemical reaction compound atom-to-atom mapping libraries are currently supported:

1. The **[Chytorch RxnMap](https://github.com/chython/chytorch-rxnmap) <sup>[[1]](#References)</sup>** library
   utilizes a Transformer model for processing chemical compound graphs.
2. The **[EPAM Indigo](https://github.com/epam/Indigo) <sup>[[2]](#References)</sup>** library utilizes a chemical
   compound graph-matching algorithm.
3. The **[LocalMapper](https://github.com/snu-micc/LocalMapper) <sup>[[3]](#References)</sup>** library utilizes a
   human-in-the-loop Message Passing Neural Network model.
4. The **[RXNMapper](https://github.com/rxn4chemistry/rxnmapper)  <sup>[[4]](#References)</sup>** library utilizes a
   chemically agnostic attention-guided Transformer model.


## What's Next?
The following updates are currently planned for version **v.2024.07**:

- [ ] Create the _/documentation_ directory.
- [ ] Create the _/notebooks_ directory.
- [ ] Create the _/scripts_ directory.


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual references
for more details regarding the license information of external resources utilized within this repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to use [GitHub Issues](https://github.com/neo-chem-synth-wave/ncsw-chemistry/issues).


## References
**[[1]](https://doi.org/10.1021/acs.jcim.2c00344)** Nugmanov, R., Dyubankova, N., Gedich, A., and Wegner, J.K.
**Bidirectional Graphormer for Reactivity Understanding: Neural Network Trained to Reaction Atom-to-atom Mapping Task**.
_J. Chem. Inf. Model., 2022, 62, 14, 3307–3315_.

**[[2]](https://lifescience.opensource.epam.com/indigo/index.html)** **EPAM Indigo**:
https://lifescience.opensource.epam.com/indigo/index.html. Accessed on: June 1st, 2024.

**[[3]](https://doi.org/10.1038/s41467-024-46364-y)** Chen, S., An, S., Babazade. R., and Jung, Y. **Precise
Atom-to-atom Mapping for Organic Reactions via Human-in-the-loop Machine Learning**.  _Nat. Commun., 15, 2250, 2024_.

**[[4]](https://doi.org/10.1126/sciadv.abe4166)** Schwaller, P., Hoover, B., Reymond, J., Strobelt, H., and Laino, T.
**Extraction of Organic Chemistry Grammar from Unsupervised Learning of Chemical Reactions**. _Sci. Adv., 7, 15,
eabe4166, 2021_.
