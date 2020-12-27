import random
import copy
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import urllib.request
from urllib.request import urlopen
from django.urls import reverse
from secretsanta.models import Room
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .forms import PasswordForm,RoomCreateForm,SendInvitation

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}



# helper functions
def secretSantaDict(room):
    current = list(room.users.all())
    n = len(current)
    try:
        choose = copy.copy(current)
        result = []
        for i in current:
            names = copy.copy(current)
            names.pop(names.index(i))
            chosen = random.choice(list(set(choose)&set(names)))
            result.append((i,chosen))
            choose.pop(choose.index(chosen))
        pprint("Result {}".format(result))
        sendrec = {}
        for i in result:
            x,y = i
            sendrec[x] = y 
        return sendrec 
    except Exception as e:
        dict = {"error_message":"There was some error while processing. Please try again later."}
        return dict 


def getAmazonLink(budget):
	return "https://www.amazon.in/s?k=gift&rh=p_36%3A-"+str(budget)+"00&s=review-rank"


def getLinks(n,budget):
	link = getAmazonLink(budget)
	r = requests.get(link, headers=headers)
	soup = BeautifulSoup(r.text,'lxml')
	links = soup.find_all("a", attrs={'class':'a-link-normal a-text-normal'})
	

	links_list = []
	for link in links:
		links_list.append(link.get('href'))
	
	return links_list[:n]


def getImages(n,budget):
	link = getAmazonLink(budget)
	r = requests.get(link,headers=headers)
	soup = BeautifulSoup(r.text,'lxml')
	image_paths = soup.find_all("img",attrs={'class':'s-image'})
	links = image_paths[:n]

	images_list = []
	for link in links:
		images_list.append(link.get("src"))
	return images_list[:n]

class Developer():
    def __init__(self,name,pos,pic,gitlink) -> None:
        self.name = name 
        self.position = pos
        self.picture = pic
        self.gitlink = gitlink


# Create your views here.

def homeView(request):
    context = {}
    return render(request,"index.html",context)


class RoomListView(ListView):
    model = Room 
    queryset = Room.activeRooms.all()
    context_object_name = 'rooms'
    template_name = 'room/list.html'


@login_required
def RoomDetailView(request,pk):
    room = get_object_or_404(Room,id=pk)
    # giftlist = getLinks(len(list(room.users.all())),room.budget)
    giftlist = getLinks(20,room.budget)
    giftlistpics = getImages(20,room.budget)
    gifts = {}
    for i in range(len(giftlist)):
        gifts[giftlist[i]] = giftlistpics[i]
    return render(request,"room/detail.html",{"room":room,"giftlist":giftlist,"giftlistpics":giftlistpics,"gifts":gifts})
    # context = {"room":room,"giftlist":None}
    # return render(request,"room/detail.html",context)


@login_required
def RoomEntryView(request,pk):
    EntryAccess = False
    room = get_object_or_404(Room,id=pk)
    context = {"room":room}
    form = PasswordForm()
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == room.password or cd['password'] == room.masterPassword :
                print("correct password")
                EntryAccess = True
                if request.user not in room.users.all():
                    room.users.add(request.user)
                    room.save()
                giftlist = getLinks(20,room.budget)
                giftlistpics = getImages(20,room.budget)
                gifts = {}
                for i in range(len(giftlist)):
                    gifts[giftlist[i]] = giftlistpics[i]
                return render(request,"room/detail.html",{"room":room,"giftlist":giftlist,"giftlistpics":giftlistpics,"gifts":gifts})
            else:
                print("incorrect password")
    else:
        form = PasswordForm()

    context["form"] = form 
    return render(request,"room/roomauth.html",context)        



@login_required
def RoomCreateView(request):
    new_room = None
    if request.method == 'POST':
        roomForm = RoomCreateForm(request.POST)
        if roomForm.is_valid():
            new_room = roomForm.save(commit=False)
            new_room.save()
            new_room.users.add(request.user)
            new_room.save()
            return redirect(reverse('home'))
    else:
        roomForm = RoomCreateForm()
    context = {"roomForm":roomForm}
    return render(request,"room/new.html",context)


@login_required
def RoomUpdateView(request,pk):
    room = get_object_or_404(Room,id=pk)
    form = RoomCreateForm(instance=room)
    context = {"form":form}

    if request.method == 'POST':
        form = RoomCreateForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))

    return render(request,"room/update.html",context)


@login_required
def RoomUpdateAuthView(request,pk):
    room = get_object_or_404(Room,id=pk)
    passwordform = PasswordForm()
    UpdateAccess = False 
    if request.method == 'POST':
        if passwordform.is_valid():
            cd = passwordform.cleaned_data
            if cd['password'] == room.masterPassword:
                print("Master Password accepted")
                UpdateAccess = True 
                context = {"room":room}
                return redirect(reverse('',args=[room.pk]))
            else:
                print("Master Password False")
    else:
        passwordform = PasswordForm()



@login_required
def RoomDeleteAuthView(request,pk):
    room = get_object_or_404(Room,id=pk)
    passwordform = PasswordForm()
    DeleteAccess = False 
    if request.method == 'POST':
        passwordform = PasswordForm(request.POST)
        if passwordform.is_valid():
            cd = passwordform.cleaned_data
            if cd['password'] == room.masterPassword:
                print("Master Password accepted")
                DeleteAccess = True 
                room.delete()
                return redirect(reverse('home'))
            else:
                print("Master Password False")
    else:
        passwordform = PasswordForm()
    context = {"passwordform":passwordform,"room":room,"deleteAccess":DeleteAccess}
    return render(request,"room/deleteauth.html",context)



@login_required
def makeAuthSecretSanta(request,pk):
    room = get_object_or_404(Room,id=pk)
    context = {}
    passwordform = PasswordForm()
    SecretSantaAccess = False 
    if request.method == 'POST':
        passwordform = PasswordForm(request.POST)
        if passwordform.is_valid():
            cd = passwordform.cleaned_data
            if cd['password'] == room.masterPassword:
                print("Master Password Accepted")
                SecretSantaAccess = True 
                context["sendrec"] = secretSantaDict(room)
                sendrec = secretSantaDict(room)
                for user in room.users.all():
                    subject = "secret santa - gift sending"
                    message = "You are the secret santa for {}.\n Surprise them with a cool gift. Also make sure your gift price is under the budget.".format(sendrec[user])
                    send_mail(subject,message,'guessthegift.secret.santa@gmail.com',[user.email])
            else:
                print("Master Password false")
    else:
        passwordform = PasswordForm()
    context = {"passwordform":passwordform,"room":room,"secretaccess":SecretSantaAccess}
    return render(request,"room/secretsantaauth.html",context)


@login_required
def createSecretSanta(request,pk):
    room = get_object_or_404(Room,id=pk)
    context = {"room":room}
    # current = list(room.users.all())
    # n = len(current)
    # try:
    #     choose = copy.copy(current)
    #     result = []
    #     for i in current:
    #         names = copy.copy(current)
    #         names.pop(names.index(i))
    #         chosen = random.choice(list(set(choose)&set(names)))
    #         result.append((i,chosen))
    #         choose.pop(choose.index(chosen))
    #     pprint("Result {}".format(result))
    #     sendrec = {}
    #     for i in result:
    #         x,y = i
    #         sendrec[x] = y 
    #     context["sendrec"] = sendrec 
    # except Exception as e:
    #     context["errorMessage"] = "Some error occured. Please try again properly."
    context["sendrec"] = secretSantaDict(room)
    return render(request,"room/secretsanta.html",context)


@login_required
def sendEmailInvites(request,pk):
    room = get_object_or_404(Room,id=pk)
    form = SendInvitation()
    sent = False 
    if request.method == 'POST':
        form = SendInvitation(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            pprint(cd)
            if cd['password'] == room.masterPassword:
                pprint("master password accepted")
                post_url = room.get_absolute_url()
                subject = "secret santa invitation"
                message = "{} is inviting you for secret santa at {}. The password for entry is {}".format(request.user.username,post_url,room.password)
                send_mail(subject,message,'guessthegift.secret.santa@gmail.com',cd['to'])
                sent = True 
                # return redirect('home')
            else:
                pprint("master password invalid")
    else:
        form = SendInvitation()
    context = {"room":room,"form":form,"sent":sent}
    return render(request,"room/sendinvites.html",context)



def aboutView(request):
    prasanna = Developer('R Prasannavenkatesh','Backend Dev','https://avatars0.githubusercontent.com/u/54119123?s=400&u=f08e1a3b2cb36bd9ebda9dd40f1c6c97f7ed3fa2&v=4','https://github.com/hanzohasashi33')
    vijay = Developer('Vijay Jaisankar','Frontend Dev','https://avatars3.githubusercontent.com/u/56185979?s=400&u=65beb118f34e21c0acb0d56ed98f75b11e1647bc&v=4','https://github.com/vijay-jaisankar')
    context = {"prasanna":prasanna,"vijay":vijay}
    return render(request,"about.html",context)