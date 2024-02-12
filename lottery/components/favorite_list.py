from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import UserFavorite, Country, State, LotteryMetadata,LotteryStateMapper

class FavoriteListView(UnicornView):
    id: int = 0
    favorites: QuerySetType[UserFavorite] = UserFavorite.objects.none()
    div_id: str = ""
    add_display_1: str = "none"
    add_display_2: str = "none"
    add_display_3: str = "none"
    add_display_4: str = "none"
    new_country: str = ""
    new_state: str = ""
    new_game: str = ""
    countries: QuerySetType[Country] = Country.objects.none()
    states: QuerySetType[State] = State.objects.none()
    games: QuerySetType[LotteryMetadata] = LotteryMetadata.objects.none()
    games_data: list = []

    def mount(self):
        next_draw_list = []
        self.favorites = UserFavorite.objects.filter(user=self.request.user.id)
        self.favorite_ids = []
        for favorite in self.favorites:
            self.favorite_ids.append((favorite.lottery_id))
            self.div_id += ":" + "timerID_" + str(favorite.lottery_id) + ":"
            next_draw_info = {'date': favorite.lottery.next_result_datetime.timestamp() * 1000, 'div_name': 'timerID_' + str(favorite.id)}
            next_draw_list.append(next_draw_info)
        self.call("setFavoriteTimers", next_draw_list)

    def remove_fav(self, id):
        UserFavorite.objects.filter(id=id).delete()
        self.favorites = UserFavorite.objects.filter(user=self.request.user.id)

    def new_lottery_start(self):
        if self.add_display_1 == "none":
            country_list = []
            results = LotteryMetadata.objects.filter(active_state=4).values('country').distinct().order_by('country')
            for result in results:
                country_list.append(result['country'])
            self.countries = Country.objects.filter(id__in=country_list)
            self.new_country = "Select a Country/Region"
            self.new_state = ""
            self.new_game = ""
            self.add_display_1 = "block"
            self.add_display_2 = "none"
            self.add_display_3 = "none"
            self.add_display_4 = "none"

    def new_lottery_cancel(self):
        self.new_country = "Select a Country/Region"
        self.new_state = ""
        self.new_game = ""
        self.add_display_1 = "none"
        self.add_display_2 = "none"
        self.add_display_3 = "none"
        self.add_display_4 = "none"
        self.favorite_ids = []

    def new_lottery_save(self):
        UserFavorite(user=self.request.user, lottery=LotteryMetadata.objects.get(id=self.new_game)).save()
        self.favorites = UserFavorite.objects.filter(user=self.request.user.id)
        self.new_lottery_cancel()

    def new_lottery_country(self):
        if int(self.new_country) == 1:
            # USA CASE
            state_list = []
            results = LotteryMetadata.objects.filter(active_state=4, country_id=1).values('state').distinct().order_by('state')
            for result in results:
                state_list.append(result['state'])
            self.states = State.objects.filter(id__in=state_list)
            self.new_state = "Select a State/Territory"
            self.add_display_2 = "block"
            self.add_display_3 = "none"
            self.add_display_4 = "none"
        else:
            self.add_display_2 = "none"
            self.add_display_3 = "block"
            self.add_display_4 = "none"
            self.games = LotteryMetadata.objects.filter(active_state=4, country_id=self.new_country).values('id','game').distinct().order_by('game')
            self.new_game = "Select a Game"


    def new_lottery_state(self):
        if int(self.new_country) == 1:
            # USA CASE
            self.games = LotteryMetadata.objects.filter(active_state=4, country_id=self.new_country, state_id=self.new_state).values('id','game').distinct().order_by('game')
            national_game_ids = LotteryStateMapper.objects.filter(state=38).values_list('lottery', flat=True)
            self.games |= LotteryMetadata.objects.filter(active_state=4, id__in=national_game_ids).values('id','game').distinct().order_by('game')
            self.games_data = []
            for game in self.games:
               self.games_data.append({'id': game['id'], 'game': game['game'], 'enable': game['id'] not in self.favorite_ids})
#                self.games_data.append({'stuff': game, 'enable': game.game not in self.favorite_ids})
            self.new_game = "Select a Game"
            self.add_display_3 = "block"
            self.add_display_4 = "none"
        else:
            text = "WHY ARE WE HERE IN THE CODE!!!"
            self.add_display_2 = "none"
            self.add_display_3 = "block"
            self.new_game = "Select a Game"

    def new_lottery_game(self):
        self.add_display_4 = "block"
