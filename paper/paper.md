---
title: 'Regi0: A Python toolkit to complement and verify biological records'
tags:
  - Python
  - biodiversity data
authors:
  - name: Marcelo Villa-Piñeros^[co-first author]
    affiliation: 1
  - name: Helena Olaya-Rodríguez^[co-first author]
    affiliation: 1
  - name: Erika Suarez-Valencia
    affiliation: 1
  - name: Daniel López-Lozano
    affiliation: 1
affiliations:
  - name: Instituto de Investigación de Recursos Biológicos Alexander von Humboldt, Bogotá, Colombia
    index: 1
date: 10 February 2022
bibliography: paper.bib
---
 
# Summary
`regi0` (pronounced re-hyoh) is a Python library to complement and verify existing geographic and taxonomic
information from biological records. Relying on user-provided data or third party APIs, it offers functions
to extract information (*e.g.* country of occurrence or higher-level taxonomic classification) based on each
record's coordinates and scientific name. Furthermore, `regi0` provides a verification function that compares 
existing values in a dataset with extracted (*i.e.* expected) ones, flagging those records that do not match
and adding new suggested values. `regi0` aims to give its users the ability to complete datasets and create 
flexible verification workflows in order to assess their quality before carrying out further analysis or 
uploading them to biodiversity information repositories. Regi0's name comes from a wordplay between *registro*
(record in spanish) and the number zero, which refers to the initial state of the primary biodiversity data.

# Statement of need
`regi0` arises from the Alexander von Humboldt Biological Resources Research Institute, which is the biodiversity 
research arm in the continental territory of the Nation of the National Environmental System (Sina) of Colombia. 
Likewise, it coordinates the Colombian Biodiversity Information System (SiB Colombia) and the creation of the national 
biodiversity inventory. Therefore, the Humboldt Institute is one of the largest publishers of open data on biodiversity 
in SiB Colombia. The Institute handles primary biodiversity data from its collection (both in the field and by review of 
secondary information), cleaning, verification and publication, to its use in different types of analyzes that describe 
the status and trends of biodiversity in the continental territory of Colombia. 

In 2020, it was identified that different teams within the Institute had developed various methodologies and procedures 
for managing biodiversity data, which respond to different objectives and needs. In 2021, it was proposed to generate an 
open tool that would allow unifying the common processes of all teams to assess the quality of primary biodiversity data, 
in a standardized, efficient and open way so that it can continue to be developed in the future according to the needs of 
users, related to the management of biodiversity data. The package is a product created by many hands, with the aim of 
continuing to grow in the number of functions that more contributors consider relevant, therefore it is an open source product 
that is expected to continue its development in the future.

# Acknowledgments

# References
