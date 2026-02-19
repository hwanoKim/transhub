---
description: 완성된 자막(SRT) 파일을 요청사항에 따라 수정합니다
argument-hint: <srt-or-video-path> "<요청사항>"
disable-model-invocation: true
---

# Video Subtitle Fix

완성된 SRT 자막 파일을 사용자 요청에 따라 수정한다.

## 입력

- `$ARGUMENTS`: `<파일경로> <요청사항>`
  - 첫 번째 토큰: SRT 또는 비디오 파일 경로
  - 나머지: 수정 요청사항 (따옴표 포함 가능)

경로가 `.mp4`, `.mkv` 등 비디오 파일이면 같은 디렉토리에서 같은 이름의 `.srt`를 찾는다.

예시:
```
/video-subtitle-fix c:/video.srt "hk는 히어로 킹으로 통일해줘"
/video-subtitle-fix c:/video.mp4 이름에 역할 넣어줘
/video-subtitle-fix c:/video.srt 3번째부터 10번째까지 다시 번역해줘
/video-subtitle-fix c:/video.srt 존댓말로 바꿔줘
```

## 파이프라인

### Step 1: 인자 파싱 + SRT 확인

1. `$ARGUMENTS`에서 파일 경로와 요청사항 분리
2. 비디오 확장자면 → 같은 이름의 `.srt` 탐색
3. SRT 없으면 중단, 경로 확인 요청

세그먼트 수를 빠르게 확인한다:
```bash
grep -c "^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]" "<SRT경로>"
```

### Step 2: 요청 분류

요청사항을 분석하여 **처리 전략**을 결정한다.

| 전략 | 조건 | 예시 |
|------|------|------|
| **A. 기계적 치환** | 용어/이름 변환, 표기 통일 | "hk→히어로 킹", "이름에 역할 넣어줘" |
| **B. 범위 지정 수정** | 특정 세그먼트 범위 | "3~10번째 다시 번역해줘" |
| **C. 전체 의미 수정** | 톤/문체 변경, 전체 재검토 | "존댓말로 바꿔줘", "전체적으로 다듬어줘" |

혼합 요청이면 각각 순차 실행한다 (예: "hk 통일하고 존댓말로" → A 먼저, C 이후).

### Step 3: 참고 자료 DB 로드

**DB 위치**: `.claude/skills/video-subtitle/refdb/`

1. `refdb/*/` 도메인 폴더를 Glob으로 확인
2. 각 `_config.yaml`의 `name`, `description`을 읽는다
3. **도메인 판별**: SRT 파일명 또는 요청사항의 키워드로 매칭
   - 파일명이나 경로에 도메인 힌트가 있으면 우선 사용
   - 판별 불가 시 SRT에서 첫 50줄만 Grep으로 키워드 탐색
   - 그래도 매칭 불가면 `_default/`만 사용
4. 매칭된 도메인 폴더의 YAML 전부 + `_default/` YAML을 Read

**YAML 스키마:**
- `terms.yaml` — 약어 (key, full, ko, context)
- `characters.yaml` — 캐릭터 (name, ko, aliases, description)
- `staff.yaml` — 팀원 (name, ko, aliases, role)
- `glossary.yaml` — 용어 (term, ko, note)

---

## 전략 A: 기계적 치환

**SRT 전체를 Read하지 않는다.** Grep과 Python으로 처리한다.

### A-1: 치환 맵 구성

요청사항 + DB 정보로 치환 규칙을 만든다.

예시:
```python
replacements = {
    "hk": "히어로 킹",
    "HK": "히어로 킹",
    # ... DB에서 추출
}
```

**인물 첫 등장 + 역할 표기** 요청 시:
- staff.yaml에서 name→ko, role 매핑 구성
- 각 인물의 첫 등장에만 `이름(역할)` 형식 적용, 이후는 `이름`만

### A-2: Grep으로 대상 확인

치환 대상이 실제로 SRT에 존재하는지 Grep으로 확인한다.
매칭 건수를 미리 파악하여 결과 보고에 활용.

### A-3: Python 일괄 치환

Bash로 Python 스크립트를 실행하여 한 번에 치환한다.

```bash
.venv/Scripts/python -c "
import re

# SRT 읽기
with open(r'<SRT경로>', 'r', encoding='utf-8') as f:
    content = f.read()

# 치환 (타임스탬프 줄은 건너뜀)
lines = content.split('\n')
result = []
for line in lines:
    if re.match(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->', line) or re.match(r'^\d+$', line.strip()):
        result.append(line)  # 인덱스/타임스탬프는 그대로
    else:
        # 치환 적용
        <치환 로직>
        result.append(line)

with open(r'<SRT경로>', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))
"
```

**인물 첫 등장 역할 표기**처럼 상태 추적이 필요한 치환은 Python 스크립트 내에서 `seen = set()`으로 관리한다.

→ **Step 4로 이동**

---

## 전략 B: 범위 지정 수정

### B-1: 범위 파싱

요청에서 세그먼트 범위를 추출한다 (예: "3번째부터 10번째" → 3~10).

### B-2: 해당 범위만 Read

SRT에서 해당 세그먼트 범위의 줄 번호를 계산하여 Read의 offset/limit으로 읽는다.

세그먼트 1개 ≈ 4줄 (인덱스 + 타임스탬프 + 텍스트 + 빈줄).
세그먼트 N의 시작 줄 ≈ `(N-1) * 4 + 1`.

정확한 위치가 필요하면:
```bash
grep -n "^<N>$" "<SRT경로>" | head -1
```

### B-3: 수정 + Edit

읽은 범위를 수정하고 Edit 도구로 해당 부분만 교체한다.

**수정 시 DB 참조**: 해당 범위 내 용어/이름은 DB 표기를 따른다.

→ **Step 4로 이동**

---

## 전략 C: 전체 의미 수정

톤/문체 변경, 전체 재검토 등 LLM이 문맥을 이해해야 하는 작업.

### C-1: 규모 판단

| 세그먼트 수 | 처리 방식 |
|-------------|-----------|
| **≤ 100** | 직접 처리 (전체 Read → 수정 → Write) |
| **101+** | 청크 분할 → 서브에이전트 병렬 |

### C-2a: 직접 처리 (≤ 100)

1. SRT 전체를 Read
2. 요청에 따라 수정 (DB 참조)
3. Write로 덮어쓰기

### C-2b: 청크 병렬 처리 (101+)

1. SRT를 약 100 세그먼트 단위로 논리적으로 분할 (Read의 offset/limit 활용)
2. 청크마다 `general-purpose` 서브에이전트 실행 (최대 4개 배치)
   - 각 에이전트에 전달: 청크 내용 + 요청사항 + DB 정보 + SRT 형식 규칙
   - 에이전트는 수정된 청크 SRT를 임시 파일에 Write
3. 모든 청크 완료 후 병합하여 최종 SRT 덮어쓰기

**서브에이전트에 반드시 전달:**
- 수정 요청사항
- DB 용어집 (terms, characters, staff, glossary)
- **타임스탬프 불변** 규칙
- SRT 형식 유지 규칙

→ **Step 4로 이동**

---

## Step 4: 결과 보고

수정 완료 후 간결하게 보고:

- 처리 전략 (A/B/C)
- 수정 건수 / 전체 세그먼트 수
- 주요 변경 요약 (예: "hk → 히어로 킹 12건", "톤 변경 전체")
- 변경되지 않은 자막은 언급하지 않음

## 공통 규칙

- **타임스탬프는 절대 변경하지 않는다**
- **SRT 형식 유지** (인덱스, 타임스탬프, 텍스트, 빈 줄)
- **DB 표기 우선** — DB에 정의된 번역/표기를 따른다
- **인물 첫 언급 시 `이름(역할)`** — staff.yaml 기반, 이후는 이름만
- **DB 동기화 필수** — SRT에서 용어/이름/역할을 수정하면 refdb의 해당 YAML도 반드시 함께 수정한다. SRT만 고치고 DB를 안 고치면 다음 작업에서 틀린 표기가 다시 적용된다
- 요청과 무관한 자막은 원본 그대로 유지
