# dodo_mcp PLAN（敏捷规划）

## 目标
把 dodo_napcat 的 QQ 能力迁移成 MCP server，供北极星（MCP 客户端）接入；后端可用 MaiBot 或 AstrBot。

## 待确认
- [ ] 北极星对 MCP 的约束（LLM 用什么、能连哪些平台、识图/语音要求）
- [ ] 选 MaiBot（活/QQ）还是 AstrBot（生态大/多平台）
- [ ] QQ 侧 NapCat 是否保留（识别/引用/群昵称依赖 OneBot v11 字段）

## MCP 边界（第一版最小 server）
- 工具1：`qq_send_text`（发文本）
- 工具2：`qq_send_image`（发图）
- 工具3：`qq_recognize_image`（识图：收到图 → 视觉模型/OCR → 返回描述）
- 工具4：`qq_list_messages`（拉消息/触发）
- （后续）按群绑定、回复规则、语音/表情

## 进度（2026-08-24）
- [x] 文档：README / PLAN / ARCHITECTURE / STATUS / CHANGELOG
- [x] 研究：MaiBot/AstrBot 生态、社区 QQ→MCP、SnowLuma 语音图片、MaiBot maim_message
- [x] MaiBot MCP v1 核心（maibot_mcp/，FastMCP + OneBot 手 + TTS，复用 SnowLuma 语音条）
- [ ] 接线（OneBot HTTP 地址+token）
- [ ] mcp-cli/Inspector 本地验证
- [ ] 北极星/op 配置接入 → 闭环
- [ ] AstrBot MCP

## 交付顺序（敏捷，参考）
1. 文档：README / PLAN / DESIGN / ARCHITECTURE / STATUS（先写，可改）
2. 最小 MCP server（Python/FastMCP）+ mcp.json 示例
3. 用 mcp-cli / Inspector 本地验证
4. 北极星（或 op）配置接入 → 闭环
5. 对接 MaiBot / AstrBot

## 复用
- `mcp-builder` / `mcp-cli` skill
- `operit_editor`（本机 MCP 系统）
- `napcat_pro_bridge` 的逻辑