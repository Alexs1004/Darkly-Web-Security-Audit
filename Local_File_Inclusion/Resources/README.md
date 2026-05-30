# Local File Inclusion via Path Traversal

## Description de la vulnérabilité
Le paramètre `page` de l'application est vulnérable à une inclusion de fichiers locaux (LFI). L'absence d'assainissement (*sanitization*) des entrées utilisateur permet d'injecter des séquences de traversée de répertoires afin d'accéder à des ressources arbitraires du système de fichiers sous-jacent.

## Méthode d'exploitation
L'exploitation est réalisée en forgeant une requête GET manipulant le paramètre cible pour remonter l'arborescence et forcer l'inclusion du fichier système `/etc/passwd`.
1. **Injection :** Exécution de la traversée de répertoires via l'utilitaire curl :
```bash
curl -s "http://192.168.159.133/?page=../../../../../../../etc/passwd" | grep -i "flag"
```

## Remédiation

La sécurisation nécessite un contrôle strict des fichiers inclus dynamiquement par l'application.

1. **Implémentation d'une Whitelist :** Restreindre les valeurs acceptées par le paramètre `page` à une liste stricte et prédéfinie de fichiers légitimes.
2. **Assainissement des entrées :** Utiliser des fonctions comme `basename()` pour rejeter systématiquement les caractères de traversée (`../`).
3. **Désactivation des directives à risque :** Configurer le fichier de configuration PHP pour s'assurer que `allow_url_fopen` et `allow_url_include` sont positionnés à `Off`.
