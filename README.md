# redmi/ —— 红米 + 北极星 适配版

> 北极星**不能装 Python/插件**，故采用「**远程 streamable HTTP/SSE**」接入：MCP server 部署在服务器 `101.43.38.124`，走 **Tailscale 内网** `100.85.178.93`，红米北极星用「远程」填 URL 即可，**红米零本地安装**。

## 连线信息（2026-08-24 实测）
- 红米能连 **Tailscale** `100.85.178.93`（一加不行，红米行）✅
- 服务器 Python 3.12.3 + `fastmcp 3.4.4` + `websocket-client 1.7.0`（已就绪）✅
- NapCat WS `6098` 就在服务器本机 → server 连 `ws://127.0.0.1:6098`

## 端点（北极星用「远程」接入）
- **URL**：`http://100.85.178.93:9080/mcp`
- **类型**：streamable-http
- 见 `maibot_mcp/mcp.json`

## 部署位置（服务器）
- MCP server 跑在 `101.43.38.124`（Tailscale），`~/redmi/maibot_mcp/`
- 启动：`MAIBOT_ONEBOT_TOKEN=... python3 server_http.py`（streamable-http, :9080）

## 工具集
send_text / send_voice / send_image / handle_image / get_login_info（同 oneplus 版，复用 SnowLuma 语音条链路）
