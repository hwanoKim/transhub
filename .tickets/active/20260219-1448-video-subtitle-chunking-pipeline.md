---
title: 대량 세그먼트 번역 파이프라인 개선
class: coding
status: review
category: video
priority: normal
tags: [video, subtitle, pipeline, chunking]
relations:
  follows: ["20260219-1500-video-subtitle-command"]
---

## Goal

`/video-subtitle` 스킬의 대량 세그먼트(500+) 처리 파이프라인을 개선한다. 현재 SKILL.md에 "50개씩 나누어 번역"이라는 규칙만 있고, **구체적인 분할/처리/병합 전략이 없어** 실제 962개 세그먼트 작업 시 20분간 결과물 없이 컨텍스트만 소모하는 문제가 발생했다.

### 발생한 문제 (2026-02-19 실제 실행)

| 문제 | 상세 |
|------|------|
| **JSON 읽기 병목** | `transcription.json`이 58K 토큰 → Read 1회 불가. 300줄씩 8회+ 읽기로 컨텍스트만 소모 |
| **번역 전략 부재** | 962개 세그먼트를 어떻게 분할/번역/병합할지 구체 절차 없음 |
| **중간 결과물 없음** | 20분간 읽기만 수행, SRT 파일 0바이트. 사용자 입장에서 진행 불투명 |
| **컨텍스트 낭비** | 세그먼트 텍스트를 메인 컨텍스트에 전부 로드 → 번역 작업 전에 컨텍스트 한계 도달 |
| **병렬화 미활용** | 독립적인 청크 번역을 순차로 시도 → 서브에이전트 병렬 활용 안 함 |

### 개선 방향: 2-Pass 병렬 파이프라인

#### 아키텍처

```
Split: transcription.json → chunk_001~NNN.json

Pass 1 (병렬): 서브에이전트 N개 동시 실행
  ├─ agent-1: chunk_001 번역 → draft_001.srt + context_001.md
  ├─ agent-2: chunk_002 번역 → draft_002.srt + context_002.md
  └─ agent-N: chunk_NNN 번역 → draft_NNN.srt + context_NNN.md

메인 에이전트: context_001~NNN.md 취합 → style_guide.md 작성
  (용어집, 톤/존댓말 결정, 특이사항 정리)

Pass 2 (병렬): 서브에이전트 N개 동시 실행
  ├─ agent-1: style_guide.md + draft_001.srt → chunk_001.srt (최종)
  ├─ agent-2: style_guide.md + draft_002.srt → chunk_002.srt (최종)
  └─ agent-N: ...

Merge: chunk_001~NNN.srt → 최종 .srt
```

#### 문맥 관리 (context_NNN.md)

각 서브에이전트가 Pass 1에서 작성하는 문맥 파일:
- 해당 청크의 대화 주제/흐름 요약
- 등장하는 고유명사, 전문용어
- 번역 시 판단이 필요했던 표현 (예: "stock" → "재고" vs "백로그")
- 화자 톤, 격식 수준

#### style_guide.md (메인 에이전트 정리)

Pass 1 완료 후 메인 에이전트가 모든 context를 취합하여 작성:
- 전체 톤 결정 (해요체/합니다체/반말)
- 용어 통일 (용어집 테이블)
- 고유명사 표기법
- 기타 전체 청크에 적용할 번역 규칙

### 수정 대상 파일

| 파일 | 변경 |
|------|------|
| `.claude/skills/video-subtitle/SKILL.md` | 2-Pass 병렬 파이프라인 반영 |
| `.claude/skills/video-subtitle/scripts/translate_chunks.py` | (완료) 청크 분할/병합 유틸리티 |

## Progress
- [x] 청크 분할/병합 전략 설계
- [x] translate_chunks.py 작성
      - [x] split 서브커맨드 (JSON → 청크 분할 + 노이즈 필터)
      - [x] merge 서브커맨드 (청크 SRT → 최종 SRT 병합)
- [x] SKILL.md 기본 파이프라인 (v1: STT 스킵, 세그먼트 분기, 청크 번역)
- [x] SKILL.md 2-Pass 병렬 파이프라인 (v2)
      - [x] Pass 1: 병렬 초벌 번역 + context 파일 생성 절차
      - [x] 메인 에이전트 style_guide.md 작성 절차
      - [x] Pass 2: style_guide 기반 검토 절차
      - [x] 재개 가능 구조 (pass/단계별 스킵)
- [ ] 실제 962세그먼트 파일로 테스트 (사용자 별도 세션)

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|
| 1 | 메인 세션에서 300줄씩 순차 Read + 직접 번역 시도 | X | 8회 Read 후에도 전체 못 읽음. 번역 시작 전 20분 소모, 결과물 0 |

## Notes
- 원본 테스트 파일: `C:\tmp\GMT20260213-200109_Recording.cutfile.20260218133656676_3840x2160.mp4`
- 감지 언어: fr (프랑스어), 세그먼트 수: 962, JSON 크기: 58K 토큰
- 세그먼트 250-261은 영상 재생 중 노이즈 ("Hey, hey, hey", "Oh, oh, oh") — 자동 필터링 대상
- translate_chunks.py 실검증: 962세그먼트 → 노이즈 17개 필터 → 945개 활성 → 19청크
