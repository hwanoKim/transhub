---
name: hx--claude-code-research
description: Claude Code 공식 문서, 방식, 자료를 조사할 때 사용합니다. 플러그인, 스킬, 커맨드, 훅 등 Claude Code 기능에 대한 최신 정보를 찾을 때 호출됩니다.
allowed-tools: WebSearch, WebFetch, Read
---

# Claude Code 공식 자료 조사

Claude Code의 공식 문서, 기능, 방식을 조사하는 스킬입니다.

## 공식 자료 출처

### 1. 공식 문서 사이트

- **메인 문서**: https://code.claude.com/docs/en/
- **스킬/커맨드 문서**: https://code.claude.com/docs/en/slash-commands
- **플러그인 문서**: https://code.claude.com/docs/en/plugins
- **마켓플레이스**: https://code.claude.com/docs/en/plugins/marketplaces
- **훅 문서**: https://code.claude.com/docs/en/hooks

### 2. GitHub 저장소

- **Claude Code 메인 저장소**: https://github.com/anthropics/claude-code
- **이슈 및 토론**: https://github.com/anthropics/claude-code/issues

### 3. 검색 키워드

조사할 때 다음 키워드와 함께 검색:
- `site:code.claude.com`
- `site:github.com/anthropics claude-code`
- `"claude code" plugin`
- `"claude code" SKILL.md`

## 조사 절차

### Step 1: 웹 검색
```
WebSearch로 관련 키워드 검색
예: "claude code command frontmatter" site:code.claude.com
```

### Step 2: 공식 문서 확인
```
WebFetch로 공식 문서 페이지 내용 확인
예: https://code.claude.com/docs/en/slash-commands
```

### Step 3: 로컬 가이드 참조
```
Read로 프로젝트 내 가이드 문서 확인
예: .docs/claude-code-plugin-guide.md
```

## 주요 조사 주제

| 주제 | 참고 URL |
|------|----------|
| 커맨드/스킬 작성 | https://code.claude.com/docs/en/slash-commands |
| 훅 설정 | https://code.claude.com/docs/en/hooks |
| 플러그인 구조 | https://code.claude.com/docs/en/plugins |
| MCP 서버 | https://code.claude.com/docs/en/mcp |
