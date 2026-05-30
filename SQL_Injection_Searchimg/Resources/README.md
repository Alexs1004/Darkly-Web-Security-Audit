# SQL Injection (UNION Based) sur le champ de recherche d'images

## Description de la vulnérabilité
L'application implémente une fonctionnalité de recherche d'images via le paramètre `image_number` sur l'endpoint `?page=searchimg`. Les entrées utilisateur ne sont pas correctement nettoyées ni paramétrées avant d'être intégrées dans la requête SQL globale exécutée par le serveur.

L'absence de messages d'erreur SQL explicites est contournée en observant le comportement logique de l'application (injection d'opérateurs booléens `AND 1=1` et `AND 1=2`). La vulnérabilité permet à un attaquant d'exécuter des requêtes SQL arbitraires en exploitant l'opérateur `UNION` pour exfiltrer des données sensibles de la base de données.

## Méthode d'exploitation
L'exploitation est réalisée manuellement ou via injection de payloads spécifiques dans le champ de saisie afin de cartographier la structure et d'extraire les données cachées.

1. **Détermination du nombre de colonnes :**
   Le payload `1 UNION SELECT 1,2` confirme que la requête d'origine sélectionne exactement deux colonnes visibles à l'écran.

2. **Évitement du filtrage des guillemets (WAF/Sanitizer Bypass) :**
   Le filtrage des chaînes de caractères (guillemets simples) est contourné en encodant le nom de la table cible (`list_images`) en valeur hexadécimale (`0x6c6973745f696d61676573`).

3. **Exfiltration de la structure de la table :**
   Extraction des colonnes via la table système :
   `1 UNION SELECT group_concat(column_name), 2 FROM information_schema.columns WHERE table_name=0x6c6973745f696d61676573`
   Rendu : `id,url,title,comment`

4. **Extraction du secret :**
   La colonne `comment` contient une consigne de décodage cryptographique :
   `1 UNION SELECT group_concat(comment), 2 FROM list_images`
   Résultat : Un hash MD5 accompagné de l'instruction exigeant son décodage en minuscules, puis son re-hachage en SHA-256 pour générer le flag.

## Remédiation
1. **Requêtes préparées (Parametric Queries) :** Utiliser systématiquement des requêtes préparées avec PDO (en PHP) pour séparer strictement le code SQL des données utilisateurs.
2. **Principe du moindre privilège :** Restreindre les privilèges de l'utilisateur de la base de données afin qu'il ne puisse pas accéder aux tables système comme `information_schema`.
