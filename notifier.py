from plyer import notification

def show(title, message):
    # Windows balloon tips have length limits
    if len(title) > 64:
        title = title[:61] + "..."
    if len(message) > 256:
        message = message[:253] + "..."

    notification.notify(
        app_name="LazySearch",
        title=title,
        message=message,
        timeout=10
    )

def show_error(message):
    show("LazySearch - Error", message)
    