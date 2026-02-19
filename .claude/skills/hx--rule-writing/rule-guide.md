# Rule Writing Guide

룰(메모리/지침)을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/memory

---

## 메모리 타입 계층

| 타입 | 위치 | 용도 | 스코프 |
|------|------|------|--------|
| **관리 정책** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | 조직 전체 지침 | 모든 사용자 |
| **프로젝트 메모리** | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 팀 공유 지침 | 버전 관리 포함 |
| **프로젝트 룰** | `./.claude/rules/*.md` | 모듈화된 주제별 지침 | 버전 관리 포함 |
| **사용자 메모리** | `~/.claude/CLAUDE.md` | 개인 설정 | 개인 사용자 |
| **사용자 룰** | `~/.claude/rules/*.md` | 개인 룰 (모든 프로젝트 적용) | 개인 사용자 |
| **로컬 메모리** | `./CLAUDE.local.md` | 개인 프로젝트 설정 | 자동 gitignore |

---

## 룰 디렉토리 구조

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 메인 프로젝트 지침
│   └── rules/
│       ├── code-style.md   # 코드 스타일 가이드
│       ├── testing.md      # 테스트 규칙
│       ├── security.md     # 보안 요구사항
│       └── frontend/       # 하위 폴더로 구성 가능
│           ├── react.md
│           └── styles.md
```

- `.claude/rules/` 내 모든 `.md` 파일은 **자동으로 로드**됨
- 재귀적으로 하위 디렉토리 탐색
- `.claude/CLAUDE.md`와 동일한 우선순위

---

## 룰 파일 Frontmatter

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/services/**/*.ts"
---

# API 개발 룰

- 모든 API 엔드포인트는 입력 검증 필수
- 표준 에러 응답 포맷 사용
- OpenAPI 문서 주석 포함
```

### paths 필드 (선택)

특정 파일 패턴에만 룰을 적용할 때 사용:

```yaml
---
paths:
  - "src/**/*.ts"              # src 내 모든 TypeScript 파일
  - "lib/**/*.ts"              # lib 내 모든 TypeScript 파일
  - "tests/**/*.test.ts"       # 테스트 파일
  - "src/**/*.{ts,tsx}"        # .ts와 .tsx 모두
  - "{src,lib}/**/*.ts"        # 여러 디렉토리 (brace expansion)
  - "*.md"                     # 루트의 마크다운 파일
  - "src/components/*.tsx"     # 특정 디렉토리
---
```

---

## Import 구문

CLAUDE.md 파일에서 다른 파일을 가져올 수 있음:

```markdown
프로젝트 개요는 @README 참조, npm 명령어는 @package.json 참조

# 추가 지침
- git 워크플로우: @docs/git-instructions.md
- 개인 설정: @~/.claude/my-project-instructions.md
```

**Import 규칙:**
- 상대/절대 경로 지원
- 최대 5단계 재귀 import
- 코드 블록 내부에서는 평가되지 않음
- `/memory` 명령어로 로드된 메모리 확인 가능

---

## CLAUDE.md vs .claude/rules/ 비교

| 항목 | CLAUDE.md | .claude/rules/ |
|------|-----------|----------------|
| **용도** | 일반적인 프로젝트 지침 | 모듈화된 주제별 룰 |
| **위치** | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | `./.claude/rules/*.md` |
| **구성** | 단일 파일 | 여러 파일 + 하위 폴더 |
| **스코프** | 프로젝트 전체 | frontmatter로 경로별 지정 가능 |
| **적합한 용도** | 아키텍처, 워크플로우, 일반 가이드라인 | 언어별, 기능별 룰 |

---

## 메모리 조회 순서

1. 현재 디렉토리에서 상위로 `CLAUDE.md`, `CLAUDE.local.md` 탐색
2. 하위 디렉토리 읽을 때 해당 경로의 `CLAUDE.md` 발견
3. 프로젝트 레벨에서 `.claude/rules/` 로드
4. 사용자 레벨 `~/.claude/rules/`는 프로젝트 룰보다 먼저 로드 (프로젝트 룰이 더 높은 우선순위)

---

## 룰 파일 템플릿

### 기본 룰

```markdown
# 코드 스타일 룰

- 2칸 들여쓰기 사용
- ESLint 규칙 준수
- 함수는 단일 책임 원칙 따르기
```

### 경로 제한 룰

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API 개발 룰

모든 API 엔드포인트는:
- 입력 검증 필수
- 에러 핸들링 구현
- 로깅 포함
```

### 심볼릭 링크 활용

```bash
# 공유 룰 디렉토리 링크
ln -s ~/shared-claude-rules .claude/rules/shared

# 개별 룰 파일 링크
ln -s ~/company-standards/security.md .claude/rules/security.md
```

---

## 유용한 명령어

| 명령어 | 설명 |
|--------|------|
| `/memory` | 메모리 파일 편집 |
| `/init` | 프로젝트용 CLAUDE.md 생성 |

---

## 작성 모범 사례

1. **룰을 집중적으로 유지** - 파일당 하나의 주제 (예: `testing.md`, `api-design.md`)
2. **설명적인 파일명 사용** - 파일명이 적용 범위를 나타내도록
3. **하위 디렉토리로 구성** - 관련 룰 그룹화 (예: `frontend/`, `backend/`)
4. **구체적으로 작성** - "코드 포맷팅하기" 보다 "2칸 들여쓰기 사용"
5. **정기적으로 검토** - 프로젝트 발전에 맞춰 메모리 업데이트
6. **구조화하기** - 마크다운 제목 아래 불릿 포인트로 정리
7. **조건부 룰은 신중하게** - 특정 파일 타입에만 적용되는 경우에만 `paths` frontmatter 추가
