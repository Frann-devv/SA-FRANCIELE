import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(BASE_DIR, "dados_alunos.json")

# Procura o index.html em 'interface' (ao lado do app.py ou um nível acima)
# ou em 'templates'. Usa a primeira pasta que realmente contém o index.html.
CANDIDATAS = [
    os.path.join(BASE_DIR, "interface"),
    os.path.abspath(os.path.join(BASE_DIR, "..", "interface")),
    os.path.join(BASE_DIR, "templates"),
]

TEMPLATE_DIR = next(
    (pasta for pasta in CANDIDATAS
     if os.path.exists(os.path.join(pasta, "index.html"))),
    CANDIDATAS[-1],
)

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "chave-secreta-portal-aluno"


# =========================================
# CLASSE ALUNO
# =========================================

class Aluno:
    def __init__(self, nome, senha, turma, notas, faltas, quadro_horarios):
        self.nome = nome
        self.senha = senha
        self.turma = turma
        self.notas = notas
        self.faltas = faltas
        self.quadro_horarios = quadro_horarios

    def calcular_media(self, materia):
        notas_materia = self.notas.get(materia, [])
        if not notas_materia:
            return None
        return sum(notas_materia) / len(notas_materia)

    def obter_faltas_materia(self, materia):
        return self.faltas.get(materia, 0)

    def calcular_total_faltas(self):
        return sum(self.faltas.values())

    def obter_materias(self):
        return list(dict.fromkeys(list(self.notas.keys()) + list(self.faltas.keys())))

    def to_dict(self):
        return {
            "nome": self.nome,
            "senha": self.senha,
            "turma": self.turma,
            "notas": self.notas,
            "faltas": self.faltas,
            "quadro_horarios": self.quadro_horarios,
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            nome=dados["nome"],
            senha=dados["senha"],
            turma=dados["turma"],
            notas=dados.get("notas", {}),
            faltas=dados.get("faltas", {}),
            quadro_horarios=dados.get("quadro_horarios", turmas.get(dados["turma"], {})),
        )


# =========================================
# DADOS BASE
# =========================================

materias_base = [
    "Matemática", "História", "L.Portuguesa", "L.E.Inglês",
    "ED.Física", "Biologia", "Artes", "L.E.Espanhol",
    "Filosofia", "Física", "Geografia", "Química", "Sociologia",
]

turmas = {
    "Turma A": {
        "Segunda-Feira": ["Matemática", "Sociologia", "Matemática", "Geografia", "História", "ED.Física"],
        "Terça-Feira": ["L.E.Espanhol", "Sociologia", "L.E.Inglês", "Filosofia", "L.E.Inglês", "Geografia"],
        "Quarta-Feira": ["Física", "Artes", "L.Portuguesa", "L.Portuguesa", "ED.Física", "Química"],
        "Quinta-Feira": ["Biologia", "Geografia", "L.Portuguesa", "História", "Matemática", "L.Portuguesa"],
        "Sexta-Feira": ["Química", "Matemática", "Física", "L.Portuguesa", "Biologia", "Biologia"],
    },
    "Turma B": {
        "Segunda-Feira": ["L.Portuguesa", "L.Portuguesa", "Física", "Química", "Artes", "Filosofia"],
        "Terça-Feira": ["Matemática", "Matemática", "Biologia", "História", "Geografia", "ED.Física"],
        "Quarta-Feira": ["L.E.Inglês", "Sociologia", "Matemática", "Química", "Biologia", "História"],
        "Quinta-Feira": ["Geografia", "Física", "L.E.Espanhol", "L.Portuguesa", "ED.Física", "Sociologia"],
        "Sexta-Feira": ["Filosofia", "Artes", "Matemática", "L.Portuguesa", "Física", "Geografia"],
    },
}

banco_alunos = {
    "ana": Aluno(
        nome="Ana Silva",
        senha="1234",
        turma="Turma A",
        notas={
            "Matemática": [8.5, 8.0, 0.0],
            "História": [9.0, 9.0, 10.0],
            "L.Portuguesa": [10.0, 8.0, 7.0],
            "L.E.Inglês": [6.0, 8.5, 7.0],
            "ED.Física": [7.0, 9.5, 8.0],
            "Biologia": [4.0, 10.0, 7.0],
            "Artes": [],
            "L.E.Espanhol": [9.5, 10.0, 7.0],
            "Filosofia": [9.5, 10.0, 7.5],
            "Física": [8.0, 6.0, 10.0],
            "Geografia": [10.0, 10.0, 10.0],
            "Química": [7.0, 8.5, 10.0],
            "Sociologia": [8.0, 6.0, 7.0],
        },
        faltas={
            "Matemática": 4, "História": 2, "L.Portuguesa": 1, "L.E.Inglês": 4,
            "ED.Física": 3, "Biologia": 2, "Artes": 0, "L.E.Espanhol": 1,
            "Filosofia": 0, "Física": 2, "Geografia": 3, "Química": 1, "Sociologia": 2,
        },
        quadro_horarios=turmas["Turma A"],
    )
}


# =========================================
# PERSISTÊNCIA EM JSON
# =========================================

def salvar_dados():
    dados = {login: aluno.to_dict() for login, aluno in banco_alunos.items()}
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        salvar_dados()
        return

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    banco_alunos.clear()
    for login, info in dados.items():
        banco_alunos[login] = Aluno.from_dict(info)


carregar_dados()


# =========================================
# ROTAS
# =========================================

def obter_aluno_logado():
    login = session.get("usuario")
    return banco_alunos.get(login) if login else None


@app.route("/", methods=["GET", "POST"])
def index():
    erro = None
    sucesso = None
    aba_ativa = "login"

    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "login":
            aba_ativa = "login"
            login_usuario = request.form.get("usuario", "").strip().lower()
            senha = request.form.get("senha", "").strip()
            aluno = banco_alunos.get(login_usuario)

            if aluno and aluno.senha == senha:
                session["usuario"] = login_usuario
                return redirect(url_for("index"))
            erro = "Usuário ou senha incorretos!"

        elif acao == "cadastro":
            aba_ativa = "cadastro"
            nome_completo = request.form.get("nome", "").strip()
            login = request.form.get("novo_usuario", "").strip().lower()
            senha = request.form.get("nova_senha", "").strip()
            turma_selecionada = request.form.get("turma", "")

            if not nome_completo:
                erro = "O nome não pode ficar em branco."
            elif not login or " " in login:
                erro = "Usuário inválido ou contém espaços."
            elif login in banco_alunos:
                erro = "Este usuário já está cadastrado!"
            elif not senha.isdigit():
                erro = "A senha deve conter apenas números."
            elif turma_selecionada not in turmas:
                erro = "Turma inválida."
            else:
                banco_alunos[login] = Aluno(
                    nome=nome_completo,
                    senha=senha,
                    turma=turma_selecionada,
                    notas={materia: [] for materia in materias_base},
                    faltas={materia: 0 for materia in materias_base},
                    quadro_horarios=turmas[turma_selecionada],
                )
                salvar_dados()
                sucesso = f"Aluno '{nome_completo}' cadastrado! Agora faça login com '{login}'."
                aba_ativa = "login"

    aluno = obter_aluno_logado()
    boletim = []
    total_faltas = 0

    if aluno:
        total_faltas = aluno.calcular_total_faltas()
        for materia in aluno.obter_materias():
            media = aluno.calcular_media(materia)
            faltas = aluno.obter_faltas_materia(materia)
            notas_lista = aluno.notas.get(materia, [])
            boletim.append({
                "materia": materia,
                "notas": notas_lista,
                "media_num": media,
                "media": f"{media:.2f}" if media is not None else "Sem notas",
                "faltas": faltas,
            })

    return render_template(
        "index.html",
        aluno=aluno,
        turmas=list(turmas.keys()),
        boletim=boletim,
        total_faltas=total_faltas,
        erro=erro,
        sucesso=sucesso,
        aba_ativa=aba_ativa,
    )


@app.route("/sair")
def sair():
    session.pop("usuario", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
