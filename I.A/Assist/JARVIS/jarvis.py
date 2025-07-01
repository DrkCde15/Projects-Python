# J.A.R.V.I.S - Just A Rather Very Intelligent System

import google.generativeai as genai
import pyttsx3
import webbrowser
import os
import json
import datetime
import re
import speech_recognition as sr
import traceback
from dotenv import load_dotenv

# ========== CONFIGURAÇÃO ==========
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

idioma = 'pt'
COMANDOS_PATH = "comandos.json"

engine = pyttsx3.init()
voices = engine.getProperty('voices')

voz_ativa = True  # controla se a assistente fala

# ========== FUNÇÕES DE VOZ ==========
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

# ========== COMANDOS PERSONALIZADOS ==========
def carregar_comandos_personalizados():
    if os.path.exists(COMANDOS_PATH):
        with open(COMANDOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_comandos_personalizados(comandos):
    with open(COMANDOS_PATH, "w", encoding="utf-8") as f:
        json.dump(comandos, f, indent=4)

comandos_personalizados = carregar_comandos_personalizados()

# ========== GEMINI ==========
def responder_com_gemini(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        resposta = model.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        print(f"Erro Gemini: {e}")
        return "Erro ao acessar o Gemini."

# ========== PADRÕES DE COMANDO ==========
def abrir_site(site):
    urls = {
        'youtube': 'https://youtube.com',
        'netflix': 'https://netflix.com',
        'google': 'https://google.com',
        'microsoft teams': 'https://teams.microsoft.com'
    }
    if site in urls:
        try:
            os.system(f"start {urls[site]}")  # método alternativo
            return f"Abrindo {site}."
        except Exception as e:
            return f"Erro ao abrir {site}: {str(e)}"
    return "Site não reconhecido."

def falar_hora():
    hora = datetime.datetime.now().strftime('%H:%M')
    return f"Agora são {hora}."

def falar_data():
    data = datetime.datetime.now().strftime('%d/%m/%Y')
    return f"Hoje é {data}."

padroes = [
    (r'abrir\s+(youtube|netflix|google|microsoft teams)', lambda m: abrir_site(m.group(1))),
    (r'que horas|horas|hora atual', lambda m: falar_hora()),
    (r'data|que dia é hoje', lambda m: falar_data())
]

def processar_regex(comando):
    for padrao, acao in padroes:
        match = re.search(padrao, comando, re.IGNORECASE)
        if match:
            return acao(match)
    return None

# ========== EXECUTA COMANDO ==========
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
            salvar_comandos_personalizados(comandos_personalizados)
            return f"Comando '{nome}' cadastrado com sucesso."
        except:
            return "Formato inválido. Use: cadastrar comando NOME para LINK ou COMANDO."

    if comando in comandos_personalizados:
        destino = comandos_personalizados[comando]
        if destino.startswith("http"):
            webbrowser.open(destino)
        else:
            os.system(destino)
        return f"Executando {comando}."

    resposta_regex = processar_regex(comando)
    if resposta_regex:
        return resposta_regex

    return responder_com_gemini(comando)

# ========== MODO VOZ ==========
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
    falar("Modo voz ativado. Diga seu comando.")
    while True:
        comando = ouvir_comando()
        if comando:
            if comando in ['sair', 'exit']:
                falar("Até mais Senhor.")
                break
            resposta = executar_comando(comando)
            falar(resposta)

def modo_continuo():
    falar("Modo contínuo ativado. Fale comigo.")
    while True:
        comando = ouvir_comando()
        if comando:
            if 'sair do modo contínuo' in comando:
                falar("Saindo do modo contínuo, Até mais Senhor.")
                break
            resposta = executar_comando(comando)
            falar(resposta)

# ========== MODO TEXTO (JARVIS) ==========
def modo_texto_terminal():
    print("Modo texto ativado. Digite 'x' ou 'exit' para encerrar.\n")

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
            resposta = responder_com_gemini(prompt)
            mensagens.append(f"JARVIS: {resposta}")
            print(f"\nJARVIS: {resposta}\n")
    except KeyboardInterrupt:
        print("\nInterrupção detectada. Até mais Senhor.")
    except Exception:
        print("Erro inesperado:")
        traceback.print_exc()

# ========== MENU PRINCIPAL ==========
if __name__ == "__main__":
    print("\nEscolha a forma de interação:")
    print("1 - Modo por voz (fala um comando por vez)")
    print("2 - Modo contínuo (escuta sem parar)")
    print("3 - Modo texto (JARVIS)")

    escolha = input("Digite 1, 2 ou 3: ").strip()

    if escolha == '1':
        voz_ativa = True
        modo_voz_manual()
    elif escolha == '2':
        voz_ativa = True
        modo_continuo()
    elif escolha == '3':
        voz_ativa = False
        modo_texto_terminal()
    else:
        print("Opção inválida.")
