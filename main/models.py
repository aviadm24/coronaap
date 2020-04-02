from django.db import models


# https://devcenter.heroku.com/articles/heroku-postgres-backups#creating-a-backup
# heroku pg:backups:capture --app caneti
# heroku pg:backups:restore caneti::{id - like b141} DATABASE_URL --app caneti-staging

# https://stackoverflow.com/questions/4733609/how-do-i-clone-a-django-model-instance-object-and-save-it-to-the-database


class Sms(models.Model):
    number = models.CharField(max_length=100)
    message_id = models.CharField(max_length=100)
    project_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.project_id
