# 📄  LangChain_e_Python

Sistema de perguntas e respostas baseado em documentos PDF utilizando RAG (Retrieval-Augmented Generation) com execução 100% local.

O projeto permite consultar informações de arquivos PDF de forma inteligente, utilizando busca semântica e um modelo de linguagem rodando no LM Studio.

🚀 Funcionalidades
📚 Leitura de múltiplos arquivos PDF
✂️ Divisão inteligente de textos (chunking)
🧠 Geração de embeddings locais (Hugging Face)
🔍 Busca semântica com FAISS
🤖 Respostas com LLM rodando localmente (LM Studio)
🔒 Sem dependência de APIs externas
🧠 Como funciona

O fluxo do projeto segue a arquitetura RAG:

Carrega os PDFs
Divide o conteúdo em pedaços menores
Converte os textos em embeddings (vetores)
Armazena no FAISS
Busca os trechos mais relevantes para a pergunta
Envia contexto + pergunta para o modelo LLM
Gera uma resposta baseada apenas no conteúdo dos documentos

🛠️ Tecnologias utilizadas
Python 3.10+
LangChain
FAISS
Sentence Transformers (Hugging Face)
LM Studio (modelo local)

📦 Instalação
1. Clone o repositório
git clone https://github.com/seu-usuario/rag-pdf-assistant-local.git
cd rag-pdf-assistant-local
2. Crie e ative um ambiente virtual
python -m venv .venv
Windows:
.venv\Scripts\activate
Linux / Mac:
source .venv/bin/activate
3. Instale as dependências
pip install langchain langchain-community langchain-openai
pip install langchain-text-splitters
pip install sentence-transformers
pip install faiss-cpu
pip install pypdf

🤖 Configuração do LM Studio
Baixe e instale o LM Studio
Carregue um modelo (ex: gemma, llama, mistral)
Inicie o servidor local
Verifique se está rodando em:
http://127.0.0.1:1234/v1

📁 Estrutura do projeto
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

▶️ Como usar
Adicione seus PDFs na pasta documentos/
Execute o script:
python main_rag.py
O sistema irá responder perguntas com base nos documentos carregados

💬 Exemplo de uso
print(responder("Como proceder em caso de item roubado?"))

⚠️ Observações importantes
Certifique-se de que o LM Studio está rodando
O modelo precisa estar carregado antes da execução
Em Windows, evite caminhos muito longos (ou ative suporte a long paths)
Para melhor desempenho, utilize modelos LLM mais robustos

🚀 Melhorias futuras
💾 Persistência do índice FAISS
⚡ Otimização de performance
🧠 Uso de modelos mais avançados
🔎 Implementação de reranking
🌐 Interface web (Streamlit ou FastAPI)
📜 Licença

Este projeto é livre para uso educacional e estudos.

👨‍💻 Autor
Anderson Pinheiro da Silva

Desenvolvido para estudos em Engenharia de IA e aplicações com LangChain.
