# Scraping Hidden Directory (Information Disclosure & Misconfiguration)

## Description de la vulnérabilité
L'application web souffre d'une mauvaise configuration de son serveur Nginx ainsi que d'une divulgation d'informations sensibles via son fichier de directives d'indexation.

En inspectant le fichier `http://192.168.159.133/robots.txt`, deux répertoires interdits aux robots d'indexation ont été identifiés : `/whatever` et `/.hidden/`. 

Le répertoire `/.hidden/` est accessible publiquement et l'option *Autoindex* y est activée, permettant de lister son contenu. Afin d'entraver les analyses manuelles, la structure a été volontairement complexifiée : elle est composée d'une arborescence massive et automatisée de sous-dossiers imbriqués (3 niveaux de profondeur, chacun contenant 26 dossiers nommés de manière aléatoire). Au bout de chaque arborescence se trouve un fichier `README`. Si la majorité de ces fichiers contient des chaînes de caractères génériques destinées à induire en erreur (*false positives*), l'un d'eux contient le flag recherché.

## Méthode d'exploitation
L'exploitation manuelle étant irréalisable en raison du nombre massif de combinaisons ($26^3 = 17\ 576$ chemins possibles), le processus de crawling et de filtrage a été automatisé en ligne de commande.

L'utilisation d'un aspirateur web standard (`wget`) combinée à un contournement des restrictions de sécurité du serveur permet d'extraire l'intégralité de la structure en quelques secondes.

1. **Aspiration récursive et agressive des fichiers cibles :**
   Depuis un terminal, la commande suivante est exécutée pour forcer le téléchargement récursif en ignorant les interdictions du fichier `robots.txt` et en ne conservant que les fichiers dont le nom commence par `README` :
   ```bash
   wget -e robots=off -r -np -nd -A "README*" [http://192.168.159.133/.hidden/](http://192.168.159.133/.hidden/)

```

*Options utilisées :*

* `-e robots=off` : Ignore les règles restrictives définies dans `robots.txt`.
* `-r` : Active le téléchargement récursif à travers tous les sous-dossiers.
* `-np` (*No Parent*) : Empêche l'outil de remonter dans l'arborescence supérieure.
* `-nd` (*No Directories*) : Extrait tous les fichiers à plat dans le répertoire courant sans recréer l'arborescence locale.
* `-A "README*"` : Accepte uniquement les fichiers correspondants à ce pattern.

2. **Filtrage et exfiltration du Flag :**
Une fois les 36 558 fichiers analysés et stockés sur le disque, un tri par expressions régulières inversées (`grep -vE`) est appliqué pour éliminer tout le bruit visuel et isoler l'unique ligne légitime :
```bash
grep -vE "Toujours pas|Demande à ton voisin|Tu es sur la mauvaise piste|Moi aussi|pas bon" README*

```


*Résultat obtenu dans le fichier `README.15795` :*
```text
Hey, here is your flag : d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466

```



## Remédiation

Pour corriger cette vulnérabilité et empêcher l'exfiltration d'informations structurelles, plusieurs mesures doivent être appliquées sur le serveur Nginx :

1. **Désactiver le listage des répertoires (*Directory Browsing*) :**
Il est impératif de s'assurer que l'option `autoindex` est configurée sur `off` dans le fichier de configuration de Nginx (`nginx.conf`) pour empêcher un utilisateur de lister le contenu d'un dossier sans fichier d'index valide.
```nginx
location /.hidden/ {
    autoindex off; 
} 
```

2. **Restreindre l'accès aux dossiers sensibles :**
Les fichiers ou dossiers qui ne doivent pas être indexés par les moteurs de recherche ne doivent pas pour autant être laissés en accès libre. Si un répertoire contient des éléments sensibles, son accès doit être protégé par une authentification forte (ex: `auth_basic`) ou restreint aux adresses IP de confiance.

3. **Principe du moindre privilège :**
Ne jamais stocker de secrets, de fichiers de configuration ou de documentations techniques de déploiement au sein de l'arborescence publique (*web root*) du serveur web.

