# 🔐 Iyuno AI Security Agent

NIST AI 및 Cybersecurity 공개 문서를 기반으로 검색하고 답변하는 **RAG + AI Agent 시스템**입니다.

사용자의 질문에 대해 Gemini Agent가 필요한 경우 `search_documents` Tool을 호출하고, ChromaDB에 저장된 NIST 문서를 검색한 뒤 검색 결과를 바탕으로 답변을 생성합니다.

## 📌 Project Overview

이 프로젝트는 AI Agent 포트폴리오 과제로 다음 기술을 하나의 시스템으로 구현했습니다.

* Public document ingestion
* PDF text extraction
* Document chunking
* Sentence Transformer embeddings
* ChromaDB vector database
* Retrieval-Augmented Generation (RAG)
* Gemini-based AI Agent
* Function / Tool Calling
* Source citation
* Retrieval evaluation
* Faithfulness evaluation
* Pytest automated testing
* GitHub Actions CI
* Streamlit web demo

## 🏗️ Architecture

```text
                         ┌────────────────────┐
                         │      User Query    │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │   Gemini AI Agent  │
                         └─────────┬──────────┘
                                   │
                              Tool Calling
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │   search_documents Tool  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       ChromaDB            │
                    │   Vector Similarity Search│
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      NIST Documents      │
                    │       7,391 chunks       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Retrieved Source Context │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                         ┌────────────────────┐
                         │   Gemini Answer    │
                         │ + Source Citation  │
                         └────────────────────┘
```

## 📚 Dataset

총 **21개의 NIST 공개 문서**를 수집하여 RAG 시스템에 사용했습니다.

주요 문서 범위:

* NIST AI Risk Management Framework
* NIST Generative AI Profile
* NIST Cybersecurity Framework
* NIST Cybersecurity Controls
* NIST Zero Trust Architecture
* NIST Incident Response
* NIST Supply Chain Security
* NIST Secure Software Development Framework
* NIST Privacy Framework
* NIST Risk Assessment
* NIST Digital Identity
* NIST Cloud Computing
* NIST Penetration Testing
* NIST Key Management
* NIST Log Management
* NIST Security Engineering
* NIST Forensics
* NIST Container Security
* NIST Intrusion Detection / Prevention
* NIST System Security Engineering
* NIST CSF Overview

### Document processing

```text
21 PDF documents
        ↓
PDF text extraction
        ↓
Chunking
        ↓
7,391 chunks
        ↓
Sentence Transformer embeddings
        ↓
ChromaDB
```

## 🧩 Technology Stack

| Component      | Technology                               |
| -------------- | ---------------------------------------- |
| Language       | Python 3.13                              |
| LLM            | Gemini                                   |
| LLM API        | OpenAI-compatible Gemini API             |
| Embedding      | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB      | ChromaDB                                 |
| PDF Extraction | pypdf                                    |
| Web UI         | Streamlit                                |
| Testing        | pytest                                   |
| CI             | GitHub Actions                           |

## 📁 Project Structure

```text
iyuno-agent-portfolio/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── chunk.py
│   ├── embeddings.py
│   ├── extract.py
│   ├── ingest.py
│   ├── rag.py
│   ├── retriever.py
│   ├── tools.py
│   └── web.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── chunks/
│   └── chroma/
│
├── eval/
│   ├── evaluate.py
│   ├── faithfulness.py
│   ├── faithfulness_results.json
│   └── questions.json
│
├── tests/
│   ├── test_agent.py
│   ├── test_rag.py
│   └── test_tools.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🤖 AI Agent & Tool Calling

Agent는 사용자의 질문을 분석하고 필요할 경우 `search_documents` Tool을 호출합니다.

```text
User
 ↓
Gemini Agent
 ↓
search_documents()
 ↓
ChromaDB Retrieval
 ↓
Relevant NIST Chunks
 ↓
Gemini
 ↓
Final Answer
```

Tool은 검색 결과와 함께 다음 정보를 반환합니다.

* Source document
* Chunk index
* Similarity distance
* Retrieved text

이를 통해 최종 답변의 근거가 되는 문서를 확인할 수 있습니다.

## 🔎 RAG

RAG 시스템은 다음 단계로 동작합니다.

1. 사용자 질문 입력
2. 질문 embedding 생성
3. ChromaDB similarity search
4. 관련 문서 chunk 검색
5. 검색 결과를 context로 구성
6. Gemini에 context 전달
7. 검색된 근거를 기반으로 답변 생성
8. Source 및 chunk 정보 표시

모델이 검색된 문서에 없는 내용을 임의로 생성하지 않도록 prompt에 grounding 규칙을 적용했습니다.

## 📊 Evaluation

### Retrieval Evaluation

30개의 평가 질문을 사용하여 source-level Recall을 측정했습니다.

| Metric                    |        Result |
| ------------------------- | ------------: |
| Recall@1                  |     **0.767** |
| Recall@3                  |     **0.933** |
| Recall@5                  |     **0.933** |
| Average Retrieval Latency | **0.009 sec** |

Recall은 각 질문의 expected source document가 검색 결과에 포함되는지를 기준으로 계산했습니다.

### Faithfulness Evaluation

5개의 샘플 질문에 대해 검색된 source context와 최종 답변을 비교하여 평가했습니다.

| Metric                 |    Result |
| ---------------------- | --------: |
| Questions attempted    |         5 |
| Successfully evaluated |         5 |
| Faithful answers       |         5 |
| Faithfulness           | **1.000** |

> Faithfulness 결과는 5-question sample에 대한 평가 결과입니다. API 오류는 실제 불충실한 답변으로 간주하지 않고 평가에서 제외하도록 구현했습니다.

## ⚡ Performance

예시 실행에서 Retrieval과 LLM 응답 시간을 별도로 측정했습니다.

```text
Retrieval latency: approximately 0.01 sec
LLM latency: approximately 1~20 sec
```

LLM latency는 API 서버 상태와 모델 응답 시간에 따라 달라질 수 있습니다.

## 🧪 Testing

현재 pytest 기반 테스트를 사용합니다.

```powershell
python -m pytest -q
```

현재 로컬 테스트 결과:

```text
5 passed
```

테스트는 다음 영역을 검증합니다.

* RAG context 생성
* Tool 결과 구조
* Tool source 반환
* Agent 기본 응답
* Agent Tool Calling 동작

실제 ChromaDB 및 Gemini API에 의존하지 않는 mock 기반 테스트를 사용하여 CI 환경에서도 실행할 수 있도록 구성했습니다.

## 🔄 Continuous Integration

GitHub Actions를 사용하여 코드 Push 또는 Pull Request 발생 시 자동으로 테스트를 실행합니다.

```text
Git Push
   ↓
GitHub Actions
   ↓
Python environment
   ↓
Install dependencies
   ↓
pytest
   ↓
Pass / Fail
```

현재 최신 CI workflow는 성공 상태입니다.

## 🌐 Streamlit Demo

로컬에서 다음 명령으로 실행할 수 있습니다.

```powershell
python -m streamlit run app/web.py
```

실행 후 브라우저에서:

```text
http://localhost:8501
```

으로 접속합니다.

Streamlit 화면에서는:

* 질문 입력
* Agent 실행
* Tool Calling 여부 확인
* 최종 답변 확인
* Retrieved Sources 확인
* Source document / chunk 확인

이 가능합니다.

## ⚙️ Installation

### 1. Repository clone

```powershell
git clone https://github.com/lhjk7654/iyuno-agent-portfolio.git
cd iyuno-agent-portfolio
```

### 2. Virtual environment

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Environment variable

프로젝트 루트에 `.env` 파일을 생성합니다.

```text
GEMINI_API_KEY=your_api_key
```

> API key는 GitHub에 업로드하지 않습니다.

## 🗂️ Data Pipeline

문서 수집부터 Vector DB 구축까지의 전체 pipeline:

```powershell
python -m app.ingest
python -m app.extract
python -m app.chunk
python -m app.embeddings
```

이 과정을 통해 NIST PDF 문서를 처리하고 ChromaDB에 embedding을 저장합니다.

## ▶️ R
