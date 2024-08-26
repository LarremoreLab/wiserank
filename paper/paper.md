---
title: 'wiserank: a platform for running pairwise comparison experiments'
tags:
  - pairwise comparisons
  - preferences
  - ranking
  - flask
  - vue.js
authors:
 - name: Ian Van Buskirk
   orcid: 0000-0003-2298-5149
   affiliation: 1
 - name: Aaron Clauset
   orcid: 0000-0002-3529-8746
   affiliation: "1, 2, 3"
 - name: Daniel B. Larremore
   orcid: 0000-0001-5273-5234
   affiliation: "1, 2"
affiliations:
 - name: Department of Computer Science, University of Colorado Boulder, Boulder, CO, USA
   index: 1
 - name: BioFrontiers Institute, University of Colorado Boulder, Boulder, CO, USA
   index: 2
 - name: Santa Fe Institute, Santa Fe, NM, USA
date: 26 August 2024
bibliography: paper.bib
---

# Summary

``wiserank`` is a platform with which researchers can run pairwise comparison experiments. To start, researchers specify a set of items (e.g. movies) and load them into the platform. Then each participant in the study selects a subset of the items that are relevant to them and makes a number of pairwise comparisons between their selected items. Each participant can also visualize an inferred ranking of the items they have selected based on the comparisons they made. All of the participant data is collected and stored in a database for researchers to access and analyze.

# Statement of Need

In trying to run our own pairwise comparison experiment we found the existing means too inflexible (e.g. [all our ideas](https://all-our-ideas.citizens.is/domain/1)) and/or too oriented towards industry (e.g. [OpinionX](https://www.opinionx.co/)). As a result, we developed our own software which we are using in an ongoing study of the publication preferences of academics. This experience motivated us to extract the core functionalities of the application we built and create ``wiserank`` in the hopes that it can serve as a starting place for other researchers. Thus, the ``wiserank`` platform serves the dual needs of enabling researchers to (1) immediately run a basic pairwise comparison experiment and (2) develop a more custom application to suit their particular needs.

# Acknowledgements

We acknowledge early and valuable feedback from Kate Wootton and Johan Ugander in shaping the design of this project.

# References