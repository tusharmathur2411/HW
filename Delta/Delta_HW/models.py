from django.db import models

# Create your models here.
class Appuser(models.Model):
    class Meta:
        db_table = 'Appuser'

    scur = models.TextField(primary_key=True)
    user_first_name = models.TextField(max_length=30)
    user_last_name = models.TextField(max_length=30)
    password = models.TextField(max_length=30)
    # consecutive_failed_logins = models.SmallIntegerField(default=0)

    def Create(cls, first_name, last_name, password):
        scur = first_name[0] + last_name[0:3]
        cn = Appuser.objects.filter(scur__startswith=sc).count()
        if cn:
            scur += str(cn + 1)

        user = cls(scur=scur, user_first_name=first_name, user_last_name=last_name, password=password)
        return user

    def __str__(self):
        return '%s %s' % (self.user_first_name, self.user_last_name)
