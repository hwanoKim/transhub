# 하위 도메인 스킬 (중첩 구조)

복잡한 스킬은 하위 도메인으로 분리하여 구성할 수 있습니다. SKILL.md가 라우터 역할을 하고, 각 도메인별 `main.md`가 해당 영역의 메인 문서가 됩니다.

---

## 구조

```
my-skill/
├── SKILL.md              # 라우터: 도메인별 진입점 안내
├── domain-a/
│   ├── main.md           # 도메인 A 메인 문서
│   ├── detail-1.md
│   └── detail-2.md
├── domain-b/
│   ├── main.md           # 도메인 B 메인 문서
│   └── examples.md
└── domain-c/
    └── main.md           # 도메인 C 메인 문서
```

---

## SKILL.md 라우터 패턴

```markdown
---
name: my-skill
description: 여러 도메인 지원. (domain-a, domain-b, domain-c)
---

# My Skill

## 도메인 라우팅

| 트리거 | 도메인 |
|--------|--------|
| "키워드1", "키워드2" | [domain-a](domain-a/main.md) |
| "키워드3", "키워드4" | [domain-b](domain-b/main.md) |
| "키워드5" | [domain-c](domain-c/main.md) |

## 폴더 기반 자동 선택

| 경로 패턴 | 도메인 |
|-----------|--------|
| `src/feature-a/**` | domain-a |
| `src/feature-b/**` | domain-b |
```

---

## 동작 방식

1. 스킬 호출 시 SKILL.md가 먼저 로드됨
2. Claude가 라우팅 테이블을 보고 적절한 도메인 판단
3. 해당 도메인의 `main.md`를 Read 도구로 읽음
4. 필요시 추가 상세 문서도 읽음

---

## 컨벤션

| 파일 | 역할 |
|------|------|
| `SKILL.md` | 스킬 진입점, 라우터 |
| `<domain>/main.md` | 각 도메인의 메인 문서 |
| `<domain>/*.md` | 도메인 내 상세 문서 |

**주의**: 하위 도메인 문서는 자동 로드되지 않습니다. Claude가 SKILL.md의 링크를 보고 능동적으로 읽어야 합니다.
