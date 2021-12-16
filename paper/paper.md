---
title: 'RIAssigner: A Python package for gas chromatographic retention index calculation'
tags:
  - Python
  - gas chromatography
  - retention index
  - analytical chemistry
authors:
  - name: Helge Hecht^[first author]
    orcid: 0000-0001-6744-996X
    affiliation: 1
  - name: Maksym Skoryk
    orcid: 0000-0003-2056-8018
    affiliation: 2
affiliations:
 - name: RECETOX, Masaryk University, Brno, Czech Republic
   index: 1
 - name: Institute of Computer Science, Masaryk University, Brno, Czech Republic
   index: 2
date: 16 December 2021
bibliography: references.bib
---

# Summary

RIAssigner is a software package for the computation of gas chromatographic retention indices. The package uses matchms [@Huber2020] and pandas [@reback2020pandas] for data IO and supports `.msp` as well as tabular (`.csv` & `.tsv`) input and output data formats. It supports multiple keywords identifying the retention time and retention index columns and support SI units for retention time.


# Statement of need
The retention index is required to compare results from different chromatographic columns. While the retention times of one compound analyzed on different columns can differ, the retention index is only subject to very small deviations. It can therefore be used for identification of unknown target compounds alongside spectral library matching [@Strehmel2008; @Wei2014]

# State of the field
Even though retention index computation is contained in the most widely used GUI applications - MS-DIAL [@Tsugawa2015] and MZmine2 [@Pluskal2010] - there is no standalone package which provides support for various computation methods or retention indices, such as the Kovats RI [@Kovats1958], the Fiehn RI [@Kind2009] or the virtual carbon number [@Harangi2003].
These tools are bound to consume input data in fixed formats or to only allow for RI computation and filtering inside the workflow run within the software.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Acknowledgements


# References
