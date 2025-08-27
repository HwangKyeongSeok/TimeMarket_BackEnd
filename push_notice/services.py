from typing import Dict, List, Optional
from django.conf import settings

# firebase-admin은 선택적으로 사용합니다. 미설치/미구성 시 예외를 억제합니다.
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
except Exception:  # pragma: no cover
    firebase_admin = None
    credentials = None
    messaging = None

from .models import DeviceToken
from users.models import User


_initialized = False

def initialize_firebase() -> bool:
    global _initialized
    if _initialized:
        return True
    if firebase_admin is None:
        return False
    try:
        # 이미 초기화된 경우 패스
        if firebase_admin._apps:
            _initialized = True
            return True
        cred_path = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_FILE', None)
        if not cred_path:
            return False
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        _initialized = True
        return True
    except Exception:
        return False


def send_push_to_tokens(tokens: List[str], title: str, body: str, data: Optional[Dict[str, str]] = None) -> Dict:
    if not tokens:
        return {"success": 0, "failure": 0, "message": "no tokens"}
    if not initialize_firebase() or messaging is None:
        return {"success": 0, "failure": len(tokens), "message": "firebase not configured"}

    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data={k: str(v) for k, v in (data or {}).items()},
        tokens=tokens,
    )
    response = messaging.send_multicast(message)
    return {"success": response.success_count, "failure": response.failure_count}


def send_push_to_user(user: User, title: str, body: str, data: Optional[Dict[str, str]] = None) -> Dict:
    tokens = list(
        DeviceToken.objects.filter(user=user, is_active=True).values_list('token', flat=True)
    )
    return send_push_to_tokens(tokens, title, body, data)


def send_chat_push(receiver: User, sender: User, message_preview: str, room_id: int) -> Dict:
    title = f"{sender.nickname}"
    body = message_preview[:120]
    data = {"type": "chat", "room_id": str(room_id), "sender": sender.nickname}
    return send_push_to_user(receiver, title, body, data)

