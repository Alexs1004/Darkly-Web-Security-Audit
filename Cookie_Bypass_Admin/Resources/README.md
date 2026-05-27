# Privilege Escalation via Cookie Tampering

## Description de la vulnérabilité
L'application s'appuie sur un cookie nommé `I_am_admin` pour déterminer les privilèges d'administration. Ce cookie contient le hash MD5 du mot `false` (`68934a3e9455fa72420237eb05902327`). L'état d'authentification étant géré à tort côté client, sa valeur peut être falsifiée.

## Méthode d'exploitation
1. **Analyse :** Identification du type de hash (MD5) et de sa valeur originale (`false`).
2. **Génération :** Calcul du hash MD5 pour la valeur `true` (`b326b5062b2f0e69046810717534cb09`).
3. **Injection :** Altération du cookie via la commande réseau suivante pour usurper l'identité d'un administrateur :

```bash
curl -s -b "I_am_admin=b326b5062b2f0e69046810717534cb09" "[http://192.168.159.133/](http://192.168.159.133/)"
```

## Remédiation
1. **Gestion des sessions côté serveur :** Ne jamais stocker de rôles ou de privilèges critiques directement dans les cookies clients. Utiliser des identifiants de session (`Session ID`) pointant vers un état sécurisé côté serveur.
2. **Signature des jetons :** Si les données doivent transiter côté client, implémenter des jetons signés cryptographiquement (ex: JWT) pour empêcher toute modification non autorisée.
