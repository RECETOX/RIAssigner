---
title: 'RIAssigner: A package for gas chromatographic retention index calculation'
tags:
  - Python
  - gas chromatography
  - retention index
  - analytical chemistry
authors:
  - name: Helge Hecht
    orcid: 0000-0001-6744-996X
    affiliation: 1
  - name: Maksym Skoryk
    orcid: 0000-0003-2056-8018
    affiliation: 2
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
The package uses matchms [@Huber2020] and pandas [@reback2020pandas] for data IO and among others supports `.msp` as well as tabular (`.csv` & `.tsv`) formats.
It supports multiple keywords identifying the retention time (RT) and RI columns and support SI units for RT.
The RI can be computed using the method by @VanDenDool:1963 or cubic spline interpolation [@Halang1978] using a reference list containing RT & RI.
The package is hosted via bioconda [@bioconda] and is available on Galaxy [@galaxy].

# Statement of need
The RI is required to compare results from multiple experiments, especially with differing analytical methods.
While the RT of an analyzed compound can differ, the RI is only subject to very small deviations (<100 units on a comparable column), as it is based on a set of standard reference compounds (traditionally an Alkane series) analyzed as part of the experiment.
An example use case is illustrated in \autoref{fig:main}.
It can therefore be used to improve identification of unknown target compounds when employed alongside spectral similarity in spectral library matching based identification of unknowns[@Strehmel2008; @Wei2014].
To leverage the RI in open-source identification workflows, a package providing computation methods as well as file handling is crucial.

# State of the field
Even though retention index computation is contained in the most widely used GUI applications such as MS-DIAL [@Tsugawa2015] and MZmine2 [@Pluskal2010], the Galaxy tool metaMS [@Wehrens2014] and the python package CoreMS [@corilo2021], there is no standalone package which provides support for various computation methods, such as the Kovats RI [@Kovats1958], the Fiehn RI [@Kind2009] or the virtual carbon number [@Harangi2003].
Additionally, these tools expect input data in a fixed format and only perform RI computation and filtering inside the workflow run within the software.

![Identifications across experiments become comparable when mapping the RT to a RI using a list of reference compounds, e.g an alkane series or FAMEs. The markers denote the positions of reference compounds while the arrows indicate the RT and RI values of chemical compounds identified in both studies.\label{fig:main}](images/method_comparison.png)

RIAssigner is a lightweight python package which supports multiple computation methods and data formats and is built on an expandable architecture, closing the gap towards modular annotation workflows.
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
