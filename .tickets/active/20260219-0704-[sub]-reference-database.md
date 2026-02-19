---
title: 참고 자료 DB + 파이프라인 연동
class: coding
status: backlog
category: video
priority: normal
tags: [video, subtitle, database, mcp, windless]
relations:
  parent: "20260219-0704-[main]-subtitle-quality-system"
  follows: ["20260219-1448-video-subtitle-chunking-pipeline"]
---

## Goal

도메인별 참고 자료 DB를 구축하고, 자막 번역 파이프라인의 style_guide 작성 단계에서 자동으로 참조하도록 연동한다.

### 문제

현재 style_guide.md는 영상 내부 문맥(context_NNN.md)만으로 작성된다. 게임개발 회의 영상처럼 도메인 특화 용어가 많은 경우, 영상 문맥만으로는 정확한 번역이 불가능하다.

예시: "hk" → 영상 문맥만으로는 무엇인지 알 수 없음 → DB에서 "hk = 영웅왕(Hero King), windless 프로젝트의 캐릭터"를 찾아야 함

### 설계 방향

#### 1. 참고 자료 DB 구조

도메인(프로젝트)별로 용어집/고유명사/약어를 관리:

```
예시 구조 (형식은 리서치 필요):
windless/
├── terms.yaml          # 용어집 (약어 → 정식 명칭 + 번역)
├── characters.yaml     # 캐릭터/인물
└── glossary.yaml       # 일반 용어
```

#### 2. 파이프라인 연동

style_guide 작성 단계에서:
1. context 파일들에서 미확인 용어/약어 추출
2. 참고 자료 DB에서 매칭 검색
3. DB에 없으면 → MCP로 위키/외부 소스 조회하여 보충
4. 찾은 정보를 style_guide.md 용어집에 반영

#### 3. MCP 연동

DB에 없는 용어가 나오면 MCP 도구로 추가 조사:
- 프로젝트 위키 조회
- 외부 참고 자료 검색
- 결과를 style_guide에 반영 + (선택) DB에 추가

## Progress
- [ ] DB 형식 리서치 (YAML, JSON, SQLite 등 비교)
- [ ] windless 참고 자료 DB 초기 구축
- [ ] style_guide 작성 단계에 DB 조회 로직 추가
- [ ] MCP 연동 설계 (위키 조회 등)

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|

## Notes
- 첫 번째 대상 도메인: windless (게임개발 프로젝트)
- DB는 수동 편집 + 자동 학습(번역 과정에서 발견된 용어 축적) 병행이 이상적
