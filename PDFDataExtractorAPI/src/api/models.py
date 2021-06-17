from django.db import models

# Create your models here.


class Candidate(models.Model):
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.location} : {self.email}, {self.mobile}"
