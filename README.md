# Atom-to-atom Mapping
[![Static Badge](https://img.shields.io/badge/atom__to__atom__mapping-2025.4.1-%23556DC8?logo=github&style=flat)](https://github.com/neo-chem-synth-wave/atom-to-atom-mapping/releases/tag/2024.7.2)
[![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)](https://www.isct.ac.jp)
[![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)](https://www.elix-inc.com)

Welcome to the chemical reaction compound **Atom-to-atom Mapping** research project !!!

A chemical reaction can be defined as the transformation of a set of chemical compounds into another. Accompanied by
energy change, the atoms of the reactant chemical compounds are rearranged to form the product chemical compounds, with
or without the help of spectator compounds. Therefore, correctly mapping this rearrangement of chemical compound atoms
is paramount for capturing the essence of the chemical reaction. This task, commonly referred to as atom-to-atom mapping
or atom mapping, has proven challenging as it is a generalization of the well-known and NP-complete subgraph isomorphism
problem. Consequently, the main objective of the **Atom-to-atom Mapping** research project is to systematically curate
and facilitate access to relevant chemical reaction compound atom-to-atom mapping resources.


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
# Assumption #1: The current directory is 'atom-to-atom-mapping'.

pip install .

# Note #1: The 'atom_to_atom_mapping.egg-info' directory created by the process can be safely removed.
```


### LocalMapper
According to the issues [#4](https://github.com/snu-micc/LocalMapper/issues/4) and
[#5](https://github.com/snu-micc/LocalMapper/issues/5) on the official
[LocalMapper](https://github.com/snu-micc/LocalMapper) repository, there may be potential conflicts between libraries.
The [appropriate version of the DGL library](https://www.dgl.ai/pages/start.html) can be installed using the
[pip](https://pip.pypa.io) command as follows:

```shell
pip uninstall dgl

# Example #1: This command installs the DGL library assuming the PyTorch and CUDA library versions 2.4 and 12.1, respectively.
pip install dgl -f https://data.dgl.ai/wheels/torch-2.4/cu121/repo.html
```


## Utilization
The purpose of the [scripts](/scripts) directory is to illustrate how to map chemical reactions using the following
approaches:

1. [Indigo](https://github.com/epam/Indigo) <sup>[[1](https://lifescience.opensource.epam.com/indigo/index.html)]</sup>
2. [RXNMapper](https://github.com/rxn4chemistry/rxnmapper) <sup>[[2](/references/2021/20210407_schwaller_p_et_al.md)]</sup>
3. [Chytorch RxnMap](https://github.com/chython/chytorch-rxnmap)
<sup>[[3](/references/2022/20220706_nugmanov_r_et_al.md)]</sup>
4. [LocalMapper](https://github.com/snu-micc/LocalMapper) <sup>[[4](/references/2024/20240313_chen_s_et_al.md)]</sup>

The [map_reactions](/scripts/map_reactions.py) script can be utilized as follows:

```shell
# Use Case #1: Map a chemical reaction SMILES string using the Indigo approach.
python scripts/map_reactions.py \
  --atom-to-atom-mapping-approach "indigo" \
  --reaction_smiles "[O-][N+](=O)c1ccc(Br)cn1.CC(=O)Nc1ccc(O)cc1>>CC(=O)Nc1ccc(Oc2ccc(nc2)[N+]([O-])=O)cc1"

# Use Case #2: Map a chemical reaction SMILES dataset using the Indigo approach.
python scripts/map_reactions.py \
  --atom-to-atom-mapping-approach "indigo" \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al/data_processed.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/data_processed_indigo.csv"
```

<sup>**rxnmapper**</sup> Please keep in mind that the execution device of the model at the center of the approach is
[determined automatically](https://github.com/rxn4chemistry/rxnmapper/blob/90a7012c9c0127f4a347baf815e270d8807b5a39/rxnmapper/core.py#L73C15-L73C83).
Therefore, the [visibility of the devices](https://developer.nvidia.com/blog/cuda-pro-tip-control-gpu-visibility-cuda_visible_devices)
and subsequent batch size should be adjusted before executing the scripts.

<sup>**chytorch_rxnmap**</sup> Please keep in mind that the execution device of the model at the center of the approach
is [set to the CPU by default](https://github.com/chython/chython/blob/70299a60f1eddb361abb6d89274c21b7cd430f43/chython/__init__.py#L29),
and the number of utilized CPU cores is not easily controllable.

<sup>**local_mapper**</sup> Please keep in mind that the execution device of the model at the center of the approach is
[set to the CPU by default](https://github.com/chython/chython/blob/70299a60f1eddb361abb6d89274c21b7cd430f43/chython/__init__.py#L29),
and the number of utilized CPU cores is not easily controllable.


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual references
for more details regarding the license information of external resources utilized within this repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to do so using [GitHub Issues](https://github.com/neo-chem-synth-wave/atom-to-atom-mapping/issues).


## References
**[[1](https://lifescience.opensource.epam.com/indigo/index.html)]** **EPAM Indigo**:
https://lifescience.opensource.epam.com/indigo/index.html. Accessed on: April 9th, 2025.

**[[2](/references/2021/20210407_schwaller_p_et_al.md)]** Schwaller, P., Hoover, B., Reymond, J., Strobelt, H., and
Laino, T. **Extraction of Organic Chemistry Grammar from Unsupervised Learning of Chemical Reactions**. _Sci. Adv._, 7,
eabe4166, 2021.

**[[3](/references/2022/20220706_nugmanov_r_et_al.md)]** Nugmanov, R., Dyubankova, N., Gedich, A., and Wegner, J.K.
**Bidirectional Graphormer for Reactivity Understanding: Neural Network Trained to Reaction Atom-to-atom Mapping Task**.
_J. Chem. Inf. Model._, 2022, 62, 14, 3307–3315.

**[[4](/references/2024/20240313_chen_s_et_al.md)]** Chen, S., An, S., Babazade, R., and Jung, Y. **Precise Atom-to-atom
Mapping for Organic Reactions via Human-in-the-loop Machine Learning**.  _Nat. Commun._, 15, 2250, 2024.
