from rest_framework.serializers import *
from .models import *


class ActiveStateSerializer(ModelSerializer):
    class Meta():
        model = ActiveState
        fields = "__all__"


class StateSerializer(ModelSerializer):
    class Meta():
        model = State
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    class Meta():
        model = Country
        fields = "__all__"


class LotteryMetadataSerializer(ModelSerializer):
    class Meta():
        model = LotteryMetadata
        fields = "__all__"


class HistoryDataSerializer(ModelSerializer):
    class Meta():
        model = HistoryData
        fields = "__all__"


class UserFavoriteSerializer(ModelSerializer):
    class Meta():
        model = UserFavorite
        fields = "__all__"


class UserHistorySerializer(ModelSerializer):
    class Meta():
        model = UserHistory
        fields = "__all__"


from rest_framework import serializers


class FavoritesOutput(serializers.Serializer):
    agency_id = serializers.IntegerField(help_text="Agency ID.")
    id = serializers.IntegerField(help_text="User ID.")
    legacy_id = serializers.CharField(help_text="Legacy ID.")
    email = serializers.EmailField(help_text="User email address.")
    first_name = serializers.CharField(help_text="User first name.")
    last_name = serializers.CharField(help_text="User last name.")
    is_admin = serializers.BooleanField(help_text="Is user an admin.")
    timezone = serializers.CharField(
        source="agency.timezone", help_text="Agency timezone."
    )
    phone_number = serializers.CharField(
        source="best_phone.number",
        default="",
        help_text="User phone number.",
    )
    phone_extension = serializers.CharField(
        source="best_phone.extension",
        default="",
        help_text="User phone extension.",
    )