from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import re


from .models import Signup, Clubs, Post, Mac, Comment, Notification


class Story:
    def __init__(self, item, text):
        self.item = item
        self.text = text

def land(request):
    if request.method == 'POST':
        q = Signup(email=request.POST['email'], signup_date=timezone.now())
        q.save()
        return render(request, 'land/landing.html')
    else:
        return render(request, 'land/landing.html')

@login_required
def prodash(request):
    user = request.user
    clubs = Mac.objects.filter(username=user.username).all()
    notifications = Notification.objects.filter(user_rec=user.username).order_by('-pub_date')[:5]
    for noti in notifications:
        noti.seen = noti.seen+1
        noti.save()
    return render(request, 'land/prodash.html', {
        'clubs': clubs,
        'user': user,
        'notifications': notifications })

@login_required
def grodash(request, club_id):
    user = request.user
    club = Clubs.objects.get(pk=club_id)
    safety = Mac.objects.filter(username=user.username).filter(club=club).count()
    if safety > 0:
        posts = Post.objects.filter(club=club).order_by('-pub_date')
        user_list = Mac.objects.filter(club=club).values_list('username', flat=True)
        return render(request, 'land/grodash.html', {
            'club': club,
            'user_list': user_list,
            'user': user,
            'posts' : posts })
    else:
        #flash do not have access message to be added
        return HttpResponseRedirect('/prodash/')


@login_required
def joingroup(request):
    user = request.user
    if request.method == 'POST':
        club = Clubs.objects.get(name=request.POST['clubname'])
        safety = Mac.objects.filter(username=user.username).filter(club=club).count()
        if safety > 0:
            #flash already part of this group to be added
            return HttpResponseRedirect('/prodash/')
        elif club.password == request.POST['password']:
            addtogroup = Mac(club=club, username=user.username)
            addtogroup.save()
            #flash success to be added
            return HttpResponseRedirect('/prodash/')
        else:
            #flash failure message to be added
            return HttpResponseRedirect('/prodash/')
    else:
        return HttpResponseRedirect('/prodash/')

@login_required
def creategroup(request):
    user = request.user
    if request.method == 'POST':
        q = Clubs(name=request.POST['name'], tagline=request.POST['tagline'], password=request.POST['password'], admin=user.username)
        q.save()
        addtogroup = Mac(club=q, username=user.username)
        addtogroup.save()
        #flash group creation success to be added
        return HttpResponseRedirect('/prodash')
    else:
        return HttpResponseRedirect('/prodash')

@login_required
def createpost(request):
    if request.method == 'POST':
          user = request.user
          club = Clubs.objects.get(pk=request.POST['club_id'])
          user_list = Mac.objects.filter(club=club).values_list('username', flat=True)
          q = Post(question_text=request.POST['question_text'], title=request.POST['title'], username=user.username, pub_date=timezone.now(), club=club)
          q.save()
          for dog in user_list:
              x = Notification(user_rec=dog, user_sent=user.username, post=q, pub_date=timezone.now(), seen=0, notification="added story,")
              x.save()
          return HttpResponseRedirect('/prodash/')
    else:
          return HttpResponseRedirect('/prodash/')

@login_required
def post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    club = post.club.pk
    safety = Mac.objects.filter(username=user.username).filter(club=club).count()
    if safety > 0:
        user_list = Mac.objects.filter(club=club).values_list('username', flat=True)
        text2 = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', post.question_text)
        i=0
        posts=[]
        for text in text2:
            t=Story(i,text)
            posts.append(t)
            i=i+1
        comments = Comment.objects.filter(post=post)
        return render(request, 'land/post.html', {
            'club': club,
            'user_list': user_list,
            'user': user,
            'post': post,
            'posts': posts,
            'comments': comments })
    else:
        #flash do not have access message to be added
        return HttpResponseRedirect('/prodash/')

@login_required
def addcomment(request):
    if request.method == 'POST':
          user = request.user
          post_id = int(request.POST['post_id'])
          post = Post.objects.get(pk=post_id)
          sentence = int(request.POST['sentence'])
          notification="commented on"
          q = Comment(comment=request.POST['comment'], sentence=sentence, username=user.username, pub_date=timezone.now(), post=post)
          q.save()
          x = Notification(user_rec=post.username, user_sent=user.username, post=post, pub_date=timezone.now(), seen=0, notification=notification)
          x.save()
          return HttpResponseRedirect('/prodash/')
    else:
          return HttpResponseRedirect('/prodash/')

@staff_member_required
def anal_dashboard(request):
    #analytics dashboard in progress
    return render(request, 'land/analytics.html')
