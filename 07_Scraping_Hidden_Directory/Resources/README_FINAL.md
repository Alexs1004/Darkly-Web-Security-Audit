# Information Disclosure via Hidden Directory Scraping

## Description de la vulnérabilité
L'application souffre d'une divulgation d'informations sensibles due à une mauvaise configuration du serveur Nginx. 

Le fichier `robots.txt` révèle publiquement l'existence d'un répertoire interdit aux moteurs de recherche nommé `/.hidden/`. L'option *Autoindex* étant activée sur ce dossier, un attaquant peut en lister le contenu. La structure a été volontairement complexifiée par une arborescence automatisée de sous-dossiers imbriqués (3 niveaux de profondeur contenant chacun 26 dossiers) dissimulant des milliers de fichiers `README` génériques (*false positives*). L'un de ces fichiers contient le flag recherché.

## Méthode d'exploitation
L'analyse manuelle étant impossible en raison du volume de chemins ($26^3 = 17\ 576$), le processus de crawling et de filtrage a été automatisé en ligne de commande.

1. **Aspiration récursive de la structure :** Utilisation de l'utilitaire `wget` pour télécharger l'intégralité des fichiers nommés `README` en forçant l'outil à ignorer les directives restrictives du serveur.

```bash
wget -e robots=off -r -np -nd -A "README*" http://192.168.159.133/.hidden/

```

* `-e robots=off` : Ignore les règles restrictives définies dans `robots.txt`.

* `-r` : Active le téléchargement récursif à travers tous les sous-dossiers.

* `-np` (*No Parent*) : Empêche l'outil de remonter dans l'arborescence supérieure.

* `-nd` (*No Directories*) : Extrait tous les fichiers à plat dans le répertoire courant sans recréer l'arborescence locale.

* `-A "README*"` : Accepte uniquement les fichiers correspondants à ce pattern.

2. **Filtrage des données :** Application d'un tri par expressions régulières inversées via `grep` pour éliminer le bruit visuel et isoler l'unique fichier légitime contenant le sésame (`README.15795`).

```bash
grep -vE "Toujours pas|Demande à ton voisin|Tu es sur la mauvaise piste|Moi aussi|pas bon" README*

```

## Remédiation

1. **Désactiver l'Autoindex :** Configurer la directive `autoindex` à `off` dans le bloc de configuration Nginx du site pour empêcher le listage public des répertoires sans fichier d'index.
2. **Restriction d'accès :** Bloquer l'accès aux répertoires sensibles via des règles de filtrage IP ou une authentification forte côté serveur (`auth_basic`).
3. **Principe du moindre privilège :** Ne jamais stocker de documentations techniques, fichiers de configuration ou secrets dans l'arborescence publique (*web root*) du serveur.