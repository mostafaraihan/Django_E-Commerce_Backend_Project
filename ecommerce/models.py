from django.db import models


class Brand(models.Model):
    brandName = models.CharField(max_length=100)
    brandImg = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


