# Iyuno AI Security RAG Agent

공개된 NIST 사이버보안·AI 보안 문서를 기반으로 질문에 답변하는 **AI Agent / RAG 기반 보안 지식 검색 시스템**입니다.

사용자의 질문을 임베딩하여 관련 문서를 검색하고, 검색된 문서 내용을 Gemini LLM에 전달하여 답변을 생성합니다. 답변에는 사용된 문서와 chunk 정보를 함께 표시하여 근거를 확인할 수 있도록 구성했습니다.

## 1. Project Overview

### 목표

사이버보안 및 AI 보안 분야의 공개 문서를 수집하고, 다음 과정을 자동화하는 RAG 시스템을 구현했습니다.

```text
User Question
      ↓
Embedding
      ↓
Vector Search
      ↓
Relevant Documents
      ↓
Context Construction
      ↓
Gemini LLM
      ↓
Answer + Sources
```

### 주요 기능

* NIST 공개 문서 21개 수집
* PDF 텍스트 추출
* 문서 chunking
* Sentence Transformer 기반 임베딩
* ChromaDB 벡터 데이터베이스 구축
* Semantic Search
* Gemini 기반 RAG 답변 생성
* 답변 출처 표시
* Retrieval latency 측정
* LLM latency 및 token usage 측정
* Recall@1 / Recall@3 / Recall@5 평가
* pytest 기반 자동 테스트
* GitHub Actions 기반 CI

---

## 2. Tech Stack

| Category        | Technology            |
| --------------- | --------------------- |
| Language        | Python 3.13           |
| LLM             | Google Gemini         |
| Embedding       | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2`    |
| Vector DB       | ChromaDB              |
| PDF Processing  | pypdf                 |
| Environment     | python-dotenv         |
| Testing         | pytest                |
| CI              | GitHub Actions        |
| Version Control | Git / GitHub          |

---

## 3. Data

본 프로젝트에서는 NIST에서 공개한 AI 및 사이버보안 관련 문서를 사용했습니다.

총 **21개의 공개 문서**를 수집했으며, 문서에는 다음과 같은 주제가 포함됩니다.

* AI Risk Management Framework
* Generative AI
* Cybersecurity Framework
* Privacy Framework
* Zero Trust Architecture
* Risk Management Framework
* Security Controls
* Incident Response
* Secure Software Development
* Cybersecurity Supply Chain Risk Management
* Penetration Testing
* Digital Identity
* Cryptographic Key Management
* Log Management
* Cloud Computing Security
* Container Security
* Intrusion Detection and Prevention
* Computer Forensics

원본 문서는 NIST 공개 문서이며 프로젝트 실행 시 `app/ingest.py`를 통해 다운로드할 수 있습니다.

---

## 4. Project Structure

```text
iyuno-agent-portfolio/
│
├── app/
│   ├── __init__.py
│   ├── ingest.py
│   ├── extract.py
│   ├── chunk.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── rag.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── chunks/
│   └── chroma/
│
├── eval/
│   ├── questions.json
│   ├── evaluate.py
│   └── results.json
│
├── tests/
│   └── test_rag.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── requirements.txt
```

`data/raw`, `data/processed`, `data/chunks`, `data/chroma`는 실행 과정에서 생성되는 데이터이므로 Git 저장소에는 포함하지 않습니다.

---

## 5. Installation

### 5.1 Clone Repository

```bash
git clone https://github.com/lhjk7654/iyuno-agent-portfolio.git
cd iyuno-agent-portfolio
```

### 5.2 Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

가상환경 활성화:

```powershell
.venv\Scripts\Activate.ps1
```

### 5.3 Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 6. API Key

프로젝트 루트에 `.env` 파일을 생성하고 Gemini API Key를 설정합니다.

```text
GEMINI_API_KEY=YOUR_API_KEY
```

API Key는 GitHub에 업로드하지 않습니다.

`.gitignore`에 `.env`가 포함되어 있습니다.

---

## 7. Data Pipeline

### Step 1. Download Documents

```powershell
python -m app.ingest
```

NIST 공개 PDF 문서를 `data/raw/`에 저장합니다.

### Step 2. Extract Text

```powershell
python -m app.extract
```

PDF에서 텍스트를 추출하여 `data/processed/`에 저장합니다.

### Step 3. Chunk Documents

```powershell
python -m app.chunk
```

문서를 일정한 크기의 chunk로 분할합니다.

현재 설정:

```text
Chunk size: 1200 characters
Overlap: 200 characters
```

총 **7,391개 chunk**를 생성했습니다.

### Step 4. Create Embeddings

```powershell
python -m app.embeddings
```

`all-MiniLM-L6-v2` 모델을 이용해 문서를 벡터화하고 ChromaDB에 저장합니다.

---

## 8. RAG Query

RAG 시스템을 실행하려면:

```powershell
python -m app.rag
```

예시 질문:

```text
What are the characteristics of trustworthy AI?
```

시스템은 관련 문서를 검색한 후 Gemini에 전달하여 답변을 생성합니다.

답변에는 사용된 문서와 chunk 정보가 포함됩니다.

예:

```text
Sources

- nist_ai_rmf.txt — Chunk 32
- nist_ai_rmf.txt — Chunk 33
- nist_ai_rmf.txt — Chunk 36
```

---

## 9. Performance Measurement

RAG 실행 시 다음 항목을 측정합니다.

* Prompt tokens
* Completion tokens
* Total tokens
* Retrieval latency
* LLM latency
* Total latency

예시 실행 결과:

```text
Prompt tokens:     1484
Completion tokens: 207
Total tokens:      2305

Retrieval latency: 0.055s
LLM latency:       6.568s
Total latency:     6.623s
```

Token usage 값은 Gemini API가 반환한 usage 정보를 기준으로 기록합니다.

---

## 10. Evaluation

30개의 질문을 사용하여 retrieval 성능을 평가했습니다.

평가 기준은 질문에 대한 정답 문서가 Top-k 검색 결과에 포함되는지를 확인하는 **source-level Recall@k**입니다.

### Results

| Metric                    | Result |
| ------------------------- | -----: |
| Questions                 |     30 |
| Recall@1                  |  0.767 |
| Recall@3                  |  0.933 |
| Recall@5                  |  0.933 |
| Average Retrieval Latency | 0.009s |

즉, 30개의 평가 질문에서 정답 문서가 Top-3 검색 결과에 포함된 비율은 **93.3%**였습니다.

평가 결과는 다음 파일에 저장됩니다.

```text
eval/results.json
```

---

## 11. Testing

pytest를 사용하여 RAG 검색 및 context construction에 대한 기본 테스트를 구성했습니다.

실행:

```powershell
python -m pytest -q
```

현재 테스트 결과:

```text
3 passed
```

테스트 항목:

1. Retriever가 검색 결과를 반환하는지 확인
2. 특정 질문에서 올바른 NIST 문서를 검색하는지 확인
3. 생성된 context에 source 및 chunk 정보가 포함되는지 확인

---

## 12. Continuous Integration

GitHub Actions를 이용하여 코드가 push되거나 Pull Request가 생성될 때 자동으로 테스트를 실행하도록 구성했습니다.

Workflow:

```text
.github/workflows/ci.yml
```

CI 과정:

```text
GitHub Push / Pull Request
          ↓
Checkout Repository
          ↓
Setup Python 3.13
          ↓
Install Dependencies
          ↓
Run pytest
          ↓
Pass / Fail
```

---

## 13. Limitations

현재 시스템에는 다음과 같은 한계가 있습니다.

### Retrieval

현재 평가에서는 문서 단위의 Recall@k를 사용합니다. 따라서 동일 문서 안에서 정확한 chunk를 검색했는지까지는 평가하지 않습니다.

### Chunking

현재는 고정 길이 character-based chunking을 사용합니다. 문서의 heading이나 문단 구조를 완전히 반영하는 semantic chunking은 적용하지 않았습니다.

### Faithfulness

LLM 기반 faithfulness 평가는 Gemini API의 무료 quota 제한으로 인해 전체 평가를 완료하지 못했습니다. 따라서 현재 README에서는 retrieval 평가 결과를 주요 정량 평가 결과로 사용합니다.

### Vector Database

ChromaDB 데이터는 실행 시 생성되는 파일이므로 GitHub repository에는 저장하지 않습니다. 프로젝트를 새 환경에서 실행할 경우 문서 다운로드부터 embedding 생성까지의 pipeline을 다시 실행해야 합니다.

---

## 14. Future Improvements

향후 다음 기능을 추가할 수 있습니다.

* Streamlit 기반 Web UI
* FastAPI API 서버
* Page-level citation
* Semantic chunking
* Hybrid search
* Reranking
* 더 많은 evaluation questions
* Faithfulness / Answer Relevance 평가
* Tool calling 기반 보안 도구 연동
* Docker 환경 구성
* Agent workflow 확장

---

## 15. Example

질문:

```text
What are the characteristics of trustworthy AI?
```

RAG 시스템은 NIST AI Risk Management Framework에서 관련 내용을 검색하고 다음과 같은 주요 특성을 기반으로 답변을 생성합니다.

```text
- Valid and reliable
- Safe
- Secure and resilient
- Accountable and transparent
- Explainable and interpretable
- Privacy-enhanced
- Fair with harmful bias managed
```

답변에는 관련 NIST 문서와 chunk 정보가 함께 제공됩니다.

---

## 16. Project Repository

GitHub:

https://github.com/lhjk7654/iyuno-agent-portfolio