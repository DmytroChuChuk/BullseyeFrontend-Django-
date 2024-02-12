from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import HistoryData, UserFavorite, LotteryMetadata
from datetime import datetime, timedelta
from django.db.models.functions import Length
from datetime import datetime


class GraphListView(UnicornView):
    history: QuerySetType[HistoryData] = HistoryData.objects.none()
    lotteries:  QuerySetType[UserFavorite] = UserFavorite.objects.none()
    target_lottery: str = ""
    current_lottery: QuerySetType[UserFavorite] = UserFavorite.objects.none()
    range_start = 365
    range_end = -10

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
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

    def lottery_select(self):
        self.current_lottery = self.lotteries.filter(lottery=self.target_lottery)
        self.build_history()
        self.call("setCountdownDisplay", self.current_lottery[0].lottery.next_result_datetime.timestamp() * 1000)

