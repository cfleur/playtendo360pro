from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=70, unique=True, blank=True)
    description = models.TextField()
    price = models.FloatField()
    preview_pic = models.ImageField(upload_to='preview_pic', default='staticfiles/default_game_preview.png') #requires Pillow to be installed (pip install Pillow)
    link = models.URLField(unique=True)
    GENRE_CHOICES = (
        ('action','Action'),
        ('adventure','Adventure'),
        ('shooter','Shooter'),
        ('fighting','Fighting'),
        ('platformer','Platformer'),
        ('survival','Survival'),
        ('rpg','Role-playing'),
        ('strategy','Strategy'),
        ('sports','Sports'),
        ('racing','Racing'),
        ('party','Party'),
        ('educational','Educational'),
    )
    genre =  models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    owners = models.ManyToManyField('authentication.Account', related_name="owned_games",
                                    related_query_name="game")
    developer = models.ForeignKey('authentication.Account', on_delete=models.CASCADE,
                                  related_name="submitted_games", related_query_name="game")
class Score(models.Model):
    score = models.FloatField(default = 0)

    player = models.ForeignKey('authentication.Account', on_delete=models.CASCADE, related_name="playerScores",
                                    related_query_name="score")
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name="leaderBoard",
                                    related_query_name="score")
