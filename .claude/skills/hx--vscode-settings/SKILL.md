---
name: hx--vscode-settings
description: VSCode 설정 수정. "단축키", "keybinding", "테마", "색상" 관련 요청 시 사용.
---

# VSCode Settings 관리

## 사용 시점
- 단축키 변경/추가 요청
- 테마, 색상 커스터마이징
- 확장 설정 변경
- 기타 VSCode 설정 수정

## 핵심 원칙

**Settings Sync 최우선**
- VSCode Settings Sync가 활성화되어 있음
- 포맷 후 VSCode 로그인만 하면 모든 설정 자동 복원
- 설정 변경은 **반드시 사용자 설정 파일**에만 할 것

## 수정 대상 파일

| 설정 종류 | 파일 위치 | Sync 여부 |
|----------|----------|----------|
| 일반 설정, 테마, 색상, 확장 설정 | `C:\Users\hwano\AppData\Roaming\Code\User\settings.json` | Sync |
| 키보드 단축키 | `C:\Users\hwano\AppData\Roaming\Code\User\keybindings.json` | Sync |
| 스니펫 | `C:\Users\hwano\AppData\Roaming\Code\User\snippets\` | Sync |
| 워크스페이스 설정 | `.vscode/settings.json` | Git으로만 관리 |

## 주의사항
- **절대** 워크스페이스 설정(`.vscode/settings.json`)에 개인 설정 넣지 말 것
- 사용자 설정 파일만 Settings Sync로 동기화됨
- 확장 프로그램 설정도 반드시 사용자 설정 파일에 추가

## 단축키 관련 특이사항

### command-runner 확장
- 단축키: `keybindings.json`에 정의
- 명령어: `settings.json`의 `command-runner.commands`에 정의
- **둘 다 사용자 설정 파일에 있어야 Settings Sync로 동기화됨**

예시:
```json
// keybindings.json
{
    "key": "alt+a",
    "command": "workbench.action.tasks.runTask",
    "args": "Send File to Maya",
    "when": "editorTextFocus && editorLangId == 'python'"
}

// settings.json
{
    "command-runner.commands": {
        "Send File to Maya": "python \"path/to/script.py\" \"${file}\""
    }
}
```
