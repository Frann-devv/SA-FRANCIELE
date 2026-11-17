import os
import time


class Aluno:
    def __init__(self, nome, notas, faltas):
        self.nome = nome
        self.notas = notas
        self.faltas = faltas

    def calcular_media(self, materia):
        notas_materia = self.notas.get(materia, [])
        if not notas_materia:
            return 0.0
        return sum(notas_materia) / len(notas_materia)

    def obter_faltas_materia(self, materia):
        return self.faltas.get(materia, 0)

    def calcular_total_faltas(self):
        return sum(self.faltas.values())

    def obter_materias(self):
        return list(dict.fromkeys(list(self.notas.keys()) + list(self.faltas.keys())))
        # Keys -> serve para extrair apenas os nomes (chaves) de um dicionário, ignorando os valores guardados dentro deles.


class PortalAluno:
    SENHA_PADRAO = "1234"

    def __init__(self, aluno, quadro_horarios):
        self.aluno = aluno
        self.quadro_horarios = quadro_horarios

    def pausar(self, mensagem="\nPressione ENTER para voltar..."):
        input(mensagem)

    def selecionar_materia(self, titulo_menu):
        lista_materias = self.aluno.obter_materias()
        while True:
            os.system("cls")
            print(f"| {titulo_menu} |")
            for i, materia in enumerate(lista_materias, start=1):
                print(f"{i} - {materia}")
            print("0 - Voltar ao Menu Principal")
            try:
                opcao = int(input("\nDigite a opção que deseja: "))
            except ValueError:
                print("Por favor, digite uma opção válida!")
                time.sleep(1.3)
                continue
            if opcao == 0:
                return None
            elif 1 <= opcao <= len(lista_materias):
                return lista_materias[opcao - 1]
            else:
                print("Opção inexistente!")
                time.sleep(1.3)

    def mostrar_nota_especifica(self, nome_materia):
        os.system("cls")
        notas = self.aluno.notas.get(nome_materia, [])
        media = self.aluno.calcular_media(nome_materia)
        print(f"Notas de {nome_materia.upper()}")
        print(f"Notas: {notas if notas else 'Nenhuma nota lançada'}")
        print(f"Média final: {media:.2f}")
        self.pausar("\nPressione ENTER para voltar às matérias...")

    def menu_notas(self):
        while True:
            materia_escolhida = self.selecionar_materia("Notas por Matéria")
            if materia_escolhida is None:
                break
            self.mostrar_nota_especifica(materia_escolhida)

    def mostrar_falta_especifica(self, nome_materia):
        os.system("cls")
        qtd_faltas = self.aluno.obter_faltas_materia(nome_materia)
        total_geral = self.aluno.calcular_total_faltas()

        print(f"Faltas em {nome_materia.upper()}")
        print(f"Faltas nesta matéria: {qtd_faltas}")
        print(f"Total de faltas no bimestre (todas as matérias): {total_geral}")
        self.pausar("\nPressione ENTER para voltar às matérias...")

    def menu_faltas(self):
        while True:
            materia_escolhida = self.selecionar_materia("Faltas por Matéria")
            if materia_escolhida is None:
                break
            self.mostrar_falta_especifica(materia_escolhida)

    def exibir_horario(self):
        os.system("cls")  # Corrigido: faltava o argumento "cls"
        print("Quadro de Horários\n")
        for dia, aulas in self.quadro_horarios.items():
            print(f"{dia}:")
            for idx, aula in enumerate(aulas, start=1):
                print(f"  {idx}º - {aula}")
            print()
        self.pausar()

    def exibir_media_geral(self):
        os.system("cls")
        print("Média Final e Faltas por Matéria\n")
        for materia in self.aluno.obter_materias():
            media = self.aluno.calcular_media(materia)
            faltas = self.aluno.obter_faltas_materia(materia)
            print(f"{materia:<15} | Média: {media:.2f} | Faltas: {faltas}")
        print(f"\nTotal de faltas: {self.aluno.calcular_total_faltas()}")
        self.pausar()

    def menu_principal(self):
        while True:
            os.system("cls")
            print(f"| 𝕄𝕖𝕟𝕦 ℙ𝕣𝕚𝕟𝕔𝕚𝕡𝕒𝕝 | \n |ᵇᵉᵐ ᵛⁱⁿᵈᵒ⁽ᵃ⁾, {self.aluno.nome} |")
            time.sleep(2)
            print("1 - Ver Notas")
            time.sleep(1)
            print("2 - Ver Faltas")
            time.sleep(1)
            print("3 - Quadro de Horários")
            time.sleep(1)
            print("4 - Boletim Geral (Médias e Faltas)")
            time.sleep(1)
            print("0 - Sair")
            time.sleep(0.5)
            try:
                opcao = int(input("\nDigite a opção que deseja: "))
            except ValueError:
                print("Por favor, digite apenas números!")
                time.sleep(1.3)
                continue
            if opcao == 1:
                self.menu_notas()
            elif opcao == 2:
                self.menu_faltas()
            elif opcao == 3:
                self.exibir_horario()
            elif opcao == 4:
                self.exibir_media_geral()
            elif opcao == 0:
                print("Encerrando o portal...")
                time.sleep(1)
                break
            else:
                print("Opção inválida!")
                time.sleep(1.3)

    def iniciar(self):
        while True:
            os.system("cls")
            print("_____________________________")
            print("|  Ｐｏｒｔａｌ Ａｌｕｎｏ   |")
            print("_____________________________")
            nome_usuario = input("Digite seu nome: ").strip()
            if not nome_usuario:
                print("Campo Obrigatório")
                time.sleep(1.2)
                continue
            senha = input("Digite sua senha: ").strip()
            if not senha.isdigit():
                print("A senha deve conter apenas números!")
                time.sleep(1.2)
                continue
            if senha == self.SENHA_PADRAO:
                self.aluno.nome = nome_usuario
                print("Acesso Liberado.")
                time.sleep(1.3)
                self.menu_principal()
                break
            else:
                print("Senha incorreta!")
                time.sleep(1.5)


if __name__ == "__main__":
    notas = {
        "Matemática": [8.5, 8.0, 0.0],
        "História": [9.0, 9.0, 10.0],
        "L.Portuguesa": [10.0, 8.0, 7.0],
        "L.E.Inglês": [6.0, 8.5, 7.0],
        "ED.Física": [7.0, 9.5, 8.0],
        "Biologia": [4.0, 10.0, 7.0],
        "Artes": [10.0, 9.0, 8.0],
        "L.E.Espanhol": [9.5, 10.0, 7.0],
        "Filosofia": [9.5, 10.0, 7.5],
        "Física": [8.0, 6.0, 10.0],
        "Geografia": [10.0, 10.0, 10.0],
        "Química": [7.0, 8.5, 10.0],
        "Sociologia": [8.0, 6.0, 7.0],
    }
    faltas = {
        "Matemática": 4,
        "História": 2,
        "L.Portuguesa": 1,
        "L.E.Inglês": 4,
        "ED.Física": 3,
        "Biologia": 2,
        "Artes": 0,
        "L.E.Espanhol": 1,
        "Filosofia": 0,
        "Física": 2,
        "Geografia": 3,
        "Química": 1,
        "Sociologia": 2,
    }
    horarios_turma = {
        "Segunda-Feira": ["Matemática", "Sociologia", "Matemática", "Geografia", "História", "ED.Física"],
        "Terça-Feira": ["L.E.Espanhol", "Sociologia", "L.E.Inglês", "Filosofia", "L.E.Inglês", "Geografia"],
        "Quarta-Feira": ["Física", "Artes", "L.Portuguesa", "L.Portuguesa", "ED.Física", "Química"],
        "Quinta-Feira": ["Biologia", "Geografia", "L.Portuguesa", "História", "Matemática", "L.Portuguesa"],
        "Sexta-Feira": ["Química", "Matemática", "Física", "L.Portuguesa", "Biologia", "Biologia"],
    }
    aluno_atual = Aluno(nome="", notas=notas, faltas=faltas)
    portal = PortalAluno(aluno=aluno_atual, quadro_horarios=horarios_turma)
    portal.iniciar()