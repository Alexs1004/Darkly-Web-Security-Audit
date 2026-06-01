#brute force

## Description de la vulnérabilité
Sur la page suivante: `http://192.168.122.37/?page=signinhttp://192.168.122.37/?page=signin`. On a systeme de login.
Grace a l'exploit des injections des SQL on a quelques utilisateurs. Notamenet `getTheFlag`.
Apres quelques tentatives, on ne remarque aucune restrictions. 
On peut donc tenter une attaque par brute force.

https://owasp.org/www-community/attacks/Brute_force_attack


## Méthode d'exploitation
Pour ce faire, on utilise un script qui va iterer a travers une liste de mot de passe standard sur l'utilisateur getTheFlag.
Et envoyer les requests avec les parametres suivants: 
`http://IP/?page=signin&username=${username}&password=${password}&Login=Login#`

## Remédiation
1. Restriction de temps apres plusieurs de temps.
2. Fail to jail ? 

