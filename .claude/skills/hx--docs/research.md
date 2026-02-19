# Research 문서

## 사용 시점

- "XXX 조사해줘"
- "XXX 리서치해줘"
- "XXX에 대해 알아봐줘"
- "문서로 정리해줘"

## 저장 위치

```
.docs/references/research/
├── ref-research-index.md       # 인덱스
├── {YYYYMM}/                   # 월별 폴더
│   └── {YYYYMMDD}-{title}.md
└── {topic}/                    # 주제별 폴더 (선택)
    └── {topic}-index.md
```

## 파일명 형식

```
{YYYYMMDD}-{title}.md
```

예시: `20260123-api-design-patterns.md`

## 리서치 절차

### 1. 주제 파악

- 조사 주제
- 조사 범위 (깊이, 넓이)
- 예상 결과물 형태

### 2. 정보 수집

| 소스 | 방법 |
|------|------|
| 웹 | WebSearch, WebFetch |
| AI | 다른 AI에게 요청 |
| 코드베이스 | Grep, Glob, Read |
| 기존 문서 | .docs/ 폴더 검색 |

### 3. 정보 정리

- 핵심 내용 요약
- 카테고리별 분류
- 비교표 작성 (해당 시)

### 4. 문서 생성

아래 템플릿 사용

## 대규모 리서치

관련 문서가 3개 이상이면 서브폴더 사용:

```
.docs/references/research/
└── {topic}/
    ├── {topic}-index.md        # 인덱스 (필수)
    ├── {topic}-overview.md     # 개요
    ├── raw/                    # 원문/소스
    │   ├── {topic}-raw-chatgpt.md
    │   └── {topic}-raw-perplexity.md
    └── {subtopic}/             # 하위 주제
        └── {topic}-{subtopic}.md
```

## 문서 템플릿

```markdown
# {제목}

[[index|Project]] > [[ref-research-index|Research]] > {제목}

---

**조사일**: YYYY-MM-DD

## 개요

{주제 설명}

## 조사 내용

### {섹션 1}

{내용}

### {섹션 2}

{내용}

## 결론/요약

{핵심 정리}

## 출처

- [출처1](URL)
- [출처2](URL)

---

[[index|Project]] > [[ref-research-index|Research]] > {제목}
```

## 완료 체크리스트

- [ ] 정보 수집 완료
- [ ] 문서 생성
- [ ] `ref-research-index.md` 업데이트
- [ ] 출처 명시
- [ ] 브레드크럼 확인
