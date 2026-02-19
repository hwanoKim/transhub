# Subagent Writing Guide

서브에이전트를 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/sub-agents

---

## 서브에이전트 위치

| 스코프 | 위치 | 용도 |
|--------|------|------|
| 프로젝트 | `.claude/agents/<name>.md` | 현재 프로젝트만 |
| 사용자 | `~/.claude/agents/<name>.md` | 모든 프로젝트 |
| 플러그인 | `<plugin>/agents/<name>.md` | 플러그인 활성화된 곳 |

**우선순위**: 프로젝트 > 사용자 (이름 충돌 시 프로젝트 우선)

---

## 핵심 특징

1. **독립 컨텍스트**: 메인 대화와 분리된 컨텍스트 윈도우
2. **도구 제한**: 서브에이전트별로 다른 도구 접근 설정
3. **전문성**: 특정 도메인에 최적화된 지시
4. **재사용성**: 여러 프로젝트에서 재사용, 팀 공유 가능

---

## Frontmatter 필드

```yaml
---
name: code-reviewer
description: 코드 리뷰 전문가. 코드 변경 후 자동 사용.
tools: Read, Grep, Glob, Bash
model: inherit
permissionMode: default
skills: skill1, skill2
---
```

### 필수 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| `name` | 고유 식별자 (소문자, 하이픈) | `code-reviewer` |
| `description` | 언제/무엇을 하는지 | `Code review specialist. Use after code changes.` |

### 선택 필드

| 필드 | 설명 | 기본값 | 예시 |
|------|------|--------|------|
| `tools` | 사용 가능 도구 | 모든 도구 | `Read, Grep, Glob, Bash` |
| `model` | 사용 모델 | 기본 모델 | `sonnet`, `opus`, `haiku`, `inherit` |
| `permissionMode` | 권한 모드 | `default` | `default`, `acceptEdits`, `bypassPermissions` |
| `skills` | 자동 로드 스킬 | 없음 | `skill1, skill2` |

---

## 내장 서브에이전트

### general-purpose

| 항목 | 값 |
|------|-----|
| 모델 | Sonnet |
| 도구 | 모든 도구 |
| 용도 | 복잡한 다단계 작업, 탐색+수정 필요 시 |

### Plan

| 항목 | 값 |
|------|-----|
| 모델 | Sonnet |
| 도구 | Read, Glob, Grep, Bash (읽기 전용) |
| 용도 | 계획 수립 전 맥락 수집 |

### Explore

| 항목 | 값 |
|------|-----|
| 모델 | Haiku (빠름) |
| 도구 | Glob, Grep, Read, Bash (읽기 전용) |
| 용도 | 코드베이스 검색/탐색 |

**철저함 수준:**
- `quick`: 빠른 검색
- `medium`: 속도/철저함 균형
- `very thorough`: 포괄적 분석

---

## 호출 방식

### 1. 자동 위임

Claude가 description 기반으로 자동 판단:

```yaml
description: 금융 코드 검증. 백테스트/매매 로직 수정 후 사용.
```

→ 백테스트 코드 수정하면 자동 호출

**자동 호출 강화 키워드:**
- "use PROACTIVELY"
- "MUST BE USED"
- "Use immediately after..."

### 2. 명시적 호출

사용자가 직접 지정:

```
> Use the code-reviewer subagent to check my changes
> Have the debugger subagent investigate this error
```

### 3. Task 도구로 호출

```json
{
  "description": "Continue analysis",
  "prompt": "Examine error handling patterns",
  "subagent_type": "code-analyzer",
  "resume": "abc123"
}
```

---

## 서브에이전트 템플릿

```markdown
---
name: agent-name
description: 역할 설명. 트리거 키워드 포함.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a [역할] specializing in [전문 분야].

When invoked:
1. 단계 1
2. 단계 2
3. 단계 3

Checklist:
- 확인 사항 1
- 확인 사항 2

Output format:
- 출력 형식 설명
```

---

## 예제

### 1. 코드 리뷰어

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific code examples for how to fix each issue.
```

### 2. 디버거

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### 3. 테스트 러너

```markdown
---
name: test-runner
description: Test automation expert. Use proactively to run tests and fix failures. MUST BE USED when you see code changes.
tools: Read, Edit, Bash, Grep
---

You are a test automation expert.

When invoked:
1. Run appropriate test suite for the codebase
2. Identify test failures
3. Analyze failure reasons
4. Implement fixes while preserving test intent
5. Verify all tests pass

Test running strategy:
- Run full suite first
- Check which tests fail
- Examine test code and implementation
- Fix implementation or test as appropriate
- Re-run to verify

For each failure:
- Root cause of the failure
- Whether to fix code or test
- Specific implementation
- Verification steps
```

---

## Skill과의 비교

| 항목 | 서브에이전트 | Skill |
|------|-------------|-------|
| **컨텍스트** | 독립 (메인과 분리) | 메인에 포함 |
| **용도** | 복잡한 다단계 작업 | 지식/지시사항 제공 |
| **메인 컨텍스트 영향** | 없음 | 포함됨 |
| **복잡 작업** | 좋음 | 좋음 |
| **간단 지시** | 오버헤드 가능 | 효율적 |

### 서브에이전트 사용

- 복잡한 다단계 작업
- 독립적인 맥락 필요
- 특정 도구만 허용해야 함
- 메인 대화와 완전 분리 필요

예: 코드 리뷰어, 테스트 러너, 디버거

### Skill 사용

- Claude가 자동으로 발견해야 함
- 지식/지시사항 제공
- 복잡한 참고 자료 필요
- 스크립트/유틸리티 포함

예: PDF 처리, 데이터 분석, 문서 생성

---

## 작성 모범 사례

### 해야 할 것

1. **단일 책임**: 하나의 명확한 역할만
2. **상세한 프롬프트**: 구체적 지시, 예시, 제약 조건
3. **도구 제한**: 필요한 도구만 허용
4. **명확한 description**: 자동 호출 유도
5. **버전 관리**: git에 커밋

### 하지 말 것

1. **범용 에이전트**: 너무 많은 책임
2. **모호한 description**: 자동 호출 실패
3. **과도한 도구**: 보안/집중도 저하
4. **문서 없음**: 유지보수 어려움
5. **너무 많이 만들기**: 10개 이상은 관리 어려움
6. **중복 금지**: Rule/Skill에 있는 내용 반복하지 않음 (링크로 참조)

---

## description 작성법

### 좋은 예

```yaml
description: Code review specialist for security, performance, and style. Use proactively IMMEDIATELY AFTER code changes.
```

- 구체적 행동 동사 ("review", "fix", "test")
- 트리거 키워드 포함
- "MUST BE USED", "use PROACTIVELY" 명시

### 나쁜 예

```yaml
description: Helps with code
```

- 너무 일반적
- 트리거 키워드 없음
