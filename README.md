# The Atom-to-atom Mapping Project
![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)
![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)

Welcome to the chemical reaction compound atom-to-atom mapping project !!!

A chemical reaction can be defined as the transformation of a set of chemical compounds into another. Accompanied by
energy change, the atoms of the reactant chemical compounds are rearranged to form the product chemical compounds.
Therefore, correctly mapping this rearrangement of chemical compound atoms is essential for capturing the nature of the
chemical reaction. This atom-to-atom mapping or atom mapping task has proven challenging as it is a generalization of
the well-known subgraph isomorphism problem. Consequently, the main objective of this project is to systematically
curate and facilitate access to relevant chemical reaction compound atom-to-atom mapping research resources.


## Installation
A standalone environment can be created using the [git](https://git-scm.com) and [conda](https://conda.io) commands as
follows:

```shell
git clone https://github.com/neo-chem-synth-wave/atom-to-atom-mapping.git

cd atom-to-atom-mapping

conda env create -f environment.yaml

conda activate atom-to-atom-mapping-env
```

The [atom_to_atom_mapping](/atom_to_atom_mapping) package can be installed using the [pip](https://pip.pypa.io) command
as follows:

```shell
pip install --no-build-isolation -e .
```


## Utilization
The purpose of the [scripts](/scripts) directory is to illustrate how to run the atom-to-atom mapping using the
following approaches:

1. [Indigo](https://github.com/epam/Indigo) <sup>[[1]](https://lifescience.opensource.epam.com/indigo/index.html)</sup>
by [EPAM](https://www.epam.com)
2. [RXNMapper](https://github.com/rxn4chemistry/rxnmapper) <sup>[[2]](/references/20210407_schwaller_p_et_al.md)</sup>
by [IBM RXN for Chemistry](https://rxn.res.ibm.com)
3. [Chytorch RxnMap](https://github.com/chython/chytorch-rxnmap)
<sup>[[3]](/references/20220706_nugmanov_r_et_al.md)</sup> by [CIMM KFU](https://cimm.kpfu.ru)
4. [LocalMapper](https://github.com/snu-micc/LocalMapper) <sup>[[4]](/references/20240313_chen_s_et_al.md)</sup> by
[MICC SNU](https://micc.snu.ac.kr)


### Indigo
The [map_reaction_smiles_using_indigo](/scripts/map_reaction_smiles_using_indigo.py) script can be utilized as follows:

```shell
# Example #1: Map a chemical reaction SMILES string using the Indigo approach.
python scripts/map_reaction_smiles_using_indigo.py \
  --reaction_smiles "[O-][N+](=O)c1ccc(Br)cn1.CC(=O)Nc1ccc(O)cc1>>CC(=O)Nc1ccc(Oc2ccc(nc2)[N+]([O-])=O)cc1"

# Example #2: Map a chemical reaction SMILES dataset using the Indigo approach.
python scripts/map_reaction_smiles_using_indigo.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_indigo.csv"
```


### RXNMapper
The [map_reaction_smiles_using_rxnmapper](/scripts/map_reaction_smiles_using_rxnmapper.py) script can be utilized as
follows:

```shell
# Example #1: Map a chemical reaction SMILES string using the RXNMapper approach.
python scripts/map_reaction_smiles_using_rxnmapper.py \
  --reaction_smiles "COC(Cl)=O.Fc1cccc(COc2ccc3CCNCCc3c2)c1>>COC(=O)N1CCc2ccc(OCc3cccc(F)c3)cc2CC1"

# Example #2: Map a chemical reaction SMILES dataset using the RXNMapper approach.
python scripts/map_reaction_smiles_using_rxnmapper.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_rxnmapper.csv"
```

Please keep in mind that the execution device of the model at the center of the approach is
[determined automatically](https://github.com/rxn4chemistry/rxnmapper/blob/90a7012c9c0127f4a347baf815e270d8807b5a39/rxnmapper/core.py#L73C15-L73C83).
Therefore, the [visibility of the devices](https://developer.nvidia.com/blog/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices)
and subsequent batch size should be adjusted before executing the scripts.


### Chytorch RxnMap
The [map_reaction_smiles_using_chytorch_rxnmap](/scripts/map_reaction_smiles_using_chytorch_rxnmap.py) script can be
utilized as follows:

```shell
# Example #1: Map a chemical reaction SMILES string using the Chytorch RxnMap approach.
python scripts/map_reaction_smiles_using_chytorch_rxnmap.py \
  --reaction_smiles "OCN1C(=O)Cc2ccccc12.c1nc2ccccc2[nH]1>>O=C1Cc2ccccc2N1Cn1cnc2ccccc12"

# Example #2: Map a chemical reaction SMILES dataset using the Chytorch RxnMap approach.
python scripts/map_reaction_smiles_using_chytorch_rxnmap.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_chytorch_rxnmap.csv"
```

Please keep in mind that the execution device of the model at the center of the approach is
[set to the CPU by default](https://github.com/chython/chython/blob/70299a60f1eddb361abb6d89274c21b7cd430f43/chython/__init__.py#L29),
and the number of utilized CPU cores is not easily controllable.


### LocalMapper
The [map_reaction_smiles_using_local_mapper](/scripts/map_reaction_smiles_using_local_mapper.py) script can be utilized
as follows:

```shell
# Example #1: Map a chemical reaction SMILES string using the LocalMapper approach.
python scripts/map_reaction_smiles_using_local_mapper.py \
  --reaction_smiles "CS(Cl)(=O)=O.OCCN1CCCc2cc(ccc12)C#N>>CS(=O)(=O)OCCN1CCCc2cc(ccc12)C#N"

# Example #2: Map a chemical reaction SMILES dataset using the LocalMapper approach.
python scripts/map_reaction_smiles_using_local_mapper.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_local_mapper.csv"
```


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual references
for more details regarding the license information of external resources utilized within this repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to use [GitHub Issues](https://github.com/neo-chem-synth-wave/atom-to-atom-mapping/issues).


## References
**[[1]](https://lifescience.opensource.epam.com/indigo/index.html)** **EPAM Indigo**:
https://lifescience.opensource.epam.com/indigo/index.html. Accessed on: July 26th, 2024.

**[[2]](/references/20210407_schwaller_p_et_al.md)** Schwaller, P., Hoover, B., Reymond, J., Strobelt, H., and Laino, T.
**Extraction of Organic Chemistry Grammar from Unsupervised Learning of Chemical Reactions**. _Sci. Adv._, 7,
eabe4166, 2021.

**[[3]](/references/20220706_nugmanov_r_et_al.md)** Nugmanov, R., Dyubankova, N., Gedich, A., and Wegner, J.K.
**Bidirectional Graphormer for Reactivity Understanding: Neural Network Trained to Reaction Atom-to-atom Mapping Task**.
_J. Chem. Inf. Model._, 2022, 62, 14, 3307–3315.

**[[4]](/references/20240313_chen_s_et_al.md)** Chen, S., An, S., Babazade, R., and Jung, Y. **Precise Atom-to-atom
Mapping for Organic Reactions via Human-in-the-loop Machine Learning**.  _Nat. Commun._, 15, 2250, 2024.
