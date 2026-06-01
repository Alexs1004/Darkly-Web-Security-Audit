# Survey Parameter Tampering

## Description de la vulnérabilité

Sur la page `?page=survey`, l'application web propose un questionnaire permettant à l'utilisateur de sélectionner une valeur.

En inspectant le code source de la page, on observe le formulaire suivant :

```html
<form action="#" method="post">
    <input type="hidden" name="sujet" value="2">
    <select name="valeur" onChange="javascript:this.form.submit();">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
    </select>
</form>
```

La présence d’un paramètre côté client (`sujet`) défini en dur dans un champ caché (`hidden`) expose l’application à une vulnérabilité de type **Web Parameter Tampering**. En effet, les données envoyées par le client ne doivent jamais être considérées comme fiables, puisqu’elles peuvent être modifiées avant transmission au serveur.

Cette vulnérabilité permet à un utilisateur de manipuler des paramètres applicatifs censés être contrôlés par le serveur. Cela peut conduire à :

* Un accès non autorisé à certaines fonctionnalités ;
* Une altération du comportement logique de l’application ;
* Une exposition de données ou de contenus protégés (ici, le flag).

## Méthode d’exploitation

En accédant à la page et en utilisant l’inspecteur du navigateur, il est possible de modifier manuellement la valeur du paramètre `value` contenu dans le champ caché `sujet`.

Une fois la requête soumise avec une valeur modifiée, l’application accepte le paramètre sans validation côté serveur, ce qui permet d’accéder à des comportements non prévus, notamment l’obtention du flag.

On peut aussi passer par curl si voulu: 
```
curl -X POST "http://192.168.122.37/index.php?page=survey"   -d "sujet=VALEUR_MODIFIEE"   -d "valeur=16000000" | grep "flag"
```


## Remédiation

1. **Valider systématiquement les entrées côté serveur**
   Ne jamais faire confiance aux valeurs envoyées par le client, y compris celles présentes dans des champs `hidden`.

2. **Éviter de stocker des données sensibles côté client**
   Les paramètres critiques comme `sujet` devraient être gérés côté serveur (session, base de données ou logique backend).

3. **Mettre en place une validation stricte des valeurs attendues**
   Vérifier que les valeurs reçues correspondent à une liste blanche de valeurs autorisées avant tout traitement.

4. **Implémenter des contrôles d’autorisation côté serveur**
   Même si une valeur est modifiée par un utilisateur, le serveur doit vérifier que celui-ci est autorisé à effectuer l’action demandée.

