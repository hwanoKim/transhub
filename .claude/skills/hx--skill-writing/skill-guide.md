# Skill Writing Guide

스킬을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/skills

---

## 스킬 위치

| 스코프 | 위치 | 용도 |
|--------|------|------|
| 엔터프라이즈 | 관리 설정 | 조직 전체 |
| 개인 | `~/.claude/skills/<skill-name>/SKILL.md` | 모든 프로젝트 |
| 프로젝트 | `.claude/skills/<skill-name>/SKILL.md` | 해당 프로젝트만 |
| 플러그인 | `<plugin>/skills/<skill-name>/SKILL.md` | 플러그인 활성화된 곳 |

**우선순위**: 엔터프라이즈 > 개인 > 프로젝트

---

## 스킬 구조

```
.claude/skills/
└── my-skill/
    ├── SKILL.md           # 필수: 메인 지침
    ├── reference.md       # 선택: 상세 문서
    ├── examples.md        # 선택: 사용 예시
    └── scripts/           # 선택: 실행 스크립트
        └── validate.sh
```

모든 스킬은 반드시 `SKILL.md` 파일이 필요합니다.

---

## 상세 가이드

| 주제 | 문서 |
|------|------|
| Frontmatter, 변수, 훅 | [frontmatter.md](frontmatter.md) |
| 스킬 템플릿 | [templates.md](templates.md) |
| 하위 도메인 (중첩 구조) | [nested-skills.md](nested-skills.md) |

---

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| 스킬이 트리거되지 않음 | description을 자연어에 맞게 수정; `/skill-name`으로 직접 호출 시도 |
| 너무 자주 트리거됨 | description을 더 구체적으로; `disable-model-invocation: true` 추가 |
| Claude가 모든 스킬을 보지 못함 | 스킬 description이 15,000자 예산 초과 확인 (`SLASH_COMMAND_TOOL_CHAR_BUDGET` 환경변수로 조정) |

---

## Commands vs Skills 비교

| 항목 | Commands | Skills |
|------|----------|--------|
| **위치** | `commands/<name>.md` | `skills/<name>/SKILL.md` |
| **구조** | 단일 파일 | 폴더 (지원 파일 포함 가능) |
| **훅** | 지원 안 함 | frontmatter에서 훅 정의 가능 |
| **용도** | 단순한 명령어 | 복잡한 워크플로우, 라이프사이클 관리 |

둘 다 동일한 frontmatter 필드를 지원하지만, Skills가 더 많은 기능을 제공합니다.

---

## 작성 모범 사례

1. **description을 명확하게** - Claude가 자동 호출 판단에 사용
2. **부작용 있는 작업**은 `disable-model-invocation: true`
3. **필요한 도구만** `allowed-tools`로 제한
4. **지원 파일 활용** - 복잡한 문서는 별도 파일로 분리
5. **서브에이전트 활용** - 독립적인 작업은 `context: fork`
