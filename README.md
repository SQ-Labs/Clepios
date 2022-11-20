# Clepios
## Chiffrement homomorphe et diagnostic médical

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Implémentation d'un algorithme de diagnostic médical, s'appliquant sur des données chiffrées avec un schéma homomorphe.

## Features

- Détection de la probabilité de maladie cardiaque (données chiffées)
- Calcul du % de body fat à partir de la taille et du poids (données chiffrées)

## Installation

Installation de Pyfhel:
https://github.com/ibarrond/Pyfhel


## Build et lancement du programme
```sh
cd clepios/
docker build -t clepios .
docker run -it --rm -p 5000:5000 clepios
> server available at http://localhost:5000
```
