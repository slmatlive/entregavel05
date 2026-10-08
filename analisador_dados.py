import csv
import re
import sys
from datetime import datetime
from pathlib import Path


# Criei essa exceção para avisar quando algum campo do cadastro está errado.
class FormatoInvalidoError(Exception):
    pass


def validar_email(email):
    padrao = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
    return re.fullmatch(padrao, email) is not None


def validar_cpf(cpf):
    # Aqui eu verifico o formato, mas não os dígitos verificadores do CPF.
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return re.fullmatch(padrao, cpf) is not None


def validar_telefone(telefone):
    # Formato usado: (99) 99999-9999.
    padrao = r"^\(\d{2}\)\s?\d{5}-\d{4}$"
    return re.fullmatch(padrao, telefone) is not None


def validar_data(data):
    padrao = r"^\d{2}/\d{2}/\d{4}$"

    if re.fullmatch(padrao, data) is None:
        return False

    # Além do formato, vejo se a data existe de verdade.
    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False
    else:
        return True


def conferir_registro(registro):
    # Primeiro eu vejo quais informações estão incorretas.
    problemas = []

    if not registro["nome"]:
        problemas.append("nome vazio")
    if not validar_email(registro["email"]):
        problemas.append("e-mail inválido")
    if not validar_cpf(registro["cpf"]):
        problemas.append("CPF fora do formato")
    if not validar_telefone(registro["telefone"]):
        problemas.append("telefone fora do formato")
    if not validar_data(registro["data"]):
        problemas.append("data inválida")

    if problemas:
        raise FormatoInvalidoError(", ".join(problemas))


def analisar_arquivo(caminho_csv):
    registros = []
    colunas_necessarias = ["nome", "email", "cpf", "telefone", "data"]

    # Uso with open porque ele fecha o arquivo automaticamente.
    with open(caminho_csv, "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        if leitor.fieldnames is None:
            raise ValueError("O CSV está vazio ou não possui cabeçalho.")

        for coluna in colunas_necessarias:
            if coluna not in leitor.fieldnames:
                raise KeyError(coluna)

        # Começo na linha 2 porque a primeira linha é o cabeçalho.
        for numero_linha, linha in enumerate(leitor, start=2):
            registro = {"linha": numero_linha}

            for coluna in colunas_necessarias:
                registro[coluna] = (linha.get(coluna) or "").strip()

            try:
                conferir_registro(registro)
            except FormatoInvalidoError as erro:
                registro["situacao"] = "INVÁLIDO"
                registro["motivo"] = str(erro)
            else:
                registro["situacao"] = "VÁLIDO"
                registro["motivo"] = "Nenhum problema encontrado"

            registros.append(registro)

    return registros


def montar_relatorio(registros):
    total = len(registros)
    total_validos = sum(1 for registro in registros if registro["situacao"] == "VÁLIDO")
    total_invalidos = total - total_validos
    percentual_validos = (total_validos / total * 100) if total > 0 else 0

    linhas = [
        "RELATÓRIO DE ANÁLISE DE DADOS",
        "=" * 60,
        f"Total de registros: {total}",
        f"Registros válidos: {total_validos}",
        f"Registros inválidos: {total_invalidos}",
        f"Percentual de válidos: {percentual_validos:.1f}%",
        "-" * 60,
    ]

    for registro in registros:
        linhas.append(f"Linha {registro['linha']} - {registro['nome'] or '(sem nome)'}")
        linhas.append(f"E-mail: {registro['email']} | CPF: {registro['cpf']}")
        linhas.append(f"Telefone: {registro['telefone']} | Data: {registro['data']}")
        linhas.append(f"Situação: {registro['situacao']}")
        linhas.append(f"Observação: {registro['motivo']}")
        linhas.append("-" * 60)

    return "\n".join(linhas) + "\n"


def main():
    pasta_projeto = Path(__file__).resolve().parent

    # Se eu não informar outro arquivo, o programa usa o dados.csv da pasta.
    caminho_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else pasta_projeto / "dados.csv"
    caminho_relatorio = pasta_projeto / "relatorio.txt"

    try:
        registros = analisar_arquivo(caminho_csv)
        relatorio = montar_relatorio(registros)

        # Salvo o mesmo relatório que aparece no terminal.
        with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:
            arquivo.write(relatorio)

    except FileNotFoundError:
        print(f"Não encontrei o arquivo: {caminho_csv}")
    except KeyError as erro:
        print(f"O arquivo CSV está sem a coluna: {erro}")
    except ValueError as erro:
        print(f"Encontrei um problema com os dados: {erro}")
    except OSError as erro:
        print(f"Não consegui ler ou salvar o arquivo: {erro}")
    else:
        print(relatorio)
        print(f"Relatório salvo em: {caminho_relatorio}")
    finally:
        print("Fim da execução.")


if __name__ == "__main__":
    main()
