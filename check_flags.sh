#!/bin/bash

# Script de suivi des flags manquants par branche
echo "=================================================="
echo "🔍 ANALYSE DES FLAGS MANQUANTS SUR LES BRANCHES"
echo "=================================================="

for b in $(git branch | sed 's/*//'); do
    # Trouver le chemin du fichier flag dans la branche
    flag_file=$(git ls-tree -r --name-only "$b" | grep -i 'flag' | head -n 1)
    
    if [ -z "$flag_file" ]; then
        echo "❌ $b : Aucun fichier 'flag' trouvé."
    else
        # Récupérer le contenu sans les espaces/retours à la ligne
        content=$(git show "$b:$flag_file" 2>/dev/null | tr -d '[:space:]')
        if [ -z "$content" ]; then
            echo "⚠️ $b : Fichier 'flag' présent mais VIDE."
        fi
    fi
done
echo "=================================================="
