# Atom-to-atom Mapping
![Static Badge](https://img.shields.io/badge/atom__to__atom__mapping-v.2024.07.1-%2300E78A?logo=github&style=flat)
![Static Badge](https://img.shields.io/badge/Institute%20of%20Science%20Tokyo-%231C3177?style=flat)
![Static Badge](https://img.shields.io/badge/Elix%2C%20Inc.-%235EB6B3?style=flat)

A chemical reaction can be defined as the transformation of a set of chemical compounds into another. Accompanied by
energy change, the atoms of the reactant chemical compounds are rearranged to form the product chemical compounds.
Therefore, correctly mapping this rearrangement of chemical compound atoms is essential for capturing the nature of the
chemical reaction. This atom-to-atom mapping or atom mapping task has proven challenging as it is a generalization of
the subgraph isomorphism problem. The main objective of the **Atom-to-atom Mapping** project is to systematically curate
and facilitate access to relevant chemical reaction compound atom-to-atom mapping resources.


## Installation
A minimal virtual environment can be created using the [git](https://git-scm.com) and [conda](https://conda.io) commands
as follows:

```shell
git clone https://github.com/neo-chem-synth-wave/atom-to-atom-mapping.git

cd atom-to-atom-mapping

conda env create -f environment.yaml

conda activate atom-to-atom-mapping
```

The package can be locally installed using the [pip](https://pip.pypa.io) command as follows:

```shell
pip install --no-build-isolation -e .
```


## Utilization
The purpose of the **scripts** directory is primarily to illustrate how to utilize the **atom_to_atom_mapping** package.
Regardless, the individual scripts can be utilized to run atom-to-atom-mapping on reaction SMILES strings using the
following libraries:

1. [Indigo](https://github.com/epam/Indigo) by [EPAM](https://github.com/epam)
2. [RXNMapper](https://github.com/rxn4chemistry/rxnmapper) by [IBM RXN for Chemistry](https://github.com/rxn4chemistry)
3. [Chytorch RxnMap](https://github.com/chython/chytorch-rxnmap) by [CIMM KFU](https://github.com/cimm-kzn)
4. [LocalMapper](https://github.com/snu-micc/LocalMapper) by [MICC SNU](https://github.com/snu-micc)


### Indigo
The **Indigo <sup>[[1]](#references)</sup>** atom-to-atom-mapping approach can be utilized as follows:

```shell
python scripts/map_reaction_smiles_using_indigo.py \
  --reaction_smiles "[O-][N+](=O)c1ccc(Br)cn1.CC(=O)Nc1ccc(O)cc1>>CC(=O)Nc1ccc(Oc2ccc(nc2)[N+]([O-])=O)cc1"

python scripts/map_reaction_smiles_using_indigo.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_indigo.csv" \
  --number_of_processes 1
```


### RXNMapper
The **RXNMapper <sup>[[2]](#references)</sup>** atom-to-atom-mapping approach can be utilized as follows:

```shell
python scripts/map_reaction_smiles_using_rxnmapper.py \
  --reaction_smiles "COC(Cl)=O.Fc1cccc(COc2ccc3CCNCCc3c2)c1>>COC(=O)N1CCc2ccc(OCc3cccc(F)c3)cc2CC1"

python scripts/map_reaction_smiles_using_rxnmapper.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_rxnmapper.csv" \
  --batch_size 10
```


### Chytorch RxnMap
The **Chytorch RxnMap <sup>[[3]](#references)</sup>** atom-to-atom-mapping approach can be utilized as follows:

```shell
python scripts/map_reaction_smiles_using_chytorch_rxnmap.py \
  --reaction_smiles "OCN1C(=O)Cc2ccccc12.c1nc2ccccc2[nH]1>>O=C1Cc2ccccc2N1Cn1cnc2ccccc12"

python scripts/map_reaction_smiles_using_chytorch_rxnmap.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_chytorch_rxnmap.csv" \
  --number_of_processes 5
```

### LocalMapper
The **LocalMapper <sup>[[4]](#references)</sup>** atom-to-atom-mapping approach can be utilized as follows:

```shell
python scripts/map_reaction_smiles_using_local_mapper.py \
  --reaction_smiles "CS(Cl)(=O)=O.OCCN1CCCc2cc(ccc12)C#N>>CS(=O)(=O)OCCN1CCCc2cc(ccc12)C#N"

python scripts/map_reaction_smiles_using_local_mapper.py \
  --input_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al.csv" \
  --reaction_smiles_column_name "rxn_smiles" \
  --output_csv_file_path "data/uspto_50k_by_20171116_coley_c_w_et_al_local_mapper.csv" \
  --batch_size 10
```


## License Information
The contents of this repository are published under the [MIT](/LICENSE) license. Please refer to individual references
for more details regarding the license information of external resources utilized within this repository.


## Contact
If you are interested in contributing to this repository by reporting bugs, suggesting improvements, or submitting
feedback, feel free to use [GitHub Issues](https://github.com/neo-chem-synth-wave/ncsw-chemistry/issues).


## References
**[[1]](https://lifescience.opensource.epam.com/indigo/index.html)** **EPAM Indigo**:
https://lifescience.opensource.epam.com/indigo/index.html. Accessed on: July 1st, 2024.

**[[2]](/references/20210407_schwaller_p_et_al.md)** Schwaller, P., Hoover, B., Reymond, J., Strobelt, H., and Laino, T.
**Extraction of Organic Chemistry Grammar from Unsupervised Learning of Chemical Reactions**. _Sci. Adv., 7, 15,
eabe4166, 2021_. DOI: https://doi.org/10.1126/sciadv.abe4166.

**[[3]](/references/20220706_nugmanov_r_et_al.md)** Nugmanov, R., Dyubankova, N., Gedich, A., and Wegner, J.K.
**Bidirectional Graphormer for Reactivity Understanding: Neural Network Trained to Reaction Atom-to-atom Mapping Task**.
_J. Chem. Inf. Model., 2022, 62, 14, 3307–3315_. DOI: https://doi.org/10.1021/acs.jcim.2c00344.

**[[4]](/references/20240313_chen_s_et_al.md)** Chen, S., An, S., Babazade. R., and Jung, Y. **Precise Atom-to-atom
Mapping for Organic Reactions via Human-in-the-loop Machine Learning**.  _Nat. Commun., 15, 2250, 2024_.
DOI: https://doi.org/10.1038/s41467-024-46364-y.
