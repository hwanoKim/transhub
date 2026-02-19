---
name: hx--hooks-writing
description: Claude Code 훅을 작성하거나 수정할 때 사용합니다. "훅 만들어줘", "hooks.json 작성해줘" 요청에 트리거.
---

# Hooks Writing Guide

훅을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/hooks

## 훅 설정 위치

| 위치 | 파일 | 스코프 |
|------|------|--------|
| 사용자 설정 | `~/.claude/settings.json` | 모든 프로젝트 |
| 프로젝트 설정 | `.claude/settings.json` | 팀 공유 (버전 관리) |
| 로컬 설정 | `.claude/settings.local.json` | 개인 프로젝트 (gitignore) |
| 플러그인 | `<plugin>/hooks/hooks.json` | 플러그인 활성화된 곳 |
| 스킬/에이전트 | frontmatter의 `hooks` 필드 | 해당 컴포넌트 활성화 중 |

상세 가이드는 [hooks-guide.md](hooks-guide.md) 참조.

## 훅 이벤트 라이프사이클

```
SessionStart → UserPromptSubmit → PreToolUse → PermissionRequest →
PostToolUse → Stop → SubagentStart → SubagentStop → SessionEnd
```

## hooks.json 기본 구조

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash-script",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 보안 모범 사례

1. **입력 검증** - 입력 데이터를 맹목적으로 신뢰하지 않기
2. **변수 인용** - `$VAR` 대신 `"$VAR"` 사용
3. **경로 탐색 차단** - 경로에 `..` 확인
4. **절대 경로 사용** - 스크립트에 전체 경로 지정
5. **민감한 파일 건너뛰기** - `.env`, `.git`, 키 파일 피하기
