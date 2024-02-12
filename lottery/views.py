from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models.functions import Length
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from lottery.models import UserFavorite, HistoryData, UserHistory, LotteryMetadata
from userauth.models import CustomUser

def get_target_lottery(request, user_id):
    target = request.COOKIES.get("target_lottery")
    if target is None:
        target = UserFavorite.objects.filter(user=user_id).first().lottery.id
    return target


def build_lottery_data(user_id):
    results_list = {}
    for fav in UserFavorite.objects.filter(user=user_id):
        results_collection = {}
        jackpot = ""
        if fav.lottery.track_jackpot == 1:
            jackpot = "PENDING"
            future_history = HistoryData.objects.filter(lottery=fav.lottery.id, balls="")
            if future_history.count() == 1:
                jackpot = future_history.first().jackpot

        results = HistoryData.objects.annotate(balls_len=Length('balls')).filter(balls_len__gt=0, lottery=fav.lottery.id).order_by("-date").first()

        if fav.lottery.state is None:
            if fav.lottery.country.name == "USA":
                location = "Multistate, USA"
            else:
                location = fav.lottery.country.name
        else:
            location = fav.lottery.state.name + ", " + fav.lottery.country.name

        results_collection["id"] = fav.lottery.id
        results_collection["image"] = fav.lottery.image_name
        results_collection["name"] = fav.lottery.game
        results_collection["location"] = location
        results_collection["next_draw_date"] = fav.lottery.next_result_date
        results_collection["next_draw_time"] = fav.lottery.next_result_datetime
        results_collection["jackpot"] = jackpot
        results_collection["date"] = results.date
        results_collection["balls"] = results.balls.split(",") if len(results.balls) > 0 else None
        results_collection["special_balls"] = results.special_balls.split(",") if len(results.special_balls) > 0 else None
        results_collection["second_draw_balls"] = results.second_draw_balls.split(",") if len(results.second_draw_balls) > 0 else None
        results_collection["second_draw_special_balls"] = results.second_draw_special_balls.split(",") if len(results.second_draw_special_balls) > 0 else None
        results_collection["third_draw_balls"] = results.third_draw_balls.split(",") if len(results.third_draw_balls) > 0 else None
        results_collection["multiplier"] = results.multiplier
        results_collection["ball_color"] = fav.lottery.ball_color
        results_collection["special_ball_color"] = fav.lottery.special_ball_color
        results_collection["second_draw_name"] = fav.lottery.second_draw_name
        results_collection["third_draw_name"] = fav.lottery.third_draw_name
        results_list[fav.lottery.id] = results_collection

    return results_list


def bullseye_picks_view(request):
    return render(request, 'bullseye_picks.html', {})

def custom_picks_view(request):
    return render(request, 'custom_picks.html', {})

def manual_picks_view(request):
    return render(request, 'manual_picks.html', {})

def wheeling_picks_view(request):
    return render(request, 'wheeling_picks.html', {})

def profile_view(request):
    return render(request, 'profile.html', {})


@login_required
def favorite_view(request):
    #results = build_lottery_data(request.user.id)

    return render(request, 'favorites.html', {})


def get_recent_history(user_id, days_start, days_end):
    results = {}
    now_minus_months = datetime.utcnow() - timedelta(days=days_start)
    date_limit_start = now_minus_months.date()
    if days_end is not None:
        now_minus_months = datetime.utcnow() - timedelta(days=days_end)
        date_limit_end = now_minus_months.date()
        history = UserHistory.objects.filter(user=user_id, date__gte=date_limit_start, date__lte=date_limit_end).order_by("-date")
    else:
        history = UserHistory.objects.filter(user=user_id, date__gte=date_limit_start).order_by("-date")


    for entry in history:
        if entry.date not in results:
            results[entry.date] = {}
        if entry.lottery.id not in results[entry.date]:
            # if entry.lottery.state is None:
            #     if entry.lottery.country.name == "USA":
            #         location = "Multistate, USA"
            #     else:
            #         location = entry.lottery.country.name
            # else:
            #     location = entry.lottery.state.name + ", " + entry.lottery.country.name


            results[entry.date][entry.lottery.id] = []
        results[entry.date][entry.lottery.id].append(entry)
        #     results[entry.date][entry.lottery.id]["name"] = entry.lottery.game
        #     results[entry.date][entry.lottery.id]["image"] = entry.lottery.image_name
        #     results[entry.date][entry.lottery.id]["location"] = location
        #     results[entry.date][entry.lottery.id]["history"] = []
        #     history = HistoryData.objects.filter(lottery=entry.lottery, date=entry.date).first()
        #     if history is None or history.balls is None or len(history.balls) == 0:
        #         continue
        #     data_point = {}
        #     data_point["date"] = history.date
        #     data_point["balls"] = history.balls.split(",") if len(history.balls) > 0 else None
        #     data_point["special_balls"] = history.special_balls.split(",") if len(history.special_balls) > 0 else None
        #     data_point["multiplier"] = history.multiplier
        #     data_point["second_draw_balls"] = history.second_draw_balls.split(",") if len(history.second_draw_balls) > 0 else None
        #     data_point["second_draw_special_balls"] = history.second_draw_special_balls.split(",") if len(history.second_draw_special_balls) > 0 else None
        #     data_point["second_draw_name"] = entry.lottery.second_draw_name
        #     data_point["third_draw_balls"] = history.third_draw_balls.split(",") if len(history.third_draw_balls) > 0 else None
        #     data_point["third_draw_name"] = entry.lottery.third_draw_name
        #     results[entry.date][entry.lottery.id]["draw"] = data_point
        # data_point = {}
        # data_point["date"] = entry.date
        # data_point["balls"] = entry.balls.split(",") if len(entry.balls) > 0 else None
        # data_point["special_balls"] = entry.special_balls.split(",") if len(entry.special_balls) > 0 else None
        # data_point["multiplier"] = ""
        # results[entry.date][entry.lottery.id]["history"].append(data_point)
    return results


@login_required
def recent_view(request):
    user_id = request.user.id
    full_results = {}
    full_results["results"] = build_lottery_data(user_id)
    target_lottery = get_target_lottery(request, user_id)
    full_results["target_id"] = target_lottery
    full_results["history"] = get_recent_history(user_id,7, None)
    return render(request, 'recent.html', {"results": full_results})


def get_history(lottery_id, days_start, days_end):
    results = {}
    now_minus_months = datetime.utcnow() - timedelta(days=days_start)
    date_limit_start = now_minus_months.date()
    now_minus_months = datetime.utcnow() - timedelta(days=days_end)
    date_limit_end = now_minus_months.date()

    history = HistoryData.objects.filter(lottery=lottery_id, date__gte=date_limit_start, date__lte=date_limit_end).order_by("-date")
    for entry in history:
        data_point = {"date": entry.date, "balls": entry.balls.split(",") if len(entry.balls) > 0 else None,
                      "special_balls": entry.special_balls.split(",")
                      if (entry.special_balls is not None and len(entry.special_balls) > 0) else None,
                      "multiplier": entry.multiplier, "second_draw_balls": entry.second_draw_balls.split(",")
                      if (entry.second_draw_balls is not None and len(entry.second_draw_balls) > 0) else None,
                      "second_draw_special_balls": entry.second_draw_special_balls.split(",")
                      if (entry.second_draw_special_balls is not None and len(entry.second_draw_special_balls) > 0)
                      else None,
                      "third_draw_balls": entry.third_draw_balls.split(",") if (
                                  entry.third_draw_balls is not None and len(entry.third_draw_balls) > 0) else None}
        results[entry.date] = data_point
    return results


@login_required
def lottery_history_view(request):
    user_id = request.user.id
    full_results = {}
    full_results["results"] = build_lottery_data(user_id)
    target_lottery = get_target_lottery(request, user_id)
    full_results["second_draw_name"] = full_results["results"][target_lottery]["second_draw_name"]
    full_results["third_draw_name"] = full_results["results"][target_lottery]["third_draw_name"]
    full_results["target_id"] = target_lottery
    full_results["next_time"] = full_results["results"][target_lottery]["next_draw_time"]

    full_results["history"] = get_history(target_lottery, 90, 0)
    return render(request, 'lottery_history.html', {"results": full_results})


@login_required
def graph_view(request):
    user_id = request.user.id
    results_list = {}
    for fav in UserFavorite.objects.filter(user=user_id):
        if fav.lottery.state is None:
            if fav.lottery.country.name == "USA":
                location = "Multistate, USA"
            else:
                location = fav.lottery.country.name
        else:
            location = fav.lottery.state.name + ", " + fav.lottery.country.name

        results_collection = {}
        results_collection["lottery_id"] = fav.lottery.id
        results_collection["lottery_image"] = fav.lottery.image_name
        results_collection["lottery_name"] = fav.lottery.game
        results_collection["lottery_location"] = location
        results_collection["user"] = request.user
        results_collection["userid"] = request.user.id
        results_list[fav.lottery.id] = results_collection
    return render(request, 'graph.html', {"results": results_list})


def get_user_history(user_id, lottery_id, days_start, days_end):
    results = {}
    now_minus_months = datetime.utcnow() - timedelta(days=days_start)
    date_limit_start = now_minus_months.date()
    if days_end is not None:
        now_minus_months = datetime.utcnow() - timedelta(days=days_end)
        date_limit_end = now_minus_months.date()
        history = UserHistory.objects.filter(user=user_id, lottery=lottery_id, date__gte=date_limit_start, date__lte=date_limit_end).order_by("-date")
    else:
        history = UserHistory.objects.filter(user=user_id, lottery=lottery_id, date__gte=date_limit_start).order_by("-date")

    metadata = LotteryMetadata.objects.filter(id=lottery_id).first()

    for entry in history:
        if entry.date not in results:
            results[entry.date] = {}
            results[entry.date]["history"] = []
            history = HistoryData.objects.filter(lottery=lottery_id, date=entry.date).first()
            if history is None or history.balls is None or len(history.balls) == 0:
                continue
            data_point = {}
            data_point["date"] = history.date
            data_point["balls"] = history.balls.split(",") if len(history.balls) > 0 else None
            data_point["special_balls"] = history.special_balls.split(",") if len(history.special_balls) > 0 else None
            data_point["multiplier"] = history.multiplier
            data_point["second_draw_balls"] = history.second_draw_balls.split(",") if len(history.second_draw_balls) > 0 else None
            data_point["second_draw_special_balls"] = history.second_draw_special_balls.split(",") if len(history.second_draw_special_balls) > 0 else None
            data_point["second_draw_name"] = metadata.second_draw_name
            data_point["third_draw_balls"] = history.third_draw_balls.split(",") if (
                                  history.third_draw_balls is not None and len(history.third_draw_balls) > 0) else None
            data_point["third_draw_name"] = metadata.third_draw_name
            results[entry.date]["draw"] = data_point
        data_point = {"date": entry.date, "balls": entry.balls.split(",") if len(entry.balls) > 0 else None,
                      "special_balls": entry.special_balls.split(",") if len(entry.special_balls) > 0 else None,
                      "multiplier": ""}
        results[entry.date]["history"].append(data_point)
    return results


@login_required
def user_history_view(request):
    user_id = request.user.id
    full_results = {"results": build_lottery_data(user_id)}
    target_lottery = get_target_lottery(request, user_id)
    full_results["target_id"] = target_lottery
    full_results["history"] = get_user_history(user_id, target_lottery, 90, None)
    return render(request, 'user_history.html', {"results": full_results})


@login_required
def terms_view(request):
    return render(request, 'terms.html', {})


@login_required
def privacy_view(request):
    return render(request, 'privacy.html', {})


@login_required
def contact_view(request):
    return render(request, 'contact.html', {})


@login_required
def help_view(request):
    return render(request, 'help.html', {})


def test_view(request):
    return render(request, 'base_lottery.html', {})


def test_view2(request):
    return render(request, 'base_lottery_single.html', {})


class FavoritesOutput(serializers.Serializer):
    user = CustomUser()
    lottery = LotteryMetadata()


class FavoritesListApi(APIView):
    class FavoritesListOutput(serializers.Serializer):
        results = FavoritesOutput(many=True)

    http_method_names = ["get"]

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: FavoritesListOutput},
        tags=["workflow"],
    )
    def get(self, request):
        workflows = build_lottery_data(user_id=request.user.id)
        return Response(
            data=self.FavoritesListOutput({"results": workflows}).data,
            status=status.HTTP_200_OK,
        )

class FavoritesDeleteApi(APIView):
    class WorkflowListOutput(serializers.Serializer):
        results = FavoritesOutput(many=True)

    # http_method_names = ["get"]

    # @extend_schema(
    #     request=None,
    #     responses={status.HTTP_200_OK: WorkflowListOutput},
    #     tags=["workflow"],
    # )
    # def get(self, request):
    #     workflows = list_workflows(agency_id=request.user.agency_id)
    #     return Response(
    #         data=self.WorkflowListOutput({"results": workflows}).data,
    #         status=status.HTTP_200_OK,
    #     )

# def build_lottery_recent_history_data(user_id):
#     results_list = HistoryData.objects.none()
#     for fav in UserFavorite.objects.filter(user=user_id):
#         jackpot = ""
#         if fav.lottery.track_jackpot == 1:
#             jackpot = "PENDING"
#             future_history = HistoryData.objects.filter(lottery=fav.lottery.id, balls="")
#             if future_history.count() == 1:
#                 jackpot = future_history.first().jackpot
#
#         results = HistoryData.objects.annotate(balls_len=Length('balls')).filter(balls_len__gt=0,
#                                                                                  lottery=fav.lottery.id).order_by(
#             "-date").first()
#
#         results_list |= results
#     return results_list

# def build_lottery_recent_history_data(lottery_id, track_jackpot):
#     jackpot = ""
#     if track_jackpot == 1:
#         jackpot = "PENDING"
#         future_history = HistoryData.objects.filter(lottery=lottery_id, balls="").order_by(
#         "-date").first()
#         if future_history.count() == 1:
#             jackpot = future_history.first().jackpot
#
#     results = HistoryData.objects.annotate(balls_len=Length('balls')).filter(balls_len__gt=0,
#                                                                              lottery=lottery_id).order_by(
#         "-date").first()
#
#     return results, jackpot
