from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """用户要学习的主题."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # 外键是用户，可以通过这个外键确定这个主题属于哪个用户
    owner = models.ForeignKey(User, "on_delete=models.CASCADE")

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text

class Entry(models.Model):
    """用户发表的文章"""
    # 外键是主题，可以通过这个外键确定这个文章属于哪个主题
    topic = models.ForeignKey(Topic, "on_delete=models.CASCADE")
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."
