from django.contrib import admin

from leaning_logs.models import Topic, Entry
# 注册表单
admin.site.register(Topic)
admin.site.register(Entry)

