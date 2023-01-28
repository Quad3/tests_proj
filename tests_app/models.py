from django.db import models
from django.urls import reverse


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Theme(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('Theme', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # if self.parent:
        #     return f"{self.parent} -> {self.name}"
        return self.name
    
    def get_absolute_url(self):
        return reverse('theme_detail', args=[self.name])


class TestEntry(models.Model):
    questions = models.ManyToManyField(Question)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.created_at.strftime("%d/%m/%Y, %H:%M:%S"))

    def get_absolute_url(self):
        return reverse('test_detail', args=[str(self.id)])
