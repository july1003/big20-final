# Ethos (에토스) - Central Data Node

## 이름의 유래

**Ethos**는 '성품', '신뢰'를 뜻하며 '윤리(Ethics)'의 어원입니다.
수사학에서 화자의 **고유한 성품과 신뢰성**을 의미하듯, 이 서버는 시스템 전체의 **데이터를 안전하게 보관**하고, **신뢰할 수 있는 정보(Golden Record)**를 제공하는 가장 기초가 되는 기지이기 때문에 붙여진 이름입니다.

## 주요 역할

데이터베이스, 벡터 저장소, 공통 배치 작업 등 **인프라와 데이터 지속성(Persistence)**을 담당합니다.

## 포함된 서비스 (Service Stack)

이 폴더의 `docker-compose.yml`은 다음 컨테이너들을 실행합니다:

1. **`postgres` (Vector DB)**:

   * **역할**: RAG(검색 증강 생성)를 위한 벡터 데이터와 일반 관계형 데이터를 저장합니다.
   * **이미지**: pgvector/pgvector
   * **포트**: 5432
2. **`oracle` (Enterprise DB)**:

   * **역할**: 기업 수준의 정형 데이터, 사용자 정보, 결제 정보 등을 저장합니다.
   * **포트**: 1521
3. **`embedding_server` (Ollama)**:

   * **역할**: 데이터 저장을 위해 텍스트를 벡터로 변환(Embedding)하는 전용 모델을 구동합니다.
   * **포트**: 11435
4. **`batch_app`**:

   * **역할**: 데이터베이스 유지보수, 백업, 통계 생성 등 데이터 중심의 배치 프로그램을 실행합니다.

## 실행 방법

```bash
docker-compose up -d --build
=> 에러나서 docker-compose.yml 에서 version remarked!
```
