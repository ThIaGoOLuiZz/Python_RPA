import json

def gerar_json(lista):
    with open('filmes_lancamentos.json', 'w', encoding='utf-8') as arquivo:
        json.dump(lista, arquivo, ensure_ascii=False, indent=4)