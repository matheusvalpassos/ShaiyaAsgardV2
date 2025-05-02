from django.db import models


class CustomUser(models.Model):
    useruid = models.AutoField(db_column="UserUID", primary_key=True)
    userid = models.CharField(db_column="UserID", max_length=30, unique=True)
    pw = models.CharField(db_column="Pw", max_length=50)
    enpassword = models.CharField(
        db_column="Enpassword", max_length=255, blank=True, null=True
    )
    joindate = models.DateTimeField(db_column="JoinDate", auto_now_add=True, null=True)
    admin = models.BooleanField(db_column="Admin", default=False)
    adminlevel = models.IntegerField(db_column="AdminLevel", default=0)
    status = models.IntegerField(db_column="Status", default=0)
    email = models.EmailField(db_column="Email", max_length=50)
    usertype = models.IntegerField(db_column="UserType", default=0)
    user_ip = models.CharField(db_column="UserIp", max_length=45, blank=True, null=True)

    class Meta:
        db_table = "Users_Master"
        app_label = "accounts"

    def save(self, *args, **kwargs):
        # Sempre usa o banco 'user_data'
        if "using" not in kwargs:
            kwargs["using"] = "user_data"
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.userid
