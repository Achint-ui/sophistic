from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Topic, Comment
from .forms import TopicForm, CommentForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#API
import os
os.environ["GROQ_API_KEY"] = "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"
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Create your views here.
'''
class HomeView(ListView):
    model = Topic
    template_name = 'home.html'
    context_object_name = 'topics'
'''


def HomeView(request):
    topics = Topic.objects.all()
    print('hello')
    
    if request.method == 'POST':
        topic = Topic.objects.create(
            host = request.user,
            topic = request.POST.get('topic')
        )

        return redirect('home')
            

    context = {'topics' : topics}

    return render(request, 'home.html', context)

'''
class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topic.html'
'''

def topicView(request, pk):
    form = CommentForm()   
    topic = Topic.objects.get(id=pk) 
    topic_comments = topic.comment_set.all()
    
    content = topic.topic + " in 200 words"
    
    '''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.topic = topic
            comment.save()
            return redirect('topic', pk=topic.id)
    '''
    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            topic = topic,
            body = request.POST.get('body')
        )
        return redirect('topic', pk=topic.id)
        
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": content,
        }
    ],
    model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)
    
    context = {'topic' : topic , 'topic_comments': topic_comments, 'message' : chat_completion.choices[0].message, 'form': form }

    return render(request, 'topic.html', context)   

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print("User doesn't exist")

        user = authenticate(request, username=username, password=password)        
        
        if user is not None:
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        
        else:
            print('Username OR password is incorrect!!')

    context = { 'page' : page }
    return render(request, 'login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        
    
    context = { 'form' : form}

    return render(request, 'login_register.html', context)