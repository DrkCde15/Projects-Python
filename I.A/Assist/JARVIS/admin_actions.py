import sys
import os
import getpass
from datetime import datetime

LOG_PATH = ".arq/logs_admin.txt"

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
6 - Instalar via winget
7 - Sair
8 - Alterar senha de um usuário
9 - Instalar via Chocolatey (choco)
10 - Adicionar chave ao Registro (reg add)
11 - Alterar configurações do sistema
12 - Rodar scanner de portas (nmap)
13 - Rodar antivírus (Windows Defender)
14 - Atualizar o Windows
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
                os.system(comando)
                registrar_log(usuario, f"Criou usuário '{nome}'")
        elif escolha == "3":
            nome = input("Usuário a remover: ").strip()
            os.system(f'net user "{nome}" /delete')
            registrar_log(usuario, f"Removeu usuário '{nome}'")
        elif escolha == "4":
            registrar_log(usuario, "Desligou o PC")
            os.system("shutdown /s /t 10")
        elif escolha == "5":
            registrar_log(usuario, "Reiniciou o PC")
            os.system("shutdown /r /t 10")
        elif escolha == "6":
            programa = input("Nome do pacote (winget): ").strip()
            os.system(f'winget install --id={programa} -e --accept-package-agreements --accept-source-agreements')
            registrar_log(usuario, f"Instalou via winget: {programa}")
        elif escolha == "7":
            registrar_log(usuario, "Saiu do modo admin")
            break
        elif escolha == "8":
            nome = input("Usuário: ").strip()
            nova_senha = getpass.getpass("Nova senha: ").strip()
            os.system(f'net user "{nome}" "{nova_senha}"')
            registrar_log(usuario, f"Alterou senha de '{nome}'")
        elif escolha == "9":
            pacote = input("Pacote (choco): ").strip()
            os.system(f'choco install {pacote} -y')
            registrar_log(usuario, f"Instalou via choco: {pacote}")
        elif escolha == "10":
            chave = input("Caminho da chave (ex: HKCU\\Software\\Test): ")
            nome = input("Nome do valor: ")
            tipo = input("Tipo (REG_SZ, REG_DWORD, etc): ")
            dado = input("Valor: ")
            os.system(f'reg add "{chave}" /v "{nome}" /t {tipo} /d "{dado}" /f')
            registrar_log(usuario, f"Adicionou chave no registro: {chave} -> {nome}")
        elif escolha == "11":
            comando = input("Comando PowerShell para alteração: ")
            os.system(f'powershell -Command "{comando}"')
            registrar_log(usuario, f"Rodou PowerShell: {comando}")
        elif escolha == "12":
            ip = input("IP ou host para escanear: ")
            os.system(f'nmap -A {ip}')
            registrar_log(usuario, f"Rodou nmap em {ip}")
        elif escolha == "13":
            print("Iniciando verficação completa com Windows Defender...")
            os.system("powershell -Command \"Start-MpScan -ScanType Full\"")
            registrar_log(usuario, "Rodou antivírus")
        elif escolha == "14":
            print("Verificando atualizações do Windows...")
            os.system("powershell -Command \"Install-WindowsUpdate -AcceptAll -AutoReboot\"")
            registrar_log(usuario, "Rodou atualizações do Windows")
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
