# Hooks Writing Guide

훅을 만들거나 수정하기 전에 반드시 이 가이드를 따르시오.

**공식 문서**: https://code.claude.com/docs/en/hooks

---

## 훅 설정 위치

| 위치 | 파일 | 스코프 |
|------|------|--------|
| 사용자 설정 | `~/.claude/settings.json` | 모든 프로젝트 |
| 프로젝트 설정 | `.claude/settings.json` | 팀 공유 (버전 관리) |
| 로컬 설정 | `.claude/settings.local.json` | 개인 프로젝트 (gitignore) |
| 플러그인 | `<plugin>/hooks/hooks.json` | 플러그인 활성화된 곳 |
| 스킬/에이전트 | frontmatter의 `hooks` 필드 | 해당 컴포넌트 활성화 중 |

---

## 훅 이벤트 라이프사이클

```
SessionStart → UserPromptSubmit → PreToolUse → PermissionRequest →
PostToolUse → Stop → SubagentStart → SubagentStop → SessionEnd
```

---

## 사용 가능한 훅 이벤트

| 이벤트 | 트리거 | 용도 |
|--------|--------|------|
| **SessionStart** | 세션 시작/재개 | 컨텍스트 로드, 환경변수 설정 |
| **SessionEnd** | 세션 종료 | 정리 작업 |
| **UserPromptSubmit** | 사용자 프롬프트 제출 | Claude 처리 전 검증/컨텍스트 추가 |
| **PreToolUse** | 도구 실행 전 | 도구 호출 허용/거부/수정 |
| **PermissionRequest** | 권한 대화 표시 | 권한 자동 허용/거부 |
| **PostToolUse** | 도구 성공 후 | 실행 후 피드백/검증 |
| **PostToolUseFailure** | 도구 실패 후 | 도구 실패 처리 |
| **Stop** | Claude 응답 완료 | Claude 계속 여부 결정 |
| **SubagentStart** | 서브에이전트 생성 | 서브에이전트 초기화 모니터링 |
| **SubagentStop** | 서브에이전트 종료 | 서브에이전트 완료 제어 |
| **PreCompact** | 컨텍스트 압축 전 | 압축 전 로직 |
| **Setup** | `--init`, `--maintenance` | 일회성 초기화/유지보수 |
| **Notification** | Claude Code 알림 전송 | 알림 처리 |

---

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

---

## 훅 타입

### 1. Command 훅 (`type: "command"`)

셸 명령어를 직접 실행:

```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 60
}
```

### 2. Prompt 훅 (`type: "prompt"`)

LLM을 사용한 지능적 결정 (Stop, SubagentStop, UserPromptSubmit, PreToolUse, PermissionRequest에서 사용):

```json
{
  "type": "prompt",
  "prompt": "Claude가 중지해야 하는지 평가: $ARGUMENTS. 모든 작업이 완료되었는지 확인.",
  "timeout": 30
}
```

**필수 응답 형식:**
```json
{
  "ok": true,
  "reason": "ok=false일 때 설명"
}
```

---

## 도구 매처 패턴

### 주요 도구 이름

| 도구 | 설명 |
|------|------|
| `Bash` | 셸 명령어 |
| `Write` | 파일 쓰기 |
| `Edit` | 파일 편집 |
| `Read` | 파일 읽기 |
| `Glob` | 파일 패턴 매칭 |
| `Grep` | 콘텐츠 검색 |
| `WebFetch`, `WebSearch` | 웹 작업 |
| `Task` | 서브에이전트 작업 |
| `mcp__<server>__<tool>` | MCP 도구 |

### 매처 패턴 예시

```json
{
  "matcher": "Write",           // 정확히 일치
  "matcher": "Edit|Write",      // 여러 도구 (정규식)
  "matcher": "Notebook.*",      // 정규식 패턴
  "matcher": "*",               // 모든 도구
  "matcher": ""                 // 모든 도구 (빈 문자열)
}
```

---

## 환경 변수

### 모든 훅에서 사용 가능

| 변수 | 설명 |
|------|------|
| `CLAUDE_PROJECT_DIR` | 프로젝트 루트 디렉토리 (절대 경로) |
| `CLAUDE_CODE_REMOTE` | 웹이면 "true", 로컬 CLI면 비어있음 |

### Setup & SessionStart 전용

| 변수 | 설명 |
|------|------|
| `CLAUDE_ENV_FILE` | 환경변수 지속을 위한 파일 경로 |

### 플러그인 훅 전용

| 변수 | 설명 |
|------|------|
| `${CLAUDE_PLUGIN_ROOT}` | 플러그인 디렉토리 절대 경로 |

---

## 훅 입력 스키마

### 공통 필드 (모든 훅)

```json
{
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "EventName"
}
```

### 도구별 입력 예시

**PreToolUse - Bash:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm run build",
    "description": "Build the project",
    "timeout": 120000
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**PreToolUse - Write:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**UserPromptSubmit:**
```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "사용자 입력 텍스트"
}
```

---

## 훅 출력 및 종료 코드

### 종료 코드 동작

| 코드 | 동작 |
|------|------|
| **0** | 성공. stdout이 JSON 또는 사용자에게 표시 |
| **2** | 차단 에러. stderr만 사용; 작업 차단 |
| **기타** | 비차단 에러. verbose 모드에서 stderr 표시 |

### JSON 출력 형식

**공통 필드:**
```json
{
  "continue": true,
  "stopReason": "메시지",
  "suppressOutput": false,
  "systemMessage": "경고"
}
```

### 이벤트별 출력

**PreToolUse 결정 제어:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "이유",
    "updatedInput": { "field": "new_value" },
    "additionalContext": "Claude용 컨텍스트"
  }
}
```

**PermissionRequest 결정 제어:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": { },
      "message": "텍스트",
      "interrupt": false
    }
  }
}
```

---

## 실용적인 예시

### 1. Bash 명령어 검증

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
command = input_data.get("tool_input", {}).get("command", "")

if tool_name == "Bash" and "rm -rf /" in command:
    print("위험한 명령어 차단!", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

### 2. 문서 파일 자동 승인

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
file_path = input_data.get("tool_input", {}).get("file_path", "")

if tool_name == "Read" and file_path.endswith((".md", ".txt")):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "문서 파일 자동 승인"
        }
    }
    print(json.dumps(output))

sys.exit(0)
```

### 3. 지능형 Stop 훅 (Prompt 기반)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Claude가 작업을 중지해야 하는지 평가하세요. 컨텍스트: $ARGUMENTS\n\n분석:\n1. 사용자 요청 작업이 모두 완료되었는지\n2. 해결해야 할 에러가 있는지\n3. 후속 작업이 필요한지\n\nJSON 응답: {\"ok\": true} 중지 허용, {\"ok\": false, \"reason\": \"설명\"} 계속",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 4. 민감한 파일 보호

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

### 5. TypeScript 자동 포매팅

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 6. 데스크톱 알림

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### 7. SessionStart 환경변수 지속

```bash
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  export NODE_ENV=production
  export API_KEY=your-api-key
  source ~/.nvm/nvm.sh
  nvm use 20

  # 환경변수 변경 캡처
  export -p >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

---

## 스킬/에이전트 frontmatter 훅

스킬이나 에이전트 frontmatter에서 직접 훅 정의 가능:

```yaml
---
name: secure-operations
description: 보안 검사가 포함된 작업 수행
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
---
```

### 스킬 전용 옵션

| 옵션 | 설명 |
|------|------|
| `once` | `true`: 세션당 한 번만 실행 |

---

## 훅 실행 세부사항

| 항목 | 값 |
|------|------|
| **타임아웃** | 기본 60초 (설정 가능) |
| **병렬화** | 매칭된 훅은 병렬 실행 |
| **중복 제거** | 동일한 명령어는 자동 중복 제거 |
| **작업 디렉토리** | Claude Code 환경의 현재 디렉토리 |

---

## 보안 모범 사례

1. **입력 검증** - 입력 데이터를 맹목적으로 신뢰하지 않기
2. **변수 인용** - `$VAR` 대신 `"$VAR"` 사용
3. **경로 탐색 차단** - 경로에 `..` 확인
4. **절대 경로 사용** - 스크립트에 전체 경로 지정
5. **민감한 파일 건너뛰기** - `.env`, `.git`, 키 파일 피하기
6. **명령어 검토** - 배포 전 훅 코드 이해

---

## 디버깅

디버그 출력 활성화:
```bash
claude --debug
```

훅 등록 확인:
```
/hooks
```

### 일반적인 문제

| 문제 | 해결 |
|------|------|
| JSON 구문 오류 | settings 파일의 JSON 구문 확인 |
| 대소문자 구분 | 도구 이름은 정확히 일치해야 함 |
| 이스케이프 안 된 따옴표 | JSON 문자열에서 따옴표 이스케이프 |
| 스크립트 실행 불가 | 실행 권한 및 경로 확인 |
| 타임아웃 | 느린 작업에 타임아웃 조정 |

---

## 주요 사용 사례

- **알림**: Claude Code 입력 대기 시 커스텀 알림
- **자동 포매팅**: prettier, gofmt 등 자동 실행
- **로깅**: 규정 준수/디버깅을 위한 명령어 추적
- **피드백**: 코드 규칙 준수 확인
- **커스텀 권한**: 프로덕션 파일 수정 차단
- **환경 설정**: 세션 시작 시 환경변수 로드
