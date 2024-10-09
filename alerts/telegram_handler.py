import logging
from alerts.telegram_alert import send_telegram_message

class TelegramHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            log_entry = self.format(record)
            send_telegram_message(log_entry)
        except Exception:
            self.handleError(record)
