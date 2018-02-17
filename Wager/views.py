from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Bet, User, Relationship
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
import datetime

def HomePage(request):
	if ('user' in request.session) and (User.objects.filter(pk=request.session['user']).first() != None):
		u = request.session['user']
		friends = [x.user2_id for x in Relationship.objects.filter(user1_id=u)] + [x.user1_id for x in Relationship.objects.filter(user2_id=u)]
		latest_friends_bets = Bet.objects.filter(Q(user1__pk__in=friends) | Q(user2__pk__in=friends)).order_by('-Date_created')[:5]
		context = {'latest_bet_list': latest_friends_bets}
		return render(request, 'User_Profiles/LoggedIn_HomePage.html', context)
	else:
		latest_bet_list = Bet.objects.filter(Public=True).order_by('-Date_created')[:5]
		context = {'latest_bet_list': latest_bet_list}
		return render(request, 'User_Profiles/Not_LoggedIn_HomePage.html', context)

def LogIn(request):
	return render(request, 'User_Profiles/LogIn.html')

def SignUp(request):
	return render(request, 'User_Profiles/SignUp.html')

def AddUser(request):
	if request.POST:
		U = User(User_Name=request.POST['UserName'], Password=request.POST['Password'], Date_joined=timezone.now())
		U.save()
		messages.info(request)
		return redirect('/LogIn')
	return redirect('/')

def SetLoggedIn(request):
	if request.POST:
		UserName = request.POST['UserName']
		try:
			U = User.objects.get(User_Name=UserName)
		except User.DoesNotExist:
			return HttpResponse("Not a User")

		if U.Password == request.POST['Password']:
			request.session['user'] = U.pk
			return redirect('/')
		else:
			return HttpResponse("Wrong Password")
		#request.session['username']=request.POST['your-name']
		#return redirect('/')
	return redirect('/')

def FindFriends(request):
	u = request.session['user']
	friends = [x.user2_id for x in Relationship.objects.filter(user1_id=u)] + [x.user1_id for x in Relationship.objects.filter(user2_id=u)]
	users = User.objects.all().exclude(pk__in=friends)
	context = {'users':users}
	return render(request, 'User_Profiles/AddFriend.html', context)

def AddFriend(request):
	if request.POST:
		User1 = User.objects.get(pk=request.session['user'])
		try:
			User2 = User.objects.get(User_Name=request.POST['Friend'])
		except User.DoesNotExist:
			return HttpResponse("Friend does not exist")
		R = Relationship(user1_id=User1.pk, user2_id=User2.pk, status=0, action_user_id=0)
		R.save()
		return redirect('/')
	return redirect('/')

def SetLoggedOut(request):
	request.session['user']=0
	return redirect('/')

def NewBet(request):
	u = request.session['user']
	friends = [x.user2_id for x in Relationship.objects.filter(user1_id=u)] + [x.user1_id for x in Relationship.objects.filter(user2_id=u)]
	users = User.objects.all().filter(pk__in=friends)
	context = {'users':users}
	return render(request, 'User_Profiles/NewBet.html', context)

def CreateNewBet(request):
	if request.POST:
		User1 = User.objects.get(pk=request.session['user'])
		try:
			User2 = User.objects.get(User_Name=request.POST['Opponent'])
		except User.DoesNotExist:
			return HttpResponse("Opponent does not exist")

		Public=False
		if request.POST['Public'] == "Public":
			Public = True
		b = Bet(user1=User1, user2=User2, Terms=request.POST['Terms'], Stakes=request.POST['Stakes'], Status=1, Public=Public, Date_created=timezone.now(), Due_date=timezone.now() + datetime.timedelta(days=int(request.POST['Time'])))
		b.save()
		return redirect('/')
	return redirect('/')

def Profile(request):
	u = User.objects.get(pk=request.session['user'])
	r = [x.user2_id for x in Relationship.objects.filter(user1_id=u.pk)] + [x.user1_id for x in Relationship.objects.filter(user2_id=u.pk)]
	friends = User.objects.all().filter(pk__in=r)
	for_bets = Bet.objects.filter(user1__pk=u.pk)
	against_bets = Bet.objects.filter(user2__pk=u.pk)
	context = {'user':u, 'for_bets':for_bets, 'against_bets':against_bets, 'all_bets':list(set(against_bets)|set(for_bets))}
	return render(request, 'User_Profiles/Profile_Base.html', context)

def AcceptBet(request, bet_id):
	b = get_object_or_404(Bet, pk=bet_id)
	b.Status = 2
	b.save()
	#return HttpResponse(b.Status)
	return redirect('/Profile')

def User2Wins(request, bet_id):
	b = get_object_or_404(Bet, pk=bet_id)
	b.Winner = b.user2.pk
	b.Status = 4
	b.save()
	return redirect('/Profile')

def User1Wins(request, bet_id):
	b = get_object_or_404(Bet, pk=bet_id)
	b.Winner = b.user1.pk
	b.Status = 4
	b.save()
	return redirect('/Profile')

def AcceptResult(request, bet_id):
	b = get_object_or_404(Bet, pk=bet_id)
	b.Status = 5
	b.save()
	if b.Winner == b.user1.pk:
		b.user2.Losses += 1
		b.user2.WinPercent = b.user2.Wins*100/(b.user2.Wins+b.user2.Losses)
		b.user2.LossPercent = b.user2.Losses*100/(b.user2.Wins+b.user2.Losses)
		b.user2.save()
		b.user1.Wins += 1
		b.user1.WinPercent = b.user1.Wins*100/(b.user1.Wins+b.user1.Losses)
		b.user1.LossPercent = b.user1.Losses*100/(b.user1.Wins+b.user1.Losses)
		b.user1.save()
	elif b.Winner == b.user2.pk:
		b.user2.Wins += 1
		b.user2.WinPercent = b.user2.Wins*100/(b.user2.Wins+b.user2.Losses)
		b.user2.LossPercent = b.user2.Losses*100/(b.user2.Wins+b.user2.Losses)
		b.user2.save()
		b.user1.Losses += 1
		b.user1.WinPercent = b.user1.Wins*100/(b.user1.Wins+b.user1.Losses)
		b.user1.LossPercent = b.user1.Losses*100/(b.user1.Wins+b.user1.Losses)
		b.user1.save()

	return redirect('/Profile')