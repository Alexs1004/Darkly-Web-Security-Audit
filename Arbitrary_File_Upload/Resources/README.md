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
