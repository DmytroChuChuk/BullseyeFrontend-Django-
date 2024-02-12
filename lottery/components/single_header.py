from django_unicorn.components import UnicornView, QuerySetType
from lottery.models import UserFavorite, LotteryMetadata


class SingleHeaderView(UnicornView):
    lottery: QuerySetType[LotteryMetadata] = LotteryMetadata.objects.none()
    target_lottery: int = 0

    def mount(self):
        self.target_lottery = self.request.COOKIES.get("target_lottery")
        if self.target_lottery is None:
            self.target_lottery = UserFavorite.objects.filter(user=self.request.user.id).first().lottery.id
        self.lottery = LotteryMetadata.objects.filter(id=self.target_lottery)
