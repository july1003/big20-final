# 서버별 최적 LLM 모델 추천 및 설정 가이드

각 서버(`Ethos`, `Logos`, `Pathos`)의 역할과 `docker-compose.yml` 설정을 분석하여 가장 적합한 온프레미스 모델(Ollama 기반)을 추천합니다.

## 1. Logos (실시간 면접관 & 메인 LLM)

**역할**: `web`(FastAPI), `rt_worker` (실시간 꼬리질문), `ollama` (메인 AI).
**핵심 요구사항**: 빠른 응답 속도(Latency 중요), 한국어 대화 능력, 맥락 파악(Context).

### ✅ 추천 모델: Qwen 2.5 (7B)

- **이유**: 7B 체급에서 한국어 성능과 지시 이행 능력(Instruction Following)이 가장 우수합니다. 실시간 면접 상황에서 면접관 페르소나를 유지하고 적절한 꼬리 질문을 생성하는 데 탁월합니다.
- **대안 (속도 최우선)**: `Llama 3.1 8B` (범용성 우수하나 VRAM 소모가 약간 더 큼), `Phi-3.5 Mini` (매우 빠르지만 한국어 뉘앙스 처리가 다소 부족할 수 있음).

**설치 명령 (Logos 서버 내부)**:

```bash
docker exec -it ollama_server ollama pull qwen2.5:7b
```

---

## 2. Ethos (임베딩 및 데이터 처리)

**역할**: `embedding_server` (Ollama), `postgres` (Vector DB), `batch_app`.
**핵심 요구사항**: 텍스트를 고품질 벡터로 변환(Embedding Quality), RAG(검색 증강 생성) 성능 최적화.

### ✅ 추천 모델: mxbai-embed-large

- **이유**: 현재 온프레미스 임베딩 모델 중 성능(MTEB 벤치마크)이 매우 우수하며, 다국어 및 한국어 검색 성능도 준수합니다. Ollama에서 바로 사용 가능합니다.
- **대안**: `nomic-embed-text` (긴 문맥 처리에 유리).

**설치 명령 (Ethos 서버 내부)**:

```bash
docker exec -it ollama_embedding ollama pull mxbai-embed-large
```

00.planning/서버구성.md 파일을 분석한 결과, **Ethos (Server C)**는 데이터의 중심지로서 **PostgreSQL(pgvector)**와 **Oracle**을 구동하며, 배치 작업을 통해 데이터를 적재하는 역할을 담당하고 있습니다.

이러한 구성에서 **AI 면접 시스템(레토리카)**을 위한 최적의 임베딩 모델로 **nomic-embed-text** 를 강력히 추천합니다.

### 💡 추천 모델: 설치함

```script
nomic-embed-text
```

**추천 이유:**

1. **긴 문맥 처리(Long Context) 능력** :

* 면접 시스템의 특성상 **이력서(Resume), 자기소개서, 면접 대화록** 등 긴 텍스트를 처리해야 합니다.
* `nomic-embed-text` 는 **8192 토큰**의 긴 컨텍스트 윈도우를 지원하여, 긴 이력서도 잘리지 않고 한 번에 임베딩하여 문맥을 파악하는 데 매우 유리합니다.

2. **Ollama와의 호환성 및 효율성** :

* Ethos(Server C)는 이미 DB 구동으로 리소스를 사용 중입니다. 이 모델은 상대적으로 가벼우면서도 준수한 성능을 보여주며, Ollama에서 공식적으로 밀고 있는 임베딩 모델이라 설치와 연동이 매우 간편합니다.
* PostgreSQL(pgvector)와 함께 RAG(검색 증강 생성) 시스템을 구축할 때 표준처럼 사용되는 모델입니다.

3. **검색 성능 (Retrieval Performance)** :

* MTEB(Massive Text Embedding Benchmark) 리더보드에서 상위권을 기록하며, 특히 질문-답변 검색(QA Retrieval) 성능이 뛰어나 면접 질문 매칭에 적합합니다.

### 🚀 설치 및 적용 방법

Ethos 서버(Server C)가 Ollama가 실행 중인 상태라면, 아래 명령어로 모델을 다운로드하세요.

```bash
# Ethos 서버 터미널 또는 도커 컨테이너 내부
ollama pull nomic-embed-text
```

**대안 (한국어 특화가 더 필요할 경우):** 만약 실제 테스트 시 한국어 뉘앙스 처리가 다소 아쉽다면, 다국어 성능이 강화된

**mxbai-embed-large** 또는 **bge-m3** (Ollama 라이브러리 지원 확인 필요)를 대안으로 고려할 수 있습니다. 하지만 시작은 **nomic-embed-text**로 하시는 것이 시스템 구성상 가장 무난하고 효율적입니다.

### 모델 변경시 고려사항

임베딩 모델을 변경할 때 가장 중요한 고려사항은 "**기존 데이터와의 호환성이 깨진다**"는 점입니다. 구체적으로 다음 두 가지를 반드시 고려해야 합니다.

1. **벡터 차원(Dimension) 불일치** :

* nomic-embed-text 는 **768**차원 벡터를 생성합니다.
* 만약 나중에 **1024**차원이나 **384**차원을 사용하는 다른 모델로 변경하면, DB 테이블(pgvector 컬럼)의 차원 설정과 맞지 않아 에러가 발생합니다.
* **대응:** DB 테이블의 벡터 컬럼 차원을 수정(ALTER TABLE)해야 합니다.

2. **벡터 공간(Vector Space)의 변화 ( **중요** )** :

* 모델마다 단어를 숫자로 변환하는 기준(벡터 공간)이 완전히 다릅니다. A 모델로 변환한 벡터와 B 모델로 변환한 벡터는 서로 비교(유사도 계산)할 수 없습니다.
* **대응:** 모델을 교체하는 순간, **DB에 저장해 둔 모든 기존 데이터(이력서, 질문 등)를 새로운 모델로 다시 임베딩(Re-embedding)**해서 업데이트해야 합니다. 데이터 양이 많다면 이 작업에 상당한 시간이 소요될 수 있습니다.

**요약:** 모델 변경은 단순 설정 변경이 아니라, **"DB 마이그레이션(벡터 데이터 전면 교체)"** 작업이 동반되어야 함을 미리 계획하셔야 합니다.

---

## 3. Pathos (정밀 분석 및 TTS)

**역할**: `analysis_worker` (심층 분석), `tts_service` (음성 합성).
**핵심 요구사항**: 속도보다는 정확하고 깊이 있는 분석, 긴 문장 생성 및 평가.

### ✅ 추천 모델: Llama 3.1 (8B) 또는 Gemma 2 (9B) -> VRAM 고려시 Qwen 2.5 (7B) 유지

- **이유**: `analysis_worker`는 비동기(`Celery`)로 동작하므로 실시간성보다 **분석의 깊이**가 중요합니다. `Gemma 2 9B`가 분석력은 좋지만 6GB VRAM에서 느릴 수 있으므로, 안정적인 `Llama 3.1 8B`나 `Qwen 2.5 7B`를 추천합니다. (Logos와 모델을 통일하면 관리 효율이 좋습니다.)
- **TTS**: `docker-compose.yml`에 이미 `tts_models/ko/krn/multi-vits` (Coqui TTS)가 지정되어 있어 추가 LLM 설정은 필요 없습니다.

**설치 명령 (Pathos에는 별도 Ollama 컨테이너가 없으므로 Logos나 Ethos의 Ollama를 활용하거나 필요시 추가)**:

- Pathos `docker-compose`에는 현재 `ollama` 컨테이너가 없습니다. 분석 작업은 보통 `Logos`의 `ollama` 서버 API를 호출하여 처리합니다. 따라서 Logos의 모델(Qwen 2.5)을 공용으로 사용하거나, 분석 전용으로 Logos에 `Llama 3.1`을 추가로 받아두고 API 호출 시 모델명만 다르게 지정하는 전략을 추천합니다.

---

## 요약

| 서버             | 역할             | 추천 모델                       | 설치 명령어                       |
| :--------------- | :--------------- | :------------------------------ | :-------------------------------- |
| **Logos**  | 실시간 면접관    | **Qwen 2.5 (7B)**         | `ollama pull qwen2.5:7b`        |
| **Ethos**  | 벡터 임베딩      | **mxbai-embed-large**     | `ollama pull mxbai-embed-large` |
| **Pathos** | 비동기 정밀 분석 | **Qwen 2.5** (Logos 공유) | (Logos 서버 활용)                 |
