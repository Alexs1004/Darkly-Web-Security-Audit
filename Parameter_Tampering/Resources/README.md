# Mass Assignment / Hidden Field Parameter Tampering

## Description de la vulnérabilité
L'application web implémente une fonctionnalité de récupération de mot de passe qui repose sur la confiance aveugle des données transmises par le client. L'adresse email cible est stockée dans un champ de formulaire masqué (`type="hidden"`). L'absence de validation de l'intégrité de ce champ côté serveur permet à un attaquant de modifier arbitrairement sa valeur lors de la soumission de la requête.

## Méthode d'exploitation
L'exploitation consiste à intercepter et modifier le paramètre `mail` via une requête HTTP POST contrefaite afin d'altérer la logique métier de l'application.
1. **Soumission altérée :** Envoi d'une adresse email modifiée via l'utilitaire curl :
```bash
curl -s -X POST -d "mail=admin@borntosec.com&Submit=Submit" "http://192.168.159.133/?page=recover" | grep -i "flag"

```

## Remédiation

La sécurisation de la logique transactionnelle nécessite de ne jamais faire confiance aux variables contrôlées par l'utilisateur pour définir des contextes applicatifs privilégiés.

1. **Suppression des données sensibles côté client :** Ne pas faire transiter l'adresse email de destination ou l'identité de l'utilisateur dans des champs cachés de formulaires HTML.
2. **Gestion d'état centralisée :** Associer l'action de récupération à l'identifiant de l'utilisateur ou à son email stocké de manière sécurisée dans la session active côté serveur (`$_SESSION`).
3. **Contrôle d'accès logique :** Valider rigoureusement toute entrée utilisateur par rapport à la base de données d'authentification avant de déclencher l'envoi d'un secret.
