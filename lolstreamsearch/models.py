from django.db import models


class YtStream(models.Model):
    """
    YouTube Stream Search Model

    Links to Yt Videos of League of Legends Streamers with additional information
    like champion played, enemy champion, lane, runes
    """
    streamer_name = models.CharField(max_length=64)
    youtube_id = models.CharField(max_length=64)
    champion = models.CharField(max_length=20)
    enemy_champion = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "ytstreams"

    def __str__(self):
        return f"{self.champion} vs {self.enemy_champion} : {self.youtube_id}"

    def get_absolute_url(self):
        """
        returns the absolute url of the Yt Stream
        https://www.youtube.com/watch?v=dBdzHPYt6Pg
        """
        return f"https://www.youtube.com/watch?v={self.youtube_id}"
