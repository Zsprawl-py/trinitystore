from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True)
    vip = models.BooleanField(default=False)

    def __str__(self):
        return f'profile of {self.user.username}'


class Subscribe(models.Model):
    VIP_TYPES = (
        ('MONTH', 'Month'),
        ('3MONTH', '3Month'),
        ('LIFETIME', 'Lifetime'),
        ('1YEAR', '1Year'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    acceptance = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(editable=False, blank=True, null=True)
    vip_type = models.CharField(max_length=12, choices=VIP_TYPES, default='Month')

    def __str__(self):
        return f'subscription of {self.user.username}'

    def remaining(self):
        now_utc = datetime.now(timezone.utc)
        if self.expiration > now_utc:
            user = Profile.objects.filter(user=self.user).first()
            user.vip = True
            user.save()
            return self.expiration - now_utc
        else:
            user = Profile.objects.filter(user=self.user).first()
            user.vip = False
            user.save()
            return 'subscription expired!'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Subscribe, self).save()
        if not self.expiration:
            if self.vip_type == 'MONTH':
                d = 30
            elif self.vip_type == '3MONTH':
                d = 90
            elif self.vip_type == '1YEAR':
                d = 365
            self.expiration = self.acceptance + timedelta(days=d)
            super(Subscribe, self).save()
