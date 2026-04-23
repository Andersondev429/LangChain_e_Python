# ================================
# IMPORTAÇÕES
# ================================

# Classe responsável por conectar e enviar mensagens para modelos de linguagem (LLMs)
from langchain_openai import ChatOpenAI

# Classe para criação de prompts estruturados (com system, human, etc.)
from langchain_core.prompts import ChatPromptTemplate

# Parsers para tratar a saída do modelo (texto simples ou JSON)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Classe que armazena o histórico de mensagens em memória (temporário)
from langchain_core.chat_history import InMemoryChatMessageHistory

# Permite adicionar memória (histórico) a uma cadeia (chain)
from langchain_core.runnables.history import RunnableWithMessageHistory

# Placeholder especial para inserir o histórico no prompt
from langchain_core.prompts import MessagesPlaceholder


# ================================
# CONFIGURAÇÃO DO MODELO (LLM)
# ================================

modelo = ChatOpenAI(
    model="google/gemma-3-1b",  # Nome do modelo rodando no LM Studio
    base_url="http://127.0.0.1:1234/v1",  # URL do servidor local
    api_key="lm-studio",  # Chave obrigatória (mesmo que fake em ambiente local)
    temperature=0.0  # Controla criatividade (0 = respostas mais previsíveis)
)


# ================================
# CRIAÇÃO DO PROMPT
# ================================

prompt_sugestao = ChatPromptTemplate.from_messages(
    [
        # Define o comportamento do modelo
        ("system", "Você é um assistente de viagens que sugere destinos com base em interesses."),
        
        # Aqui será inserido automaticamente o histórico da conversa
        MessagesPlaceholder(variable_name="historico"),
        
        # Entrada do usuário (pergunta dinâmica)
        ("human", "{query}.")
    ]
)


# ================================
# CRIAÇÃO DA CADEIA (CHAIN)
# ================================

# Combina: Prompt -> Modelo -> Parser de saída (texto simples)
cadeia = prompt_sugestao | modelo | StrOutputParser()


# ================================
# CONFIGURAÇÃO DA MEMÓRIA
# ================================

# Dicionário que armazena o histórico por sessão
memoria = {}

# Identificador da sessão (simula um usuário)
sessao = "sessao_1"


# Função que retorna o histórico de uma sessão específica
def historico_por_sessao(sessao: str):
    # Se a sessão ainda não existir, cria uma nova memória
    if sessao not in memoria:
        memoria[sessao] = InMemoryChatMessageHistory()
    
    # Retorna o histórico daquela sessão
    return memoria[sessao]


# ================================
# PERGUNTAS DO USUÁRIO
# ================================

lista_perguntas = [
    "Quero visitar uma cidade com praias e vida noturna agitada. Qual cidade você sugere?",
    "Qual a melhor época para visitar?",
]


# ================================
# CADEIA COM MEMÓRIA
# ================================

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,  # Cadeia principal (prompt + modelo)
    
    # Função que gerencia o histórico por sessão
    get_session_history=historico_por_sessao,
    
    # Nome da variável que contém a entrada do usuário
    input_messages_key="query",
    
    # Nome da variável onde o histórico será inserido no prompt
    history_messages_key="historico"
)


# ================================
# EXECUÇÃO DAS PERGUNTAS
# ================================

for uma_pergunta in lista_perguntas:
    
    # Envia a pergunta para a cadeia com memória
    resposta = cadeia_com_memoria.invoke(
        {"query": uma_pergunta},  # Input do usuário
        config={"session_id": sessao}  # Identifica a sessão
    )
    
    # Exibe a pergunta e a resposta
    print(f"Pergunta: {uma_pergunta}")
    print(f"Resposta: {resposta}\n")