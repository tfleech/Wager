from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.HomePage, name='HomePage'),
	url(r'^LogIn/', views.LogIn, name="LogIn"),
	url(r'^SignUp/', views.SignUp, name="SignUp"),
	url(r'^AddUser/', views.AddUser, name="AddUser"),
	url(r'^SetLoggedIn/', views.SetLoggedIn, name="SetLoggedIn"),
	url(r'^SetLoggedOut/', views.SetLoggedOut, name="SetLoggedOut"),
	url(r'^NewBet/', views.NewBet, name="NewBet"),
	url(r'^CreateNewBet/', views.CreateNewBet, name="CreateNewBet"),
	url(r'^FindFriends/', views.FindFriends, name="FindFriends"),
	url(r'^AddFriend/', views.AddFriend, name="AddFriend"),
	url(r'^Profile/', views.Profile, name="Profile"),
	url(r'^AcceptBet/(?P<bet_id>[0-9]+)/$', views.AcceptBet, name='AcceptBet'),
	url(r'^User2Wins/(?P<bet_id>[0-9]+)/$', views.User2Wins, name='User2Wins'),
	url(r'^User1Wins/(?P<bet_id>[0-9]+)/$', views.User1Wins, name='User1Wins'),
	url(r'^AcceptResult/(?P<bet_id>[0-9]+)/$', views.AcceptResult, name="AcceptResult"),
]
