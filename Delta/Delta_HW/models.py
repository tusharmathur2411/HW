from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Appuser(models.Model):
    class Meta:
        db_table = 'Appuser'

    scur = models.TextField(primary_key=True)
    user_first_name = models.TextField(max_length=30)
    user_last_name = models.TextField(max_length=30)
    password = models.TextField(max_length=30)
    consecutive_failed_logins = models.SmallIntegerField(default=0)

    @classmethod
    def create(cls, first_name, last_name, password):
        scur = first_name[0] + last_name[0:3]
        cn = Appuser.objects.filter(scur__startswith=scur).count()
        if cn:
            scur += str(cn + 1)

        user = cls(scur=scur, user_first_name=first_name, user_last_name=last_name, password=password)
        return user

    def __str__(self):
        return '%s %s' % (self.user_first_name, self.user_last_name)


class Patient(models.Model):
    class Meta:
        db_table = 'Patient'

    paaa_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=2, choices=[('M', "Male"), ('F', "Female"), ('O', "Other")])
    birthday = models.DateField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    create_userid = models.CharField(max_length=10)
    last_update_datetime = models.DateTimeField(auto_now=True)
    last_update_userid = models.CharField(max_length=10)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class PatientAddress(models.Model):
    class Meta:
        db_table = 'Patient_Address'

    gead_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paaa_id = models.ForeignKey('Patient', on_delete=models.CASCADE, )
    line_one = models.TextField(max_length=100)
    line_two = models.TextField(max_length=100)
    city = models.CharField(max_length=20, default=None)
    primary_phone_no = models.BigIntegerField()
    alternate_phone_no = models.BigIntegerField(null=True)
