"""TTS for MaiBot MCP — 复用 SnowLuma 的语音条链路（TTS -> base64 -> record）。

参考 hermes-snowluma `voice-capability-research.md`：
- Edge TTS(默认,免费,中文好)  : edge-tts --text ... --voice zh-CN-XiaoxiaoNeural --write-media out.mp3
- ElevenLabs(付费,音质好)      : ELEVENLABS_API_KEY + /v1/text-to-speech/<voice_id>
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import urllib.request
from typing import Optional


class TTSError(RuntimeError):
    pass


def tts_edge(text: str, voice: str = "zh-CN-XiaoxiaoNeural", out_path: Optional[str] = None) -> str:
    """Edge TTS（免费，中文最佳）。返回生成的音频文件路径。"""
    out_path = out_path or tempfile.mktemp(suffix=".mp3")
    cmd = ["edge-tts", "--text", text, "--voice", voice, "--write-media", out_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    except FileNotFoundError:
        raise TTSError("未安装 edge-tts：pip install edge-tts")
    except subprocess.CalledProcessError as e:
        raise TTSError(f"edge-tts 失败: {e.stderr.decode()[:200]}")
    return out_path


def tts_elevenlabs(
    text: str,
    api_key: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
    model_id: str = "eleven_multilingual_v2",
    out_path: Optional[str] = None,
) -> str:
    """ElevenLabs TTS（付费，音质好）。复用 SnowLuma 记录的音色/长度限制。"""
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=('{"text": %s, "model_id": "%s"}' % (__import__("json").dumps(text), model_id)).encode(),
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            audio = resp.read()
    except Exception as e:
        raise TTSError(f"ElevenLabs TTS 失败: {e}")
    out_path = out_path or tempfile.mktemp(suffix=".mp3")
    with open(out_path, "wb") as f:
        f.write(audio)
    return out_path


def synthesize(text: str, provider: str = "edge", voice: Optional[str] = None) -> str:
    """统一入口。provider: edge / elevenlabs。返回音频文件路径。"""
    if provider == "elevenlabs":
        key = os.environ.get("ELEVENLABS_API_KEY", "")
        if not key:
            raise TTSError("ELEVENLABS_API_KEY 未设置")
        return tts_elevenlabs(text, key, voice_id=voice or "21m00Tcm4TlvDq8ikWAM")
    # 默认 edge
    return tts_edge(text, voice or "zh-CN-XiaoxiaoNeural")