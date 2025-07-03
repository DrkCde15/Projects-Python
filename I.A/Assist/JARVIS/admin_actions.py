import sys
import os
import getpass
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

CHAVE_SECRETA = os.getenv("ADMIN_KEY")

def checar_chave(chave):
    return chave == CHAVE_SECRETA

def menu():
    print("""
=== MODO ADMINISTRADOR JARVIS ===
1 - Listar usuários do sistema
2 - Criar novo usuário
3 - Remover usuário
4 - Desligar o computador
5 - Reiniciar o computador
6 - Executar comando winget (instalar programa)
7 - Sair
""")

def listar_usuarios():
    print("\nUsuários cadastrados no sistema:")
    os.system("net user")
    input("\nPressione Enter para continuar...")

def criar_usuario():
    nome = input("Nome do novo usuário: ").strip()
    senha = getpass.getpass("Senha para o usuário: ").strip()
    if not nome or not senha:
        print("Nome ou senha inválidos.")
        return
    comando = f'net user "{nome}" "{senha}" /add'
    resultado = os.system(comando)
    if resultado == 0:
        print(f"Usuário '{nome}' criado com sucesso.")
    else:
        print("Falha ao criar usuário.")
    input("\nPressione Enter para continuar...")

def remover_usuario():
    nome = input("Nome do usuário a remover: ").strip()
    if not nome:
        print("Nome inválido.")
        return
    comando = f'net user "{nome}" /delete'
    resultado = os.system(comando)
    if resultado == 0:
        print(f"Usuário '{nome}' removido com sucesso.")
    else:
        print("Falha ao remover usuário.")
    input("\nPressione Enter para continuar...")

def desligar_pc():
    print("Desligando o computador em 10 segundos... Pressione Ctrl+C para cancelar.")
    os.system("shutdown /s /t 10")

def reiniciar_pc():
    print("Reiniciando o computador em 10 segundos... Pressione Ctrl+C para cancelar.")
    os.system("shutdown /r /t 10")

def instalar_winget():
    programa = input("Nome do programa para instalar via winget: ").strip()
    if not programa:
        print("Programa inválido.")
        return
    comando = f'winget install --id={programa} -e --accept-package-agreements --accept-source-agreements'
    print(f"Executando: {comando}")
    os.system(comando)
    input("\nPressione Enter para continuar...")

def main():
    if len(sys.argv) < 2:
        print("Chave secreta não fornecida. Encerrando.")
        return

    chave = sys.argv[1]
    if not checar_chave(chave):
        print("Chave incorreta. Acesso negado.")
        return

    while True:
        menu()
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            listar_usuarios()
        elif escolha == "2":
            criar_usuario()
        elif escolha == "3":
            remover_usuario()
        elif escolha == "4":
            desligar_pc()
        elif escolha == "5":
            reiniciar_pc()
        elif escolha == "6":
            instalar_winget()
        elif escolha == "7":
            print("Saindo do modo administrador.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()