# dodo_mcp — dodo 的 MCP 迁移工程

> 面向「从 Operit 搬到北极星」的 MCP 版 QQ/AI 集成。把 dodo_napcat 的 QQ 收发/识图/触发逻辑，包成 MCP server，供北极星（或任何 MCP 客户端）接入；可对接 MaiBot / AstrBot 等 Agent 后端。

## 背景
- 现状：dodo_napcat（Operit 插件）走 NapCat + OneBot v11，靠 Operit 的 `Tools.Chat` 调 AI。
- 目标：搬去北极星（只用 MCP），QQ 侧仍走 OneBot v11 / NapCat，AI/Agent 侧换成 MCP。

## 关键结论（2026-08-24）
- **本机 Operit 已是完整 MCP 主机**（mcp_config.json 有多个 server），可先在 op 上试 MCP。
- **MaiBot（麦麦）**：QQ 陪伴型，支持 **语音/表情/识图/MCP(streamable HTTP)/插件系统**，人设更"活"。
- **AstrBot**：通用 Agent 平台，**MCP 原生 / 多平台 / DeepSeek / 多模态 / 1000+ 插件**，生态更大。
- 两者走 MCP 都是**标准 mcpServers JSON 配置**接入。

## 可借鉴
- `mcp-builder` / `mcp-cli`：写 & 测 MCP server 方法论。
- `operit_editor`：本机 MCP 配置系统（mcp_config.json / 远程 endpoint / 部署规则）。
- `napcat_pro_bridge`：QQ 触发/识图/按群绑定逻辑（要移植进 MCP server 的核心素材）。
- `ptrel1/napcat_mcp`：把 NapCat/OneBot11 暴露成 MCP 工具的现成轮子。

## 路线（敏捷）
1. 先写 PLAN / DESIGN / ARCHITECTURE（迁移决策、两个后端对比、MCP 边界）。
2. 写**一个最小可跑 MCP server**（先包一条：QQ 收 → 识图 → 回），用 mcp-cli/Inspector 验证。
3. 在北极星（或 op）用 mcpServers 配置接入，验证闭环。
4. 按需对接 MaiBot 或 AstrBot 当 Agent 后端。

## 安全
- 代码/配置不含真实 IP/token/QQ 号；敏感值走 env/config 占位符。
- 提交前过敏感扫描。
