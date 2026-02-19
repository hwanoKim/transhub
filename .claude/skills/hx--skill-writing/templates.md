# 스킬 템플릿

## 기본 스킬

```markdown
---
name: explain-code
description: 코드를 시각적 다이어그램과 비유로 설명합니다
---

코드를 설명할 때 항상 다음을 포함하세요:

1. **비유로 시작**: 일상생활에 비유
2. **다이어그램 그리기**: ASCII 아트로 흐름/구조 표현
3. **코드 설명**: 단계별로 설명
4. **주의사항 강조**: 흔한 실수는?

설명은 대화체로 유지합니다.
```

---

## 사이드 이펙트가 있는 스킬

```markdown
---
name: deploy
description: 프로덕션에 배포합니다
disable-model-invocation: true
allowed-tools: Bash(npm:*), Bash(git:*)
---

# 배포

$ARGUMENTS를 프로덕션에 배포:

1. 테스트 스위트 실행
2. 애플리케이션 빌드
3. 배포 푸시
```

---

## 서브에이전트로 실행하는 스킬

```markdown
---
name: deep-research
description: 주제를 심층 조사합니다
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

# 심층 조사

$ARGUMENTS에 대해 철저히 조사:

1. Glob과 Grep으로 관련 파일 찾기
2. 코드 읽고 분석
3. 파일 참조와 함께 발견 사항 요약
```

---

## 읽기 전용 스킬

```markdown
---
name: safe-reader
description: 파일을 수정 없이 읽습니다
allowed-tools: Read, Grep, Glob
---

# 안전한 파일 읽기

파일을 읽고 분석하되 수정하지 않습니다.

$ARGUMENTS
```

---

## 지원 파일 참조

SKILL.md에서 같은 폴더의 다른 파일을 참조:

```markdown
- 전체 API 상세는 [reference.md](reference.md) 참조
- 사용 예시는 [examples.md](examples.md) 참조
```
