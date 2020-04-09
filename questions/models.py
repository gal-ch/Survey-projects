from django.db import models


class Question(models.Model):
    text = models.TextField()
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.text[:10]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    timestemp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.text[:10]
