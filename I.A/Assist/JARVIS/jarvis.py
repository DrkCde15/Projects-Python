import speech_recognition as sr
import pyttsx3
import datetime
import os
import platform
import webbrowser
import openai

# ========== CONFIGURAÇÕES ==========
openai.api_key = "SUA_CHAVE_API"
engine = pyttsx3.init()
voices = engine.getProperty('voices')
idioma = 'pt'  # padrão inicial

# ========== FUNÇÕES DE VOZ ==========
def configurar_voz():
    for voice in voices:
        if idioma == 'pt' and 'brazil' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return
        elif idioma == 'en' and 'english' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return

def falar(texto):
    configurar_voz()
    engine.say(texto)
    engine.runAndWait()

# ========== OUVIDOR ==========
def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escutando...")
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language='pt-BR' if idioma == 'pt' else 'en-US')
        print("Você disse:", comando)
        return comando.lower()
    except:
        return ""

# ========== GPT ==========
def responder_com_gpt(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente virtual simpático." if idioma == 'pt' else "You are a friendly virtual assistant."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Erro com API:", e)
        return "Desculpe, ocorreu um erro ao acessar o ChatGPT." if idioma == 'pt' else "Sorry, there was an error accessing ChatGPT."

# ========== COMANDOS ==========
def executar_comando(comando):
    global idioma

    if 'change to english' in comando or 'mudar para inglês' in comando:
        idioma = 'en'
        falar("Language changed to English.")
        return
    elif 'mudar para português' in comando or 'switch to portuguese' in comando:
        idioma = 'pt'
        falar("Idioma alterado para português.")
        return

    if 'hora' in comando or 'time' in comando:
        hora = datetime.datetime.now().strftime('%H:%M')
        falar(f"Agora são {hora}" if idioma == 'pt' else f"It's {hora}")
    elif 'data' in comando or 'date' in comando:
        data = datetime.datetime.now().strftime('%d/%m/%Y')
        falar(f"Hoje é {data}" if idioma == 'pt' else f"Today is {data}")
    elif 'abrir youtube' in comando or 'open youtube' in comando:
        webbrowser.open("https://youtube.com")
    elif 'abrir navegador' in comando or 'open browser' in comando:
        webbrowser.open("https://www.google.com")
    elif 'abrir vscode' in comando or 'open code' in comando:
        if platform.system() == 'Windows':
            os.system("start code")
        else:
            os.system("code")
    elif comando.startswith('pesquisar ') or comando.startswith('search for '):
        if idioma == 'pt':
            termo = comando.replace('pesquisar ', '')
            url = f"https://www.google.com/search?q={termo}"
            falar(f"Pesquisando por {termo}")
        else:
            termo = comando.replace('search for ', '')
            url = f"https://www.google.com/search?q={termo}"
            falar(f"Searching for {termo}")
        webbrowser.open(url)
    elif 'desligar' in comando or 'shutdown' in comando:
        if platform.system() == 'Windows':
            os.system("shutdown /s /t 5")
        else:
            os.system("shutdown now")
    elif 'sair' in comando or 'exit' in comando:
        falar("Até logo!" if idioma == 'pt' else "Goodbye!")
        exit()
    else:
        resposta = responder_com_gpt(comando)
        print("Assistente: {}".format(resposta))
        falar(resposta)

# ========== INÍCIO ==========
falar("Olá, diga um comando ou digite 1 para voz, 2 para texto." if idioma == 'pt' else "Hello, say a command or type 1 for voice, 2 for text.")

while True:
    print("\nEscolha a forma de interação:")
    print("1 - Falar (voz)")
    print("2 - Digitar (texto)")
    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == '1':
        comando = ouvir_comando()
        if comando:
            executar_comando(comando)
    elif escolha == '2':
        comando = input("You: ").lower()
        executar_comando(comando)
    else:
        falar("Opção inválida, tente novamente." if idioma == 'pt' else "Invalid option, try again.")
