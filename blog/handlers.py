import logging

class AdminLogHandler(logging.Handler):
    def emit(self, record):
        try:
            # Importni emit() ichida, kerak bo‘lganda qilamiz
            from blog.models import AdminLog
            AdminLog.objects.create(
                level=record.levelname,
                message=self.format(record)
            )
        except Exception:
            pass

