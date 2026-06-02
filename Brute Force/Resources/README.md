# Brute Force

## Description de la vulnérabilité

La page d'authentification de l'application est accessible à l'adresse :

`http://192.168.122.37/?page=signin`

À la suite de l'exploitation d'une vulnérabilité d'injection SQL, plusieurs noms d'utilisateurs ont pu être identifiés, notamment le compte `getTheFlag`.

Des tests de connexion répétés ont ensuite été effectués afin d'évaluer les mécanismes de protection. Aucun contrôle de sécurité n'a été observé :

* Absence de limitation du nombre de tentatives de connexion ;
* Absence de verrouillage temporaire du compte ;
* Absence de délai progressif entre les tentatives ;
* Absence de mécanisme CAPTCHA.

Cette configuration permet à un attaquant de réaliser une attaque par force brute afin de deviner le mot de passe d'un compte valide.

Référence OWASP : Brute Force Attack.

## Méthode d'exploitation

L'exploitation consiste à automatiser l'envoi de tentatives d'authentification sur le compte identifié `getTheFlag` à l'aide d'une liste de mots de passe courants (wordlist).
On utilise un script pour envoyer les requêtes sur la route suivante:

```text
http://{IP}/?page=signin&username=<username>&password=<password>&Login=Login
```

## Remédiation

1. **Mettre en place une limitation du nombre de tentatives de connexion:** Verrouillage temporaire du compte après plusieurs échecs consécutifs
2. **Implémenter un délai progressif (rate limiting):** Augmenter progressivement le temps d'attente après chaque tentative échouée.
3. **Déployer un mécanisme CAPTCHA:** Exiger une vérification supplémentaire après plusieurs échecs d'authentification.
5. **Utiliser un outil de bannissement automatique** Utilisation de Fail2Ban permettent de bloquer temporairement les adresses IP.


