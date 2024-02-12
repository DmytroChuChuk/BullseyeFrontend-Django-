from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import UserHistory, UserFavorite
from datetime import datetime, timedelta


class UserDrawHistoryListView(UnicornView):
    history: QuerySetType[UserHistory] = UserHistory.objects.none()
    shift_distance: int = 30
    base_end: int = -10
    range_start: int = 30
    range_end: int = -10
    disable_next: bool = True
    disable_previous: bool = False
    history_ordered: set[QuerySetType[UserHistory]] = []
    lotteries:  QuerySetType[UserFavorite] = UserFavorite.objects.none()
    target_lottery: str = ""
    current_lottery: QuerySetType[UserFavorite] = UserFavorite.objects.none()

    def build_history(self):
        now_minus_months = datetime.utcnow() - timedelta(   days=self.range_start)
        date_limit_start = now_minus_months.date()
        now_minus_months = datetime.utcnow() - timedelta(days=self.range_end)
        date_limit_end = now_minus_months.date()

        if self.range_end <= 0:
            self.history = UserHistory.objects.filter(lottery=self.target_lottery, date__gte=date_limit_start).order_by("-date")
        else:
            self.history = UserHistory.objects.filter(lottery=self.target_lottery, date__gte=date_limit_start,
                                                 date__lte=date_limit_end).order_by("-date")

        self.history_ordered = []
        current_list = []
        current_date = ''
        for entry in self.history:
            if entry.date != current_date:
                current_date = entry.date
                if len(current_list) > 0:
                    self.history_ordered.append(current_list)
                    current_list = []
            current_list.append(entry)
        self.history_ordered.append(current_list)

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

    def get_older(self):
        self.range_end = self.range_start
        self.range_start += self.shift_distance
        self.build_history()
        if self.range_end >= 90:
            self.disable_previous = True
        self.disable_next = False

    def get_newer(self):
        self.range_start = self.range_end
        self.range_end -= self.shift_distance
        if self.range_end <= 0:
            self.disable_next = True
            self.range_end = self.base_end
        self.disable_previous = False
        self.build_history()

    def lottery_select(self):
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.disable_next = True
        self.disable_previous = False
        self.range_start = self.shift_distance
        self.range_end = self.base_end
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

