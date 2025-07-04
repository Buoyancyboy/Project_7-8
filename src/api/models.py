from django.db import models

class LogData(models.Model):
    log_data_ID = models.AutoField(primary_key=True)
    message = models.TextField()
    topic_config_ID = models.IntegerField()
    date_logged = models.DateTimeField()

    class Meta:
        db_table = 'log_data'
        managed = False  # Don't let Django try to alter this table

    def __str__(self):
        return f"{self.date_logged} - {self.message}"
