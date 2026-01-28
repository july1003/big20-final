## 1. DBeaver 연결 설정 값

DBeaver에서 **새 연결(New Connection)**을 누르고 **Oracle**을 선택한 뒤, 다음 항목들을 입력하세요.

| **항목**            | **입력 값** | **비고**                      |
| ------------------------- | ----------------- | ----------------------------------- |
| **Connection Type** | **Basic**   | 기본 설정                           |
| **Host**            | 192.68.40.54      |                                     |
| **Port**            | `1521`          |                                     |
| **Database (SID)**  | `XE`            | `gvenzl/oracle-xe`이미지의 기본값 |
| **Username**        | `SYSTEM`        | 또는 `.env`에 설정한 계정         |
| **Password**        | oracle_pass       | `ORACLE_PASSWORD`값               |

## 2. 오라클 DB 작업

```
관계형 데이터베이스 (Oracle) 는 데이터 무결성을 보장하기 위해 사용됩니다 .

● **Users (** 사용자 **):** id, email, role (candidate/recruiter), password_hash, created_at.
● **Interviews (** 면접 세션 **):** id, candidate_id, job_posting_id, status(scheduled/live/completed), start_time, end_time, overall_score.
● **Questions (** 질문 은행 **):** id, content, category, difficulty, rubric_json ( 평가 기준 ), vector_id
(Vector DB 참조 ).
● **Transcripts (** 대화 기록 **):** id, interview_id, speaker (AI/User), text, timestamp, sentiment_score.
● **Evaluation_Reports (** 평가 리포트 **):** id, interview_id, technical_score, communication_score, cultural_fit_score, summary_text, details_json.
```

식별된 RFP 요구사항을 바탕으로 Docker 환경의 Oracle XE에서 실제 서비스를 운영할 수 있는 수준까지의 설정 과정을 **Step-by-Step**으로 정리해 드립니다.

이미 Docker 컨테이너가 실행 중이라는 가정하에, DBeaver를 사용하거나 `docker exec`를 통해 작업하시면 됩니다.

---

### Step 1. 관리자(SYSTEM) 계정으로 접속 및 전용 사용자 생성

Oracle은 관리자 계정(SYSTEM)으로 직접 데이터를 넣기보다, 서비스 전용 사용자(Schema)를 만들어 사용하는 것이 표준입니다.

1. **DBeaver**에서 위에서 설정한 `SYSTEM` 계정으로 접속합니다.
2. **SQL Editor**를 열고 아래 명령어를 실행하여 서비스를 위한 사용자를 생성합니다. (예: `my_service` 계정)

**SQL**

```
-- 1. 사용자 생성
CREATE USER rhetorica IDENTIFIED BY rhetorica_project2026;

-- 2. 권한 부여 
GRANT CONNECT, RESOURCE, UNLIMITED TABLESPACE TO rhetorica ;

-- 3. 테이블 생성 권한 명시적 부여
GRANT CREATE TABLE TO rhetorica;

-- 4. (혹시 모르니) 뷰, 시퀀스 생성 권한도 함께 주면 나중에 편합니다
GRANT CREATE VIEW, CREATE SEQUENCE TO rhetorica;

```

---

### Step 2. 생성한 사용자 계정으로 다시 접속

이제 `SYSTEM`이 아닌, 방금 만든 rhetorica 계정으로 DBeaver에서 **새로운 연결**을 만듭니다. 이후 모든 테이블 생성 작업은 이 계정에서 진행합니다.

---

### Step 5. 작업 확인

DBeaver의 왼쪽 **Database Navigator**에서 생성된 테이블 목록을 확인하고, `SELECT * FROM 테이블명;`을 실행하여 정상적으로 생성되었는지 확인하면 모든 준비가 끝납니다.

**정리하자면:**

1. 관리자로 접속 -> 2. 서비스 계정 생성 -> 3. 서비스 계정으로 재접속 -> 4. DDL(테이블 생성) 실행 순으로 진행하시면 됩니다!
