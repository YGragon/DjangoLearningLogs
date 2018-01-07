from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry, MyEncoder, TopicEncoder, EntryEncoder
from .forms import TopicForm, EntryForm
import json
from django.http import HttpResponse

def index(request):
    """学习笔记的主页"""
    return render(request, 'leaning_logs/index.html')

@login_required
def topics(request):
    """显示所有的主题，login_required：加入登录验证，owner=request.user才能查看主题列表"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 将结果存在context字典中
    context = {'topics':topics}

    # OK
    # result_set = Topic.objects.all().values()
    # word = list(result_set) #ValuesQuerySet对象需要先转换成list
    # data = json.dumps(word, cls=MyEncoder) # 把list转成json
    # return HttpResponse(data) #返回json

    # 返回给网页使用
    return render(request, 'leaning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    # -date_added -表示按时间降序显示
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}

    # OK
    # result_set = topic.entry_set.all().values()
    # word = list(result_set) #ValuesQuerySet对象需要先转换成list
    # data = json.dumps(word, cls=MyEncoder) # 把list转成json
    # return HttpResponse(data) #返回json

    return render(request, 'leaning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据，对数据进行处理
        form =TopicForm(request.POST)
        if form.is_valid():
            # 先修改主题，再保存到数据库中
            new_topic = form.save(commit=False)
            # 将当前修改主题的人变为新的话题所有者
            new_topic.owner = request.user
            # 保存到数据库
            new_topic.save()

            # ok
            # result_set = Topic.objects.all().values()
            # word = list(result_set) #ValuesQuerySet对象需要先转换成list
            # data = json.dumps(word, cls=MyEncoder) # 把list转成json
            # return HttpResponse(data) #返回json

            # 返回主页
            return HttpResponseRedirect(reverse('leaning_logs:topics'))

    context = {'form':form}

    return render(request, 'leaning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定的主题重添加条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据，对数据进行处理
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('leaning_logs:topic', args=[topic_id]))
    context = {'topic':topic, 'form':form}
    return render(request, 'leaning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('leaning_logs:topic',args=[topic.id]))

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'leaning_logs/edit_entry.html',context)