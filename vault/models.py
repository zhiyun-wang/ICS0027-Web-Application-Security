from django.conf import settings
from django.db import models


class VaultProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    salt = models.BinaryField(max_length=16)


class Entry(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    website = models.CharField(max_length=150)

    nonce = models.BinaryField(max_length=12)

    ciphertext = models.BinaryField()