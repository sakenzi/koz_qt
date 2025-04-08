import os
from plyer import notification


class NotificationManager:
    def __init__(self):
        self.icon_path = os.path.join(os.path.dirname(__file__), "..", "icon", "11003355.png")

    def show_notification(self, title, message, timeout=5):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="kӨz",
                timeout=timeout,
                app_icon=self.icon_path if os.path.exists(self.icon_path) else None
            )
        except Exception as e:
            print(f"Хабарды жеткізу кезінде бәле пайда болды. Ол бәле - {e}")