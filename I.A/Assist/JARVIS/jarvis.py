import tkinter as tk
from tkinter import scrolledtext
import openai
import pyttsx3
import webbrowser
import os
import json
import datetime
import re
import speech_recognition as sr
from dotenv import load_dotenv

# ========== CONFIGURAÇÃO ==========
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
idioma = 'pt'
COMANDOS_PATH = "comandos.json"

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def configurar_voz():
    for voice in voices:
        if idioma == 'pt' and 'brazil' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return

def falar(texto):
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

# ========== GPT ==========
def responder_com_gpt(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente simpático que ajuda com comandos e respostas úteis."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Erro ao acessar o ChatGPT."

# ========== PADRÕES DE COMANDO ==========
def abrir_site(site):
    urls = {
        'youtube': 'https://youtube.com',
        'netflix': 'https://netflix.com',
        'google': 'https://google.com',
    }
    if site in urls:
        webbrowser.open(urls[site])
        return f"Abrindo {site}."
    return "Site não reconhecido."

def falar_hora():
    hora = datetime.datetime.now().strftime('%H:%M')
    return f"Agora são {hora}."

def falar_data():
    data = datetime.datetime.now().strftime('%d/%m/%Y')
    return f"Hoje é {data}."

padroes = [
    (r'abrir\s+(youtube|netflix|google)', lambda m: abrir_site(m.group(1))),
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

    return responder_com_gpt(comando)

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
                falar("Encerrando.")
                break
            resposta = executar_comando(comando)
            falar(resposta)

def modo_continuo():
    falar("Modo contínuo ativado. Fale comigo.")
    while True:
        comando = ouvir_comando()
        if comando:
            if 'sair do modo contínuo' in comando:
                falar("Saindo do modo contínuo.")
                break
            resposta = executar_comando(comando)
            falar(resposta)

# ========== MODO TEXTO TERMINAL ==========
def modo_texto_terminal():
    print("Modo texto ativado. Digite 'sair' para encerrar.")
    while True:
        comando = input("Você: ").strip().lower()
        if comando in ['sair', 'exit']:
            print("Até logo!")
            break
        resposta = executar_comando(comando)
        print("Assistente:", resposta)
        falar(resposta)

# ========== MODO TKINTER ==========
class AssistenteApp:
    def __init__(self, root):
        self.root = root
        root.title("Assistente Virtual")
        root.geometry("600x500")
        root.resizable(False, False)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.configure(state='disabled')

        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry.pack(fill=tk.X, padx=10, pady=(0,10))
        self.entry.bind("<Return>", self.enviar)

        self.bot_falar = True
        self.mostrar_mensagem("Assistente", "Olá! Digite seu comando abaixo.")

    def mostrar_mensagem(self, remetente, mensagem):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"{remetente}: {mensagem}\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)
        if remetente == "Assistente" and self.bot_falar:
            falar(mensagem)

    def enviar(self, event):
        comando = self.entry.get().strip()
        if not comando:
            return
        self.mostrar_mensagem("Você", comando)
        resposta = executar_comando(comando)
        self.mostrar_mensagem("Assistente", resposta)
        self.entry.delete(0, tk.END)

# ========== MENU PRINCIPAL ==========
if __name__ == "__main__":
    print("\nEscolha a forma de interação:")
    print("1 - Modo por voz (fala um comando por vez)")
    print("2 - Modo contínuo (escuta sem parar)")
    print("3 - Modo texto (terminal)")
    print("4 - Modo gráfico (interface Tkinter)")

    escolha = input("Digite 1, 2, 3 ou 4: ").strip()

    if escolha == '1':
        modo_voz_manual()
    elif escolha == '2':
        modo_continuo()
    elif escolha == '3':
        modo_texto_terminal()
    elif escolha == '4':
        root = tk.Tk()
        app = AssistenteApp(root)
        root.mainloop()
    else:
        print("Opção inválida.")