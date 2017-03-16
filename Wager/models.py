from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
import datetime

class User(models.Model):
	User_Name = models.CharField(max_length=50)
	Password = models.CharField(max_length=50)
	Date_joined = models.DateTimeField()
	Wins = models.IntegerField(default=0)
	Losses = models.IntegerField(default=0)
	WinPercent = models.IntegerField(default=0)
	LossPercent = models.IntegerField(default=0)

	def __str__(self):
		return self.User_Name

class Bet(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
	Terms = models.CharField(max_length=200)
	Stakes = models.CharField(max_length=300)
	Due_date = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=1))
	#Status:
	#1 = Made but not accepted
	#2 = Accepted, waiting for time passed
	#3 = time passed, waiting for result
	#4 = result in, waiting for accepted
	#5 = all finished
	Status = models.IntegerField()
	Public = models.BooleanField()
	Date_created = models.DateTimeField()

	def __str__(self):
		return self.Terms

class Relationship(models.Model):
	user1_id = models.IntegerField()
	user2_id = models.IntegerField()
	status = models.IntegerField()
	action_user_id = models.IntegerField()

	class Meta:
		unique_together = ("user1_id", "user2_id")

	def __str__(self):
		return str(self.user1_id) + "-" + str(self.user2_id)