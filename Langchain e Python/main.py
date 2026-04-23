# ================================
# IMPORTAÇÕES
# ================================

# Classe responsável por conectar e enviar mensagens para modelos de linguagem (LLMs)
from langchain_openai import ChatOpenAI

# Classe usada para criar prompts (mensagens) dinâmicos com variáveis
from langchain_core.prompts import PromptTemplate

# Parsers (formatadores) para transformar a saída do modelo em texto simples ou JSON estruturado
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Biblioteca para criação de modelos de dados estruturados (validação de dados)
from pydantic import BaseModel, Field


# ================================
# CONFIGURAÇÃO DO AMBIENTE
# ================================

# 1 - Criar ambiente virtual (venv):
# python -m venv .venv
# -> Cria um ambiente isolado para evitar conflitos de dependências

# 2 - Ativar o ambiente virtual (Windows):
# .venv\Scripts\activate
# -> Ativa o ambiente criado

# 3 - Instalar dependências:
# pip install openai langchain langchain-openai
# -> Instala as bibliotecas necessárias para rodar o projeto


# ================================
# CRIAÇÃO DOS MODELOS DE DADOS (SAÍDA ESTRUTURADA)
# ================================

# Define o formato esperado da resposta para sugestão de cidade
class Destino(BaseModel):
    cidade: str = Field("Nome da cidade sugerida")  # Nome da cidade
    motivo: str = Field("Motivo para a sugestão da cidade")  # Justificativa da escolha

# Define o formato esperado da resposta para restaurantes
class Restaurante(BaseModel):
    cidade: str = Field("Nome da cidade sugerida")  # Cidade analisada
    restaurantes: str = Field("Restaurantes recomendados na cidade")  # Lista de restaurantes


# ================================
# PARSERS (CONVERSÃO DA RESPOSTA)
# ================================

# Parser que converte a resposta do modelo para o formato do modelo Destino (JSON estruturado)
parseador_destino = JsonOutputParser(pydantic_object=Destino)

# Parser que converte a resposta do modelo para o formato do modelo Restaurante
parseador_restaurante = JsonOutputParser(pydantic_object=Restaurante)


# ================================
# CRIAÇÃO DOS PROMPTS (ENTRADA)
# ================================

# Prompt para sugerir uma cidade com base em um interesse
prompt_cidade = PromptTemplate(
    template="""
    Sugira uma cidade dado o meu interesse por {interesse}.
    {Formato_de_saida}
    """,
    input_variables=["interesse"],  # Variável dinâmica que será informada na execução

    # Injeta automaticamente instruções de como o modelo deve formatar a resposta (JSON)
    partial_variables={
        "Formato_de_saida": parseador_destino.get_format_instructions()
    }
)

# Prompt para sugerir restaurantes em uma cidade
prompt_restaurante = PromptTemplate(
    template="""
    Sugira restaurantes na cidade de {cidade}.
    {Formato_de_saida}
    """,

    # Também força o modelo a responder no formato JSON esperado
    partial_variables={
        "Formato_de_saida": parseador_restaurante.get_format_instructions()
    }
)

# Prompt para sugerir atividades culturais (resposta livre, sem JSON)
prompt_cultural = PromptTemplate(
    template="""
    Sugira atividades culturais na cidade de {cidade}.
    """
)


# ================================
# CONFIGURAÇÃO DO MODELO
# ================================

# Inicializa o modelo de linguagem via LangChain
# Aqui está configurado para usar um modelo LOCAL via LM Studio
modelo = ChatOpenAI(
    model="google/gemma-3-1b",  # Nome do modelo carregado no LM Studio
    base_url="http://127.0.0.1:1234/v1",  # Endpoint local do servidor
    api_key="lm-studio",  # Chave obrigatória (mesmo que fake no ambiente local)
    temperature=0.0  # 0 = respostas mais previsíveis e determinísticas
)


# ================================
# CRIAÇÃO DAS CADEIAS (PIPELINES)
# ================================

# Cadeia 1:
# Entrada (interesse) → cria prompt → envia ao modelo → formata saída como JSON (Destino)
cadeia_1 = prompt_cidade | modelo | parseador_destino

# Cadeia 2:
# Usa a cidade gerada → cria prompt → modelo → formata como JSON (Restaurante)
cadeia_2 = prompt_restaurante | modelo | parseador_restaurante

# Cadeia 3:
# Usa a cidade → gera atividades culturais → retorna texto simples
cadeia_3 = prompt_cultural | modelo | StrOutputParser()

# Encadeia todas as etapas:
# interesse → cidade → restaurantes → atividades culturais
cadeia = cadeia_1 | cadeia_2 | cadeia_3


# ================================
# EXECUÇÃO
# ================================

# Executa toda a cadeia passando o interesse como entrada inicial
resposta = cadeia.invoke(
    {
        "interesse": "praias"  # Tema desejado pelo usuário
    }
)


# ================================
# SAÍDA
# ================================

# Exibe o resultado final (atividades culturais da cidade sugerida)
print(resposta)