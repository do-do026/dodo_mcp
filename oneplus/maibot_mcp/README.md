# MaiBot MCP（第一版核心）

让 **op/polaris 当脑**、**MaiBot（经 OneBot/NapCat）当手**进 QQ 的 MCP server。
复用 **SnowLuma（hermes-snowluma）** 的语音条/图片链路，**不引入 Hermes/SnowLuma 本体**。

## 文件
- `server.py`  — FastMCP server（工具入口）
- `onebot_ws.py` — **WS 版** OneBot 手：发文本/语音/图片（base64 record = SnowLuma 语音条套路）
- `tts.py`     — 语音合成：edge(默认) / elevenlabs（可选）
- `mcp.json`   — mcpServers 配置示例
- `requirements.txt`

## 工具
| 工具 | 作用 |
|---|---|
| `send_text` | 发文本（私聊/群聊） |
| `send_voice` | **语音条**：TTS → base64 → `[CQ:record]`（复用 SnowLuma） |
| `send_image` | 发图片（URL） |
| `handle_image` | 收到 QQ 图片 → 回传 URL，交脑识图 |
| `get_login_info` | 确认 QQ 端在跑 |

## 配置（env）
- `MAIBOT_ONEBOT_URL`：MaiBot 所用 OneBot/NapCat 的 HTTP 地址（默认 `http://127.0.0.1:3000`）
- `MAIBOT_ONEBOT_TOKEN`：OneBot access token
- `ELEVENLABS_API_KEY`：可选，走 ElevenLabs 语音条

## 依赖
```bash
pip install fastmcp edge-tts
# 或只用 ElevenLabs：设 ELEVENLABS_API_KEY，可不装 edge-tts
```

## 接入
在 op/polaris 的 MCP 界面用 **远程/配置导入** 填 `mcp.json`（或填 stdio command）。