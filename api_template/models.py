from django.db import models

# Create your models here.

ROLE_CHOICES = sorted([("admin", "Admin"), ("user", "User")])

class UserAccounts(models.Model):
    IdNumber = models.CharField(db_column='id_number', max_length=20, null = True)
    FullName = models.CharField(db_column='full_name', max_length=50, null = True)
    Username = models.CharField(db_column='username', max_length=50, null = True)
    Password = models.CharField(db_column='password', max_length=50, null = True)
    Section = models.CharField(db_column='section', max_length=50, null = True)
    Role = models.CharField(db_column='role', choices=ROLE_CHOICES, default="user", max_length=20, null = True)

    class Meta:
        db_table = 'user_accounts'
        managed = False

    def __str__(self):
        return self.IdNumber