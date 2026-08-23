"""MaiBot MCP - OneBot(QQ) hand.

复用 SnowLuma（hermes-snowluma）的语音条/图片实现：
- 语音条: OneBot `send_private_msg` / `send_group_msg` + `[CQ:record,file=base64://...]`
- 图片:   `[CQ:image,file=<bot-local-path>]` (经 download_file 让 QQ 端拉取)
- 通用:   OneBot v11 HTTP API + Bearer token

注意：MaiBot 本身跑在 NapCat/OneBot 之上；本模块直接打 OneBot HTTP API，
即 MaiBot 的 QQ 层（也是 AstrBot 会用的同一层）。
"""
from __future__ import annotations

import base64
import json
import os
import urllib.request
from typing import Optional


class OneBotError(RuntimeError):
    pass


class OneBotClient:
    def __init__(self, base_url: str, token: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def _post(self, path: str, payload: dict) -> dict:
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise OneBotError(f"OneBot HTTP {e.code}: {e.read()[:200]}")
        except Exception as e:  # noqa: BLE001
            raise OneBotError(f"OneBot request failed: {e}")

    def _check(self, result: dict) -> int:
        if result.get("status") != "ok":
            raise OneBotError(f"OneBot status != ok: {result}")
        data = result.get("data") or {}
        return data.get("message_id")

    def send_private(self, user_id: int, message: list) -> int:
        return self._check(self._post("/send_private_msg", {"user_id": user_id, "message": message}))

    def send_group(self, group_id: int, message: list) -> int:
        return self._check(self._post("/send_group_msg", {"group_id": group_id, "message": message}))

    def send_text(self, target: int, text: str, is_group: bool = False) -> int:
        return self.send_group(target, [{"type": "text", "data": {"text": text}}]) if is_group \
            else self.send_private(target, [{"type": "text", "data": {"text": text}}])

    def send_voice_file(self, target: int, audio_path: str, is_group: bool = False) -> int:
        """SnowLuma 语音条实现：读文件 -> base64 -> [CQ:record,file=base64://...]"""
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        msg = [{"type": "record", "data": {"file": f"base64://{b64}"}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def send_voice_url(self, target: int, url: str, is_group: bool = False) -> int:
        """语音条：直接给 QQ 图床 URL（大文件用 URL 而非 base64）。"""
        msg = [{"type": "record", "data": {"file": url}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def send_image_path(self, target: int, image_path: str, is_group: bool = False) -> int:
        """SnowLuma 图片实现：先 download_file 让 QQ 端拉到本地，再 [CQ:image,file=本地路径]。"""
        raise NotImplementedError("图片需结合 download_file + 本地路径，见 send_image_url")

    def send_image_url(self, target: int, url: str, is_group: bool = False) -> int:
        """图片：直接给可公网访问的 URL。"""
        msg = [{"type": "image", "data": {"file": url}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def get_login_info(self) -> dict:
        return self._post("/get_login_info", {})
