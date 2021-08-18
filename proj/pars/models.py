from django.db import models


class Page(models.Model):
    link = models.TextField()
    title = models.TextField()
    article_author = models.TextField()
    pub_date = models.DateField()
    tags = models.TextField()
    text = models.TextField()

    def __str__(self):
        return f"{self.title}"
