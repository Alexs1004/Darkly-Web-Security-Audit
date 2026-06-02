#XSS_Data_Uri

## Description de la vulnérabilité
L'application possède une fonctionnalité d'affichage et d'inclusion de médias via la page `index.php?page=media`. Elle utilise un paramètre `src` pour charger des ressources locales (comme l'image par défaut `nsa`).

La vulnérabilité réside dans le fait que l'application reflète et tente de traiter directement la valeur fournie au paramètre `src` sans assainissement (sanitization) ni filtrage adéquat des protocoles réseau. Bien que certaines balises HTML brutes soient bloquées, l'application est vulnérable à l'utilisation du wrapper de flux `data:`.

## Méthode d'exploitation
En exploitant le schéma d'URI `data:`, il est possible d'injecter du code HTML contenant un script JavaScript malveillant directement dans l'URL. Afin de contourner d'éventuels filtres de requêtes textuels, le payload est encodé en Base64 (`PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==` qui correspond à `<script>alert(1)</script>`).

Lorsque le serveur reçoit la requête, il traite l'URI injectée comme une source de données légitime et la reflète dans la page, permettant l'exécution du script côté client et déclenchant la génération du flag.


```bash
curl -s "http://192.168.159.133/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==" | grep -i "flag"
```

## Remédiation
Pour corriger cette vulnérabilité et bloquer les attaques de type Cross-Site Scripting réfléchi via des wrappers :

1. **Validation par liste blanche (Whitelist) :** Restreindre strictement les valeurs acceptées par le paramètre `src` à une liste fermée de fichiers ou d'identifiants autorisés (ex: `nsa`, `albatroz`).
2. **Désactivation des wrappers de protocoles :** Refuser systématiquement les entrées utilisateur commençant par des schémas d'URI non sécurisés ou applicatifs tels que `data:`, `file:`, `php:`, ou `gopher:`.
3. **Échappement des sorties (Output Encoding) :** Encoder les données avant de les injecter ou de les refléter dans le DOM HTML pour s'assurer qu'elles soient traitées comme du texte brut et non comme du code exécutable.




