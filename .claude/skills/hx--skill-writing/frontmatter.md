# Frontmatter 필드

## 전체 예시

```yaml
---
name: explain-code
description: 코드를 다이어그램과 비유로 설명합니다
argument-hint: [filename] [format]
model: claude-sonnet-4-20250514
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
user-invocable: true
context: fork
agent: Explore
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

## 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | 권장 | 표시 이름 (소문자, 하이픈, 최대 64자) |
| `description` | 권장 | 언제/왜 사용하는지 설명. Claude가 자동 호출 판단에 사용 |
| `argument-hint` | 선택 | 자동완성 힌트 (예: `[filename]`, `[issue-number]`) |
| `model` | 선택 | 특정 모델 강제 사용 |
| `allowed-tools` | 선택 | 스킬 활성화 시 사용 가능한 도구 제한 |
| `disable-model-invocation` | 선택 | `true`: 사용자만 호출 가능 (배포, 커밋 등) |
| `user-invocable` | 선택 | `false`: `/` 메뉴에서 숨김 (백그라운드 지식용) |
| `context` | 선택 | `fork`: 독립된 서브에이전트 컨텍스트에서 실행 |
| `agent` | 선택 | 서브에이전트 타입: `Explore`, `Plan`, `general-purpose` |
| `hooks` | 선택 | 스킬 라이프사이클 훅 |

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
---
name: pr-summary
context: fork
agent: Explore
---

## PR 컨텍스트
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`

이 PR을 요약하세요...
```

명령은 즉시 실행되며, Claude는 명령어가 아닌 출력 결과를 받습니다.

---

## 스킬 라이프사이클 훅

스킬 frontmatter에서 훅을 정의하여 스킬 활성화 동안만 실행:

```yaml
---
name: secure-operations
description: 보안 검사가 포함된 작업 수행
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
---
```

### 지원되는 훅 이벤트

| 이벤트 | 설명 |
|--------|------|
| `PreToolUse` | 도구 사용 전 (차단 가능) |
| `PostToolUse` | 도구 사용 후 |
| `Stop` | 스킬 종료 시 |

### 훅 옵션

| 옵션 | 설명 |
|------|------|
| `once` | `true`: 세션당 한 번만 실행 (스킬 전용) |

---

## 호출 제어

### Claude 자동 호출 비활성화
- `disable-model-invocation: true` 설정
- 배포, 커밋 등 부작용이 있는 작업에 사용

### 사용자 호출 비활성화
- `user-invocable: false` 설정
- `/` 메뉴에서 숨김, 백그라운드 지식용

### 도구 접근 제한
- `allowed-tools`로 필요한 도구만 허용
