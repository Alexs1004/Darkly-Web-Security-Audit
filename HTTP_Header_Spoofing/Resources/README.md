# Broken Access Control via HTTP Header Spoofing

## Description de la vulnérabilité
L'application web implémente un mécanisme de contrôle d'accès défaillant basé exclusivement sur la vérification d'en-têtes HTTP restrictifs (`User-Agent` et `Referer`). 

Dans la page `© BornToSec` dans le footer. L'analyse des commentaires HTML de la page cible révèle que le backend restreint l'affichage du secret aux requêtes provenant prétendument du domaine `https://www.nsa.gov/` et utilisant un agent utilisateur customisé nommé `ft_bornToSec`. Ces informations transitant entièrement côté client, elles peuvent être falsifiées pour contourner la restriction.

## Méthode d'exploitation
L'exploitation est réalisée en forgeant une requête HTTP `GET` configurée avec les attributs requis pour tromper les vérifications du serveur.

1. **Falsification des en-têtes :** Utilisation de l'utilitaire `curl` avec les drapeaux `-H` (Header) et `-e` (Referer) pour injecter les valeurs attendues.

```bash
curl -s -H "User-Agent: ft_bornToSec" -e "https://www.nsa.gov/" "http://192.168.159.133/?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f" | grep -i "flag"
```

## Remédiation

1. **Suppression de la sécurité par l'obscurité :** Ne jamais stocker de règles d'accès ou d'indices critiques dans les commentaires du code source HTML envoyé au client.
2. **Contrôle d'accès robuste :** Ne jamais se fier aux en-têtes HTTP (`User-Agent`, `Referer`, `X-Forwarded-For`) pour valider l'authentification ou les droits d'un utilisateur. Implémenter un contrôle d'accès basé sur des sessions d'authentification sécurisées côté serveur (RBAC).
