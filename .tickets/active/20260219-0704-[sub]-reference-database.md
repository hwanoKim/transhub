---
title: 참고 자료 DB + 파이프라인 연동
class: coding
status: closed
category: video
priority: normal
tags: [video, subtitle, database, mcp, windless, confluence]
relations:
  parent: "20260219-0704-[main]-subtitle-quality-system"
  follows: ["20260219-1448-video-subtitle-chunking-pipeline"]
---

## Goal

도메인별 참고 자료 DB를 구축하고, 자막 번역 파이프라인의 style_guide 작성 단계에서 자동으로 참조하도록 연동한다.

### 문제

현재 style_guide.md는 영상 내부 문맥(context_NNN.md)만으로 작성된다. 게임개발 회의 영상처럼 도메인 특화 용어가 많은 경우, 영상 문맥만으로는 정확한 번역이 불가능하다.

예시: "hk" → 영상 문맥만으로는 무엇인지 알 수 없음 → DB에서 "hk = 영웅왕(Hero King), windless 프로젝트의 캐릭터"를 찾아야 함

### 설계 결정사항

#### 1. DB 형식: YAML

- 사람이 직접 편집하기 쉬움 (수동 편집 + 자동 학습 병행이 목표)
- SQLite는 이 규모에서 과도함 (프로젝트당 수십~수백 항목)
- JSON은 수동 편집이 불편

#### 2. 디렉토리 구조

```
.claude/skills/video-subtitle/refdb/
├── windless/
│   ├── _config.yaml       # 이 도메인의 자료 수집 방법 정의
│   ├── terms.yaml         # 약어 → 정식 명칭 + 번역
│   ├── characters.yaml    # 캐릭터/인물
│   ├── staff.yaml         # 주요 인물 (개발팀)
│   ├── glossary.yaml      # 일반 도메인 용어 (main, 분할 가능)
│   ├── glossary-gameplay.yaml  # 게임플레이 용어
│   └── glossary-world.yaml     # 세계관 용어
└── _default/
    └── glossary.yaml      # 공통 용어 (프로젝트 무관)
```

#### 3. YAML 스키마

**terms.yaml** (약어/줄임말):
```yaml
- key: hk
  full: Hero King
  ko: 영웅왕
  context: 캐릭터 클래스명
```

**characters.yaml**:
```yaml
- name: Hero King
  ko: 영웅왕
  aliases: [hk, HK]
  description: windless 프로젝트의 캐릭터
```

**staff.yaml**:
```yaml
- name: Max Pepin
  ko: 막스 페팽
  role: Game Director
  region: Montreal
```

#### 4. 파이프라인 연동 (SKILL.md 3B-4 단계)

```
context_NNN.md 취합 → refdb 조회 → (DB에 없으면 Confluence MCP 조사) → style_guide.md 작성
```

1. 모든 context_NNN.md를 읽는다
2. 도메인을 식별하여 해당 refdb 폴더 + _default 로드
3. 미확인 용어는 _config.yaml의 lookup 순서대로 조사 (Confluence MCP 등)
4. 찾은 정보를 style_guide에 반영

#### 5. Confluence MCP 연동

- windless 도메인의 1차 lookup: Confluence wiki (Atlassian 플러그인)
- `atlassian:search-company-knowledge` 스킬로 검색 가능

## Progress
- [x] DB 형식 결정 (YAML)
- [x] windless 도메인 refdb 구축
      - [x] _config.yaml (Confluence lookup 설정, spaces: idol/MTLKRAFTON)
      - [x] terms.yaml (13개 약어)
      - [x] characters.yaml (캐릭터/종족/신 — BTDT 공식 용어집 기반)
      - [x] staff.yaml (한국 3명 + 몬트리올 18명, 한국인은 한국이름 사용)
      - [x] glossary.yaml → 3분할 (lore/gameplay/world, 각 80줄 이하)
- [x] _default/glossary.yaml 공통 용어 작성
- [x] SKILL.md 3B-4 단계에 refdb 조회 로직 추가 + staff 인물 표기 규칙
- [x] Confluence MCP 연동 테스트 (BTDT 공식 용어집 발견/반영)
- [x] 파일 분할 규칙 추가 (_config.yaml max_lines_per_file: 150)

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|
| 1 | SRT 샘플링으로 초기 DB 구축 | O | 19개 청크 중 8개 샘플링하여 용어/인물 추출 |
| 2 | Confluence MCP로 공식 자료 보강 | O | BTDT Korean-English Glossary 발견, 공식 영문 표기 반영 |
| 3 | glossary 159줄 → 3파일 분할 | O | lore(51) + gameplay(65) + world(45) |

## Commits
- Git: `{COMMIT_HASH}` - refdb: windless 도메인 구축 완료 (terms, characters, staff, glossary 3분할) + SKILL.md 3B-4 단계 refdb 연동

## Notes
- 첫 번째 대상 도메인: windless (게임개발 프로젝트)
- DB는 수동 편집 + 자동 학습(번역 과정에서 발견된 용어 축적) 병행이 이상적
- Confluence MCP: Atlassian 플러그인 설치됨, 세션 재시작 후 사용 가능
- `atlassian:search-company-knowledge` 스킬로 Confluence/Jira 내부 문서 검색 가능
- SKILL.md 3B-4 단계에 인물 표기 규칙 추가: refdb의 staff.yaml에 매칭되는 인물은 첫 언급 시 `이름(역할)` 형식으로 표기
