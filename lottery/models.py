from django.db import models
from datetime import datetime
from django.db.models.functions import Length

def remove_leading_zeros(num):
    return num.lstrip('0')

class ActiveState(models.Model):
    description = models.CharField(
        blank=False,
        null=False,
        default="",
        max_length=128
    )


class State(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        default="",
        max_length=128
    )


class Country(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        default="",
        max_length=128
    )


class HistoryData(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lottery', 'date'], name='unique_lottery_date_combination'
            )
        ]

    lottery = models.ForeignKey(
        "LotteryMetadata",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    date = models.DateField(
        null=False,
        blank=False,
        default=None,
    )

    balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    special_balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    second_draw_balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    second_draw_special_balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    third_draw_balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    multiplier = models.CharField(
        null=True,
        blank=False,
        max_length=16
    )

    jackpot = models.CharField(
        null=True,
        blank=False,
        max_length=64
    )

    write_time = models.DateTimeField(
        null=False,
        blank=False,
        default=datetime.utcnow()
    )

    @property
    def balls_as_list(self) -> list[str]:
        return list(map(remove_leading_zeros, self.balls.split(","))) if len(self.balls) > 0 else None

    @property
    def special_balls_as_list(self) -> list[str]:
        return list(map(remove_leading_zeros, self.special_balls.split(","))) if len(self.special_balls) > 0 else None

    @property
    def second_balls_as_list(self) -> list[str]:
        return list(map(remove_leading_zeros, self.second_draw_balls.split(","))) if len(self.second_draw_balls) > 0 else None

    @property
    def second_special_balls_as_list(self) -> list[str]:
        return list(map(remove_leading_zeros, self.second_draw_special_balls.split(","))) if len(self.second_draw_special_balls) > 0 else None

    @property
    def third_balls_as_list(self) -> list[str]:
        return list(map(remove_leading_zeros, self.third_draw_balls.split(","))) if len(self.third_draw_balls) > 0 else None


class LotteryMetadata(models.Model):
    game = models.CharField(
        blank=False,
        null=False,
        max_length=128
    )

    active_state = models.ForeignKey(
        "ActiveState",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    country = models.ForeignKey(
        "Country",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    state = models.ForeignKey(
        "State",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    number_of_balls = models.IntegerField(
        null=False,
        blank=False,
    )

    ball_name = models.CharField(
        null=True,
        blank=True,
        max_length=128
    )

    ball_min_value = models.IntegerField(
        null=False,
        blank=False,
    )

    ball_max_value = models.IntegerField(
        null=False,
        blank=False,
    )

    ball_allow_repeats = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    ball_color = models.CharField(
        null=True,
        blank=False,
        default=None,
        max_length=128
    )

    number_of_special_balls = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )

    special_ball_name = models.CharField(
        null=True,
        blank=True,
        default="",
        max_length=128
    )

    special_ball_min_value = models.IntegerField(
        null=True,
        blank=False,
    )

    special_ball_max_value = models.IntegerField(
        null=True,
        blank=False,
    )

    special_ball_allow_repeats = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    special_ball_color = models.CharField(
        null=True,
        blank=False,
        default=None,
        max_length=128
    )

    has_second_draw = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    second_draw_name = models.CharField(
        null=True,
        blank=False,
        default=None,
        max_length=128
    )

    has_second_special_ball = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    has_third_draw = models.BooleanField(
        null=True,
        blank=False,
        default=False
    )

    third_draw_name = models.CharField(
        null=True,
        blank=False,
        default=None,
        max_length=128
    )

    draw_times = models.CharField(
        null=False,
        blank=False,
        max_length=128
    )

    time_zone = models.CharField(
        null=False,
        blank=False,
        max_length=128
    )

    order_matters = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    use_multiplier = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    generate_special_balls = models.BooleanField(
        null=False,
        blank=False,
        default=True
    )

    uses_sum = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    track_jackpot = models.BooleanField(
        null=True,
        blank=False,
        default=False
    )

    number_of_balls_drawn = models.IntegerField(
        null=True,
        blank=False,
        default=None
    )

    reporting_delay_in_minutes = models.IntegerField(
        null=True,
        blank=False,
        default=None
    )

    skip_dates = models.TextField(
        null=True,
        blank=False,
        default=None,
    )

    start_date = models.DateField(
        null=True,
        blank=False,
        default=None
    )

    last_result_date = models.DateField(
        null=True,
        blank=False,
        default=None
    )

    next_result_date = models.DateField(
        null=True,
        blank=False,
        default=None
    )

    next_result_datetime = models.DateTimeField(
        null=True,
        blank=False,
        default=None
    )

    link_to_game_site = models.CharField(
        null=False,
        blank=False,
        max_length=256
    )

    best_sum_min = models.IntegerField(
        null=True,
        blank=False,
        default=None
    )

    best_sum_max = models.IntegerField(
        null=True,
        blank=False,
        default=None
    )

    image_name = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    @property
    def location(self) -> str:
        if self.state is None:
            if self.country.name == "USA":
                location = "Multistate, USA"
            else:
                location = self.country.name
        else:
            location = self.state.name + ", " + self.country.name
        return location

    @property
    def jackpot(self) -> str:
        jackpot = ""
        if self.track_jackpot == 1:
            jackpot = "PENDING"
            future_history = HistoryData.objects.filter(lottery=self.id, balls="").order_by("-date")
            if future_history is not None and len(future_history) == 1:
                jackpot = future_history.first().jackpot
        return jackpot

    @property
    def latest_results(self) -> HistoryData:
        return HistoryData.objects.annotate(
            balls_len=Length('balls')).filter(balls_len__gt=0, lottery=self.id).order_by("-date").first()


class LotteryStateMapper(models.Model):
    lottery = models.ForeignKey(
        "LotteryMetadata",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    state = models.ForeignKey(
        "State",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

class UserFavorite(models.Model):
    user = models.ForeignKey(
        "userauth.CustomUser",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    lottery = models.ForeignKey(
        "LotteryMetadata",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )


class UserHistory(models.Model):
    user = models.ForeignKey(
        "userauth.CustomUser",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    lottery = models.ForeignKey(
        "LotteryMetadata",
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    date = models.DateField(
        null=False,
        blank=False,
        default=None,
    )

    balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    special_balls = models.CharField(
        null=True,
        blank=False,
        max_length=256
    )

    @property
    def balls_as_list(self) -> list[str]:
        return self.balls.split(",") if len(self.balls) > 0 else None

    @property
    def special_balls_as_list(self) -> list[str]:
        return self.special_balls.split(",") if len(self.special_balls) > 0 else None

    @property
    def actual_balls_as_list(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.balls.split(",") if len(history.balls) > 0 else None

    @property
    def actual_special_balls_as_list(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.special_balls.split(",") if len(history.special_balls) > 0 else None
    @property
    def actual_second_balls_as_list(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.second_draw_balls.split(",") if len(history.second_draw_balls) > 0 else None

    @property
    def actual_second_special_balls_as_list(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.second_draw_special_balls.split(",") if len(history.second_draw_special_balls) > 0 else None

    @property
    def actual_third_balls_as_list(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.third_draw_balls.split(",") if len(history.third_draw_balls) > 0 else None

    @property
    def actual_multiplier(self) -> list[str]:
        history = HistoryData.objects.filter(lottery=self.lottery_id, date=self.date).first()
        return history.multiplier if history is not None else ""

