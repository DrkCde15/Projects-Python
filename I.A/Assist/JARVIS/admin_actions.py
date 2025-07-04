import sys
import os
import getpass
from datetime import datetime

LOG_PATH = "logs_admin.txt"

# Função para registrar ações no log
def registrar_log(usuario, acao):
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{agora}] {usuario}: {acao}\n")

def menu(usuario):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"""
=== MODO ADMINISTRADOR JARVIS ===
Usuário autenticado: {usuario}

1 - Listar usuários do sistema
2 - Criar novo usuário
3 - Remover usuário
4 - Desligar o computador
5 - Reiniciar o computador
6 - Executar comando winget (instalar programa)
7 - Sair
""")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            registrar_log(usuario, "Listou usuários")
            os.system("net user")
        elif escolha == "2":
            nome = input("Nome do novo usuário: ").strip()
            senha = getpass.getpass("Senha para o novo usuário: ").strip()
            if nome and senha:
                comando = f'net user "{nome}" "{senha}" /add'
                resultado = os.system(comando)
                registrar_log(usuario, f"Tentou criar usuário '{nome}'")
                print("Usuário criado com sucesso." if resultado == 0 else "Erro ao criar usuário.")
            else:
                print("Nome ou senha inválidos.")
        elif escolha == "3":
            nome = input("Nome do usuário a remover: ").strip()
            if nome:
                comando = f'net user "{nome}" /delete'
                resultado = os.system(comando)
                registrar_log(usuario, f"Tentou remover usuário '{nome}'")
                print("Usuário removido com sucesso." if resultado == 0 else "Erro ao remover usuário.")
        elif escolha == "4":
            registrar_log(usuario, "Desligou o PC")
            print("Desligando o computador em 10 segundos...")
            os.system("shutdown /s /t 10")
        elif escolha == "5":
            registrar_log(usuario, "Reiniciou o PC")
            print("Reiniciando o computador em 10 segundos...")
            os.system("shutdown /r /t 10")
        elif escolha == "6":
            programa = input("Nome do programa para instalar via winget: ").strip()
            if programa:
                registrar_log(usuario, f"Instalando programa via winget: {programa}")
                comando = f'winget install --id={programa} -e --accept-package-agreements --accept-source-agreements'
                os.system(comando)
        elif escolha == "7":
            registrar_log(usuario, "Saiu do modo administrador")
            print("Saindo do modo administrador.")
            break
        else:
            print("Opção inválida.")

        input("\nPressione Enter para continuar...")

def main():
    if len(sys.argv) < 2:
        print("Usuário autenticado não informado.")
        return

    usuario = sys.argv[1]
    registrar_log(usuario, "Entrou no modo administrador")
    menu(usuario)

if __name__ == "__main__":
    main()
