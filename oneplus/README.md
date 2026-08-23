# oneplus/ —— 一加 Operit 适配版

> 本文件夹是「一加手机 + Operit」上跑通并验证的版本（2026-08-24）。

**版本特征**
- 走 **OneBot 反向 WS**（`ws://101.43.38.124:6098`，token `dodo-meow-meow`）
- **Tailscale `100.85.178.93` 从本机连不通**（一加不在 tailnet），故用**公网 IP**
- MCP server 以 **stdio** 方式被 Operit spawn（`python3 server.py`）
- 已验证：WS 连通 / `get_login_info` / `send_text`（发文本）✅
- 语音条：record 链路可用；音频生成需能装 edge-tts 或配 `ELEVENLABS_API_KEY`

**适配目标**：一加 Operit 当脑，本 MCP 当手，走 WS 进 QQ。

## 结构
- `maibot_mcp/` — MaiBot MCP server（server.py / onebot_ws.py / tts.py / mcp.json / requirements.txt / README.md）

## 说明
红米 + 北极星版将在 `redmi/` 下另建（届时可能改用「远程 streamable HTTP/SSE」部署，红米不装 Python）。