import requests
from django.conf import settings


def notify_excel_updated(excel):
    try:
        requests.post(
            settings.EXTERNAL_WEBHOOK_URL,
            json={
                "event": "excel_updated",
                "updated_at": excel.updated_at.isoformat(),
                "file_url": excel.file.url,
            },
            timeout=5
        )
    except Exception as e:
        # اگر خواستی لاگ بگیری
        print("Webhook notify failed:", e)
