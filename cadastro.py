import json
import os
import time
import hashlib

from collections import Counter
# ---------------- Criptografar --------------- 
def criptografar(valor):
    return hashlib.sha256(valor.encode()).hexdigest()

# -------------------- DADOS --------------------
ARQUIVO = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO, "w") as f:
        json.dump(usuarios, f, indent=4)

# -------------------- CADASTRO --------------------
def cadastrar_usuario():
    usuarios = carregar_usuarios()
    nome_original = input("Nome: ").strip().lower()
    senha = input("Senha: ")
    idade = int(input("Idade: "))
    print("Gênero: \n1-Masculino \n2-Feminino \n3-Outros")
    genero_opcao = input("Escolha: ")
    genero = {"1": "Masculino", "2": "Feminino"}.get(genero_opcao, "Outros")

    nome_hash = criptografar(nome_original)
    senha_hash = criptografar(senha)

    # Verifica se nome já existe
    for user in usuarios:
        if user.get("nome") == nome_hash:
            print("Usuário já existe!")
            return

    usuario = {
        "nome": nome_hash,
        "senha": senha_hash,
        "idade": idade,
        "genero": genero,
        "tempo_de_uso": 0,
        "tempos_quiz": []
    }
    usuarios.append(usuario)
    salvar_usuarios(usuarios)
    print("Cadastro feito!")


# -------------------- LOGIN --------------------
def login():
    usuarios = carregar_usuarios()
    nome = input("Nome: ").lower()
    senha = input("Senha: ")
    nome_hash = criptografar(nome)
    senha_hash = criptografar(senha)

    for user in usuarios:
        if user.get("nome") == nome_hash and user.get("senha") == senha_hash:
            print(f"Bem-vindo!")
            return nome_hash
    print("Nome ou senha errados.")
    return None


# -------------------- QUIZ --------------------
def fazer_quiz(nome_usuario):
    perguntas_por_nivel = {
        "facil": [
            {
                "pergunta": "Qual comando usamos para exibir algo na tela em Python?",
                "alternativas": ["a) print", "b) display", "c) show", "d) log"],
                "resposta": "a"
            },
            {
                "pergunta": "Qual símbolo usamos para comentar uma linha em Python?",
                "alternativas": ["a) //", "b) #", "c) --", "d) !"],
                "resposta": "b"
            },
            {
                "pergunta": "Como declaramos uma variável que recebe o valor 10 em Python?",
                "alternativas": ["a) x := 10", "b) x = 10", "c) let x = 10", "d) const x = 10"],
                "resposta": "b"
            },
        ],
        "intermediario": [
            {
                "pergunta": "Como criamos uma função chamada 'soma' que recebe dois parâmetros em Python?",
                "alternativas": ["a) function soma(a, b)", "b) def soma(a, b):", "c) soma = def (a, b)", "d) soma(a, b) =>"],
                "resposta": "b"
            },
            {
                "pergunta": "Qual estrutura de repetição usamos para percorrer uma lista em Python?",
                "alternativas": ["a) while", "b) for", "c) if", "d) loop"],
                "resposta": "b"
            },
            {
                "pergunta": "Como tratamos exceções em Python?",
                "alternativas": ["a) try/catch", "b) if/else", "c) try/except", "d) handle/except"],
                "resposta": "c"
            },
        ],
        "avancado": [
            {
                "pergunta": "O que significa o conceito de 'herança' em programação orientada a objetos?",
                "alternativas": ["a) criar novas classes", "b) herdar atributos e métodos", "c) instanciar objetos", "d) encapsular dados"],
                "resposta": "b"
            },
            {
                "pergunta": "Explique o que é uma 'lambda function' em Python.",
                "alternativas": ["a) função recursiva", "b) função anônima", "c) função decorada", "d) função geradora"],
                "resposta": "b"
            },
            {
                "pergunta": "Qual a diferença entre 'list comprehension' e um loop tradicional para criar listas em Python?",
                "alternativas": ["a) não há diferença", "b) list comprehension é mais lento", "c) list comprehension é mais concisa", "d) loop tradicional é mais legível"],
                "resposta": "c"
            },
        ]
    }
    print("Escolha o nível do quiz: 1-Fácil 2-Intermediário 3-Avançado")
    nivel_opcao = input("Nível: ")
    if nivel_opcao == "1":
        perguntas = perguntas_por_nivel["facil"]
    elif nivel_opcao == "2":
        perguntas = perguntas_por_nivel["intermediario"]
    else:
        perguntas = perguntas_por_nivel["avancado"]

    acertos = 0
    inicio = time.time()
    for pergunta in perguntas:
        print(pergunta["pergunta"])
        for alternativa in pergunta["alternativas"]:
            print(alternativa)
        resposta_usuario = input("Escolha a alternativa (a, b, c, d): ").lower()
        if resposta_usuario == pergunta["resposta"]:
            acertos += 1
    fim = time.time()
    tempo = (fim - inicio) / 60
    print(f"Acertos: {acertos}")
    print(f"Tempo quiz: {tempo:.2f} min")
    usuarios = carregar_usuarios()
    for user in usuarios:
        if user.get("nome") == nome_usuario:
            user.setdefault("tempos_quiz", [])
            user["tempos_quiz"].append(tempo)
            user["tempo_de_uso"] = user.get("tempo_de_uso", 0) + 1
            break


    salvar_usuarios(usuarios)

# -------------------- MENU --------------------
def menu_usuario(nome):
    while True:
        print("\n1. Fazer quiz\n2. Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            fazer_quiz(nome)
        elif opcao == "2":
            break

def main():
    while True:
        print("\n1. Cadastrar\n2. Login\n3. Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario = login()
            if usuario:
                menu_usuario(usuario)
        elif opcao == "3":
            break

main()
