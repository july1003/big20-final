# 서버 하드웨어 스펙에 맞는 모델 추천

## 서버사양

장치 이름 DESKTOP-PD2UJVD

프로세서 AMD Ryzen 5 PRO 4650G with Radeon Graphics   3.70 GHz

설치된 RAM 32.0GB

저장소 466 GB SSD Samsung SSD 970 EVO 500GB

그래픽 카드 NVIDIA GeForce GTX 1660 SUPER (6 GB)

장치 ID 38D638E4-70AE-46F3-83B7-03281568EEF2

제품 ID 00330-80000-00000-AA354

시스템 종류 64비트 운영 체제, x64 기반 프로세서

현재 보유하신 **GTX 1660 SUPER(6GB VRAM)**와 **32GB RAM** 사양은 온프레미스 AI 환경을 구축하기에 매우 효율적인 사양입니다. 다만, 그래픽 카드 메모리(VRAM)가 6GB로 한정적이기 때문에 **경량화 모델(Quantized models)**과 **메모리 효율화 라이브러리**를 조합하는 것이 핵심입니다.

모의 면접 시스템의 단계별 필수 모델과 호환성 있는 라이브러리 버전을 추천합니다.

### 1. 단계별 추천 모델 (6GB VRAM 최적화)

| **구분**            | **추천 모델**                          | **선정 이유**                                                                                   |
| ------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **STT (음성 인식)** | **Faster-Whisper (small 또는 medium)** | 일반 Whisper보다 4배 이상 빠르며,`small`모델은 VRAM 2GB 미만으로 구동 가능합니다.                   |
| **LLM (평가/대화)** | **Llama-3.1-8B-Instruct (Q4_K_M)**     | 4비트 양자화 시 약 5GB VRAM을 사용하며, 한국어 이해도가 가장 뛰어난 8B급 모델입니다.                  |
| **TTS (음성 합성)** | **Edge-TTS**또는**Glow-TTS**     | `Edge-TTS`는 CPU 부담이 거의 없고 음질이 뛰어나며, 완전 로컬을 원할 경우 `Glow-TTS`가 가볍습니다. |

---

### 2. 호환성 있는 라이브러리 버전 (requirements.txt)

현재 사양에서 가장 안정적으로 동작하는 **Python 3.10** 환경 기준의 패키지 구성입니다.

**Plaintext**

```
# 핵심 프레임워크 (CUDA 12.1 대응)
torch==2.3.1+cu121
torchaudio==2.3.1+cu121
--extra-index-url https://download.pytorch.org/whl/cu121

# LLM 인터페이스 및 오케스트레이션
langchain==0.2.14
langchain-community==0.2.12
ollama==0.3.1  # Ollama를 로컬 서버로 실행 시 권장

# STT (음성 인식)
faster-whisper==1.0.3

# TTS (음성 합성)
edge-tts==6.1.12  # 속도와 품질 면에서 가장 무난함

# API 서버 및 환경 설정
fastapi==0.112.1
uvicorn==0.30.6
python-dotenv==1.0.1
psycopg2-binary==2.9.9
```

---

### 3. 구축 전략 및 최적화 팁

1. LLM 실행 (Ollama 권장):
   직접 transformers 라이브러리로 모델을 로드하기보다 Ollama를 백그라운드 서버로 사용하는 것을 추천합니다. VRAM이 부족할 경우 자동으로 시스템 RAM(32GB)을 활용하는 메모리 스와핑 기능이 있어 6GB 이상의 모델도 끊김 없이 처리할 수 있습니다.

   * 설치 후: `ollama run llama3.1`
2. STT 최적화 (Faster-Whisper):
   메모리 점유를 줄이기 위해 아래와 같이 int8 연산 모드를 사용하세요.
   **Python**

   ```
   from faster_whisper import WhisperModel
   model = WhisperModel("small", device="cuda", compute_type="int8_float16")
   ```

3. 메모리 충돌 방지:
   STT와 LLM을 동시에 GPU에 올리면 6GB 메모리가 초과될 수 있습니다.

   * 사용자의 음성을 텍스트로 변환하는 동안에는 LLM을 대기시키고, 변환이 끝난 후 LLM에 텍스트를 전달하는 **순차적 처리(Sequential Workflow)** 로직을 구현하는 것이 시스템 안정성에 유리합니다.
4. 저장소 활용:
   Samsung 970 EVO는 속도가 매우 빠르므로 모델 로딩 시간은 걱정하지 않으셔도 됩니다. 다만, 대형 모델 파일들이 용량을 많이 차지하므로 모델은 가급적 /models 폴더를 별도로 지정하여 관리하는 것이 좋습니다.

이 구성은 현재 하드웨어의 성능을 최대한 끌어내면서도 모델 간의 충돌 없이 모의 면접 시스템을 안정적으로 운영할 수 있는 최적의 조합입니다. 구축 과정에서 특정 모델의 추론 속도를 높이는 방법이나 프롬프트 엔지니어링이 필요하시면 추가로 말씀해 주세요.
