import csv
import tempfile
import unittest
from pathlib import Path

from analisador_dados import (
    FormatoInvalidoError,
    analisar_arquivo,
    conferir_registro,
    montar_relatorio,
    validar_cpf,
    validar_data,
    validar_email,
    validar_telefone,
)


class TestesDoAnalisador(unittest.TestCase):
    def setUp(self):
        self.registro = {
            "nome": "Pessoa Exemplo",
            "email": "pessoa@exemplo.com",
            "cpf": "123.456.789-09",
            "telefone": "(98) 98765-4321",
            "data": "08/10/2026",
        }

    def test_email_correto(self):
        self.assertTrue(validar_email("pessoa@exemplo.com"))

    def test_email_errado(self):
        self.assertFalse(validar_email("pessoa.exemplo.com"))

    def test_cpf_correto(self):
        self.assertTrue(validar_cpf("123.456.789-09"))

    def test_cpf_errado(self):
        self.assertFalse(validar_cpf("12345678909"))

    def test_telefone_correto(self):
        self.assertTrue(validar_telefone("(98) 98765-4321"))

    def test_telefone_errado(self):
        self.assertFalse(validar_telefone("98987654321"))

    def test_data_valida(self):
        self.assertTrue(validar_data("08/10/2026"))

    def test_data_impossivel(self):
        self.assertFalse(validar_data("31/02/2026"))

    def test_data_formato_errado(self):
        self.assertFalse(validar_data("2026-10-08"))

    def test_registro_valido(self):
        self.assertIsNone(conferir_registro(self.registro))

    def test_excecao_personalizada(self):
        registro_errado = self.registro.copy()
        registro_errado["email"] = "sem-arroba"
        with self.assertRaises(FormatoInvalidoError):
            conferir_registro(registro_errado)

    def test_arquivo_inexistente(self):
        with tempfile.TemporaryDirectory() as pasta:
            with self.assertRaises(FileNotFoundError):
                analisar_arquivo(Path(pasta) / "arquivo_inexistente.csv")

    def test_coluna_ausente(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "sem_cpf.csv"
            caminho.write_text("nome,email,telefone,data\nAna,ana@exemplo.com,(98) 98765-4321,08/10/2026\n", encoding="utf-8")
            with self.assertRaises(KeyError):
                analisar_arquivo(caminho)

    def test_csv_vazio(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "vazio.csv"
            caminho.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                analisar_arquivo(caminho)

    def test_exemplo_e_relatorio(self):
        caminho = Path(__file__).resolve().parent / "dados.csv"
        registros = analisar_arquivo(caminho)
        self.assertEqual(len(registros), 8)
        self.assertEqual(sum(r["situacao"] == "VÁLIDO" for r in registros), 3)
        relatorio = montar_relatorio(registros)
        self.assertIn("Registros inválidos: 5", relatorio)
        self.assertIn("Percentual de válidos: 37.5%", relatorio)

    def test_linha_com_campo_faltando(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "incompleto.csv"
            with caminho.open("w", encoding="utf-8", newline="") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(["nome", "email", "cpf", "telefone", "data"])
                escritor.writerow(["Ana", "ana@exemplo.com", "123.456.789-09"])
            registros = analisar_arquivo(caminho)
            self.assertEqual(registros[0]["situacao"], "INVÁLIDO")


if __name__ == "__main__":
    unittest.main()
