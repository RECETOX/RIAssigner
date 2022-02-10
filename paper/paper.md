---
title: 'RIAssigner: A package for gas chromatographic retention index calculation'
tags:
  - Python
  - gas chromatography
  - retention index
  - analytical chemistry
authors:
  - name: Helge Hecht^[corresponding author]
    orcid: 0000-0001-6744-996X
    affiliation: 1
  - name: Maksym Skoryk
    orcid: 0000-0003-2056-8018
    affiliation: "1, 2"
  - name: Martin Čech
    orcid: 0000-0002-9318-1781
    affiliation: "1, 3"
  - name: Elliott James Price
    orcid: 0000-0001-5691-7000
    affiliation: 1

affiliations:
 - name: RECETOX, Faculty of Science, Masaryk University, Kotlarska 2, Brno 60200, Czech Republic
   index: 1
 - name: Institute of Computer Science, Masaryk University, Brno, Czech Republic
   index: 2
 - name: Institute of Organic Chemistry and Biochemistry of the CAS, Prague, Czech Republic
   index: 3
date: 16 December 2021
bibliography: references.bib
---

# Summary

RIAssigner is a software package for the computation of gas chromatographic (GC) retention indices (RIs).
The package uses matchms [@Huber2020] and pandas [@reback2020pandas] for data IO and supports `.msp` as well as tabular (`.csv` & `.tsv`) formats, among others.
It supports multiple keywords identifying the retention time (RT) and RI information and handling SI units for RT.
The RI can be computed using non-isothermal Kováts retention-indexing (from temperature programming, using the definition of @VanDenDool:1963) or cubic spline interpolation [@Halang1978] based on a reference dataset containing RT & RI.
The package is hosted via bioconda [@bioconda] and is accessible to users through the Galaxy ecosystem [@galaxy; @umsa].

# Statement of need
Compounds can be characterized by their retention behavior or elution time from a chromatographic column, under specified conditions.
Analyte retention behavior is a function of physicochemical properties and elution time varies with chromatographic conditions.
In gas chromatography, the retention index of n-alkanes is solely dependent on number of carbon atoms (similarly, the retention indices for other homologous series can depend solely on number of functional groups) and so unlike retention time, retention index provides a direct relationship to chemical structure [@Peng2010].

Therefore, RI is only subject to very small deviations when using a column with similar separation properties.
This allows comparison of data coming from samples analyzed under different analytical conditions e.g., columns of different length or different temperature gradient.
An example use case is illustrated in \autoref{fig:main}.
It can therefore be used to improve identification of unknown target compounds when employed alongside spectral similarity in spectral library matching based identification of unknowns [@Strehmel2008; @Halket1999c].

To leverage the RI in open-source identification workflows, a package providing computation methods as well as data handling is crucial.

![Example mapping of RI between two experiments with differing chromatographic setup. The markers denote the positions of reference compounds while the arrows indicate the RT and RI values of chemical compounds measured as standards via @rcx_metabolomics and identified in the study conducted in [@Weidt2016].\label{fig:main}](images/method_comparison_v2.png)
# State of the field
RI computation is contained in the most widely used GUI applications such as MS-DIAL [@Tsugawa2015] and MZmine2 [@Pluskal2010], the Galaxy tool metaMS [@Wehrens2014] and the python package CoreMS [@corilo2021].
However, there is no standalone package which provides support for various computation methods based on homologous series (e.g., alkanes [@Kovats1958], fatty acid methyl esters (FAMEs) [@Kind2009]) or the virtual carbon number [@Harangi2003].
Additionally, existing tools expect input data in a fixed format and only perform RI computation and filtering inside the workflow run within the respective software.

RIAssigner is a lightweight Python package which supports multiple computation methods and data formats and is built on an expandable architecture, closing the gap towards modular annotation workflows.
It can be integrated into file-based workflows by supporting various open standards or linked directly via its API into more complex Python applications.

# Author's Contributions
HH wrote the manuscript and developed the software.
MS contributed to the software.
MČ contributed via code reviews and implementation guidance.
EJP provided conceptual oversight and contributed to the manuscript.

# Acknowledgements
The work was supported from Operational Programme Research, Development and Innovation - project RECETOX RI - CZ.02.1.01/0.0/0.0/16_013/0001761.
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 857560.
This publication/presentation reflects only the author's view and the European Commission is not responsible for any use that may be made of the information it contains.

# References
