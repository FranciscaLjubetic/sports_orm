from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Avg, Count, Q

from . import team_maker

def index(request):
	context = {
		#"leagues": League.objects.all(),
		#"teams": Team.objects.all(),
		#"players": Player.objects.all(),
		"baseball_leagues" : League.objects.filter(sport = 'Baseball'),
		"women_leagues": League.objects.filter(name__contains= 'Women'),
		"hockey_leagues": League.objects.filter(sport__contains = 'hockey'),
		"no_futball_leagues": League.objects.exclude(sport__contains = 'football'),
		"Leagues_conferences": League.objects.filter(name__contains= 'onference'),
		"atlantic_leagues": League.objects.filter(name__contains= 'Atlantic'),
		"Dallas_teams": Team.objects.filter(location__contains = 'Dallas'),
		"Raptors_teams": Team.objects.filter(team_name = 'Raptors'),
		"City_teams": Team.objects.filter(location__contains = 'City'),
		"team_names_starting_with_t": Team.objects.filter(team_name__startswith = 'T'),
		"teams_orderasc_by_location": Team.objects.order_by('location'),
		"teams_orderdesc_by_team_name": Team.objects.order_by('-team_name'),
		"cooper_last_named_players": Player.objects.filter(last_name = 'Cooper'),
		"joshua_first_named_players": Player.objects.filter(first_name__startswith = 'Joshua'),
		"cooper_last_named_players_but_joshuas": Player.objects.filter(last_name = 'Cooper').exclude(first_name__startswith = 'Joshua'),
		"every_alexander_or_wyatt": Player.objects.filter(first_name='Alexander')| Player.objects.filter(first_name='Wyatt'),

	}
	return render(request, 'leagues/index.html', context)

def make_data(request):
	team_maker.gen_leagues(20)
	team_maker.gen_teams(20)
	team_maker.gen_players(300)

	return redirect("index")

def indextwo(request):
	
	
	every_player_with_num_teams_he_has_played= Player.objects.annotate(all_teams_account = Count('all_teams__id')).order_by('all_teams_account')
	
	withnum_players_teams = Team.objects.annotate(num_players= Count('all_players')).order_by('-num_players')
	every_team_with_12ormore_players = [team for team in withnum_players_teams if team.num_players > 11 ]

	historical_manitoba_players = Player.objects.filter(all_teams__team_name= 'Manitoba')
	
	context = {
		
		'all_atlantic_soccer_conference_teams': Team.objects.filter(league__name= 'Atlantic Soccer Conference'),#check
		'all_current_boston_penguins_players': Player.objects.filter(curr_team__team_name = 'Penguins').filter(curr_team__location ='Boston'),#check
		'all_International_colegiate_baseball_conference_current_players': Player.objects.filter(curr_team__league__name = 'International Collegiate Baseball Conference'), #check
		'all_the_American_Amateur_Football_Conference_last_named_lopez_players' : Player.objects.filter(curr_team__league__name ='American Conference of Amateur Football').filter(last_name__iexact ='Lopez'),
		'all_football_players': Player.objects.filter(curr_team__league__sport__in = ['Soccer', 'soccer', 'Football', 'football']) | Player.objects.filter(all_teams__league__sport__in = ['Soccer', 'soccer', 'Football', 'football']),
		'all_current_players_named_Sophia': Player.objects.filter(first_name= 'Sophia'),
		'all_teams_with_named_sophia_current_players': Team.objects.filter(curr_players__first_name= 'Sophia'), 
		'all_leagues_with_named_sophia_current_players': League.objects.filter(teams__curr_players__first_name = 'Sophia'),
		'all_not_current_last_named_flores_players_who_played_for_washington_roughriders': Player.objects.filter(all_teams__team_name= 'Roughriders').filter(last_name='Flores').exclude(curr_team__team_name= 'Roughriders'),
		'all_teams_where_samuel_evans_has_played': Team.objects.filter(all_players__first_name= 'Samuel').filter(all_players__last_name='Evans'),
		'all_historical_manitobatigers_players': Player.objects.filter(all_teams__location= 'Manitoba'),
		'only_oldnotcurrent_wichitas': Player.objects.filter(all_teams__team_name= 'Vikings', all_teams__location='Wichita').exclude(curr_team__team_name= 'Vikings'),
		'every_Jacob_Gray_Team_before_OregonColts': Team.objects.filter(all_players__first_name= 'Jacob', all_players__last_name='Gray').exclude(team_name='Colts', location= 'Oregon').exclude(curr_players__first_name= 'Jacob'),
		'every_Joshua_who_has_played_at_the_atlanticamateurbaseballfederation': Player.objects.filter(first_name= 'Joshua', all_teams__league__name= 'Atlantic Federation of Amateur Baseball Players'),
		'every_team_with_12ormore_players': every_team_with_12ormore_players,
		'every_player_with_num_teams_he_has_played': every_player_with_num_teams_he_has_played,

		#todos los equipos que han tenido 12 o más jugadores, pasados y presentes. (SUGERENCIA: busque la función de anotación de Django).
		#todos los jugadores y el número de equipos para los que jugó, ordenados por la cantidad de equipos para los que han jugado
	}
	return render(request, 'leagues/sports_orm_ii.html', context)