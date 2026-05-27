# Privilege Escalation via Cookie Tampering

## Description de la vulnérabilité
L'application web s'appuie sur un cookie nommé `I_am_admin` pour déterminer les privilèges d'administration de l'utilisateur. Par défaut, ce cookie contient le hash MD5 du mot `false` (`68934a3e9455fa72420237eb05902327`). L'état d'authentification étant géré côté client et non côté serveur, la valeur peut être falsifiée.

## Méthode d'exploitation
1. Identification du type de hash (MD5) et de sa valeur originale (`false`).
2. Génération du hash MD5 pour la valeur `true` (`b326b5062b2f0e69046810717534cb09`).
3. Injection du cookie modifié dans la requête via la commande suivante :
   ```bash
   curl -s -b "I_am_admin=b326b5062b2f0e69046810717534cb09" [http://192.168.159.133/](http://192.168.159.133/)
