---
title: 영/한 이중 자막 생성 (언어 선택용)
class: coding
status: backlog
category: video
priority: normal
tags: [video, subtitle, multilingual, srt, english, korean]
relations:
  follows: ["20260219-0704-[main]-subtitle-quality-system"]
---

## Goal

자막 생성 시 **영어 SRT + 한국어 SRT** 두 파일을 나눠서 생성하여, 플레이어에서 자막을 선택할 수 있게 한다.

**목적**: 한글 자막으로 시청하다가 헷갈리는 부분이 있을 때 영어 원문 자막으로 전환하여 확인할 수 있도록 함.

### 번역 흐름

```
원본 영상 (프랑스어 + 영어 혼재)
    │
    ▼ [STT - Whisper]
transcription.json (원본 언어 그대로)
    │
    ▼ [1단계: 영어 번역]
    │  - 프랑스어 등 비영어 → 영어로 번역
    │  - 영어 대사 → 그대로 유지
    │  - 한국어 대사 → 한국어 그대로 유지
    │
    ▼ output: {name}.en.srt  ← 영어 기본 자막
    │
    ▼ [2단계: 한국어 번역]
    │  - 영어 SRT 기반으로 한국어 번역
    │  - 이미 한국어인 대사 → 그대로 유지
    │
    ▼ output: {name}.ko.srt  ← 한국어 자막
```

### 왜 영어를 먼저 만드는가

- 원본에 프랑스어가 섞여 있음
- 프랑스어 → 영어 번역이 프랑스어 → 한국어보다 품질이 높음
- 영어를 중간 기본본으로 만들고, 그 위에 한국어를 만드는 2단계 접근

### 분할 전략

기존 2-Pass 청크 파이프라인(`translate_chunks.py`)을 활용하되, 각 단계(영어 번역 / 한국어 번역)에 적용:
- 세그먼트 100개 이하: 직접 번역
- 세그먼트 101개 이상: 청크 분할 → 병렬 번역 → 병합
- 영어 번역과 한국어 번역 각각에 독립적으로 분할 전략 적용 (무겁지 않게)

### 출력 파일

```
video.mp4
video.en.srt    ← 영어 (기본본)
video.ko.srt    ← 한국어
```

### 기존 시스템 참고

- 파이프라인 명세: `.claude/skills/video-subtitle/SKILL.md`
- 청크 분할/병합: `.claude/skills/video-subtitle/scripts/translate_chunks.py`
- STT: `.claude/skills/video-subtitle/scripts/transcribe.py`
- refdb 용어집: `.claude/skills/video-subtitle/refdb/`
- 아키텍처 문서: `.docs/architecture/arch-subtitle-pipeline.md`

## Progress
- [ ] SKILL.md 파이프라인 수정 (영어 → 한국어 2단계 흐름)
- [ ] translate_chunks.py 수정 (영어/한국어 SRT 분리 출력)
- [ ] 영어 번역 단계 프롬프트/로직 설계
- [ ] 한국어 번역 단계 프롬프트/로직 설계 (영어 SRT 기반)
- [ ] 기존 분할 전략 재활용 (단계별 독립 적용)

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|

## Notes
- 기존 파이프라인은 단일 SRT(한국어) 출력 → 이중 출력으로 확장
- refdb 용어집은 한국어 번역 단계에서 기존과 동일하게 적용
- 영어 번역 단계에서는 refdb의 영어 원문(term/name)을 일관성 유지에 활용
