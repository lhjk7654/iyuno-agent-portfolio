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

### Job Requirement Mapping

| Iyuno AI Agent Engineer 요구사항 | 프로젝트 구현                           |
| ---------------------------- | --------------------------------- |
| LLM 기반 AI Agent 시스템 설계       | Gemini AI Agent                   |
| RAG 검색 및 응답 시스템              | ChromaDB 기반 RAG                   |
| Tool Calling                 | `search_documents` Tool           |
| API / 데이터 통합                 | Gemini API + ChromaDB             |
| 다단계 Agent workflow           | Agent → Tool → Retrieval → Answer |
| 평가 및 품질 측정                   | Recall@k / Faithfulness / Latency |
| 테스트 및 신뢰성                    | pytest + GitHub Actions CI        |
| Demo / 실사용 인터페이스             | Streamlit                         |

## 📌 Job Posting Source

### Iyuno AI Agent Engineer

* **Company:** Iyuno
* **Position:** AI Agent Engineer
* **Location:** Seoul / Hybrid
* **Employment:** Full-time
* **Requisition:** JR101122
* **Application Deadline:** 2026-09-30
* **Job Posting:** https://iyuno.wd3.myworkdayjobs.com/careers/job/seoul/ai-agent-engineer_jr101122

### Project Connection

The project requirements were derived from the AI Agent Engineer job posting and translated into an executable GitHub portfolio project.

| Job Posting Requirement        | Portfolio Implementation          |
| ------------------------------ | --------------------------------- |
| LLM-based AI Agent             | Gemini AI Agent                   |
| RAG search and response system | NIST document RAG                 |
| Tool Calling                   | `search_documents` Tool           |
| API / data integration         | Gemini API + ChromaDB             |
| Multi-step workflow            | Agent → Tool → Retrieval → Answer |
| Evaluation and feedback        | Recall@k / Faithfulness / Latency |
| Reliability and testing        | pytest + GitHub Actions           |
| Working demonstration          | Streamlit                         |

### Related Job Posting

The assignment also provided an optional RideFlux engineering recruitment track as an additional reference.

* **RideFlux 2026 H2 Engineering Recruitment**
* https://inthiswork.com/archives/393239
* **Deadline:** 2026-09-27

The primary implementation and evaluation in this repository are based on the **Iyuno AI Agent Engineer** position.

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

## ▶️ Run the Project

### Streamlit Demo

```powershell
python -m streamlit run app/web.py
```

실행 후 브라우저에서 다음 주소로 접속합니다.

```text
http://localhost:8501
```

Streamlit 데모에서는 다음 기능을 확인할 수 있습니다.

* 사용자 질문 입력
* Gemini Agent 실행
* `search_documents` Tool Calling 여부 확인
* 최종 답변 확인
* Retrieved Sources 확인
* Source document / chunk 확인

### Run Tests

```powershell
python -m pytest -q
```

현재 테스트 결과:

```text
5 passed
```

### Run Retrieval Evaluation

```powershell
python -m eval.evaluate
```

### Run Faithfulness Evaluation

```powershell
python -m eval.faithfulness
```

> Faithfulness 평가는 현재 5-question sample에 대해 수행되었습니다.

## 💼 Job Posting Source & Requirement Mapping

이 프로젝트의 주요 대상 공고는 **Iyuno AI Agent Engineer**입니다.

* Company: Iyuno
* Position: AI Agent Engineer
* Location: Seoul / Hybrid
* Employment: Full-time
* Requisition: JR101122
* Application Deadline: 2026-09-30
* Job Posting: https://iyuno.wd3.myworkdayjobs.com/careers/job/seoul/ai-agent-engineer_jr101122

| Job Requirement    | Portfolio Implementation          |
| ------------------ | --------------------------------- |
| LLM 기반 AI Agent 설계 | Gemini AI Agent                   |
| RAG 검색·응답 시스템      | NIST + ChromaDB RAG               |
| Tool Calling       | `search_documents` Tool           |
| API / 데이터 통합       | Gemini API + ChromaDB             |
| 다단계 workflow       | Agent → Tool → Retrieval → Answer |
| 평가 및 품질 측정         | Recall@k / Faithfulness / Latency |
| Reliability        | pytest + GitHub Actions CI        |
| Working Demo       | Streamlit                         |

과제에서 추가 선택 트랙으로 제공된 RideFlux 공고:

* RideFlux 2026 H2 Engineering Recruitment
* https://inthiswork.com/archives/393239
* Deadline: 2026-09-27

본 repository의 실제 구현 및 평가는 **Iyuno AI Agent Engineer 공고**를 기준으로 진행했습니다.

## 📈 Evaluation Artifacts

30개의 평가 질문을 이용한 retrieval evaluation 결과:

| Metric                    |        Result |
| ------------------------- | ------------: |
| Recall@1                  |     **0.767** |
| Recall@3                  |     **0.933** |
| Recall@5                  |     **0.933** |
| Average Retrieval Latency | **0.009 sec** |

Faithfulness 결과:

| Metric                 |    Result |
| ---------------------- | --------: |
| Questions attempted    |         5 |
| Successfully evaluated |         5 |
| Faithful answers       |         5 |
| Faithfulness           | **1.000** |

> Faithfulness 결과는 전체 30문항이 아니라 **5-question sample**에 대한 결과입니다.

관련 평가 파일:

* [Evaluation Metrics](evaluation/metrics.json)
* [Recall Metrics Graph](evaluation/plots/recall_metrics.png)
* [Latency Graph](evaluation/plots/latency.png)
* [Evaluation Summary Graph](evaluation/plots/evaluation_summary.png)
* [Evaluation Plot Script](eval/create_plots.py)

## 📚 Data Sources & Licensing

이 프로젝트는 NIST에서 공개한 AI 및 Cybersecurity 관련 기술 문서를 사용합니다.

* Source organization: National Institute of Standards and Technology (NIST)
* Documents: **21**
* Processed chunks: **7,391**
* Processing date: **2026-09-23**
* Original public PDF files are not redistributed in this repository.

문서 출처, 처리 과정, attribution 및 licensing 정보:

[DATA_SOURCES.md](DATA_SOURCES.md)

## 🔒 Security

* API key는 `.env` 환경변수로 관리합니다.
* `.env`는 `.gitignore`에 포함되어 있습니다.
* API credentials는 GitHub repository에 포함하지 않습니다.
* Raw downloaded documents는 Git에 포함하지 않습니다.
* Local ChromaDB 데이터도 Git에 포함하지 않습니다.
* 개인정보 및 사내 비공개 데이터 대신 공개 NIST 문서를 사용합니다.

## ⚠️ Limitations

현재 프로젝트에는 다음과 같은 제한사항이 있습니다.

* Retrieval 평가는 exact chunk-level relevance가 아닌 **source-level Recall@k**를 사용합니다.
* Faithfulness는 전체 30문항이 아닌 **5-question sample**에 대해 평가했습니다.
* 질문 표현과 문서 용어에 따라 retrieval 결과가 달라질 수 있습니다.
* 현재 Agent는 document search 중심의 단일 Tool을 사용합니다.
* Fresh clone에서는 ChromaDB를 다시 생성해야 합니다.
* LLM response latency는 Gemini API와 네트워크 상태에 영향을 받습니다.
* 현재 별도의 public cloud deployment는 포함하지 않았습니다.

## 🔁 Reproducibility

Fresh clone 환경에서는 다음 순서로 프로젝트를 재현할 수 있습니다.

### 1. Clone

```powershell
git clone https://github.com/lhjk7654/iyuno-agent-portfolio.git
cd iyuno-agent-portfolio
```

### 2. Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure API Key

프로젝트 루트에 `.env` 파일을 생성합니다.

```text
GEMINI_API_KEY=your_api_key_here
```

### 5. Build Vector Database

```powershell
python -m app.ingest
python -m app.extract
python -m app.chunk
python -m app.embeddings
```

### 6. Run Demo

```powershell
python -m streamlit run app/web.py
```

### 7. Run Tests

```powershell
python -m pytest -q
```

### 8. Run Evaluation

```powershell
python -m eval.evaluate
python -m eval.faithfulness
```

## 🚀 Future Improvements

* Faithfulness 평가를 전체 평가 질문으로 확대
* 추가 Tool 및 외부 API integration
* Query routing 개선
* Retrieval reranking 적용
* Token usage 및 LLM cost tracking 강화
* CI pipeline에 automated evaluation 추가
* 사용자 feedback loop 구현
* Streamlit public deployment

## 📝 Project Summary

이 프로젝트는 Iyuno AI Agent Engineer 채용공고의 핵심 요구사항을 실제 작동하는 GitHub 프로젝트로 구현한 포트폴리오입니다.

주요 구현 요소:

* LLM-based AI Agent orchestration
* RAG-based document retrieval
* Citation-aware responses
* Tool Calling
* 21개의 NIST 공개 문서 및 7,391 chunks
* 30-question retrieval evaluation
* Faithfulness evaluation
* Latency measurement
* pytest automated testing
* GitHub Actions CI
* Streamlit demonstration
* Reproducible data processing pipeline

즉, **작동하는 AI Agent 데모 + 정량적 평가 + 테스트 + CI + 재현 가능한 문서화**를 하나의 GitHub repository로 구성했습니다.

## 🔗 Repository

https://github.com/lhjk7654/iyuno-agent-portfolio
