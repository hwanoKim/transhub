# 포매팅

## Obsidian 링크

```markdown
[[파일명]]              # 기본
[[파일명|표시텍스트]]   # 별칭
```

**주의**: Obsidian은 폴더 무시, 파일명으로만 연결

```markdown
# 올바름
[[arch-overview]]
[[arch-overview|아키텍처 개요]]

# 틀림 (폴더 경로 사용 금지)
[[architecture/arch-overview]]
[[../index]]
```

## 브레드크럼

`breadcrumb:` 메타데이터로 작성. docs-viewer가 sticky bar로 자동 렌더링.

### 형식

```markdown
# 문서 제목

breadcrumb: [[index|Project]] > [[architecture-index|Architecture]]
```

- `# Title` 아래에 `breadcrumb:` 한 줄만 작성
- 현재 페이지는 **적지 않음** — 플러그인이 `# Title`에서 자동 추출하여 마지막에 추가
- 하단 반복 불필요 (sticky bar가 항상 보이므로)
- `breadcrumb:` 라인은 본문에 표시되지 않음

### 깊이별 예시

**1단계** (최상위 인덱스):
```markdown
breadcrumb: [[index|Project]]
```

**2단계** (일반 문서):
```markdown
breadcrumb: [[index|Project]] > [[architecture-index|Architecture]]
```

**3단계** (서브폴더 문서):
```markdown
breadcrumb: [[index|Project]] > [[architecture-index|Architecture]] > [[maya-index|Maya]]
```

### 레거시 방식 (사용 금지)

이전에는 상단/하단에 동일한 브레드크럼을 반복 작성했으나, 더 이상 사용하지 않음.
docs-viewer가 레거시 패턴 감지 시 경고를 표시.

```markdown
# ❌ 레거시 (사용 금지)
[[index|Project]] > [[parent|Parent]] > 문서 제목
---
...
---
[[index|Project]] > [[parent|Parent]] > 문서 제목
```

마이그레이션: [migration.md](migration.md) 참조

## 인덱스 테이블

```markdown
| 문서 | 설명 |
|------|------|
| [[파일명]] | 한 줄 설명 |
| [[파일명|표시명]] | 한 줄 설명 |
```

## 정렬 규칙

- **인덱스**: 가나다순 또는 논리적 순서
- **Research/Discussion**: 최신 것부터 (날짜 내림차순)

## 문서 템플릿

### 일반 문서

```markdown
# {제목}

breadcrumb: [[index|Project]] > [[{parent}-index|Parent]]

## 개요

{한두 문장 설명}

## {섹션 1}

{내용}

## 관련 문서

| 문서 | 설명 |
|------|------|
| [[관련문서1]] | 설명 |
```

### 인덱스 문서

```markdown
# {카테고리명}

breadcrumb: [[index|Project]]

{한 줄 설명}

| 문서 | 설명 |
|------|------|
| [[문서1]] | 설명 |
| [[문서2]] | 설명 |
```

## 코드 블록

언어 명시 필수:

```markdown
\`\`\`python
def example():
    pass
\`\`\`

\`\`\`typescript
const example = () => {}
\`\`\`

\`\`\`bash
npm install
\`\`\`
```

## 표 정렬

```markdown
| 왼쪽 정렬 | 가운데 | 오른쪽 |
|:----------|:------:|-------:|
| 텍스트    | 텍스트 | 텍스트 |
```
