from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import HistoryData, UserFavorite, LotteryMetadata
from datetime import datetime, timedelta
from django.db.models.functions import Length
from datetime import datetime


class WheelingPicksListView(UnicornView):
    history: QuerySetType[HistoryData] = HistoryData.objects.none()
    shift_distance: int = 30
    base_end: int = -10
    range_start: int = 30
    range_end: int = -10
    disable_next: bool = True
    disable_previous: bool = False
    lotteries:  QuerySetType[UserFavorite] = UserFavorite.objects.none()
    target_lottery: str = ""
    current_lottery: QuerySetType[UserFavorite] = UserFavorite.objects.none()

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
        self.future_dates= []
        days_of_week = self.build_draw_days_maps()
        current_date = self.history.first().date
        while len(self.future_dates) < self.date_count:
            current_date += timedelta(days=1)
            day_of_week = current_date.weekday()
            if days_of_week[day_of_week] == 1:
                self.future_dates.append(current_date)


    def build_history(self):
        now_minus_months = datetime.utcnow() - timedelta(days=self.range_start)
        date_limit_start = now_minus_months.date()
        now_minus_months = datetime.utcnow() - timedelta(days=self.range_end)
        date_limit_end = now_minus_months.date()

        self.history = (HistoryData.objects.annotate(balls_len=Length('balls'))
                        .filter(balls_len__gt=0, lottery=self.target_lottery, date__gte=date_limit_start,
                                date__lte=date_limit_end).order_by("-date"))

    def mount(self):
        self.target_lottery = self.request.COOKIES.get("target_lottery")
        self.lotteries = UserFavorite.objects.filter(user=self.request.user.id)
        if self.target_lottery is None:
            self.target_lottery = self.lotteries.first().lottery.id
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.disable_next = True
        self.disable_previous = False
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

    def lottery_select(self):
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.disable_next = True
        self.disable_previous = False
        self.range_start = self.shift_distance
        self.range_end = self.base_end
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

