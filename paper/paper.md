---
title: 'wiserank: a platform for running pairwise comparison experiments'
tags:
  - pairwise comparisons
  - preferences
  - ranking
  - flask
  - vue.js
authors:
 - given-names: Ian
   non-dropping-particle: Van
   surname: Buskirk
   orcid: 0000-0003-2298-5149
   affiliation: 1
 - name: Daniel B. Larremore
   orcid: 0000-0001-5273-5234
   affiliation: "1, 2, 3"
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

``wiserank`` is software that allows researchers to run customized pairwise comparison experiments. In the most basic version of a pairwise comparison experiment, a participant is presented with a choice between a pair of items. If a participant is presented with many such pairwise choices, a researcher can learn the participant's preferences. However, this approach may require an excessive number of pairwise comparisons when there are many items to compare, making pairwise comparison experiments with a large number of items and participants slow and unwieldy.  The goal of ``wiserank`` is to provide a solution to address this issue by exposing two speedups to researcher customization in a self-contained, researcher-friendly and participant-friendly package.

From the participant's perspective, the software experience proceeds in two stages. First, the participant selects a subset of all the items (sometimes called a *consideration set*). For instance, a participant might choose only the shirts they would consider buying from the set of all shirts. Second, the participant is presented with pairs of items for comparison from the consideration set, until some stopping condition is reached. For instance, a participant might choose the shirt they like better. Optionally, a participant can also visualize an inferred ranking [@de2018physical; @springrank] of the items from the consideration set, based on the comparisons they made.

From the researcher's perspective, there are four straightforward customizations of this process: (i) specification of the items, (ii) the algorithmic procedure by which items are shown to the participant to be placed in the consideration set, (iii) the algorithmic procedure by which pairwise comparisons are suggested, and (iv) the data visualization presented to the participant. By separating the formation of the consideration set from the pairwise comparisons, and allowing for customization of algorithmic procedures, experiments can be made markedly faster for participants. All participant data is collected and stored in a database for researchers to access and analyze.

# Statement of Need

In trying to run our own pairwise comparison experiment we found the existing means too inflexible (e.g. [all our ideas](https://all-our-ideas.citizens.is/domain/1) [@salganik2015wiki]) and/or too oriented towards industry (e.g. [OpinionX](https://www.opinionx.co/)). As a result, we developed our own software which we are using in an ongoing study of the publication preferences of academics. This experience motivated us to extract the core functionalities of the application we built and create ``wiserank`` in the hopes that it can serve as a starting place for other researchers. Thus, the ``wiserank`` platform serves the dual needs of enabling researchers to (1) immediately run a basic pairwise comparison experiment and (2) develop a more custom application to suit their particular needs.

Attention can be drawn to two specific places where customization of a pairwise comparison experiment may be necessary. First, researchers may wish to implement a custom recommendation algorithm to surface particular items to participants during the item selection stage. Second, researchers may wish to implement a custom pairing algorithm to lead participants through a sequence of pairwise comparisons in a particular order. These algorithms will not only be specific to the items researchers are interested in studying but the scientific tradeoffs they wish to make: To what degree should one recommend a participant items that are similar to those they have already selected? Should one pair items for comparison at random or make use of comparisons already made by a participant? ``wiserank`` enables researchers to confront these questions and realize necessary customizations by exposing the api that is used to recommend and pair items. Simple algorithms that make use of randomization and more sophisticated algorithms are implemented for both recommending and pairing items to help facilitate this process.

# Acknowledgements

We acknowledge early and valuable feedback from Kate Wootton, Johan Ugander, and Aaron Clauset in shaping the design of this project.

# References