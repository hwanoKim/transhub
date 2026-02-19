# Ticket Management Rule

> 자동 생성 (hwano-plugins). 업데이트: `Hwano: Update Claude Rules`

## 레거시 감지 & 마이그레이션

레거시 티켓 구조 또는 `.newTickets/` 폴더가 감지되면 `hx--migration.md`의 절차를 따릅니다.

---

## 티켓 생성 시 Class 안내

티켓을 생성할 때 `config.yaml`의 class 목록을 확인합니다:

| 상황 | 동작 |
|------|------|
| `config.yaml`이 없거나 class가 하나도 없음 | 사용자에게 "현재 class가 없습니다. 어떤 class를 만들까요?" 물어보기 |
| 기존 class 중 적합한 것이 있음 | 자동으로 해당 class 할당 |
| 기존 class 중 적합한 것이 없음 | 사용자에게 "기존 class 중 적합한 것이 없습니다. 새 class를 만들까요?" 물어보기 |

새 class를 만들기로 하면:
1. class 이름 확인 (아래 기본 템플릿 중 일치하는 것이 있으면 추천)
2. 기본 템플릿이 있으면: "이 status 구성으로 만들까요?" → 승인 시 바로 생성
3. 기본 템플릿이 없으면: "status는 어떤 것들로 할까요?" 사용자에게 질문
4. `config.yaml`에 추가
5. **필수**: `.claude/rules/class-rules.md` 생성 — class를 만들면 rule 문서도 반드시 함께 생성

---

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **When to create** | 단순 오타 수정 외 모든 코드 변경 → 티켓 생성. 불확실하면 생성 |
| **Ticket first** | 코딩 전 `.tickets/active/` 확인, 없으면 생성 |
| **Find relations first** | 티켓 생성 전 **history-finder 에이전트**로 기존 티켓을 탐색하고 관계를 연결한다. coding class는 최소 `follows` 필수. 빈 relations는 research 등 독립 작업만 허용 |
| **Sync status** | 작업 단계가 바뀌면 코딩보다 티켓을 먼저 업데이트 (status 전환, progress 체크, todo 반영). 대화에서 방향이 바뀌거나 todo가 변경되면 티켓 반영 후 진행 |
| **Update before coding** | 사용자 요청이 티켓에 없으면 먼저 업데이트. 기록 없이 코딩 금지 |
| **Record sub-items** | 고수준 todo 아래 구체적 변경을 하위 항목으로 기록 |
| **Document attempts** | 방법/결과 기록. 실패 시 이유 기록 (재발 방지) |
| **Record commits** | Git 커밋 해시 기록. P4V 사용 시 changelist 번호도 함께 기록 |
| **Progress required** | status가 backlog을 벗어나면 `## Progress`에 최소 1개 `- [ ]` 필수 |
| **Inherit category** | 관련 티켓이 같은 류의 작업이면 해당 티켓의 category를 승계. 단, category는 필수가 아님 — 빠르게 생성 후 나중에 분류 가능 |
| **Auto-advance** | 현재 status의 작업이 완료되면 **반드시 다음 status로 전환하고 대기**한다. 같은 status에 머물며 "끝났습니다"라고 보고만 하지 않는다. 예: implementation 완료 → review로 전환 → 사용자 리뷰 대기 |
| **Class-rule required** | config.yaml에 class가 있으면 반드시 `.claude/rules/class-rules.md`가 존재해야 한다. 없으면 사용자에게 알리고 즉시 생성 |
| **Backlog first** | 새 티켓은 반드시 `backlog`으로 생성한다. 사용자가 "구현해줘", "진행해줘" 등 명시적으로 진행을 요청하기 전까지 status를 변경하지 않는다 |
| **Priority is user-only** | priority 기본값은 `normal`. Claude는 사용자의 명시적 요청 없이 priority를 지정/변경하지 않는다. 티켓 생성 시 항상 `normal`로 설정 |
| **Self-contained ticket** | 1 티켓 = 1 세션 원칙. 새 티켓은 다른 세션에서 컨텍스트 없이 시작되므로, Goal에 충분한 정보를 담는다: 관련 코드 위치, 원인 분석, 현재 세션에서 파악한 사항 등. "이 세션에서 논의한 대로" 같은 참조 금지 |

## 폴더 구조

```
.tickets/
├── active/                           # 모든 활성 티켓 (backlog, hold, 진행중 전부)
├── closed/                           # 닫힌 티켓 아카이브
│   └── {YYYY}/
│       └── {YYYY-MM}/
└── config.yaml                       # 보드 설정
```

**파일명**: `{YYYYMMDD}-{HHMM}-{title}.md` (KST, 24시간, 영어 kebab-case)
**title (제목)**: 한글로 작성. 칸반 보드에 표시되는 텍스트이므로 한글이 기본. 파일명은 영어, frontmatter title은 한글

## 상태 시스템

### 고정 상태 (모든 class 공통)

| 상태 | 위치 | 설명 |
|------|------|------|
| `backlog` | 좌측 고정 | 아이디어/백로그. Progress 없어도 됨 |
| `hold` | 좌측 고정 | 보류. hold-reason, hold-date 필수 |
| `closed` | 우측 고정 | 완료. "닫아줘"로 closed/로 아카이브 |

### 중간 상태 (class별 정의)

중간 상태는 각 프로젝트의 class에 따라 다릅니다.
각 class의 상태 정의와 행동 가이드는 **`.claude/rules/class-rules.md`** 문서에 정의됩니다.

**class-rule 문서는 필수입니다.** config.yaml에 class가 존재하면 반드시 대응하는 rule 문서가 있어야 합니다.

> 티켓 작업 시작 시 class-rule 문서가 없으면: "**{class-name} class의 rule 문서가 없습니다.** `.claude/rules/class-rules.md`를 생성하겠습니다." → 사용자에게 알리고 즉시 생성

### Config 검증

티켓 작업 시 아래 불일치를 감지하면 사용자에게 안내합니다:

| 상황 | 안내 |
|------|------|
| class-rule 문서에 있는 status가 `config.yaml`에 없음 | "rule에 `{status}`가 정의되어 있지만 config.yaml의 `{class}` classes에는 없습니다" |
| `config.yaml`에 있는 status가 class-rule 문서에 없음 | "config.yaml에 `{status}`가 있지만 rule 문서에 설명이 없습니다" |
| class에 대한 rule 문서 자체가 없음 | 위 '문서가 없는 경우' 절차 |

## Ticket Relations

티켓 시스템은 **티켓 간의 연결성**을 중시합니다. 관계는 3축으로 분류됩니다.

### 티켓 생성 시 필수 절차

1. **히스토리 탐색 (필수)**: **history-finder 에이전트**를 사용하여 관련 티켓을 검색한다. 메인 세션에서 직접 탐색하지 않고 에이전트에 위임
2. **관계 판단**: 분해(parent/children), 순서(follows), 종속(blocks) 중 해당하는 관계를 판단
3. **relation 기록**: frontmatter의 `relations` 필드에 기록. **빈 relations로 생성하지 않는다** (예외: 아래 class별 정책 참고)
4. **category 승계**: 같은 류의 작업이면 관련 티켓의 category를 그대로 사용

### Class별 관계 연결 정책

| Class | 정책 | 설명 |
|-------|------|------|
| **coding, refactor** | `follows` 필수 | 코드 변경은 항상 흐름이 있다. 직전 관련 티켓을 `follows`로 연결. parent/children, blocks도 적극 활용 |
| **system** | `follows` 권장 | 시스템/인프라 작업도 대부분 흐름이 있음. 독립적인 경우에만 생략 가능 |
| **research** | 관계 선택적 | 순수 리서치는 독립적일 수 있음. 단, 선행 티켓이 있으면 `follows` 연결 |
| **legacy** | 관계 선택적 | 마이그레이션된 레거시 티켓은 관계 없을 수 있음 |

### 빈 Relations 검증

티켓 생성 후 relations가 **전부 비어있으면** 아래를 확인한다:

1. 정말 독립적인 첫 작업인가? (프로젝트 첫 티켓, 완전히 새로운 영역)
2. 히스토리 탐색을 충분히 했는가? (active + closed 모두 확인했는지)
3. 시간순으로 직전 같은 class 티켓이 있지 않은가? → 있으면 `follows` 연결

**coding/refactor class에서 빈 relations는 원칙적으로 허용하지 않는다.** 최소한 같은 class의 직전 티켓이라도 `follows`로 연결한다.

### Relation 유형 (3축)

| 축 | 유형 | 설명 | 예시 |
|------|------|------|------|
| 상하 (분해) | `parent` / `children` | 큰 작업을 쪼갠 관계 | 리깅 모듈 → 가이드, 빌더 |
| 좌우 (순서) | `follows` | 시간순 선후 관계 (병렬 가능) | v1 구현 → v2 개선 |
| 좌우 (종속) | `blocks` / `blocked-by` | 반드시 순서를 지켜야 하는 관계 | API 완료 → UI 시작 |

- `fixes`, `spawned-from` → `follows` + `tags: [bugfix]`로 대체
- `relates-to` → category/tags로 자연스럽게 표현됨

### parent/children 파일명 태그

parent/children 관계가 있으면 파일명에도 역할을 표기한다:

```
20260214-0007-[main]-refactor-ticket-manager.md   ← parent
20260214-0008-[sub]-refactor-board-html.md         ← child
20260214-0009-[sub]-refactor-watcher.md            ← child
```

- `[main]`: parent 역할. 날짜-시간 뒤, 제목 앞
- `[sub]`: children 역할
- frontmatter `relations`와 병행 — 메타데이터는 파싱용, 파일명 태그는 사람이 눈으로 구분하기 위함

### 참조 형식

파일명(`.md` 제외)으로 참조합니다:

```yaml
relations:
  parent: "20260214-0007-[main]-refactor-ticket-manager"
  follows: ["20260209-1000-eye-research"]
  blocks: ["20260212-1000-ui-feature"]
  blocked-by: ["20260211-0900-base-api"]
```

- `parent`: 단일 값 (상위 티켓은 하나)
- `children`, `follows`, `blocks`, `blocked-by`: 배열
- 관계가 없으면 필드 생략
- **직접 관계만 기록** — 간접 관계(A→B→C에서 A→C)는 그래프에서 추론


## 티켓 템플릿

```markdown
---
title: {Title}
class: {class-name}
status: backlog
category:
priority: normal
tags: []
relations:
  parent:
  children: []
  follows: []
  blocks: []
  blocked-by: []
---

## Goal
{목표 설명}

## Progress
- [ ] {할 일 1}

## Attempts
| # | Method | Result | Notes |
|---|--------|--------|-------|
| 1 | ... | X | reason |

## Notes
```

### Frontmatter 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `title` | O | 티켓 제목 (한글로 작성 — 칸반 보드 표시용) |
| `class` | O | 티켓 유형 (coding, character 등) |
| `status` | O | 현재 상태 |
| `category` | - | 분류. 필수 아님 — 빠르게 생성 후 나중에 드래그&드롭으로 할당 가능 |
| `priority` | - | 우선순위 (low, normal, high, urgent) |
| `tags` | - | 태그 배열 |
| `relations` | - | 티켓 간 관계 (parent/children, follows, blocks/blocked-by) |
| `hold-reason` | hold 시 | 보류 사유 |
| `hold-date` | hold 시 | 보류 일자 |

### Progress 규칙

- `## Progress` 섹션의 `- [ ]`/`- [x]` 로 진행률 표시
- ticket-manager가 파싱하여 프로그래스바로 표시
- **backlog 상태**: Progress 없어도 됨 (아이디어 단계)
- **backlog 이외 상태**: 최소 1개의 `- [ ]` 필수 — 할 일이 지정되어야 프로그래스바가 의미있음
- Sub-item 지원:
  ```markdown
  - [ ] Main task
        - [x] Subtask 1
        - [x] Subtask 2
  ```

## Hold (보류)

**조건**: 외부 의존성 대기, 우선순위 변경, 기술적 문제

frontmatter에 추가:
```yaml
status: hold
hold-reason: 이유
hold-date: 2026-01-20
```

**Resume**: status를 이전 상태로 변경, hold-reason/hold-date 삭제

## 버전 관리 기록

```markdown
## Commits
- Git: `a1b2c3d` - 메시지
- P4V: `CL#12345` - 메시지 (P4V 사용 시)
```

## P4V Changelist 조회 방법

> P4V/Perforce를 사용하지 않는 프로젝트에서는 이 섹션을 무시하세요.

```bash
# 현재 디렉토리의 최근 submitted changelist
p4 changes -m1 -s submitted ...

# 특정 파일의 changelist
p4 changes -m1 <file>
```

## Close 처리 (티켓 닫기)

> **사용자의 명시적 요청이 있을 때만** close를 수행합니다. 작업이 끝났다고 자동으로 닫지 않습니다.

**반드시 close-handler 에이전트를 통해 닫습니다.** 메인 세션에서 직접 status 변경이나 폴더 이동을 하지 않습니다.
status 변경과 아카이브 이동이 분리되면 불완전한 close가 발생할 수 있으므로, 에이전트가 일괄 처리합니다.

트리거: "티켓 닫아줘", "close해줘", "티켓 close"

### 사후 티켓 (이미 작업 완료, 티켓 미생성 시)

트리거: "방금 한 작업 티켓으로", "완료된 작업 기록해줘"

1. `git status` & `git log -1`로 커밋 상태 확인
2. 미커밋 있으면 → 커밋 & 푸시 먼저
3. `closed/{YYYY}/{YYYY-MM}/`에 직접 생성 (frontmatter의 status: closed)
4. 커밋 해시, 관련 파일 기록
