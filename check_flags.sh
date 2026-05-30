#!/bin/bash

echo "=================================================="
echo "🔍 ANALYSE GLOBALE ET VÉRIFICATION DES FLAGS"
echo "=================================================="

# Déclarations des structures de suivi
declare -A flag_map
declare -A flag_counts
flag_index=1

# 1. Collecte et détection du statut des branches
for b in $(git branch | sed 's/[* ]//g'); do
    flag_file=$(git ls-tree -r --name-only "$b" | grep -E '^[^/]+/flag$' | head -n 1)

    if [ -z "$flag_file" ]; then
        echo "❌ $b : Aucun fichier 'flag' trouvé."
    else
        content=$(git show "$b:$flag_file" 2>/dev/null | tr -d '[:space:]')
        if [ -z "$content" ]; then
            echo "⚠️ $b : Fichier 'flag' présent mais VIDE."
        else
            # Stockage pour indexation et analyse des doublons
            flag_map["$content"]="${flag_map["$content"]} $b"
            flag_counts["$content"]=$(( ${flag_counts["$content"]} + 1 ))
            
            echo "✅ $b : Flag n°$flag_index trouvé -> $content"
            ((flag_index++))
        fi
    fi
done

echo "=================================================="
echo "📊 ANALYSE DES DUPLICATAS"
echo "=================================================="

has_duplicates=false

for flag in "${!flag_counts[@]}"; do
    if [ "${flag_counts[$flag]}" -gt 1 ]; then
        echo "🚨 DOUBLON DÉTECTÉ : Le flag [$flag] est présent sur les branches :${flag_map[$flag]}"
        has_duplicates=true
    fi
done

if [ "$has_duplicates" = false ]; then
    echo "✨ Aucun doublon détecté. Tous les flags sont uniques !"
fi
echo "=================================================="
