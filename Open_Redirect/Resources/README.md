# Open Redirect

## Description de la vulnérabilité
L'application possède une fonctionnalité de redirection globale via la page `index.php?page=redirect`. Celle-ci utilise un paramètre `site` destiné à rediriger l'utilisateur vers des plateformes partenaires spécifiques (Facebook, Twitter, Instagram).

La vulnérabilité réside dans l'absence de contrôle et de validation stricte de la valeur passée à ce paramètre. L'application fait aveuglément confiance à l'entrée utilisateur et accepte n'importe quelle URL absolue externe au lieu de restreindre la navigation au périmètre de confiance.

## Méthode d'exploitation
En manipulant directement la requête HTTP et en remplaçant la valeur par défaut du paramètre `site` par une URL externe arbitraire (comme `http://www.perdu.com`), la logique de routage interne est altérée. 

Au lieu d'exécuter la redirection, le mécanisme applicatif de la VM détecte la manipulation de la chaîne et génère le flag de validation.

```bash
curl -s "http://192.168.159.133/index.php?page=redirect&site=http://www.perdu.com"

```

## Remédiation

Pour corriger efficacement cette vulnérabilité, il est nécessaire de ne plus faire confiance aux entrées utilisateurs directes pour les redirections :

1. **Mise en place d'une liste blanche (Whitelist) :** Restreindre les valeurs acceptées à un ensemble strict d'identifiants prévisibles (ex: uniquement `facebook`, `twitter`, `instagram`) ou à des domaines explicitement autorisés.
2. **Interdiction des URL absolues :** Rejeter immédiatement toute entrée contenant des schémas d'URL globaux (`http://` ou `https://`) pour empêcher l'injection de cibles externes non maîtrisées.

