import firebase_admin
from firebase_admin import credentials, firestore, messaging
from app.config import settings
import os
from typing import Optional

_db: Optional[firestore.client] = None
_messaging: Optional[messaging.Client] = None


class FirebaseNotConfiguredError(Exception):
    pass


def get_firestore():
    global _db
    if _db is not None:
        return _db

    if not settings.firebase_project_id:
        raise FirebaseNotConfiguredError(
            "Firebase not configured. Set FIREBASE_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS."
        )

    if not os.path.exists(settings.google_application_credentials):
        raise FirebaseNotConfiguredError(
            f"Service account file not found at {settings.google_application_credentials}"
        )

    try:
        cred = credentials.Certificate(settings.google_application_credentials)
        firebase_admin.initialize_app(
            cred, {"projectId": settings.firebase_project_id}
        )
        _db = firestore.client()
        return _db
    except Exception as e:
        raise FirebaseNotConfiguredError(f"Failed to initialize Firebase: {str(e)}")


def get_messaging():
    global _messaging
    if _messaging is not None:
        return _messaging

    if not settings.firebase_project_id:
        raise FirebaseNotConfiguredError(
            "Firebase not configured. Set FIREBASE_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS."
        )

    if not os.path.exists(settings.google_application_credentials):
        raise FirebaseNotConfiguredError(
            f"Service account file not found at {settings.google_application_credentials}"
        )

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.google_application_credentials)
            firebase_admin.initialize_app(
                cred, {"projectId": settings.firebase_project_id}
            )
        _messaging = messaging.get_app().messaging
        return _messaging
    except Exception as e:
        raise FirebaseNotConfiguredError(f"Failed to initialize FCM: {str(e)}")


def is_firebase_configured() -> bool:
    return (
        settings.firebase_project_id
        and os.path.exists(settings.google_application_credentials)
    )
