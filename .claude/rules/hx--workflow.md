# Workflow Rule

> 자동 생성 (hwano-plugins). 업데이트: `Hwano: Update Claude Rules`
> **도구**: Serena MCP 활성화 시 아래 Serena 섹션 참고

## 병렬 처리

**독립적인 작업은 반드시 병렬로 실행.**

### 병렬 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| Tool 병렬 | 한 턴에 여러 도구 호출 | 여러 파일 동시 Read/Edit/Grep |
| Agent 병렬 | 여러 서브에이전트 동시 실행 | 독립적인 탐색/작업 분할 |
| Phase 병렬 | 작업 단계를 병렬화 | 코드+문서 동시 작성 |

### 의존성 판단

| 상황 | 실행 |
|------|------|
| 여러 파일 읽기 | 병렬 |
| 독립 파일 수정 | 병렬 |
| A가 만들고 B가 사용 | 순차 |
| 같은 파일 여러 번 수정 | 하나의 Edit으로 통합 |
| 코드 + 문서 (같은 기능) | **병렬** |
| 코어 모듈 + 의존 모듈 | 순차 |
| 독립적인 탐색 작업 | Agent 병렬 |

### 흔한 실수

- 파일을 하나씩 읽기 → 한 번에 읽기
- 독립 파일을 하나씩 수정 → 의존성 분석 후 병렬
- 같은 파일 여러 번 Edit → 하나로 합치기
- 문서를 마지막에 작성 → 코드와 병렬로 작성
- 단일 에이전트로 큰 탐색 → 여러 에이전트로 분할

## 에이전트 오케스트레이션

### 작업 흐름

```
사용자 요청 → 분석(code-analyzer/researcher) → 계획(code-planner) → 코딩
    → 빌드(build-error-resolver) → 리뷰(code-reviewer) → 문서(doc-updater) → 마무리
```

간단한 수정은 분석/계획을 건너뛰고 바로 코딩 가능.

### 에이전트 호출 매트릭스

| 상황 | 호출 에이전트 |
|------|-------------|
| 코드 구조/의존성 파악 | **code-analyzer** |
| 리팩토링 가능 여부 판단 | **code-analyzer** |
| 특정 변경의 영향 범위 확인 | **code-analyzer** |
| 문서/파일 탐색 후 요약 필요 | **code-analyzer** |
| 디렉토리 구조 파악 | **code-analyzer** |
| "~해도 될까?", "~분리할까?" 등 판단 질문 | **code-analyzer** |
| 외부 API/라이브러리 사용법 조사 | **researcher** |
| 공식 문서, 레퍼런스 확인 | **researcher** |
| 에러 원인/해결 사례 검색 | **researcher** |
| 복잡한 기능 구현 계획 수립 | **code-planner** |
| 대규모 리팩토링 단계 설계 | **code-planner** |
| 빌드/컴파일 실패 | **build-error-resolver** |
| 코드 작성/수정 완료 후 리뷰 | **code-reviewer** |
| 보안 취약점/데드코드 검토 | **code-reviewer** |
| 기능 변경 후 문서 동기화 | **doc-updater** |

### 왜 위임하는가

메인 세션에서 직접 분석하면 코드/문서 전체가 컨텍스트에 쌓여 낭비됨.
에이전트에 위임하면 **필요한 결과만 요약으로** 받아 컨텍스트를 절약.

### 병렬 실행 규칙

**병렬 가능:**
- `code-analyzer + code-analyzer` (독립 탐색)
- `code-analyzer + researcher` (내부 분석 + 외부 조사 동시)

**순차 필요:**
- `code-planner → 코딩 → build-error-resolver → code-reviewer`

## Serena 도구 활용

> Serena MCP 서버가 없는 프로젝트에서는 이 섹션을 무시하세요.

### 도구 선택 기준

| 작업 | Serena 도구 | 기본 도구 |
|------|-------------|----------|
| 클래스/함수 구조 파악 | `get_symbols_overview`, `find_symbol` | - |
| 참조 추적 | `find_referencing_symbols` | - |
| 심볼 단위 수정 | `replace_symbol_body`, `insert_after_symbol` | - |
| 심볼 이름 변경 | `rename_symbol` | - |
| 단순 파일 읽기 (~100줄) | - | `Read` |
| 파일명 검색 | - | `Glob` |
| 간단한 텍스트 검색 | - | `Grep` |
| 몇 줄 수정 | - | `Edit` |

### 파일 크기별 가이드

| 파일 크기 | 구조 파악 | 내용 읽기 |
|-----------|----------|----------|
| ~100줄 | `Read` | `Read` |
| 100줄+ | `get_symbols_overview` | `find_symbol` (필요한 것만) |

### 핵심 원칙

1. **심볼 단위로 생각하기** - 파일 전체가 아닌 클래스/함수/메서드 단위로 작업
2. **필요한 것만 읽기** - `find_symbol`로 특정 심볼만 조회
3. **참조 확인 후 수정** - `find_referencing_symbols`로 영향 범위 파악
4. **심볼릭 수정 우선** - `replace_symbol_body`가 `Edit`보다 안전

### 프로젝트 활성화

VSCode에서 Serena 사용 시 프로젝트가 자동 인식되지 않음. 세션 시작 시 반드시 활성화:

```
mcp__plugin_serena_serena__activate_project(project: ".")
```

또는 MCP 서버 시작 인자에 `--project` 추가로 자동화:

```bash
serena start-mcp-server --context ide-assistant --project <프로젝트경로>
```
