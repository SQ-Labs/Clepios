# Clepios
## Chiffrement homomorphe et diagnostic médical

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Implémentation d'un algorithme de diagnostic médical, s'appliquant sur des données chiffrées avec un schéma homomorphe.

## Features

- Détection de la probabilité de crise cardiaque
- Récupération de la moyenne de sommeil des patients


## Installation

Installation de Pyfhel:
https://github.com/ibarrond/Pyfhel


## Build et lancement du programme
```sh
cd clepios/
docker build -t clepios .
docker run -it --rm -v $PWD:/app -w /app python3 heart_failure.py
```