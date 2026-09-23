\# Data Sources \& Licensing



\## 1. Dataset Overview



This project uses publicly available NIST technical publications

as the knowledge base for the RAG and AI Agent system.



\- Source organization: National Institute of Standards and Technology (NIST)

\- Number of source documents: 21

\- Number of processed chunks: 7,391

\- Data type: Public technical PDF publications

\- Primary purpose: Security and AI knowledge retrieval

\- Collection and processing date: 2026-09-23



\## 2. Data Sources



The knowledge base consists of publicly available NIST publications

covering topics including:



\- NIST AI Risk Management Framework

\- NIST Generative AI Profile

\- NIST Cybersecurity Framework

\- NIST Cybersecurity Controls

\- NIST Zero Trust Architecture

\- NIST Incident Response

\- NIST Supply Chain Security

\- NIST Secure Software Development Framework

\- NIST Privacy Framework

\- NIST Risk Assessment

\- NIST Digital Identity

\- NIST Cloud Computing

\- NIST Penetration Testing

\- NIST Key Management

\- NIST Log Management

\- NIST System Security Engineering

\- NIST Forensics

\- NIST Container Security

\- NIST Intrusion Detection / Prevention



Official organization:



National Institute of Standards and Technology (NIST)



https://www.nist.gov/



\## 3. Copyright and Licensing



The source documents used in this project are publicly available

NIST technical publications.



This project does not claim ownership of the original NIST publications.



The original source PDFs are not redistributed in this GitHub repository.

They were downloaded and processed locally for the purpose of building

the RAG knowledge base.



Only the application code, evaluation configuration, metrics,

and generated visualization artifacts are maintained in this repository.



Users should review the copyright and licensing information associated

with each original publication before redistributing source materials.



\## 4. Attribution



Source organization:



National Institute of Standards and Technology (NIST),

U.S. Department of Commerce.



The NIST publications were accessed from publicly available

official NIST resources and processed for educational and portfolio

development purposes.



\## 5. Data Processing Pipeline



The source documents were processed through the following pipeline:



Public NIST PDF

&#x20;   ↓

PDF text extraction

&#x20;   ↓

Text chunking

&#x20;   ↓

Sentence Transformer embedding

&#x20;   ↓

ChromaDB vector storage

&#x20;   ↓

Semantic retrieval

&#x20;   ↓

Gemini-based answer generation



Processing configuration:



\- Chunk size: 1,200 characters

\- Chunk overlap: 200 characters

\- Embedding model: sentence-transformers/all-MiniLM-L6-v2

\- Vector database: ChromaDB

\- Processed chunks: 7,391



\## 6. Evaluation Dataset



The evaluation dataset contains 30 questions designed to test

retrieval performance against the NIST knowledge base.



Retrieval evaluation:



\- Evaluation questions: 30

\- Recall@1: 0.767

\- Recall@3: 0.933

\- Recall@5: 0.933

\- Average retrieval latency: 0.009 seconds



Faithfulness evaluation:



\- Questions attempted: 5

\- Successfully evaluated: 5

\- Faithful answers: 5

\- Faithfulness score: 1.000



Important:



The faithfulness score is based on a 5-question sample and should

not be interpreted as a 30-question faithfulness evaluation.



\## 7. Reproducibility



The data processing pipeline can be reproduced using the project scripts.



Example:



python -m app.ingest

python -m app.extract

python -m app.chunk

python -m app.embeddings



Evaluation:



python -m eval.evaluate

python -m eval.faithfulness



The generated raw documents, processed chunks, and ChromaDB files

are excluded from GitHub through .gitignore.



\## 8. Data Storage Policy



The following generated/local data is intentionally excluded from

the GitHub repository:



\- data/raw/

\- data/processed/

\- data/chunks/

\- data/chroma/



This keeps the repository lightweight and avoids redistributing

the original source documents.



The repository stores reproducible processing code and evaluation

artifacts instead.



\## 9. Project Creation and Data Processing Date



Project/data processing date:



2026-09-23



Evaluation artifact creation date:



2026-09-23



The evaluation results represent the state of the project and dataset

at the time of evaluation.



\## 10. References



NIST official website:

https://www.nist.gov/



NIST Publications:

https://www.nist.gov/nist-research-library/nist-publications



NIST Copyrights and Disclaimers:

https://www.nist.gov/copyrights-disclaimers

