# NUTRI.AI – Sistema de Nutrição com I.A. Integrada

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
import traceback

# ======== API KEY ========
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY não definida no .env")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ======== INICIALIZAÇÃO =========
try:
    chat = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.7) #gemini-1.5-flash com temperatura 0.7 para uma resposta mais objetiva e rapida
    print("NutriAI inicializada com sucesso!")
except Exception:
    print("Erro ao inicializar a IA nutricional:")
    traceback.print_exc()
    exit()

# ======== TEMPLATE DE PROMPT =========
def resposta_nutricional(mensagens):
    template = ChatPromptTemplate.from_messages([
        SystemMessage(content='''
            Você é uma nutricionista virtual altamente especializada em nutrição esportiva e dietas personalizadas.
            Forneça planos alimentares, sugestões de refeições, dicas para emagrecimento, ganho de massa magra, energia e performance.
            Sempre considere os objetivos, alergias, preferências e rotina do usuário. Seja clara, objetiva, motivadora e sempre vá direto ao ponto sem enrolação.
            E voce respondera somente perguntas sobre nutrição, treinos, e dietas personalizadas.
            Se a pergunta nao for sobre nutricao,treinos e dietas mande uma mensagem de erro.
        ''')
    ] + mensagens)
    chain = template | chat
    return chain.invoke({}).content

# ======== INTERFACE DE USO =========
print('Bem-vindo ao NutriAI! (Digite x para sair a qualquer momento.)\n')

mensagens = []

while True:
    entrada = input("Usuário: ").strip()
    if entrada.lower() in ['x', 'exit']:
        break
    mensagens.append(HumanMessage(content=entrada))
    try:
        resposta = resposta_nutricional(mensagens)
        mensagens.append(AIMessage(content=resposta))
        print(f"\nNutriAI: {resposta}\n")
    except Exception as e:
        print("Erro ao processar a resposta:")
        traceback.print_exc()

print('\nObrigado por usar o NutriAI! Cuide bem da sua saúde! Até logo, Senhor(a)!')