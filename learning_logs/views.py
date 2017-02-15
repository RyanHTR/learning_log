from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
	"""homepage of learning_logs"""
	return render(request, 'learning_logs/index.html')

	# return render(request, 'templates/learning_logs/index.html')
	# 加了templates反而会报错，猜测是Django在寻找html文件时会自动只识别到templates/
	# 后面的路径都要自己写

@login_required
def topics(request):
	"""show all the topics"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	# topics.html中直接用键topics来获取列表topics
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
	"""显示单个主题及其所有的条目"""
	topic = Topic.objects.get(id=topic_id)
	# 确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
	"""add new topic"""
	if request.method != 'POST':
		# 未提交数据，返回空表单
		form = TopicForm()
	else:
		# POST提交的数据，对数据进行处理
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""add new entry for specific topic"""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# 未提交数据，返回空表单
		form = EntryForm()
	else:
		# POST提交的数据，对数据进行处理
		form = EntryForm(data=request.POST)
		if form.is_valid():
			# 先把表单中的entry对象复制出一份，不提交
			# 再设置该entry的topic外键
			# 最后再存回数据库
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""edit an existing entry"""
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
			# 最后的args不是topic_id，这里没定义该变量，直接使用topic的属性id
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

