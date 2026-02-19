# 수정 워크플로우

## 수정 대상

`.docs-check-result.json`의 `broken_links` 항목

캐시 위치: `~/Documents/temp/docs-cache/{프로젝트명}/`

## 수정 전략

### 1. 링크 대상 파악

```json
{
  "source": "index.md",
  "source_path": ".docs/index.md",
  "broken_link": "old-doc",
  "context": "| [[old-doc]] | 설명 |"
}
```

### 2. 수정 방법 결정

| 상황 | 조치 |
|------|------|
| 파일명 변경됨 | 새 파일명으로 링크 수정 |
| 파일 삭제됨 | 링크 제거 또는 대체 문서로 변경 |
| 오타 | 올바른 파일명으로 수정 |
| 미작성 문서 | 링크 제거 또는 문서 생성 |

### 3. context 활용

`context` 필드에서 주변 맥락 확인 후 적절한 수정 판단

## 수정 후 필수 작업

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/fix/scripts/docs_indexer.py" --update
```

인덱스 업데이트로 수정 반영 확인

## 브레드크럼 수정

파일이 이동된 경우 (hash 변경, 내용 동일):

1. 상단 브레드크럼 확인
2. 하단 브레드크럼 확인
3. 경로에 맞게 수정

```markdown
# 수정 전
[[index|H-Board]] > [[old-parent]] > 현재

# 수정 후
[[index|H-Board]] > [[new-parent]] > 현재
```
