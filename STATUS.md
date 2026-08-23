# dodo_mcp — 状态（STATUS）
> 更新：2026-08-24 01:20

## 已完成
- [x] 建仓库 do-do026/dodo_mcp（公开），初始 README/PLAN
- [x] 摸清 MaiBot / AstrBot 生态（MCP、语音/表情/识图、插件）
- [x] 查社区已有 QQ→MCP 轮子（napcat_mcp / hermes-snowluma / astrbotmcp 等）
- [x] 记记忆库：astrbotmcp 可直接复用（UUID fea920df）
- [x] 拉 SnowLuma 语音条/图片实现（send-voice.py / voice-capability-research.md / send-image-to-qq）
- [x] 摸清 MaiBot 内部（maim_message：FastAPI+WS，旧版 127.0.0.1:8000，可选 API Server WS+api_key）
- [x] **MaiBot MCP 第一版核心**：maibot_mcp/（server.py / onebot.py / tts.py / mcp.json / requirements.txt / README.md），语法通过，已推 GitHub

## 进行中 / 待办
- [x] **连线信息**：实读 NapCat `onebot11_810429614.json`，仅 WS(6098/token dodo-meow-meow)，HTTP 未启用
- [x] **改走 WS（选 B）**：MaiBot MCP 改用 WS 客户端连 `ws://100.85.178.93:6098`（Tailscale 内网，不暴露公网）
- [ ] **QQ空间(说说)**：依赖 NapCat 扩展 API（OneBot v11 无），待摸
- [ ] **识图回链**：`handle_image` 目前只回传 URL，需接脑侧本地识图/OCR 真读
- [ ] **AstrBot MCP**：基于 astrbotmcp 另写一个（暂缓）
- [ ] **本地/真机验证**：在 op/polaris MCP 界面接入跑通（WS 连接、发文本/语音/图片）
- [ ] 语音条试点：edge(默认)/elevenlabs，需配 ELEVENLABS_API_KEY

## 关键结论（供回看）
- MaiBot 在 GitHub 无"被外部脑经 MCP 驱动"的现成 server（全为客户端方向）；AstrBot 有（astrbotmcp）。
- MaiBot 的 QQ 侧能力（语音/表情/识图）= OneBot 能力，`hermes-snowluma` 已包成 MCP，可直接借。
- op/polaris 本机就是完整 MCP 主机（mcp_config.json 已有多个 server），可先在本机测 MCP。
- 换轮子：AstrBot=生态大/多平台/MCP原生/DeepSeek/多模态/1000+插件；MaiBot=QQ陪伴型/人设活/语音表情识图/MCP(streamable)/插件系统。