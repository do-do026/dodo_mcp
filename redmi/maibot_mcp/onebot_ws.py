"""MaiBot MCP - OneBot(QQ) hand via WebSocket.

选 B：走 OneBot v11 **反向 WS server**（NapCat websocketServers，如 ws://100.85.178.93:6098）。
- 作为 WS 客户端连接，发送 OneBot 动作（send_private_msg / send_group_msg / ...）。
- 透传到 QQ：发文本、语音条(record base64)、图片(image URL)。
- 复用 SnowLuma 语音条实现：TTS -> base64 -> [CQ:record,file=base64://...]。

依赖：pip install websocket-client
"""
from __future__ import annotations

import json
import threading
import time
import uuid
from typing import Optional

import websocket  # websocket-client


class OneBotError(RuntimeError):
    pass


class OneBotWSClient:
    def __init__(self, url: str, token: str = "", timeout: int = 10):
        self.url = url
        self.token = token
        self.timeout = timeout
        self.ws: Optional[websocket.WebSocket] = None
        self._responses: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._connect()

    def _connect(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        url = self.url
        if self.token:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}token={self.token}"
        self.ws = websocket.create_connection(url, header=headers, timeout=self.timeout)
        threading.Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        try:
            while True:
                msg = self.ws.recv()
                if not msg:
                    continue
                data = json.loads(msg)
                echo = data.get("echo")
                if echo is not None:
                    with self._lock:
                        self._responses[echo] = data
        except Exception:
            pass

    def _call(self, action: str, params: dict) -> dict:
        if self.ws is None:
            raise OneBotError("WS 未连接")
        echo = str(uuid.uuid4())
        self.ws.send(json.dumps({"action": action, "params": params, "echo": echo}))
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            with self._lock:
                if echo in self._responses:
                    return self._responses.pop(echo)
            time.sleep(0.05)
        raise OneBotError(f"WS 请求超时: {action}")

    def send_private(self, user_id: int, message: list) -> int:
        r = self._call("send_private_msg", {"user_id": user_id, "message": message})
        return (r.get("data") or {}).get("message_id")

    def send_group(self, group_id: int, message: list) -> int:
        r = self._call("send_group_msg", {"group_id": group_id, "message": message})
        return (r.get("data") or {}).get("message_id")

    def send_text(self, target: int, text: str, is_group: bool = False) -> int:
        msg = [{"type": "text", "data": {"text": text}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def send_voice_file(self, target: int, audio_path: str, is_group: bool = False) -> int:
        """SnowLuma 语音条：读文件 -> base64 -> [CQ:record]"""
        with open(audio_path, "rb") as f:
            b64 = __import__("base64").b64encode(f.read()).decode("ascii")
        msg = [{"type": "record", "data": {"file": f"base64://{b64}"}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def send_image_url(self, target: int, url: str, is_group: bool = False) -> int:
        msg = [{"type": "image", "data": {"file": url}}]
        return self.send_group(target, msg) if is_group else self.send_private(target, msg)

    def get_login_info(self) -> dict:
        return self._call("get_login_info", {})