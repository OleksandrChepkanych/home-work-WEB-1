from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=100, null=False)
    born_date = models.CharField(max_length=100, null=False)
    born_location = models.CharField(max_length=100, null=False)
    bio = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return f"{self.full_name}"


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)

    def __str__(self):
        return f'{self.name}'


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=2000, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.author.full_name}: {self.quote}, {self.tags}"

    def quotes_author(self):
        return self.author
