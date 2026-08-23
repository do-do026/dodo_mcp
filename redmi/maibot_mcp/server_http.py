"""MaiBot MCP for 红米+北极星 — streamable HTTP 远程部署版.

北极星不能装 Python/插件 → 用「远程 streamable HTTP/SSE」接入。
本 server 部署在服务器(101.43.38.124)，走 Tailscale 内网(100.85.178.93)，
红米北极星用「远程」填 URL 即可，零本地安装。

服务端连 NapCat WS(服务器本机 127.0.0.1:6098)。
工具集同 oneplus 版：send_text / send_voice / send_image / handle_image / get_login_info。
"""
from __future__ import annotations

import os
import tempfile
from typing import Optional

from fastmcp import FastMCP

from onebot_ws import OneBotWSClient, OneBotError
from tts import synthesize

mcp = FastMCP("maibot_mcp")

# 服务器本机 NapCat WS（同一台服务器）
BASE_URL = os.environ.get("MAIBOT_ONEBOT_URL", "ws://127.0.0.1:6098")
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
def send_voice(target: int, text: str, is_group: bool = False, tts_provider: str = "edge", voice: Optional[str] = None) -> dict:
    """生成语音条发到 QQ（复用 SnowLuma 链路：TTS -> base64 -> [CQ:record]）。"""
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
    """向 QQ 发送一张图片（直接给可公网访问的 URL）。"""
    try:
        return {"ok": True, "message_id": _bot.send_image_url(target, image_url, is_group)}
    except OneBotError as e:
        return {"ok": False, "error": str(e)}


@mcp.tool
def handle_image(image_url: str) -> dict:
    """收到 QQ 图片后，把图交给脑(北极星)读取。"""
    return {
        "image_url": image_url,
        "note": "请用本地识图/视觉模型读取该图（QQ图片 -> 本地 -> 读图工具）。",
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
    mcp.run(
        transport="streamable-http",
        host=os.environ.get("MAIBOT_MCP_HOST", "0.0.0.0"),
        port=int(os.environ.get("MAIBOT_MCP_PORT", "9080")),
    )
