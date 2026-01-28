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

| 서버 | 역할 | 추천 모델 | 설치 명령어 |
| :--- | :--- | :--- | :--- |
| **Logos** | 실시간 면접관 | **Qwen 2.5 (7B)** | `ollama pull qwen2.5:7b` |
| **Ethos** | 벡터 임베딩 | **mxbai-embed-large** | `ollama pull mxbai-embed-large` |
| **Pathos** | 비동기 정밀 분석 | **Qwen 2.5** (Logos 공유) | (Logos 서버 활용) |
