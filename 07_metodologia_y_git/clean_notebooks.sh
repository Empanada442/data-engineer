#!/bin/bash
# Script para limpiar todos los notebooks antes de commit

echo "Limpiando outputs de notebooks..."

# Buscar todos los .ipynb y limpiar
find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" \-exec jupyter nbconvert --clear-output --inplace {} \;

echo "✓ Notebooks limpiados"
