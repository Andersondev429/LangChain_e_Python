# ================================
# IMPORTAÇÕES
# ================================

# Classe responsável por conectar e enviar mensagens para modelos de linguagem (LLMs)
from langchain_openai import ChatOpenAI

# Classe para criação de prompts estruturados (com system, human, etc.)
from langchain_core.prompts import ChatPromptTemplate

# Parsers para tratar a saída do modelo (texto simples ou JSON)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Tipagem para estruturar dados (dicionários tipados e valores fixos)
from typing import TypedDict, Literal

# Biblioteca para construção de fluxos baseados em grafos (LangGraph)
from langgraph.graph import StateGraph, START, END

# Configuração opcional de execução dos nós
from langchain_core.runnables import RunnableConfig

# Biblioteca para execução assíncrona
import asyncio


# ================================
# CONFIGURAÇÃO DO MODELO
# ================================

# Instancia o modelo de linguagem rodando localmente via LM Studio
modelo = ChatOpenAI(
    model="google/gemma-3-1b",        # Nome do modelo
    base_url="http://127.0.0.1:1234/v1",  # Endpoint local
    api_key="lm-studio",             # Chave fictícia (necessária para a lib)
    # Baixa criatividade (respostas mais determinísticas)
    temperature=0.0
)


# ================================
# CRIAÇÃO DOS PROMPTS (PERSONAS)
# ================================

# Prompt para especialista em destinos de praia
prompt_consultor_praia = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sra Praia. Você é um assistente de viagens com destinos praianos."),
        ("human", "{query}.")  # Pergunta do usuário (dinâmica)
    ]
)

# Prompt para especialista em destinos de montanha
prompt_consultor_montanha = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sra Montanha. Você é um assistente de viagens com destinos montanhosos."),
        ("human", "{query}.")
    ]
)

# Criação das cadeias (pipeline: prompt → modelo → parser de saída)
cadeia_praia = prompt_consultor_praia | modelo | StrOutputParser()
cadeia_montanha = prompt_consultor_montanha | modelo | StrOutputParser()


# ================================
# DEFINIÇÃO DA ROTA (SAÍDA DO ROTEADOR)
# ================================

# Define o formato esperado da decisão do roteador
class Rota(TypedDict):
    destino: Literal["praia", "montanha"]


# ================================
# PROMPT DO ROTEADOR
# ================================

# Prompt responsável por decidir para qual especialista enviar a pergunta
prompt_roteador = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um roteador de perguntas. Direcione as perguntas sobre praias para a Sra Praia e as perguntas sobre montanhas para a Sra Montanha."),
        ("human", "{query}.")
    ]
)

# Cadeia do roteador com saída estruturada (espera um JSON compatível com Rota)
roteador = prompt_roteador | modelo.with_structured_output(Rota)


# ================================
# ESTADO DO GRAFO
# ================================

# Define a estrutura de dados que será compartilhada entre os nós do grafo
class Estado(TypedDict):
    query: str       # Pergunta do usuário
    destino: Rota    # Resultado do roteador
    resposta: str    # Resposta final gerada


# ================================
# DEFINIÇÃO DOS NÓS (FUNÇÕES)
# ================================

# Nó responsável por decidir o destino (praia ou montanha)
async def no_roteador(estado: Estado, config=RunnableConfig):
    return {
        "destino": await roteador.ainvoke({"query": estado["query"]}, config)
    }

# Nó que gera resposta sobre praia


async def no_praia(estado: Estado, config=RunnableConfig):
    return {
        "resposta": await cadeia_praia.ainvoke({"query": estado["query"]}, config)
    }

# Nó que gera resposta sobre montanha


async def no_montanha(estado: Estado, config=RunnableConfig):
    return {
        "resposta": await cadeia_montanha.ainvoke({"query": estado["query"]}, config)
    }


# ================================
# LÓGICA DE DECISÃO
# ================================

# Função que escolhe qual nó executar com base no resultado do roteador
def escolher_no(estado: Estado) -> Literal["praia", "montanha"]:
    return "praia" if estado["destino"]["destino"] == "praia" else "montanha"


# ================================
# CONSTRUÇÃO DO GRAFO
# ================================

# Cria o grafo baseado no estado definido
grafo = StateGraph(Estado)

# Adiciona os nós ao grafo
grafo.add_node("rotear", no_roteador)
grafo.add_node("praia", no_praia)
grafo.add_node("montanha", no_montanha)

# Define o fluxo de execução
grafo.add_edge(START, "rotear")                    # Início → roteador
grafo.add_conditional_edges("rotear", escolher_no)  # Roteador decide próximo nó
grafo.add_edge("praia", END)                       # Praia → fim
grafo.add_edge("montanha", END)                    # Montanha → fim

# Compila o grafo em uma aplicação executável
app = grafo.compile()


# ================================
# EXECUÇÃO PRINCIPAL
# ================================

# Função principal assíncrona
async def main():
    # Envia uma pergunta para o grafo
    resposta = await app.ainvoke({
        "query": "Quero visitar uma cidade com praias e vida noturna agitada. Qual cidade você sugere?"
    })

    # Exibe a resposta final
    print(resposta["resposta"])


# Executa o programa
asyncio.run(main())
