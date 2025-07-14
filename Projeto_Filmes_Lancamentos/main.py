from gerar_relatorio import obter_dados
from gerar_json import gerar_json

if __name__ == "__main__":
    lista = obter_dados()
    gerar_json(lista)