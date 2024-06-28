#!/bin/bash

# Verifica se o número correto de argumentos foi fornecido
# if [ "$#" -lt 1 ]; then
  # echo "Uso: $0 arquivo1.md [arquivo2.md arquivo3.md ...]"
  # exit 1
# fi
# 
# for file in ${files[@]}; do 
  # echo file
# done

# Diretório que contém os arquivos .md (pode ser alterado conforme necessário)
directory="."

# Lista todos os arquivos .md no diretório e armazena seus nomes no array 'files'
files=()
while IFS= read -r -d $'\0' file; do
    files+=("$file")
done < <(find "$directory" -maxdepth 1 -name '*.md' -print0)

# Exibe o conteúdo do array 'files' para verificação
# for file in "${files[@]}"; do
    # echo "$file"
# done

# Nome do contêiner Podman a ser usado
container="docker.io/pandoc/extra"

# Template a ser usado
template="eisvogel"

# Loop através dos arquivos fornecidos na linha de comando
for file in "${files[@]}"; do
  # Verifica se o arquivo existe
  if [ -f "$file" ]; then
    # Extrai o nome do arquivo sem a extensão para usar no nome do arquivo PDF de saída
    filename=$(basename "$file" .md)
    echo "$filename"
    # Executa o comando Podman com os argumentos fornecidos
    podman run --rm --volume "$(pwd):/data:z" "$container" "$file" -o "./pdf/${filename}.pdf" --template "$template" --listings
  else
    echo "Arquivo '$file' não encontrado."
  fi
done

