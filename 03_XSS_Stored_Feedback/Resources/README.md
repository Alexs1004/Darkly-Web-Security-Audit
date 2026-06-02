# Stored Cross-Site Scripting (XSS) via Logic Flaw on Feedback Form

## Description de la vulnérabilité
L'application web présente une anomalie de validation et une vulnérabilité de type injection de script (Stored XSS) au niveau du formulaire de livre d'or (`?page=feedback`). 

Le mécanisme de vérification du backend est purement textuel et se déclenche de manière asymétrique : le serveur valide l'exercice et délivre le flag uniquement si le paramètre `txtName` contient l'amorce de script exacte `<script>al`. Parallèlement, le serveur implémente un filtre de nettoyage basique qui supprime les balises HTML correctement fermées (ex: `<script>...</script>`). Soumettre un script syntaxiquement complet neutralise donc la détection, tandis qu'un script tronqué ou incomplet contourne le filtre et déclenche l'affichage du secret.

## Méthode d'exploitation
L'exploitation tire parti de cette faille de logique en soumettant une requête `POST` forgée contenant uniquement l'amorce attendue dans le paramètre vulnérable, tout en laissant le reste du formulaire vierge.

1. **Contournement et exfiltration :** Transmission de la chaîne de caractères via l'utilitaire `curl` pour valider la condition du serveur sans subir les restrictions graphiques de taille (`maxlength`) du navigateur.

```bash
curl -s 'http://192.168.159.133/?page=feedback' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'txtName=%3Cscript%3Eal&txtMessage=&btnSign=Sign+Guestbook' | grep -i "the flag is"

```

## Remédiation

1. **Validation stricte de la logique backend :** Remplacer les vérifications textuelles basiques par une analyse comportementale réelle ou une validation stricte des entrées via des expressions régulières robustes.
2. **Encodage systématique des sorties (Output Encoding) :** Appliquer des fonctions d'encodage comme `htmlspecialchars()` en PHP sur l'ensemble des données d'origine utilisateur avant leur insertion dans le DOM, rendant toute tentative d'injection inoffensive.
