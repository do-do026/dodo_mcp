# dodo_mcp — 架构设计（ARCHITECTURE）

> 面向「从 Operit 搬到北极星」的 MCP 版 QQ/AI 集成。分三层，脑在手之上，QQ 在手之下。

## 总体分层
```
┌─────────────────────────────────────────────────────────┐
│  脑层  op/polaris 本地 AI                                │
│    · 记忆库（本地对话 AI 可调用）                         │
│    · 语音条生成（本地 TTS）                               │
│    · 识图（本地视觉/OCR，读 QQ 图片）                     │
└──────────────────────────┬──────────────────────────────┘
                           │ MCP 协议（streamable HTTP / stdio）
┌──────────────────────────▼──────────────────────────────┐
│  手层  MCP servers（两个独立）                             │
│    · maibot_mcp   （驱动 MaiBot，经 OneBot 进 QQ）        │
│    · astrbot_mcp  （驱动 AstrBot，经 OneBot 进 QQ）       │
└──────────────────────────┬──────────────────────────────┘
                           │ OneBot v11
┌──────────────────────────▼──────────────────────────────┐
│  QQ 层  OneBot v11 / NapCat                              │
│    · 收/发文本、语音条(record)、表情、图片(image)          │
└─────────────────────────────────────────────────────────┘
```

## 各层职责
| 层 | 提供 | 说明 |
|---|---|---|
| **脑层** | op/polaris | 思考、记忆、语音生成、识图。**不在本工程写**，是外部宿主能力 |
| **手层** | MCP server | 把 QQ 能力包成 MCP 工具，供脑驱动。**本工程核心** |
| **QQ 层** | OneBot v11 | MaiBot/AstrBot 都立在它上面；手直接打这一层 |

## 关键决策
- MCP 是**外部脑→手**的标准协议；op/polaris 当脑，两个 MCP 并列当手。
- 语音条/图片走 **OneBot 层**（MaiBot/AstrBot 共用），不重复实现。
- MaiBot 内部用 `maim_message`（FastAPI+WS），WebUI 发消息走 WS；故手层打其 OneBot/NapCat。

## 复用（来源标注）
- **SnowLuma（hermes-snowluma）**：语音条 `TTS→base64→[CQ:record]`、图片 `[CQ:image]`、OneBot HTTP 动作 —— 只借实现，不引入本体。
- **astrbotmcp（xunxiing）**：AstrBot 被外部脑经 MCP 驱动（图片回传）。
- **mcp-builder / mcp-cli**：写 & 测 MCP server 方法论。

## 待定
- 脑侧到底用 op 还是北极星（迁移目标未定）。
- 选 MaiBot、AstrBot、还是两者兼有当手（用户已倾向两个都写）。
- QQ空间(说说)依赖 NapCat 扩展 API（OneBot v11 无），待摸。