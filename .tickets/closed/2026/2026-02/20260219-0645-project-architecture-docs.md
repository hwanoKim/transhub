---
title: 프로젝트 아키텍처 문서화
class: coding
status: closed
category:
priority: normal
tags: [docs, architecture, diagram]
relations:
  follows: ["20260219-1500-video-subtitle-command", "20260219-1448-video-subtitle-chunking-pipeline"]
---

## Goal

Transhub 프로젝트의 전체 아키텍처와 서브에이전트 흐름을 문서화한다. 현재 프로젝트에 아키텍처 문서가 전혀 없어 전체 구조를 파악하기 어렵다.

### 문서화 범위

#### 1. 서브에이전트 흐름 다이어그램
- `/video-subtitle` 스킬 실행 시 서브에이전트의 전체 흐름을 시각적으로 표현
- 2-Pass 병렬 파이프라인 구조 (Split → Pass 1 병렬 → style_guide 취합 → Pass 2 병렬 → Merge)
- 메인 에이전트와 서브에이전트 간의 데이터 흐름 (입력/출력 파일)
- Mermaid 다이어그램 활용

#### 2. 프로젝트 전체 구성도
- 디렉토리 구조와 각 디렉토리의 역할
- 스킬/커맨드 목록과 설명
- Python 스크립트들의 역할 (transcribe.py, translate_chunks.py)
- 의존성 관계 (ffmpeg, whisper, Python 패키지 등)
- 데이터 흐름: 비디오 → 오디오 → JSON → 청크 → SRT

### 관련 코드 위치
- `.claude/skills/video-subtitle/SKILL.md` — 파이프라인 정의
- `.claude/skills/video-subtitle/scripts/transcribe.py` — STT 스크립트
- `.claude/skills/video-subtitle/scripts/translate_chunks.py` — 청크 분할/병합 유틸리티
- `requirements.txt` — Python 의존성

## Progress
- [x] 서브에이전트 흐름 다이어그램 작성
- [x] 프로젝트 전체 구성도 문서 작성

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|
| 1 | docs/ 단일 파일 | X | hx--docs 스킬 규칙 미적용. .docs/ 구조로 재작성 |
| 2 | .docs/ Obsidian 구조 | O | 4문서 분리: index, architecture-index, arch-overview, arch-subtitle-pipeline |

## Notes
- 사용자 요청: "번역할 때 서브에이전트의 흐름을 시각적으로 보고 싶다" + "프로젝트 큰 구성도 문서화 필요"
- hx--docs 스킬 규칙 적용: Obsidian 링크, breadcrumb, 인덱스 분리, Mermaid TB

## Commits
- Git: `eaf4f4b` - docs: 프로젝트 아키텍처 문서화 완료

## 관련 파일
- `.docs/index.md` — 문서 메인 인덱스
- `.docs/architecture/architecture-index.md` — 아키텍처 문서 인덱스
- `.docs/architecture/arch-overview.md` — 프로젝트 전체 구성도
- `.docs/architecture/arch-subtitle-pipeline.md` — 2-Pass 파이프라인 흐름
