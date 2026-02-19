---
name: hx--docs
description: .docs 문서 작성/관리. 문서 생성, 구조 정리, 리서치/토론 문서화 작업 시 사용.
---

# docs 스킬

**적용일**: 2026-01-23

이 날짜 이후 생성되는 문서에 적용됩니다.

## 가이드 문서

| 문서 | 설명 |
|------|------|
| [structure.md](structure.md) | 폴더 구조, 파일명 규칙, 인덱스화 |
| [formatting.md](formatting.md) | 링크, 브레드크럼, 템플릿 |
| [mermaid.md](mermaid.md) | Mermaid 다이어그램 문법, 호환성 |
| [research.md](research.md) | 리서치 문서 작성 |
| [sandbox.md](sandbox.md) | 샌드박스/실험 문서 |
| [migration.md](migration.md) | 기존 문서 마이그레이션 |

## 도메인 라우팅

| 키워드 | 참조 문서 |
|--------|-----------|
| 문서 구조, 폴더, 파일명, 인덱스화 | [structure.md](structure.md) |
| 링크, 브레드크럼, 포매팅, 템플릿 | [formatting.md](formatting.md) |
| mermaid, 다이어그램, flowchart | [mermaid.md](mermaid.md) |
| 리서치, 조사, 알아봐 | [research.md](research.md) |
| 샌드박스, 실험 | [sandbox.md](sandbox.md) |
| 기존 문서, 마이그레이션 | [migration.md](migration.md) |

**커맨드**:
- `/docs:sync` - 코드 기반 문서 동기화
- `/docs:fix` - 깨진 링크, 브레드크럼 검사/수정 → `fix` 스킬 참조

**참고**: AI 토론(Gemini/Codex)은 `llm-discussion` 플러그인 사용.

## 핵심 규칙 (요약)

- **Obsidian 호환** - `[[파일명]]` 형식 (폴더 경로 없이)
- **고유한 파일명** - 프로젝트 전체에서 중복 금지
- **브레드크럼 필수** - `breadcrumb:` 메타데이터 한 줄 (레거시 상단/하단 반복 금지)
- **인덱스는 링크만** - 내용은 하위 문서로 분리
