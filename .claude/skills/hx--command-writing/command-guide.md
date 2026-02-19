# Command Writing Rule

커맨드(슬래시 명령어)를 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/slash-commands

---

## 커맨드 위치

| 스코프 | 위치 | 용도 |
|--------|------|------|
| 프로젝트 | `.claude/commands/<name>.md` | 프로젝트 전용 |
| 개인 | `~/.claude/commands/<name>.md` | 모든 프로젝트에서 사용 |
| 플러그인 | `<plugin>/commands/<name>.md` | 플러그인 배포용 |

- 파일명이 커맨드 이름이 됨 (예: `review.md` → `/review`)
- 하위 폴더 가능 (예: `commands/frontend/component.md` → `/component`)

---

## Frontmatter 필드

```yaml
---
description: 커맨드 설명 (/help에 표시됨)
argument-hint: [filename] [format]
model: claude-sonnet-4-20250514
allowed-tools: Read, Grep, Bash(npm:*)
disable-model-invocation: true
user-invocable: true
context: fork
agent: Explore
---
```

### 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `description` | 권장 | 커맨드 설명. Claude가 자동 호출 판단에 사용 |
| `argument-hint` | 선택 | 자동완성 힌트 (예: `[issue-number]`, `[file] [format]`) |
| `model` | 선택 | 특정 모델 강제 사용 |
| `allowed-tools` | 선택 | 허용할 도구 목록 |
| `disable-model-invocation` | 선택 | `true`: 사용자만 호출 가능 (배포, 커밋 등 부작용 있는 작업) |
| `user-invocable` | 선택 | `false`: 슬래시 메뉴에서 숨김 (백그라운드 지식용) |
| `context` | 선택 | `fork`: 독립된 서브에이전트 컨텍스트에서 실행 |
| `agent` | 선택 | 서브에이전트 타입: `Explore`, `Plan`, `general-purpose` |

---

## 변수

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | 전달된 모든 인자 |
| `$1`, `$2`, ... | 위치별 인자 |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |
| `${CLAUDE_PLUGIN_ROOT}` | 플러그인 루트 경로 (플러그인 내에서만) |

---

## 동적 컨텍스트 주입

백틱과 `!`를 사용하여 명령 실행 결과를 주입:

```markdown
## 현재 상태
- Git status: !`git status --short`
- Branch: !`git branch --show-current`
```

---

## 커맨드 템플릿

### 기본 커맨드

```markdown
---
description: 간단한 설명
---

# 커맨드 제목

실행할 작업 설명...

$ARGUMENTS를 사용하여 인자 처리
```

### 사이드 이펙트가 있는 커맨드 (커밋, 배포 등)

```markdown
---
description: 변경사항을 커밋합니다
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Smart Commit

사용자가 명시적으로 호출할 때만 실행됩니다.

## 실행 절차
1. ...
2. ...
```

### 서브에이전트로 실행하는 커맨드

```markdown
---
description: 코드베이스를 분석합니다
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# 분석 작업

$ARGUMENTS에 대해 분석을 수행합니다.
```

---

## 주의사항

1. **부작용이 있는 커맨드**는 반드시 `disable-model-invocation: true` 설정
2. **description**은 명확하게 작성 (Claude가 자동 호출 판단에 사용)
3. **allowed-tools**로 필요한 도구만 허용
4. SKILL.md와 commands/*.md는 동일하게 동작함 (Skills가 더 많은 기능 지원)
