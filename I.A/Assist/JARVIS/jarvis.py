import google.generativeai as genai
import pyttsx3
import webbrowser
import os
import json
import datetime
import re
import speech_recognition as sr
import traceback
import urllib.parse
import getpass
from dotenv import load_dotenv

# ======== CONFIGURAÇÃO ========
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
ADMIN_KEY = os.getenv("ADMIN_KEY")

idioma = 'pt'
voz_ativa = True
COMANDOS_PATH = "sites.json"
APLICATIVOS_PATH = "aplicativos.json"

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# ======== VOZ ========
def configurar_voz():
    for voice in voices:
        if idioma == 'pt' and 'brazil' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return

def falar(texto):
    if not voz_ativa:
        return
    configurar_voz()
    engine.say(texto)
    engine.runAndWait()

# ======== JSON ========
def carregar_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_json(path, dados):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

comandos_personalizados = carregar_json(COMANDOS_PATH)
aplicativos = carregar_json(APLICATIVOS_PATH)

# ======== GEMINI ========
def responder_com_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return "Erro ao acessar o Gemini."

# ======== SITES/APPS/UTIL ========
urls = {
    'youtube': 'https://youtube.com',
    'netflix': 'https://www.netflix.com/browse',
    'microsoft teams': 'https://teams.microsoft.com/v2/',
    'github': 'https://github.com/DrkCde15',
    'instagram': 'https://www.instagram.com/jc_v05/',
    'whatsapp': 'https://web.whatsapp.com/',
    'tik tok': 'https://www.tiktok.com/@bx_329'
}

def abrir_site(site):
    if site in urls:
        try:
            webbrowser.open(urls[site])
            return f"Abrindo {site}."
        except Exception as e:
            return f"Erro ao abrir {site}: {str(e)}"
    return "Site não reconhecido."

def listar_sites():
    return "Sites disponíveis: " + ", ".join(sorted(urls.keys())) if urls else "Nenhum site mapeado."

def abrir_aplicativo(nome):
    nome = nome.lower().strip().split()[0]
    if nome in aplicativos:
        try:
            os.system(aplicativos[nome])
            return f"Abrindo {nome}..."
        except Exception as e:
            return f"Erro ao abrir {nome}: {str(e)}"
    return f"Aplicativo '{nome}' não está mapeado."

def falar_hora():
    return f"Agora são {datetime.datetime.now().strftime('%H:%M')}."

def falar_data():
    return f"Hoje é {datetime.datetime.now().strftime('%d/%m/%Y')}."

def listar_aplicativos():
    return "Aplicativos disponíveis: " + ", ".join(sorted(aplicativos.keys())) if aplicativos else "Nenhum aplicativo mapeado."

def pesquisar_google(termo):
    url = f"https://www.google.com/search?q={urllib.parse.quote_plus(termo)}"
    webbrowser.open(url)
    return f"Pesquisando '{termo}' no Google."

# ======== PADRÕES REGEX ========
padroes = [
    (r'\b(iniciar|abrir|executar)\s+(youtube|netflix|microsoft teams|github|instagram|whatsapp|tik tok)', lambda m: abrir_site(m.group(2))),
    (r'\b(executar|abrir|iniciar)\s+([a-zA-Z0-9_ ]+)', lambda m: abrir_aplicativo(m.group(2))),
    (r'\b(que horas|horas|hora atual|me diga as horas)\b', lambda m: falar_hora()),
    (r'\b(data|que dia é hoje|me diga a data|qual a data)\b', lambda m: falar_data()),
    (r'\b(listar)\s+(aplicativos|apps)\b', lambda m: listar_aplicativos()),
    (r'\b(listar)\s+(site|sites)\b', lambda m: listar_sites()),
    (r'pesquisar por(.+)', lambda m: pesquisar_google(m.group(1).strip()))
]

def processar_regex(comando):
    for padrao, acao in padroes:
        match = re.search(padrao, comando, re.IGNORECASE)
        if match:
            return acao(match)
    return None

# ======== EXECUÇÃO PRINCIPAL ========
def executar_comando(comando):
    comando = comando.lower().strip()

    if comando in ['sair', 'exit']:
        return "Encerrando."

    if 'mudar para inglês' in comando:
        global idioma
        idioma = 'en'
        return "Idioma alterado para inglês."

    if comando.startswith("cadastrar comando"):
        try:
            partes = comando.replace("cadastrar comando", "").strip().split(" para ")
            nome, acao = partes[0].strip(), partes[1].strip()
            comandos_personalizados[nome] = acao
            salvar_json(COMANDOS_PATH, comandos_personalizados)
            return f"Comando '{nome}' cadastrado com sucesso."
        except:
            return "Formato inválido. Use: cadastrar comando NOME para LINK ou COMANDO."

    if comando in comandos_personalizados:
        destino = comandos_personalizados[comando]
        try:
            if destino.startswith("http"):
                webbrowser.open(destino)
            elif destino.endswith("()") or destino.startswith("abrir_aplicativo"):
                return eval(destino)
            else:
                os.system(destino)
            return f"Executando {comando}."
        except Exception as e:
            return f"Erro ao executar comando: {str(e)}"

    # ===== MODO ADMINISTRADOR =====
    if comando == "modo administrador":
        falar("Modo administrador solicitado. Por favor, digite a chave secreta no terminal.")
        chave = getpass.getpass("Digite a chave secreta: ").strip()
        if not chave:
            return "Chave não fornecida. Acesso negado."
        try:
            caminho_admin = os.path.abspath("admin_actions.py")
            os.system(f'start python "{caminho_admin}" {chave}')
            return "Verificando chave e ativando modo administrador..."
        except Exception as e:
            return f"Erro ao tentar ativar modo administrador: {e}"

    # ===== REGEX PADRÕES =====
    resposta_regex = processar_regex(comando)
    if resposta_regex:
        return resposta_regex

    # ===== FALLBACK: Gemini =====
    return responder_com_gemini(comando)

# ======== MODO VOZ ========
def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Escutando...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
    try:
        comando = r.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except:
        return ""

def modo_voz_manual():
    falar("Olá Senhor, Sou seu assistente de voz JARVIS, por favor me diga um comando.")
    while True:
        comando = ouvir_comando()
        if comando:
            if comando in ['sair', 'exit']:
                falar("Até mais Senhor.")
                break
            resposta = executar_comando(comando)
            falar(resposta)

# ======== MODO TEXTO ========
def modo_texto_terminal():
    print("Ola Senhor, Sou seu assistente JARVIS. Digite 'x' ou 'exit' para encerrar.\n")
    mensagens = [
        "Você é o JARVIS, um assistente profissional que vai diretamente ao ponto, muito inteligente, frio e sempre chama o usuário de Senhor."
    ]

    try:
        while True:
            pergunta = input("Usuário: ").strip()
            if pergunta.lower() in ['x', 'exit']:
                print("Até mais Senhor!")
                break

            mensagens.append(f"Senhor: {pergunta}")
            prompt = '\n'.join(mensagens)
            resposta = executar_comando(pergunta)
            mensagens.append(f"JARVIS: {resposta}")
            print(f"\nJARVIS: {resposta}\n")
    except KeyboardInterrupt:
        print("\nInterrupção detectada. Até mais Senhor.")
    except Exception:
        print("Erro inesperado:")
        traceback.print_exc()

# ======== MENU INICIAL ========
if __name__ == "__main__":
    print("\nEscolha a forma de interação:")
    print("1 - Modo por voz (fala um comando por vez)")
    print("2 - Modo texto (JARVIS)")

    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == '1':
        voz_ativa = True
        modo_voz_manual()
    elif escolha == '2':
        voz_ativa = False
        modo_texto_terminal()
    else:
        print("Opção inválida.")