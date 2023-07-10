from django.db import models

class User(models.Model):
    id = models.TextField(primary_key=True, db_column='id')
    joining_date = models.DateField(db_column='joining_date', null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.id