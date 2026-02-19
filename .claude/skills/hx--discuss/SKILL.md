---
name: hx--discuss
description: 다른 AI(Gemini, Codex)와 토론/상의. "물어봐", "토론해", "의견 들어봐" 등의 요청 시 사용.
---

# AI 토론 스킬

## 사용 시점

- "Gemini한테 물어봐"
- "Codex랑 토론해"
- "다른 AI 의견 들어봐"
- "이거 검증해봐"

## 도구 선택

| 도구 | CLI 명령어 | 특징 |
|------|-----------|------|
| **Gemini** | `gemini` | 빠름 (3-5초) |
| **Codex** | `codex` | 느림 (10초+), 더 상세한 분석 |

**중요**: 둘 다 **읽기 전용**으로 사용. 프로젝트 파일을 읽고 의견을 들은 후, 실제 수정은 Claude Code가 수행.

## 호출 방법

### 환경별 CLI 사용법

> **참고**: CLI 버전/설치 상태가 컴퓨터마다 다를 수 있음.
> 아래 "기타 환경" 방식이 안 되면 해당 컴퓨터 이름과 작동하는 방식을 추가할 것.

#### hwano-work (회사)

```bash
# Gemini: -p 플래그 필수, --file 옵션 없음
gemini -p "이 코드의 문제점이 뭐야?"
gemini -p "이 파일 리뷰해줘: $(cat src/main.py)"

# Codex: exec 서브커맨드 필수
codex exec "이 설계 패턴에 대해 의견 줘"
codex exec "src/utils.py를 읽고 리팩토링 의견 줘"
```

#### 기타 환경 (기본값)

```bash
# Gemini: positional argument 또는 -p
gemini "이 코드의 문제점이 뭐야?"
gemini "이 파일 리뷰해줘" --file src/main.py

# Codex: exec 또는 interactive
codex exec "이 설계 패턴에 대해 의견 줘"
codex "interactive 모드로 질문"
```

### Gemini

```bash
# 단순 질문
gemini -p "이 코드의 문제점이 뭐야?"

# 파일 내용 포함 (--file 없으면 cat으로 주입)
gemini -p "이 파일 리뷰해줘: $(cat src/main.py)"
```

### Codex

**주의**: Codex CLI는 `--file` 옵션이 없음. 프롬프트에 파일 경로를 명시하면 Codex가 직접 읽음.

```bash
# 단순 질문 (프로젝트 접근 없음)
codex exec "이 설계 패턴에 대해 의견 줘"

# 프로젝트 파일 읽기/쓰기 (필수 플래그)
codex exec --dangerously-bypass-approvals-and-sandbox "src/utils.py를 읽고 리팩토링 의견 줘"

# 읽기 전용 모드
codex exec -s read-only "cli/page.py의 FlowPage 설계에 대해 분석해줘"

# 쓰기 가능 모드
codex exec -s workspace-write "테스트 코드 작성해줘"

# 자동 승인 + 쓰기
codex exec --full-auto "버그 수정해줘"
```

## 모드

| 모드 | 트리거 | 처리 |
|------|--------|------|
| **단순 질문** | "물어봐", "토론해" | CLI 호출 → 응답 전달 |
| **문서화** | "토론문서 만들어줘" | CLI 호출 → docs 스킬로 문서 저장 |

**기본은 단순 질문.** 문서 생성은 명시적 요청 시에만.

## 단순 질문 흐름

```
1. 사용자: "Gemini한테 이 로직 맞는지 물어봐"
2. Claude: gemini CLI 호출
3. Claude: Gemini 응답을 사용자에게 전달
4. (끝)
```

## 문서화 흐름

```
1. 사용자: "Codex랑 토론하고 문서로 남겨줘"
2. Claude: codex CLI 호출
3. Claude: 토론 내용 정리
4. Claude: docs 스킬 호출하여 discussions 폴더에 저장
5. (끝)
```

문서 저장 시 [discussions-template.md](discussions-template.md) 참조.

## 토론 패턴

> 아래 예시는 hwano-work 환경 기준. 다른 환경에서는 "환경별 CLI 사용법" 참조.

### 코드 리뷰

```bash
# Gemini
gemini -p "이 PR의 변경사항 리뷰해줘. 보안 이슈나 성능 문제 있는지 확인해줘: $(cat src/auth.py)"

# Codex (프롬프트에 경로 명시)
codex exec --dangerously-bypass-approvals-and-sandbox \
  "src/auth.py를 읽고 보안 이슈나 성능 문제 있는지 리뷰해줘"
```

### 설계 검증

```bash
# Gemini
gemini -p "이 아키텍처 설계에 대해 의견 줘. 확장성 관점에서 문제 있을까?: $(cat docs/architecture.md)"

# Codex
codex exec --dangerously-bypass-approvals-and-sandbox \
  "docs/architecture.md를 읽고 확장성 관점에서 문제 있는지 의견 줘"
```

### 브레인스토밍

```bash
# Gemini/Codex 동일 (파일 참조 불필요)
gemini -p "캐싱 전략 어떻게 하면 좋을까? Redis vs Memcached vs 인메모리 비교해줘"
codex exec "캐싱 전략 어떻게 하면 좋을까? Redis vs Memcached vs 인메모리 비교해줘"
```

### 버그 분석

```bash
# Gemini (여러 파일 내용 주입)
gemini -p "이 에러 왜 발생하는 거야? 해결책 알려줘. 에러로그: $(cat error.log) 핸들러: $(cat src/handler.py)"

# Codex (프롬프트에 여러 경로 명시)
codex exec --dangerously-bypass-approvals-and-sandbox \
  "error.log와 src/handler.py를 읽고 에러 원인과 해결책 알려줘"
```

## 주의사항

- **Gemini/Codex 모두 읽기 전용** - 토론용으로 프로젝트 파일을 읽고 의견을 받은 후, 실제 코드 수정은 Claude Code가 수행
- Codex는 `--file` 옵션 없음 - 프롬프트에 파일 경로 직접 명시
- Codex로 프로젝트 파일 접근 시 `--dangerously-bypass-approvals-and-sandbox` 필수
- Codex interactive 모드는 Claude Code 내부에서 실행 불가 (stdin 문제)
- **Codex Windows 한글 깨짐**: Windows 설정 → `intl.cpl` → 관리자 옵션 → 시스템 로캘 변경 → "베타: 세계 언어 지원을 위해 Unicode UTF-8 사용" 체크 → 재부팅
- 민감한 정보(API 키, 비밀번호) 포함된 파일 전송 주의
- 응답이 너무 길면 요약해서 전달
