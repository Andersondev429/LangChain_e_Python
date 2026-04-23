# ================================
# IMPORTAÇÕES
# ================================

# Classe para conectar com modelos de linguagem (LLMs), como os rodando no LM Studio
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Classe para gerar embeddings localmente usando modelos do Hugging Face
from langchain_community.embeddings import HuggingFaceEmbeddings

# Loader para carregar documentos (texto e PDF)
# (necessário instalar: pip install langchain-community)
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# Banco vetorial para armazenar embeddings e fazer busca por similaridade
from langchain_community.vectorstores import FAISS

# Classe responsável por dividir textos grandes em partes menores
# (necessário instalar: pip install langchain-text-splitters)
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Criação de prompts (estrutura da pergunta para o modelo)
from langchain_core.prompts import ChatPromptTemplate

# Converte a saída do modelo para texto simples
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


# ================================
# CONFIGURAÇÃO DO MODELO (LLM)
# ================================

# Inicializa o modelo de linguagem rodando localmente no LM Studio
modelo = ChatOpenAI(
    model="google/gemma-3-1b",  # Nome do modelo carregado no LM Studio
    base_url="http://127.0.0.1:1234/v1",  # Endereço da API local do LM Studio
    api_key="lm-studio",  # Chave obrigatória (pode ser qualquer valor no ambiente local)
    temperature=0.0  # Define o nível de criatividade (0 = respostas mais objetivas)
)


# ================================
# CONFIGURAÇÃO DOS EMBEDDINGS
# ================================

# OBS:
# É necessário instalar:
# pip install sentence-transformers
# pip install faiss-cpu

# Cria o gerador de embeddings usando um modelo local
# Esse modelo transforma textos em vetores numéricos (para busca semântica)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ================================
# CARREGAMENTO DOS DOCUMENTOS
# ================================

# Lista de arquivos PDF que serão usados como base de conhecimento
# ⚠️ Em Windows, cuidado com "\" → pode usar "/" ou r"caminho"
arquivos = [
    "documentos/GTB_gold_Nov23.pdf",
    "documentos/GTB_platinum_Nov23.pdf",
    "documentos/GTB_standard_Nov23.pdf"
]

# Carrega todos os PDFs e junta em uma única lista de documentos
documentos = sum([PyPDFLoader(arquivo).load() for arquivo in arquivos], [])


# ================================
# DIVISÃO DOS DOCUMENTOS
# ================================

# Divide os documentos em pedaços menores (chunks)
# Isso melhora a busca e evita estouro de contexto do modelo
pedacos = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamanho máximo de cada pedaço (em caracteres)
    chunk_overlap=100     # Sobreposição entre pedaços (mantém contexto)
).split_documents(documentos)


# ================================
# CRIAÇÃO DO BANCO VETORIAL (FAISS)
# ================================

# Converte os pedaços em embeddings e armazena no FAISS
# Depois transforma em "retriever", que busca os trechos mais relevantes
dados_recuperados = FAISS.from_documents(
    pedacos,
    embeddings
).as_retriever(
    search_kwargs={"k": 3}  # Retorna os 3 trechos mais relevantes
)


# ================================
# CRIAÇÃO DO PROMPT
# ================================

# Define como o modelo deve responder
# O system define o comportamento
# O human define como a pergunta será enviada
prompt_consulta_seguro = ChatPromptTemplate.from_messages(
    [
        ("system", "Responda usando exclusivamente as informações fornecidas:"),
        ("human", "{query}\n\nContexto:\n{contexto}\n\nResposta:")
    ]
)


# ================================
# CRIAÇÃO DA CADEIA (PIPELINE)
# ================================

# Junta:
# Prompt → Modelo → Conversão para texto
cadeia = prompt_consulta_seguro | modelo | StrOutputParser()


# ================================
# FUNÇÃO DE PERGUNTA E RESPOSTA
# ================================

def responder(pergunta: str):
    # Busca os trechos mais relevantes no banco vetorial
    trechos = dados_recuperados.invoke(pergunta)

    # Junta os textos encontrados em um único contexto
    contexto = "\n\n".join([um_trecho.page_content for um_trecho in trechos])

    # Envia a pergunta + contexto para o modelo gerar resposta
    return cadeia.invoke({
        "query": pergunta,
        "contexto": contexto
    })


# ================================
# EXECUÇÃO
# ================================

# Faz uma pergunta ao sistema baseado nos documentos carregados
print(responder("Como devo proceder caso tenha um item comprado roubado e caso eu tenha o cartão gold?"))