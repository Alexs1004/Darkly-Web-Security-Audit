# Arbitrary File Upload via MIME-Type Spoofing

## Description de la vulnérabilité
L'application web permet aux utilisateurs de téléverser des fichiers via le paramètre `?page=upload`. Bien que l'interface indique que seules les images sont autorisées, la validation implémentée côté serveur est défectueuse. 

Le script PHP s'appuie exclusivement sur la métadonnée `Content-Type` fournie par le client (le type MIME transmis dans l'en-tête de la requête HTTP) pour valider la nature du fichier, au lieu de vérifier l'extension réelle ou la signature binaire du document. Cette absence de contrôle strict permet à un attaquant d'uploader un script exécutable (PHP) sur le serveur.

## Méthode d'exploitation
En forgeant une requête réseau `multipart/form-data` via l'utilitaire `curl`, nous avons transmis un fichier contenant du code PHP (`test.php`) tout en altérant manuellement le type MIME pour déclarer de manière frauduleuse une image JPEG (`type=image/jpeg`).

```bash
curl -s -F "uploaded=@test.php;type=image/jpeg" \
     -F "Upload=Upload" \
     "[http://192.168.159.133/index.php?page=upload](http://192.168.159.133/index.php?page=upload)"
```

## Remédiation

1. **Validation stricte de l'extension :** Implémenter une liste blanche des extensions autorisées (ex: `.jpg`, `.jpeg`, `.png`) et rejeter systématiquement toute autre extension, indépendamment du type MIME annoncé.
2. **Vérification du contenu réel :** Utiliser des fonctions d'analyse binaire côté serveur (ex: l'extension `Fileinfo` en PHP ou l'examen des "Magic Bytes") pour valider la véritable nature du fichier.
3. **Sécurisation du stockage :** Enregistrer les fichiers téléversés en dehors de la racine web publique de l'application et désactiver l'exécution des scripts (via la configuration du serveur web ou des droits d'accès) dans le répertoire de destination.
