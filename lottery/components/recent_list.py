from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import UserHistory
from datetime import datetime, timedelta


class RecentListView(UnicornView):
    id: int = 0
    recent_draws: QuerySetType[UserHistory] = UserHistory.objects.none()
    recent_dict: dict[str, dict] = {}
    recent_dates: list[str] = list()
    index: int = 0

    def mount(self):
        now_minus_months = datetime.utcnow() - timedelta(days=7)
        date_limit_start = now_minus_months.date()
        self.recent_draws = UserHistory.objects.filter(user=self.request.user.id, date__gte=date_limit_start).order_by("lottery").order_by("-date")

        self.index = 0
        for draw in self.recent_draws:
            date_str = str(draw.date)
            if date_str not in self.recent_dict:
                self.recent_dates.append(date_str)
                self.recent_dict[date_str] = {}
                self.recent_dict[date_str]["date"] = draw.date
            # if str(draw.lottery_id) not in self.recent_dict[date_str]:
                # self.recent_dict[date_str][str(draw.lottery_id)] = {}
        #         self.recent_dict[date_str][str(draw.lottery_id)]["lottery"] = draw.lottery
        #     self.recent_dict[date_str][str(draw.lottery_id)]["draw"] = {}
        #     result = {"balls": draw.balls, "special_balls": draw.special_balls}
        #     self.recent_dict[date_str][str(draw.lottery_id)]["draw"] = result
