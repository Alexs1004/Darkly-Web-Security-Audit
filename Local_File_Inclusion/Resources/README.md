# Local File Inclusion via Path Traversal

## Description de la vulnérabilité
Le paramètre `page` de l'application est vulnérable à une [inclusion de fichiers locaux (LFI)](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion). Cette vulnérabilité repose sur le fait que certains fichiers standards sont présent sur le serveur. L'absence d'assainissement (*sanitization*) des entrées utilisateur permet d'injecter des séquences de traversée de répertoires afin d'accéder à des ressources arbitraires du système de fichiers sous-jacent.

## Méthode d'exploitation
On conste que l'url demande un nom de page à chercher via le paramètre `?page=`. L'exploitation est réalisée en forgeant une requête GET manipulant le paramètre cible pour remonter l'arborescence et forcer l'inclusion du fichier système `/etc/passwd`.
1. **Injection :** Exécution de la traversée de répertoires via l'utilitaire curl :
```bash
curl -s "http://192.168.159.133/?page=../../../../../../../etc/passwd" | grep -i "flag"
```

## Remédiation
Pour remédier à cette vulnérabilité on peut agir à deux niveaux. Au niveau de la LFI et au niveau du Path Traversal.
La sécurisation nécessite un contrôle strict des fichiers inclus dynamiquement par l'application.
1. **Non transmission d'input user:** La solution la plus simple bien que pas applicable dans ce cas. Ne pas transmettre d'input user au filesysteme ou à l'API. 
2. **Implémentation d'une Whitelist :** Si le point est pas applicable. Restreindre les valeurs acceptées par le paramètre `page` à une liste stricte et prédéfinie de fichiers légitimes.
3. **Assainissement des entrées :** Utiliser des fonctions comme `basename()` pour rejeter systématiquement les caractères de traversée (`../`).
4. **Désactivation des directives à risque :** Configurer le fichier de configuration PHP pour s'assurer que `allow_url_fopen` et `allow_url_include` sont positionnés à `Off`.
5. **Chrooted jails**: Utiliser chrooted et des polices pour restreindre l'access aux fichiers accessibles.
