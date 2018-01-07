from django.db import models
from django.contrib.auth.models import User
import json
from datetime import date, datetime

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


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

class TopicEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Topic):
            return obj.text
        return json.JSONEncoder.default(self, obj)

class EntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entry):
            return obj.text
        else:
            return json.JSONEncoder.default(self, obj)