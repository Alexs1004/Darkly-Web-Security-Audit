# Privilege Escalation via Cookie Tampering

## Description de la vulnérabilité
L'application s'appuie sur un cookie nommé `I_am_admin` pour déterminer les privilèges d'administration. Il est encodé en MD5 pour faire de l'offuscation. Mais on peut utiliser le site suivant pour décripter le cookie MD5: [https://md5decrypt.net/en/](https://md5decrypt.net/en/). Ce cookie contient le hash MD5 du mot `false` (`68934a3e9455fa72420237eb05902327`) L'état d'authentification étant géré à tort côté client, sa valeur peut être falsifiée.

## Méthode d'exploitation
1. **Analyse :** Identification du type de hash (MD5) et de sa valeur originale (`false`).
2. **Génération :** Calcul du hash MD5 pour la valeur `true` (`b326b5062b2f0e69046810717534cb09`).
3. **Injection :** Altération du cookie via la commande réseau suivante pour usurper l'identité d'un administrateur :

```bash
curl -s -b "I_am_admin=b326b5062b2f0e69046810717534cb09" "[http://192.168.159.133/](http://192.168.159.133/)"
```

## Remédiation
1. **Implemntation d'une gestion des sessions côté serveur :** En nous basant sur l'article [suivant de l'OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#session-management-implementation) : Pour s'assurer de l'authenticier d'une personne. Un site doit utiliser un système d'authentification et un système de gestion de session afin de pouvoir garentir l'identité et un suivit de ces actions à travers du site.
Il ne faut jamais stocker de rôles ou de privilèges critiques directement dans les cookies clients. Utiliser des identifiants de session (`Session ID`) pointant vers un état sécurisé côté serveur.
2. **Signature des jetons :** Si les données doivent transiter côté client, implémenter des jetons signés cryptographiquement (ex: JWT) pour empêcher toute modification non autorisée.
