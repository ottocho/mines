
from django.db import models
from django.utils import timezone

class Game(models.Model):
    PLAYING = 10
    WON = 20
    LOST = 30
    STATUS_CHOICES = (
        (PLAYING, 'playing game'),
        (WON, 'game won'),
        (LOST, 'game lost'),
    )
    start_time = models.DateTimeField(default=timezone.now)
    user_name = models.CharField(max_length=30)
    height = models.IntegerField(default=10)
    width = models.IntegerField(default=10)
    n_mines_all = models.IntegerField(default=8)
    n_mines_left = models.IntegerField(default=8)
    status = models.IntegerField(default=PLAYING, choices=STATUS_CHOICES)

    def __str__(self):
        return '%d by %s (%d*%d)[%d]' % \
               (self.id, self.user_name, self.height, self.width, self.n_mines_all)

class Brick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    x = models.IntegerField(default=0, db_index=True)
    y = models.IntegerField(default=0, db_index=True)
    is_mine = models.BooleanField(default=False, db_index=True)
    n_nearby_mines = models.IntegerField(default=0)
    is_dug = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_marked = models.BooleanField(default=False)

    def __str__(self):
        return '(%d, %d) [%s]' % (self.x, self.y, "X" if self.is_mine else " ")

