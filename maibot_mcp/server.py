"""MaiBot MCP — 让 op/polaris 当脑、MaiBot(经 OneBot/NapCat) 当手进 QQ。

工具集（第一版）：
- send_text        发文本
- send_voice       语音条：TTS(edge/elevenlabs) -> base64 -> [CQ:record]  (复用 SnowLuma 链路)
- send_image       发图片(URL)
- handle_image     收到 QQ 图片 -> 返回 URL，供脑(识图)读取
- get_login_info   确认 QQ 端在跑

用法：MCP 客户端(mcpServers)配置本 server，见 mcp.json。
依赖：pip install fastmcp ; 语音条再 pip install edge-tts（或设 ELEVENLABS_API_KEY）。
"""
from __future__ import annotations

import os
import tempfile
from typing import Optional

from fastmcp import FastMCP

from onebot import OneBotClient, OneBotError
from tts import synthesize

mcp = FastMCP("maibot_mcp")

BASE_URL = os.environ.get("MAIBOT_ONEBOT_URL", "http://127.0.0.1:3000")
TOKEN = os.environ.get("MAIBOT_ONEBOT_TOKEN", "")

_bot = OneBotClient(BASE_URL, TOKEN)


def _cleanup_tmp(path: Optional[str]) -> None:
    if path and path.startswith(tempfile.gettempdir()):
        try:
            os.remove(path)
        except OSError:
            pass


@mcp.tool
def send_text(target: int, text: str, is_group: bool = False) -> dict:
    """向 QQ 发送一条文本消息。
    Args:
        target: 私聊=QQ号；群聊=群号
        text: 要发送的文本
        is_group: True 为群聊，False 为私聊
    """
    try:
        return {"ok": True, "message_id": _bot.send_text(target, text, is_group)}
    except OneBotError as e:
        return {"ok": False, "error": str(e)}


@mcp.tool
def send_voice(target: int, text: str, is_group: bool = False,
               tts_provider: str = "edge", voice: Optional[str] = None) -> dict:
    """生成语音条发到 QQ（复用 SnowLuma 链路：TTS -> base64 -> [CQ:record]）。
    Args:
        target: 私聊=QQ号；群聊=群号
        text: 要朗读成语音的文字
        is_group: True 群聊 / False 私聊
        tts_provider: edge(默认,免费中文好) 或 elevenlabs(付费音质好)
        voice: 可选音色；edge 默认 zh-CN-XiaoxiaoNeural，elevenlabs 默认 Rachel
    """
    path = None
    try:
        path = synthesize(text, provider=tts_provider, voice=voice)
        return {"ok": True, "message_id": _bot.send_voice_file(target, path, is_group), "tts": tts_provider}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}
    finally:
        _cleanup_tmp(path)


@mcp.tool
def send_image(target: int, image_url: str, is_group: bool = False) -> dict:
    """向 QQ 发送一张图片（直接给可公网访问的 URL）。
    Args:
        target: 私聊=QQ号；群聊=群号
        image_url: 图片公网 URL
        is_group: True 群聊 / False 私聊
    """
    try:
        return {"ok": True, "message_id": _bot.send_image_url(target, image_url, is_group)}
    except OneBotError as e:
        return {"ok": False, "error": str(e)}


@mcp.tool
def handle_image(image_url: str) -> dict:
    """收到 QQ 图片后，把图交给脑(op/polaris)读取。
    Args:
        image_url: QQ 图床 URL（来自收到的消息）
    """
    return {
        "image_url": image_url,
        "note": "请用本地识图/视觉模型读取该图（QQ图片 -> 本机 -> 读图工具）。",
        "vision_tool_hint": "download image then use local vision/OCR",
    }


@mcp.tool
def get_login_info() -> dict:
    """获取 QQ 登录信息，确认端在运行。"""
    try:
        return _bot.get_login_info()
    except OneBotError as e:
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")