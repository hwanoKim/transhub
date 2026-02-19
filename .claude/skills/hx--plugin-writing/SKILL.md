---
name: hx--plugin-writing
description: Claude Code 플러그인을 작성하거나 수정할 때 사용합니다. "플러그인 만들어줘", "plugin.json 작성해줘" 요청에 트리거.
---

# Plugin Writing Guide

플러그인을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/plugins

## 플러그인 구조

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # 필수: 플러그인 매니페스트
├── commands/                # 사용자 실행 명령어 (.md 파일)
├── skills/                  # 모델 자동 호출 스킬
│   └── skill-name/
│       └── SKILL.md
├── agents/                  # 서브에이전트 정의
├── hooks/                   # 이벤트 핸들러
│   └── hooks.json
├── .mcp.json               # MCP 서버 설정
└── .lsp.json               # LSP 서버 설정
```

**중요**: `.claude-plugin/` 디렉토리 안에는 오직 `plugin.json`만 위치합니다.

상세 가이드는 [plugin-guide.md](plugin-guide.md) 참조.

## 지원되지 않는 컴포넌트

플러그인에서는 다음 디렉토리가 **지원되지 않습니다**:

| 디렉토리 | 대안 |
|----------|------|
| `rules/` | Skills의 SKILL.md에 지침 포함 |
| `tasks/` | Skills 또는 Agents로 대체 |
| `.claude/CLAUDE.md` | Skills에 지침 분산 |

## plugin.json 필수 필드

```json
{
  "name": "plugin-name",
  "description": "플러그인에 대한 간단한 설명",
  "version": "1.0.0",
  "hooks": "./hooks/hooks.json"
}
```

## 자동 업데이트 (hwano 플러그인 필수)

모든 hwano의 플러그인은 반드시 자동 업데이트 기능을 포함해야 합니다.

```json
// hooks/hooks.json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "claude plugin marketplace update hwano-plugins || echo \"[Warning] Plugin update failed\""
          }
        ]
      }
    ]
  }
}
```
