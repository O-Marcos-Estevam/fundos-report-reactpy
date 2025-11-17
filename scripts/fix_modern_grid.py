"""
Script para corrigir a ordem dos parâmetros em modern_grid
Converte: modern_grid(cols=X, gap=Y, child1, child2...)
Para: modern_grid(child1, child2..., cols=X, gap=Y)
"""

import re
from pathlib import Path

def fix_modern_grid_in_file(filepath):
    """Corrige modern_grid em um arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Padrão para encontrar modern_grid com cols/gap no início
    # Procura por modern_grid( seguido de cols= ou gap=
    pattern = r'modern_grid\(\s*(cols=\d+,\s*gap="[^"]+",)'

    matches = list(re.finditer(pattern, content))

    if not matches:
        print(f"  Nenhum modern_grid com parâmetros incorretos encontrado")
        return False

    # Processar de trás para frente para não afetar os índices
    for match in reversed(matches):
        start_pos = match.start()
        params_match = match.group(1)

        # Encontrar o fechamento do modern_grid
        # Conta parênteses para encontrar o fechamento correto
        paren_count = 1
        pos = match.end()
        while pos < len(content) and paren_count > 0:
            if content[pos] == '(':
                paren_count += 1
            elif content[pos] == ')':
                paren_count -= 1
            pos += 1

        if paren_count != 0:
            print(f"  ERRO: Não conseguiu encontrar o fechamento do modern_grid")
            continue

        # Extrair o conteúdo completo
        full_call = content[start_pos:pos]

        # Remover os parâmetros do início
        # modern_grid(cols=X, gap=Y, <children>) -> modern_grid(<children>)
        new_call = full_call.replace(f"modern_grid(\n            {params_match}\n\n            ", "modern_grid(\n            ")
        new_call = new_call.replace(f"modern_grid(\n            {params_match}\n            ", "modern_grid(\n            ")

        # Adicionar os parâmetros antes do último parêntese
        # Encontrar a última vírgula ou o último child antes do )
        last_paren = new_call.rfind(')')

        # Adicionar parâmetros antes do último )
        new_call = new_call[:last_paren] + f",\n\n            {params_match.rstrip(',')}\n        " + new_call[last_paren:]

        # Substituir no conteúdo
        content = content[:start_pos] + new_call + content[pos:]

        print(f"  Corrigido modern_grid na posição {start_pos}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Processa todos os arquivos *_modern.py"""
    pages_dir = Path("fundos_report_reactpy/src/pages")

    files = list(pages_dir.glob("*_modern.py"))

    print(f"Encontrados {len(files)} arquivos para processar\n")

    for filepath in files:
        print(f"Processando {filepath.name}...")
        changed = fix_modern_grid_in_file(filepath)
        if changed:
            print(f"  ✅ Arquivo atualizado\n")
        else:
            print(f"  ⏭️  Nenhuma alteração necessária\n")

    print("Concluído!")


if __name__ == "__main__":
    main()
