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

RIAssigner is a software package for the computation of gas chromatographic retention indices. The package uses matchms [@Huber2020] and pandas [@reback2020pandas] for data IO and supports `.msp` as well as tabular (`.csv` & `.tsv`) input and output data formats. It supports multiple keywords identifying the retention time and retention index columns and support SI units for retention time. The retention index can be computed using the method by `@VanDenDool1963` or cubic spline interpolation using a reference list containing retention times & indices. The package is hosted via bioconda and is available on Galaxy.

# Statement of need
The retention index is required to compare results from different chromatographic columns.
While the retention times of one compound analyzed on different columns can differ, the retention index is only subject to very small deviations.
It can therefore be used for identification of unknown target compounds alongside spectral library matching [@Strehmel2008; @Wei2014].

# State of the field
Even though retention index computation is contained in the most widely used GUI applications such as MS-DIAL [@Tsugawa2015] and MZmine2 [@Pluskal2010] and the Galaxy tool metaMS [@Wehrens2014] there is no standalone package which provides support for various computation methods or retention indices, such as the Kovats RI [@Kovats1958], the Fiehn RI [@Kind2009] or the virtual carbon number [@Harangi2003].
These tools are bound to consume input data in fixed formats or to only allow for RI computation and filtering inside the workflow run within the software.

RIAssigner is a lightweight python package which supports multiple computation methods and data formats and is built on an expendable architecture.
It can be used in any identification workflow and can be used as a modular building block due to its file-based input and outputs.

# Author's Contributions
HH wrote the manuscript and developed the software. MS contributed to the software. EJP developed the concepts. MC contributed via code reviews and implementation guidance.

# Acknowledgements
The work was supported from Operational Programme Research, Development and Innovation - project RECETOX RI - CZ.02.1.01/0.0/0.0/16_013/0001761.
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 857560.
This publication/presentation reflects only the author's view and the European Commission is not responsible for any use that may be made of the information it contains.

# References
