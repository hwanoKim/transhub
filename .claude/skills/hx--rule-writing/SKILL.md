---
name: hx--rule-writing
description: Claude Code 룰(메모리/지침)을 작성하거나 수정할 때 사용합니다. "룰 만들어줘", "CLAUDE.md 작성해줘", "메모리 작성해줘" 요청에 트리거.
---

# Rule Writing Guide

룰(메모리/지침)을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/memory

## 메모리 타입 계층

| 타입 | 위치 | 용도 |
|------|------|------|
| **프로젝트 메모리** | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 팀 공유 지침 |
| **프로젝트 룰** | `./.claude/rules/*.md` | 모듈화된 주제별 지침 |
| **사용자 메모리** | `~/.claude/CLAUDE.md` | 개인 설정 |
| **사용자 룰** | `~/.claude/rules/*.md` | 개인 룰 (모든 프로젝트 적용) |
| **로컬 메모리** | `./CLAUDE.local.md` | 개인 프로젝트 설정 (자동 gitignore) |

상세 가이드는 [rule-guide.md](rule-guide.md) 참조.

## 룰 디렉토리 구조

```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 메인 프로젝트 지침
│   └── rules/
│       ├── code-style.md   # 코드 스타일 가이드
│       ├── testing.md      # 테스트 규칙
│       └── frontend/       # 하위 폴더로 구성 가능
│           └── react.md
```

- `.claude/rules/` 내 모든 `.md` 파일은 **자동으로 로드**됨
- 재귀적으로 하위 디렉토리 탐색

## 작성 모범 사례

1. **룰을 집중적으로 유지** - 파일당 하나의 주제
2. **설명적인 파일명 사용** - 파일명이 적용 범위를 나타내도록
3. **구체적으로 작성** - "코드 포맷팅하기" 보다 "2칸 들여쓰기 사용"
4. **구조화하기** - 마크다운 제목 아래 불릿 포인트로 정리
