import random

from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import HistoryData, UserFavorite, LotteryMetadata, UserHistory
from userauth.models import CustomUser
from datetime import datetime, timedelta
from django.db.models.functions import Length
from datetime import datetime
import random

class BullseyePicksListView(UnicornView):
    history: QuerySetType[HistoryData] = HistoryData.objects.none()
    # shift_distance: int = 30
    # base_end: int = -10
    # range_start: int = 30
    # range_end: int = -10
    # disable_next: bool = True
    # disable_previous: bool = False
    draw_count = 20
    date_count = 5
    lotteries:  QuerySetType[UserFavorite] = UserFavorite.objects.none()
    target_lottery: str = ""
    current_lottery: QuerySetType[UserFavorite] = UserFavorite.objects.none()
    target_count = 5
    target_date_db = None
    target_date_str = ''
    future_dates = []
    future_dates_db = []
    future_date_hash = {}
    future_picks = {}
    dummy = "DEFAULT"
    check_buttons = []

    def build_history(self):
        # now_minus_months = datetime.utcnow() - timedelta(days=self.range_start)
        # date_limit_start = now_minus_months.date()
        # now_minus_months = datetime.utcnow() - timedelta(days=self.range_end)
        # date_limit_end = now_minus_months.date()

        self.history = HistoryData.objects.annotate(balls_len=Length('balls')).filter(balls_len__gt=0, lottery=self.target_lottery).order_by("-date")[:self.draw_count]


    def build_draw_days_maps(self):
        draw_days = self.current_lottery.first().lottery.draw_times
        results = [0,0,0,0,0,0,0]
        if 'D' in draw_days:
            return [1,1,1,1,1,1,1]
        if 'M' in draw_days:
            results[0] = 1
        if 'T' in draw_days:
            results[1] = 1
        if 'W' in draw_days:
            results[2] = 1
        if 'R' in draw_days:
            results[3] = 1
        if 'F' in draw_days:
            results[4] = 1
        if 'S' in draw_days:
            results[5] = 1
        if 'U' in draw_days:
            results[6] = 1
        return results

    def find_future_pics(self):
        self.future_dates = []
        self.future_dates_db = []
        days_of_week = self.build_draw_days_maps()
        current_date = self.history.first().date
        while len(self.future_dates) < self.date_count:
            current_date += timedelta(days=1)
            day_of_week = current_date.weekday()
            if days_of_week[day_of_week] == 1:
                self.future_dates.append(current_date)
                self.future_dates_db.append(current_date.strftime('%Y-%m-%d'))
                self.future_date_hash[current_date.strftime('%Y-%m-%d')] = current_date
                if len(self.future_dates) == 1:
                    self.target_date_str = str(current_date)
                    self.target_date_db = current_date.strftime("%Y-%m-%d")

    def update_check(self):
        return

    def select_all(self):
        for i in range(0, len(self.check_buttons)):
            self.check_buttons[i] = True

    def select_none(self):
        for i in range(0, len(self.check_buttons)):
            self.check_buttons[i] = False

    def select_save(self):
        for i in range(0, len(self.check_buttons)):
            if self.check_buttons[i]:
                self.dummy = self.target_date_str
                UserHistory(
                    user=CustomUser.objects.get(id=self.request.user.id),
                    lottery=LotteryMetadata.objects.get(id=self.current_lottery[0].lottery.id),
                    date=self.target_date_str,
                    balls=str(self.future_picks[str(i)]['balls'])[1:-1],
                    special_balls=str(self.future_picks[str(i)]['special_balls'])[1:-1]
                ).save()

    def pick_generator(self, history_depth):
        lottery = self.current_lottery[0].lottery
        ball_list = []
        while len(ball_list) < lottery.number_of_balls:
            candidate_ball = random.randint(lottery.ball_min_value, lottery.ball_max_value)
            if not lottery.ball_allow_repeats and candidate_ball in ball_list:
                    continue
            ball_list.append(candidate_ball)
        if not lottery.order_matters:
            ball_list.sort()
        sball_list = []
        while len(sball_list) < lottery.number_of_special_balls:
            candidate_ball = random.randint(lottery.special_ball_min_value, lottery.special_ball_max_value)
            if not lottery.special_ball_allow_repeats and candidate_ball in ball_list:
                    continue
            sball_list.append(candidate_ball)
        if not lottery.order_matters:
            sball_list.sort()

        new_result = {'balls': ball_list, 'special_balls': sball_list}
#        self.dummy = new_result
        return new_result

    def bullseye_pick_generator(self):
        return self.pick_generator(20)

    def build_picks(self):
        self.dummy = "CALLED"
        self.future_picks = {}
        self.check_buttons = []
        for i in range(0, self.target_count):
            self.check_buttons.append(False)
        index = 0
        while len(self.future_picks) < self.target_count:
            # TODO add repeat check
            self.future_picks[str(index)] = self.bullseye_pick_generator()
            index += 1

    def mount(self):
        self.target_lottery = self.request.COOKIES.get("target_lottery")
        self.lotteries = UserFavorite.objects.filter(user=self.request.user.id)
        if self.target_lottery is None:
            self.target_lottery = self.lotteries.first().lottery.id
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.find_future_pics()
        # self.disable_next = True
        # self.disable_previous = False
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

    def lottery_select(self):
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.find_future_pics()
        # self.disable_next = True
        # self.disable_previous = False
        # self.range_start = self.shift_distance
        # self.range_end = self.base_end
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

