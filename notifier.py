import sys
from plyer import notification


def show(title, message):
    # Platform-specific notification length limits
    if sys.platform == 'win32':
        # Windows balloon tips have strict length limits
        max_title = 64
        max_message = 256
    else:
        # Linux (libnotify) is more flexible but we still cap it
        max_title = 120
        max_message = 500

    if len(title) > max_title:
        title = title[:max_title - 3] + "..."
    if len(message) > max_message:
        message = message[:max_message - 3] + "..."

    notification.notify(
        app_name="LazySearch",
        title=title,
        message=message,
        timeout=10
    )

def show_error(message):
    show("LazySearch - Error", message)
    