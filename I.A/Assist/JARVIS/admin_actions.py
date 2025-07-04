import sys
import os
import getpass
from datetime import datetime

LOG_PATH = ".arq/logs_admin.txt"

def registrar_log(usuario, acao):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{agora}] {usuario}: {acao}\n")

def menu(usuario):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"""
=== MODO ADMINISTRADOR JARVIS ===
Usuário autenticado: {usuario}

1  - Listar usuários do sistema
2  - Abrir aplicativo
3  - Criar novo usuário
4  - Remover usuário
5  - Desligar o computador
6  - Reiniciar o computador
7  - Instalar via winget
8  - Instalar via Chocolatey (choco)
9  - Alterar senha de um usuário
10 - Adicionar chave ao Registro (reg add)
11 - Alterar configurações do sistema
12 - Rodar scanner de portas (nmap)
13 - Rodar antivírus (Windows Defender)
14 - Atualizar o Windows
15 - Sair
""")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            registrar_log(usuario, "Listou usuários")
            os.system("net user")

        elif escolha == "2":
            app = input("Nome do aplicativo (ex: notepad, code, chrome): ").strip()
            if app:
                comando = f'start {app}' if os.name == 'nt' else app
                registrar_log(usuario, f"Abriu aplicativo: {app}")
                os.system(comando)
            else:
                print("⚠️ Nome do aplicativo vazio.")

        elif escolha == "3":
            nome = input("Nome do novo usuário: ").strip()
            senha = getpass.getpass("Senha para o novo usuário: ").strip()
            if nome and senha:
                os.system(f'net user "{nome}" "{senha}" /add')
                registrar_log(usuario, f"Criou usuário '{nome}'")

        elif escolha == "4":
            nome = input("Usuário a remover: ").strip()
            os.system(f'net user "{nome}" /delete')
            registrar_log(usuario, f"Removeu usuário '{nome}'")

        elif escolha == "5":
            registrar_log(usuario, "Desligou o PC")
            os.system("shutdown /s /t 10")

        elif escolha == "6":
            registrar_log(usuario, "Reiniciou o PC")
            os.system("shutdown /r /t 10")

        elif escolha == "7":
            programa = input("Nome do pacote (winget): ").strip()
            if programa:
                os.system(f'winget install --id={programa} -e --accept-package-agreements --accept-source-agreements')
                registrar_log(usuario, f"Instalou via winget: {programa}")

        elif escolha == "8":
            pacote = input("Pacote (choco): ").strip()
            if pacote:
                os.system(f'choco install {pacote} -y')
                registrar_log(usuario, f"Instalou via choco: {pacote}")

        elif escolha == "9":
            nome = input("Usuário: ").strip()
            nova_senha = getpass.getpass("Nova senha: ").strip()
            os.system(f'net user "{nome}" "{nova_senha}"')
            registrar_log(usuario, f"Alterou senha de '{nome}'")

        elif escolha == "10":
            chave = input("Caminho da chave (ex: HKCU\\Software\\Test): ").strip()
            nome = input("Nome do valor: ").strip()
            tipo = input("Tipo (REG_SZ, REG_DWORD, etc): ").strip()
            dado = input("Valor: ").strip()
            os.system(f'reg add "{chave}" /v "{nome}" /t {tipo} /d "{dado}" /f')
            registrar_log(usuario, f"Adicionou chave no registro: {chave} -> {nome}={dado}")

        elif escolha == "11":
            comando = input("Comando PowerShell: ").strip()
            os.system(f'powershell -Command "{comando}"')
            registrar_log(usuario, f"Rodou PowerShell: {comando}")

        elif escolha == "12":
            ip = input("IP ou host para escanear: ").strip()
            if ip:
                os.system(f'nmap -A -T5 {ip}')
                registrar_log(usuario, f"Rodou nmap em {ip}")
            else:
                print("⚠️ IP ou host não pode estar vazio.")

        elif escolha == "13":
            print("Iniciando verificação completa com Windows Defender...")
            os.system("powershell -Command \"Start-MpScan -ScanType Full\"")
            registrar_log(usuario, "Rodou antivírus")

        elif escolha == "14":
            print("Verificando atualizações do Windows...")
            os.system("powershell -Command \"Install-WindowsUpdate -AcceptAll -AutoReboot\"")
            registrar_log(usuario, "Rodou atualizações do Windows")

        elif escolha == "15":
            registrar_log(usuario, "Saiu do modo admin")
            break

        else:
            print("⚠️ Opção inválida.")

        input("\nPressione Enter para continuar...")

def main():
    if len(sys.argv) < 2:
        print("❌ Usuário autenticado não informado.\nUse: python admin.py <nome_do_usuario>")
        return

    usuario = sys.argv[1]
    registrar_log(usuario, "Entrou no modo administrador")
    menu(usuario)

if __name__ == "__main__":
    main()