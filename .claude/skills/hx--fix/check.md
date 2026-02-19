# 검사 워크플로우

## 스크립트 실행

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/fix/scripts/docs_indexer.py" --check
```

## CLI 옵션

| 옵션 | 설명 |
|------|------|
| `--rebuild` | 전체 인덱스 재생성 |
| `--update` | 증분 업데이트 |
| `--check` | 깨진 링크 탐지 (추천) |

## 캐시 파일

캐시 위치: `~/Documents/temp/docs-cache/{프로젝트명}/`

### .docs-index.json

```json
{
  "version": "1.0",
  "project": "H-Board",
  "project_path": "C:\\document\\projects\\H-Board",
  "last_scan": "2026-01-10T14:30:00+00:00",
  "files": {
    "index.md": {
      "path": ".docs/index.md",
      "hash": "a1b2c3...",
      "content_hash": "d4e5f6...",
      "links_to": ["arch-overview"],
      "linked_by": []
    }
  }
}
```

### .docs-check-result.json

```json
{
  "scan_time": "2026-01-10T14:30:00+00:00",
  "project": "H-Board",
  "total_files": 100,
  "broken_links": [
    {
      "source": "index.md",
      "source_path": ".docs/index.md",
      "broken_link": "old-doc",
      "context": "| [[old-doc]] | 설명 |"
    }
  ],
  "duplicate_names": []
}
```

## 검사 항목

| 항목 | 설명 |
|------|------|
| 깨진 링크 | `[[링크]]` 대상 파일 없음 |
| 파일명 중복 | 같은 이름 다른 폴더 |
