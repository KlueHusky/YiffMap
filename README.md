# YiffMap

This project aims to display the *intricate relations* between furries in the most beautiful manner

![banner](images/banner.png)

## Installation 

Clone this repository

``https://github.com/KlueHusky/YiffMap.git``

## Usage

cd into the repository

``cd YiffMap``

Create yaml data file according to ``template.yaml``

This template contains two categories :

- ``individuals`` : list of individuals with prevision for country and species codes
- ``relations`` : connections between the individuals

Run the mapping code :

``python yiffmap.py data_file.yaml output_file.pdf``

the output file can also be a ``.png``