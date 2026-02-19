---
title: 비디오 자동 자막 생성 커맨드
class: coding
status: closed
category: video
priority: normal
tags: [video, subtitle, command, subagent]
relations:
---

## Goal

비디오 파일 경로를 입력하면 자동으로 한글 자막 파일을 생성하는 Claude Code 커맨드(`/video-subtitle`)를 만든다.

### 사용 예시

```
/video-subtitle c:/video.mp4
→ c:/video.srt 생성
```

### 자막 형식

- **SRT** (SubRip Text) — 가장 범용적인 자막 형식. 거의 모든 플레이어/플랫폼에서 지원
- 필요 시 SMI 등 다른 형식 변환도 고려

### 구현 방향

커맨드 하나로 아래 파이프라인을 순차 실행:

1. **음성 추출** — 비디오에서 오디오 트랙 추출 (ffmpeg)
2. **음성 인식(STT)** — 오디오를 텍스트로 변환 (Whisper 등)
3. **자막 파일 생성** — 타임스탬프 + 텍스트를 SRT 형식으로 포맷팅
4. **출력** — 원본 비디오와 같은 경로에 `.srt` 파일 저장

### 제작 항목

#### 1. 커맨드 파일
- `.claude/commands/video-subtitle.md` — 슬래시 커맨드 정의
- 인자: `$ARGUMENTS` (비디오 파일 경로)

#### 2. 서브에이전트 (순차 파이프라인)
커맨드가 호출하는 서브에이전트들:

| 순서 | 에이전트 | 역할 | 입력 | 출력 |
|------|---------|------|------|------|
| 1 | `audio-extractor` | 비디오→오디오 추출 | 비디오 경로 | 오디오 파일 경로 |
| 2 | `speech-recognizer` | 오디오→텍스트(STT) | 오디오 경로 | 타임스탬프 포함 텍스트 |
| 3 | `subtitle-generator` | 텍스트→SRT 생성 | STT 결과 | .srt 파일 |

또는 하나의 에이전트가 전체 파이프라인을 관리하는 방식도 가능 (구현 시 판단).

#### 3. 필요 도구/의존성
- **ffmpeg** — 오디오 추출 (시스템에 설치 필요)
- **Whisper** (OpenAI) 또는 다른 STT 엔진 — 음성 인식
  - `openai-whisper` (로컬) 또는 Whisper API (클라우드)
  - 한국어 지원 확인 필요
- **Python 스크립트** — SRT 포맷 변환 유틸리티

#### 4. 고려 사항
- 긴 영상 처리 시 청크 분할 전략
- 한국어 음성 인식 정확도 검증
- 에러 처리 (지원하지 않는 비디오 형식, ffmpeg 미설치 등)
- 진행 상황 표시 (큰 파일 처리 시)

## Progress
- [x] 기술 스택 리서치 (STT 엔진 선정, ffmpeg 활용법)
- [x] 스킬 파일 작성 (`.claude/skills/video-subtitle/SKILL.md`)
      - [x] 5단계 파이프라인 설계 (음성추출 → STT → 번역 → SRT 작성 → 정리)
- [x] Python 유틸리티 스크립트 작성 (`scripts/transcribe.py`)

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|
| 1 | 962세그먼트 영상 실전 테스트 (fr→ko) | X | STT 성공(~5분), 번역 단계에서 실패. JSON 58K토큰으로 Read 불가, 300줄씩 8회+ 읽기 후 20분 소모, SRT 미생성. 대량 처리 파이프라인 개선 필요 → `20260219-1448-video-subtitle-chunking-pipeline` 티켓 생성 |

## Commits
- 초기 저장소 (커밋 없음) — 스킬 파일, 스크립트는 작업 트리에 구성됨
- 구현 아티팩트: `.claude/skills/video-subtitle/SKILL.md`, `scripts/transcribe.py`

## Notes
- 프로젝트 첫 티켓. 핵심 기능인 비디오 자동 자막 생성의 시작점
- 원래 서브에이전트 3개(audio-extractor, speech-recognizer, subtitle-generator) 계획 → 스킬 1개 + Python 스크립트 1개로 간결화
- **Whisper 선정 근거 (세션 논의)**:
  - Whisper의 `task="translate"` 옵션은 모든 언어 → **영어로만** 번역 가능. 한국어 번역 불가
  - 따라서 "Whisper STT → Claude Code 번역" 구조 채택
  - Claude Code가 JSON을 읽고 직접 한국어로 의역 — 별도 번역 API 불필요, 자막 품질 우수
  - Whisper(large-v3)는 오픈소스 STT 최상위권. 속도 필요 시 faster-whisper로 교체 가능
- **의존성 확인 완료**: ffmpeg 8.0.1, openai-whisper 20250625 설치됨
