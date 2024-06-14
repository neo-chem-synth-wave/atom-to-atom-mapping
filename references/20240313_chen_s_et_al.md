# Overview
**Title:** Precise Atom-to-atom Mapping for Organic Reactions via Human-in-the-loop Machine Learning<br>
**Authors:** Shuan Chen, Sunggi An, Ramil Babazade, Yousung Jung<br>
**Publication Date:** 2024/03/13<br>
**Publication Links:** [Nature Communications](https://www.nature.com/articles/s41467-024-46364-y)<br>
**Alternative Links:** [ResearchGate](https://www.researchgate.net/publication/378939425_Precise_atom-to-atom_mapping_for_organic_reactions_via_human-in-the-loop_machine_learning)<br>
**Code Links:** [GitHub](https://github.com/snu-micc/LocalMapper)


# Abstract
Atom-to-atom mapping (AAM) is a task of identifying the position of each atom in the molecules before and after a
chemical reaction, which is important for understanding the reaction mechanism. As more machine learning (ML) models
were developed for retrosynthesis and reaction outcome prediction recently, the quality of these models is highly
dependent on the quality of the AAM in reaction datasets. Although there are algorithms using graph theory or
unsupervised learning to label the AAM for reaction datasets, existing methods map the atoms based on substructure
alignments instead of chemistry knowledge. Here, we present LocalMapper, an ML model that learns correct AAM from
chemist-labeled reactions via human-in-the-loop machine learning. We show that LocalMapper can predict the AAM for 50K
reactions with 98.5% calibrated accuracy by learning from only 2% of the human-labeled reactions from the entire
dataset. More importantly, the confident predictions given by LocalMapper, which cover 97% of 50K reactions, show 100%
accuracy for 3,000 randomly sampled reactions. In an out-of-distribution experiment, LocalMapper shows favorable
performance over other existing methods. We expect LocalMapper can be used to generate more precise reaction AAM and
improve the quality of future ML-based reaction prediction models.


# Citation
```
@article{
    Chen2024,
    author = {Shuan Chen and Sunggi An and Ramil Babazade and Yousung Jung},
    title = {Precise Atom-to-atom Mapping for Organic Reactions via Human-in-the-loop Machine Learning},
    journal = {Nature Communications},
    volume = {15},
    pages = {2250},
    year = {2024},
    doi = {https://doi.org/10.1038/s41467-024-46364-y}
}
```
