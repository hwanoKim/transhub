---
name: video-subtitle
description: 비디오 파일에서 자동으로 한글 자막(SRT)을 생성합니다. "자막 만들어줘", "subtitle 생성" 요청 시 사용.
argument-hint: <video-file-path>
disable-model-invocation: true
---

# Video Subtitle Generator

비디오 파일에서 한글 자막(SRT)을 자동 생성한다.

## 입력

- `$ARGUMENTS`: 비디오 파일 경로

## 변수 정의

파이프라인 전체에서 사용하는 경로:

| 변수 | 값 | 예시 |
|------|-----|------|
| `VIDEO` | `$ARGUMENTS` | `c:/videos/lecture.mp4` |
| `JSON` | `<비디오명>.transcription.json` | `c:/videos/lecture.transcription.json` |
| `SRT` | `<비디오명>.srt` | `c:/videos/lecture.srt` |
| `CHUNKS_DIR` | `<비디오명>_chunks/` | `c:/videos/lecture_chunks/` |

## 파이프라인

### Step 1: 음성 추출 + STT

**먼저 `JSON` 파일이 이미 존재하는지 확인한다.**

- **존재하면**: "transcription.json이 이미 있습니다. STT를 스킵합니다." → **Step 2로 건너뛰기**
- **없으면**: 아래 명령 실행

```bash
.venv/Scripts/python .claude/skills/video-subtitle/scripts/transcribe.py "$ARGUMENTS"
```

- 결과: `JSON` 파일 생성
- 시간이 걸릴 수 있음 (모델 로딩 + 변환)

> 모델 변경이 필요하면 `--model` 옵션 사용:
> `--model large` (더 정확, 느림) 또는 `--model small` (덜 정확, 빠름)

### Step 2: 세그먼트 수 확인 + 경로 분기

`JSON` 파일의 세그먼트 수를 확인하여 처리 경로를 결정한다.

```bash
.venv/Scripts/python -c "import json; d=json.load(open(r'<JSON경로>','r',encoding='utf-8')); print(f'Language: {d[\"language\"]}'); print(f'Segments: {len(d[\"segments\"])}')"
```

| 세그먼트 수 | 경로 | 설명 |
|-------------|------|------|
| **≤ 100** | → Step 3A | 직접 번역 (메인 세션) |
| **101+** | → Step 3B | 2-Pass 병렬 번역 |

---

### Step 3A: 직접 번역 (소량 ≤ 100)

`JSON` 파일을 Read로 읽고, 전체 세그먼트를 한번에 번역하여 SRT를 Write로 작성한다.

**번역 규칙:**
- 외국어 → 자연스러운 한국어. 직역보다 의역 우선
- 한국어 → 오탈자 교정, 구어체 정리, 불필요한 추임새 제거
- 타임스탬프(start, end)는 절대 변경하지 않음
- 문맥을 고려하여 앞뒤 세그먼트와 자연스럽게 이어지도록 번역
- 자막이므로 간결하게. 한 세그먼트당 2줄 이내 권장

**SRT 형식** (반드시 이 형식을 준수):
```
1
00:00:00,000 --> 00:00:02,500
안녕하세요 여러분

2
00:00:02,500 --> 00:00:05,000
오늘은 ...에 대해 이야기하겠습니다
```

**타임스탬프 변환 공식** (seconds → SRT format):
- `start` 또는 `end` 초 값을 `HH:MM:SS,mmm`으로 변환
- 예: `125.340` → `00:02:05,340`

→ **Step 4로 이동**

---

### Step 3B: 2-Pass 병렬 번역 (대량 101+)

#### 3B-1: 청크 분할

```bash
.venv/Scripts/python .claude/skills/video-subtitle/scripts/translate_chunks.py split "<JSON경로>" --chunk-size 50
```

- 결과: `CHUNKS_DIR`에 `chunk_001.json`, `chunk_002.json`, ... + `manifest.json` 생성
- 노이즈 세그먼트 자동 필터링 (반복 감탄사 등)

> **재개**: `CHUNKS_DIR`이 이미 존재하고 `manifest.json`이 있으면 분할을 스킵한다.

#### 3B-2: manifest.json 읽기

`CHUNKS_DIR/manifest.json`을 Read로 읽어 전체 청크 목록을 파악한다.

#### 3B-3: Pass 1 — 초벌 번역 + 문맥 수집 (병렬)

**서브에이전트를 병렬로 실행한다.** Task tool로 `general-purpose` 에이전트를 청크마다 하나씩 launch한다.

> **배치 크기**: 한 번에 최대 4개 에이전트를 병렬 실행한다. 19청크면 5배치 (4+4+4+4+3).

각 서브에이전트에게 전달할 프롬프트:

```
아래 청크 JSON 파일을 읽고 두 가지를 작성하라.

1. `draft_NNN.srt` — 세그먼트를 한국어로 번역한 SRT 파일
2. `context_NNN.md` — 이 청크의 문맥 정보

## 번역 규칙
- 외국어 → 자연스러운 한국어. 직역보다 의역 우선
- 타임스탬프(start, end)는 절대 변경하지 않음
- 자막이므로 간결하게. 한 세그먼트당 2줄 이내 권장

## SRT 형식
{인덱스}
{HH:MM:SS,mmm} --> {HH:MM:SS,mmm}
{번역된 텍스트}

타임스탬프 변환: 초 → HH:MM:SS,mmm (예: 125.340 → 00:02:05,340)

## context_NNN.md에 반드시 포함할 내용
- 이 청크의 대화 주제/흐름 요약 (1-2줄)
- 등장하는 고유명사, 인물명
- 전문용어나 번역 판단이 필요했던 표현 (원문 → 선택한 번역, 이유)
- 화자의 톤, 격식 수준 (반말/존댓말/캐주얼)
- 특이사항 (노이즈, 코드스위칭, 불명확한 발음 등)

## 파일 경로
- 입력: <CHUNKS_DIR>/chunk_NNN.json
- 출력: <CHUNKS_DIR>/draft_NNN.srt
- 출력: <CHUNKS_DIR>/context_NNN.md
```

> **재개**: 이미 `draft_NNN.srt`와 `context_NNN.md`가 모두 존재하면 해당 청크는 스킵한다.

#### 3B-4: style_guide.md 작성 (메인 에이전트)

**모든 Pass 1이 완료된 후**, 메인 세션에서 모든 `context_NNN.md`를 Read로 읽는다.

전체 문맥을 취합하여 `CHUNKS_DIR/style_guide.md`를 Write로 작성한다:

```markdown
## 전체 요약
(영상의 전체적인 내용, 맥락)

## 톤
(해요체/합니다체/반말 등 결정)

## 용어집
| 원문 | 번역 | 비고 |
|------|------|------|
| stock | 백로그 | 재고가 아닌 할 일 목록 의미 |
| show and tell | 발표 시간 | |

## 고유명사
| 원문 | 표기 |
|------|------|
| Maxilien | 막시밀리앙 |

## 특이사항
- (전체 청크에 공통 적용할 번역 지침)
```

#### 3B-5: Pass 2 — 스타일 기반 검토 (병렬)

**서브에이전트를 다시 병렬로 실행한다.** 배치 크기는 Pass 1과 동일 (최대 4개).

각 서브에이전트에게 전달할 프롬프트:

```
style_guide.md를 읽고, draft_NNN.srt를 검토하여 최종 chunk_NNN.srt를 작성하라.

## 검토 기준
1. style_guide.md의 톤(해요체/반말 등)과 일치하는지
2. 용어집의 번역을 따르는지
3. 고유명사 표기가 통일되어 있는지
4. 자연스러운 한국어인지 (어색한 직역 수정)

## 중요
- 타임스탬프는 절대 변경하지 않음
- 문제 없는 번역은 그대로 유지 (불필요한 수정 금지)
- 수정이 있으면 draft와 달라진 부분만 변경

## 파일 경로
- 참고: <CHUNKS_DIR>/style_guide.md
- 입력: <CHUNKS_DIR>/draft_NNN.srt
- 출력: <CHUNKS_DIR>/chunk_NNN.srt
```

> **재개**: 이미 `chunk_NNN.srt`가 존재하면 해당 청크는 스킵한다.

#### 3B-6: SRT 병합

모든 청크 SRT가 생성되면 병합:

```bash
.venv/Scripts/python .claude/skills/video-subtitle/scripts/translate_chunks.py merge "<CHUNKS_DIR>" "<SRT경로>"
```

- 인덱스 재번호, 타임스탬프 순 정렬 자동 처리

### Step 4: 정리

1. 결과 요약 보고:
   - 생성된 SRT 파일 경로
   - 총 자막 수
   - 감지된 원본 언어
   - (청크 모드였으면) 필터링된 노이즈 수, 청크 수
2. 중간 파일 삭제 (SRT 생성 성공 확인 후):
   ```bash
   rm "<JSON경로>"
   rm -rf "<CHUNKS_DIR>"
   ```
   최종 산출물은 `VIDEO`(원본)과 `SRT`(자막)만 남긴다.

## 에러 처리

| 상황 | 대응 |
|------|------|
| 파일 없음 | 사용자에게 경로 확인 요청 |
| ffmpeg 미설치 | "ffmpeg가 필요합니다. https://ffmpeg.org 에서 설치해주세요" |
| whisper 미설치 | `.venv/Scripts/pip install openai-whisper` 실행 |
| GPU 미감지 | CPU 모드로 진행됨을 안내 (느릴 수 있음) |
| 서브에이전트 실패 | 해당 청크만 재실행 (다른 청크는 스킵) |
| 청크 번역 중 세션 중단 | 재실행 시 각 단계(split/pass1/pass2)별로 완료된 파일 스킵 |
