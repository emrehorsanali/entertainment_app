from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from statistics import mean


class Channel(models.Model):
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=3)
    picture = models.ImageField(upload_to='channel_pictures')
    parent_channel = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def calculate_rating(self):
        if self.channel_set.count() == 0:
            if self.content_set.count() == 0:
                self.rating = None
            else:
                self.rating = float(self.content_set.aggregate(models.Avg('rating'))['rating__avg'])
        else:
            subchannel_ratings = []
            for channel in self.channel_set.all():
                subchannel_rating = channel.calculate_rating()
                if subchannel_rating:
                    subchannel_ratings.append(subchannel_rating)
            self.rating = round(mean(subchannel_ratings), 2)
        return self.rating


class Content(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 validators=[MaxValueValidator(10), MinValueValidator(0)])


class Video(Content):
    movie_director = models.CharField(max_length=50)
    file = models.FileField(upload_to='content_files/videos',
                            validators=[FileExtensionValidator(['mp4', ])],
                            null=True,
                            blank=True)


class Pdf(Content):
    author = models.CharField(max_length=50)
    file = models.FileField(upload_to='content_files/pdfs',
                            validators=[FileExtensionValidator(['pdf', ])],
                            null=True,
                            blank=True)


class Text(Content):
    genre = models.CharField(max_length=50)
    file = models.FileField(upload_to='content_files/txts',
                            validators=[FileExtensionValidator(['txt', ])],
                            null=True,
                            blank=True)
