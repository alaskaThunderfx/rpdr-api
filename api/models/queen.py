from django.db import models
from django.contrib.auth import get_user_model

# Drag Queen models
class Queen(models.Model):
  # Season Selector
  class Season(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13

  # Model fields
  name = models.CharField(max_length=100)
  season = models.IntegerField(choices=Season.choices)
  finished = models.CharField(max_length=100)
  owner = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE
  )

  def __str__(self):
    # This must return a string
    return f"'{self.name}' is from Season {self.season}. They finished {self.finished}."

  def as_dict(self):
    """Returns dictionary version of Mango models"""
    return {
        'id': self.id,
        'name': self.name,
        'season': self.season,
        'finished': self.finished
    }
