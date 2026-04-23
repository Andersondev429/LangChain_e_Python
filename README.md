# 🤖 LangChain Masterclass: De Cadeias a Agentes com RAG

Este repositório é um laboratório prático focado no ecossistema **LangChain**, demonstrando a evolução de aplicações de Inteligência Artificial — desde prompts estruturados até agentes inteligentes com memória e sistemas RAG.

O projeto foi desenvolvido com foco em aprendizado progressivo, explorando conceitos fundamentais e avançados de forma prática.

---

## 🌟 Diferencial: Execução 100% Local

Todo o projeto foi projetado para rodar localmente, garantindo:

- 🔒 Privacidade total: seus dados nunca saem da sua máquina  
- 💰 Custo zero: sem necessidade de APIs pagas  
- ⚡ Performance local com modelos leves  

### 📌 Modelo recomendado
```
google/gemma-3-1b
```
*(ou qualquer modelo compatível com API OpenAI via LM Studio)*

---

## 🏗️ Estrutura do Projeto

O repositório está dividido em 4 módulos principais:

---

### 🔗 1. Cadeias Sequenciais Estruturadas (`main.py`)

Demonstra o conceito de **Chain Composition**, onde a saída de uma etapa alimenta a próxima.

**Fluxo:**
```
Entrada → Cidade → Restaurantes → Roteiro Cultural
```

**Destaques:**
- Uso de JsonOutputParser  
- Validação com Pydantic  
- Estrutura confiável de dados entre etapas  

---

### 🧠 2. Chat com Memória de Sessão (`main_chat.py`)

Transforma o LLM em um assistente com memória contextual.

**Funcionalidades:**
- Histórico de conversa por sessão  
- Contexto persistente  
- Respostas mais naturais  

**Tecnologias:**
- InMemoryChatMessageHistory  
- RunnableWithMessageHistory  

---

### 🕸️ 3. Fluxos Inteligentes com LangGraph (`main_langgraph.py`)

Implementação de agentes baseados em grafos de estado.

**Lógica:**
- Um nó roteador interpreta a intenção do usuário  
- Direciona para especialistas:  
  - 🏖️ Praia  
  - 🏔️ Montanha  

**Diferencial:**
- Decisão dinâmica de fluxo  
- Arquitetura escalável de agentes  

---

### 📚 4. Sistema RAG de Seguros (`main_rag.py`)

Implementação completa de **Retrieval-Augmented Generation (RAG)**.

**Pipeline:**
1. Carregamento de PDFs  
2. Divisão de texto  
3. Geração de embeddings  
4. Armazenamento vetorial  
5. Busca semântica  
6. Geração de resposta com contexto  

---

## 📊 Arquitetura do RAG

```
Documentos PDF
       ↓
Embeddings Locais
       ↓
Banco Vetorial (FAISS)
       ↓
Busca por Similaridade
       ↓
Prompt + Contexto
       ↓
LLM Local
       ↓
Resposta Final
```

---

## 🚀 Como Configurar e Rodar

### 1️⃣ Pré-requisitos

- Instalar o LM Studio  
- Baixar um modelo compatível (ex: gemma-3-1b)  
- Iniciar o servidor local na porta 1234  

---

### 2️⃣ Instalação

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

### 3️⃣ Executar os módulos

```bash
python main.py
python main_chat.py
python main_langgraph.py
python main_rag.py
```

---

## 🛠️ Tecnologias Utilizadas

- LangChain → Orquestração de LLMs  
- LangGraph → Fluxos de agentes com estado  
- FAISS → Busca vetorial eficiente  
- HuggingFace Embeddings → Vetorização gratuita  
- PyPDF → Leitura de PDFs  
- Pydantic → Validação de dados  

---

## 📝 Boas Práticas

O projeto já inclui um `.gitignore` configurado para evitar:

- Ambientes virtuais (.venv)  
- Variáveis sensíveis (.env)  
- Cache do LangChain  

---

## 💡 Possíveis Extensões

- Integração com banco de dados  
- Deploy como API (FastAPI / Flask)  
- Interface web (Streamlit / React)  
- Uso de modelos maiores  

---

## ⭐ Contribuição

Sinta-se livre para contribuir com melhorias, sugestões ou novos exemplos.

Se este projeto te ajudou, considere deixar uma ⭐ no repositório!
