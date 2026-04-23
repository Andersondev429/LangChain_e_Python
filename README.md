# 📄  LangChain_e_Python

Sistema de perguntas e respostas baseado em documentos PDF utilizando **RAG (Retrieval-Augmented Generation)** com execução **100% local**.

O projeto permite consultar informações de arquivos PDF de forma inteligente, utilizando busca semântica e um modelo de linguagem rodando no LM Studio.

---

## 🚀 Funcionalidades

- 📚 Leitura de múltiplos arquivos PDF  
- ✂️ Divisão inteligente de textos (chunking)  
- 🧠 Geração de embeddings locais (Hugging Face)  
- 🔍 Busca semântica com FAISS  
- 🤖 Respostas com LLM rodando localmente (LM Studio)  
- 🔒 Sem dependência de APIs externas  

---

## 🧠 Como funciona

O fluxo do projeto segue a arquitetura RAG:

1. Carrega os PDFs  
2. Divide o conteúdo em pedaços menores  
3. Converte os textos em embeddings (vetores)  
4. Armazena no FAISS  
5. Busca os trechos mais relevantes para a pergunta  
6. Envia contexto + pergunta para o modelo LLM  
7. Gera uma resposta baseada apenas no conteúdo dos documentos  

---

## 🛠️ Tecnologias utilizadas

- Python 3.10+
- LangChain  
- FAISS  
- Sentence Transformers (Hugging Face)  
- LM Studio (modelo local)  

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/rag-pdf-assistant-local.git
cd rag-pdf-assistant-local
```

---

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

#### Windows:
```bash
.venv\Scripts\activate
```

#### Linux / Mac:
```bash
source .venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install langchain langchain-community langchain-openai
pip install langchain-text-splitters
pip install sentence-transformers
pip install faiss-cpu
pip install pypdf
```

---

## 🤖 Configuração do LM Studio

1. Baixe e instale o LM Studio  
2. Carregue um modelo (ex: `gemma`, `llama`, `mistral`)  
3. Inicie o servidor local  
4. Verifique se está rodando em:

```
http://127.0.0.1:1234/v1
```

---

## 📁 Estrutura do projeto

```
rag-pdf-assistant-local/
│
├── documentos/
│   ├── arquivo1.pdf
│   ├── arquivo2.pdf
│   └── arquivo3.pdf
│
├── main_rag.py
├── README.md
└── requirements.txt (opcional)
```

---

## ▶️ Como usar

1. Adicione seus PDFs na pasta `documentos/`  
2. Execute o script:

```bash
python main_rag.py
```

3. O sistema irá responder perguntas com base nos documentos carregados  

---

## 💬 Exemplo de uso

```python
print(responder("Como proceder em caso de item roubado?"))
```

---

## ⚠️ Observações importantes

- Certifique-se de que o LM Studio está rodando  
- O modelo precisa estar carregado antes da execução  
- Em Windows, evite caminhos muito longos (ou ative suporte a long paths)  
- Para melhor desempenho, utilize modelos LLM mais robustos  

---

## 🚀 Melhorias futuras

- 💾 Persistência do índice FAISS  
- ⚡ Otimização de performance  
- 🧠 Uso de modelos mais avançados  
- 🔎 Implementação de reranking  
- 🌐 Interface web (Streamlit ou FastAPI)  

---

## 📜 Licença

Este projeto é livre para uso educacional e estudos.

---

## 👨‍💻 Autor

Anderson Pinheiro da Silva

Desenvolvido para estudos em Engenharia de IA e aplicações com LangChain.
