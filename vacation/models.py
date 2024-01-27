from django.db import models

from user.models import User
from node.models import Node


class Vacation(models.Model):
    CHOICES = [('F', 'رد شده'),
               ('P', 'در حال بررسی'),
               ('T', 'تایید شده')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Vacation_User')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=CHOICES, default='P', null=True, blank=True)


class VacationResponse(models.Model):
    CHOICES = [('F', 'رد شده'),
               ('P', 'در حال بررسی'),
               ('T', 'تایید شده')]
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE,
                                 related_name='VacationResponse_Vacation')
    node = models.ForeignKey(Node, on_delete=models.CASCADE,
                             related_name='VacationResponse_Node')
    status = models.CharField(max_length=1, choices=CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)