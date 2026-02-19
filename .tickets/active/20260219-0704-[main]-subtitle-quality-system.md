---
title: 자막 번역 품질 개선 시스템
class: coding
status: backlog
category: video
priority: normal
tags: [video, subtitle, quality, database, mcp]
relations:
  children: ["20260219-0704-[sub]-reference-database", "20260219-0704-[sub]-subtitle-fix-command"]
  follows: ["20260219-1448-video-subtitle-chunking-pipeline"]
---

## Goal

비디오 자막 번역의 품질을 높이기 위한 시스템을 구축한다. 두 가지 축으로 구성:

1. **참고 자료 DB + 파이프라인 연동** — 도메인별 용어/고유명사 DB를 구축하고, style_guide 작성 시 자동으로 참조/보충
2. **자막 후처리 커맨드** — 완성된 자막을 도메인 지식 기반으로 수정하는 커맨드

### 배경

테스트 영상이 게임개발 팀 회의 영상이었는데, "hk"를 "영웅왕"으로 번역해야 하는 등 도메인 특화 지식이 필요했다. 현재 파이프라인은 영상 내부 문맥만으로 style_guide를 작성하므로, 외부 참고 자료가 없으면 고유명사/전문용어를 정확히 번역할 수 없다.

### 추가 개선: 서브에이전트 resume 패턴

현재 SKILL.md는 Pass 1과 Pass 2에서 별도 에이전트를 실행하지만, 원래 의도는 **같은 에이전트가 Pass 1 번역 컨텍스트를 유지한 채로 Pass 2까지 이어가는 것**이다. Claude Code Task tool의 `resume` 기능을 활용하여:

```
Pass 1: 청크당 1에이전트 실행 (4개씩 배치) → agent ID 보관
Pass 2: 기존 에이전트 resume (4개씩 배치) → Pass 1 컨텍스트 유지
```

배치 크기 4는 동시 실행 수일 뿐, 총 에이전트 수 = 총 청크 수.

## Progress
- [ ] 참고 자료 DB 설계 및 구축 (Sub 티켓)
- [ ] 자막 후처리 커맨드 구현 (Sub 티켓)
- [ ] SKILL.md 서브에이전트 resume 패턴 적용

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|

## Notes
- windless(게임 프로젝트) DB가 첫 번째 대상
- MCP 연동으로 위키 등 외부 소스 자동 조회 구상
