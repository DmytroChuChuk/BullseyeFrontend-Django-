from django.core.management.base import BaseCommand
import logging
from django.db import transaction
from django.db.models.functions import Length
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp
from lottery.models import *
from userauth.models import CustomUser
import pyodbc
from django.contrib.sites.models import Site
import random
from django.db import connection
from django.core.management.color import no_style

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

logger = logging.getLogger(__name__)


@transaction.atomic
def seed_active_state():
    ActiveState(1, "Metadata Only").save()
    ActiveState(2, "Metadata and Scrapper").save()
    ActiveState(3, "Metadata, Scrapper, and History").save()
    ActiveState(4, "Fully Active").save()
    ActiveState(5, "Retired").save()
    ActiveState(6, "Junk/Ignore").save()


@transaction.atomic
def seed_country():
    Country(1, "USA").save()
    Country(2, "Canada").save()
    Country(3, "United Kingdom").save()
    Country(4, "Caribbean").save()
    Country(5, "Germany").save()
    Country(6, "Ireland").save()
    Country(7, "Italy").save()
    Country(8, "Europe").save()
    Country(9, "Australia").save()
    Country(10, "New Zealand").save()
    Country(11, "Mexico").save()
    Country(12, "Singapore").save()
    Country(13, "Spain").save()
    Country(14, "Belgium").save()
    Country(15, "South Africa").save()
    Country(16, "Brazil").save()
    Country(17, "Hong Kong").save()
    Country(18, "Turkey").save()
    Country(19, "Taiwan").save()
    Country(20, "France").save()
    Country(21, "Greece").save()
    Country(22, "Malaysia").save()
    Country(23, "Aruba").save()
    Country(24, "Austria").save()
    Country(25, "Chile").save()
    Country(26, "Colombia").save()
    Country(27, "Costa Rica").save()
    Country(28, "Denmark").save()
    Country(29, "Ecuador").save()
    Country(30, "Finland").save()
    Country(31, "India").save()
    Country(32, "Argentina").save()


@transaction.atomic
def seed_state():
    State(1, 'Arizona').save()
    State(2, 'Arkansas').save()
    State(3, 'California').save()
    State(4, 'Colorado').save()
    State(5, 'Connecticut').save()
    State(6, 'Delaware').save()
    State(7, 'Florida').save()
    State(8, 'Georgia').save()
    State(9, 'Idaho').save()
    State(10, 'Illinois').save()
    State(11, 'Indiana').save()
    State(12, 'Iowa').save()
    State(13, 'Kansas').save()
    State(14, 'Kentucky').save()
    State(15, 'Louisiana').save()
    State(16, 'Maine').save()
    State(17, 'Maryland').save()
    State(18, 'Massachusetts').save()
    State(19, 'Michigan').save()
    State(20, 'Minnesota').save()
    State(21, 'Missouri').save()
    State(22, 'Montana').save()
    State(23, 'Nebraska').save()
    State(24, 'New Hampshire').save()
    State(25, 'New Jersey').save()
    State(26, 'New Mexico').save()
    State(27, 'New York').save()
    State(28, 'North Carolina').save()
    State(29, 'North Dakota').save()
    State(30, 'Ohio').save()
    State(31, 'Oklahoma').save()
    State(32, 'Oregon').save()
    State(33, 'Pennsylvania').save()
    State(34, 'Puerto Rico').save()
    State(35, 'Rhode Island').save()
    State(36, 'South Carolina').save()
    State(37, 'South Dakota').save()
    State(38, 'Tennessee').save()
    State(39, 'Texas').save()
    State(40, 'Vermont').save()
    State(41, 'US Virgin Islands').save()
    State(42, 'Virginia').save()
    State(43, 'Washington DC').save()
    State(44, 'Washington').save()
    State(45, 'West Virginia').save()
    State(46, 'Wisconsin').save()
    State(47, 'Wyoming').save()
    State(48, 'Quebec').save()
    State(49, 'Ontario').save()
    State(50, 'Atlantic Canada').save()
    State(51, 'National Canada').save()
    State(52, 'Western Canada').save()
    State(53, 'BC Canada').save()
    State(54, 'Mississippi').save()
    State(55, 'St.Maarten').save()
    State(56, 'St.Kitts & Nevis').save()
    State(57, 'Antigua').save()
    State(58, 'Anguilla').save()


@transaction.atomic
def seed_lottery_metadata():
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=bullseye-lotto-01.cn7rzjtsboi0.us-east-2.rds.amazonaws.com,'
                                '1433;uid=vexcel;pwd=qNFQ#SjZmM9Q$0#%RW&T; '
                                'Database=LottoBetaDB;', autocommit=True)
    cursor = connection.cursor()

    sql_query = 'SELECT  * FROM [LottoBetaDB].[dbo].[LotteryMetadata] '
    cursor.execute(sql_query)

    for data_row in cursor:
        country = None
        if data_row[20] is not None:
            country = Country.objects.get(id=data_row[20])
        state = None
        if data_row[18] is not None:
            state = State.objects.get(id=data_row[18])
        has_second_special_balls = data_row[34]
        if has_second_special_balls is None:
            has_second_special_balls = False
        uses_sum = data_row[22]
        if uses_sum is None:
            uses_sum = False
        special_ball_allow_repeats = data_row[11]
        if special_ball_allow_repeats is None:
            special_ball_allow_repeats = False
        LotteryMetadata(
            id=data_row[0],
            game=data_row[1],
            active_state=ActiveState.objects.get(id=data_row[2]),
            country=country,
            state=state,
            number_of_balls=data_row[3],
            ball_name=data_row[23],
            ball_min_value=data_row[6],
            ball_max_value=data_row[7],
            ball_allow_repeats=data_row[8],
            ball_color=data_row[32],
            number_of_special_balls=data_row[4],
            special_ball_name=data_row[5],
            special_ball_min_value=data_row[9],
            special_ball_max_value=data_row[10],
            special_ball_allow_repeats=special_ball_allow_repeats,
            special_ball_color=data_row[33],
            has_second_draw=data_row[21],
            second_draw_name=data_row[30],
            has_second_special_ball=has_second_special_balls,
            has_third_draw=data_row[27],
            third_draw_name=data_row[31],
            draw_times=data_row[13],
            time_zone=data_row[15],
            order_matters=data_row[16],
            use_multiplier=data_row[17],
            generate_special_balls=data_row[19],
            uses_sum=uses_sum,
            track_jackpot=data_row[24],
            number_of_balls_drawn=data_row[25],
            reporting_delay_in_minutes=data_row[26],
            skip_dates=data_row[28],
            start_date=data_row[29],
            last_result_date=data_row[35],
            next_result_date=data_row[36],
            next_result_datetime=data_row[37],
            link_to_game_site=data_row[12],
            best_sum_min=data_row[38],
            best_sum_max=data_row[39],
            image_name=data_row[40]
        ).save()


@transaction.atomic
def seed_lottery_state_mapper_metadata():
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=bullseye-lotto-01.cn7rzjtsboi0.us-east-2.rds.amazonaws.com,'
                                '1433;uid=vexcel;pwd=qNFQ#SjZmM9Q$0#%RW&T; '
                                'Database=LottoBetaDB;', autocommit=True)
    cursor = connection.cursor()

    sql_query = 'SELECT  * FROM [LottoBetaDB].[dbo].[LotteryStateMapper] '
    cursor.execute(sql_query)

    for data_row in cursor:
        LotteryStateMapper(
            lottery=LotteryMetadata.objects.get(id=data_row[0]),
            state=State.objects.get(id=data_row[1])
        ).save()


@transaction.atomic
def seed_lottery_history(lottery_id):
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=bullseye-lotto-01.cn7rzjtsboi0.us-east-2.rds.amazonaws.com,'
                                '1433;uid=vexcel;pwd=qNFQ#SjZmM9Q$0#%RW&T; '
                                'Database=LottoBetaDB;', autocommit=True)
    cursor = connection.cursor()

    sql_query = 'SELECT  * FROM [LottoBetaDB].[dbo].[HistoryData] ' \
                'WHERE  Date >  CAST(DATEADD(m, -6, GetDate()) as date) and LotteryKey = ' + str(lottery_id)
    cursor.execute(sql_query)

    for data_row in cursor:
        HistoryData(
            lottery_id=data_row[0],
            date=data_row[1],
            balls=data_row[6],
            special_balls=data_row[2],
            second_draw_balls=data_row[5],
            second_draw_special_balls=data_row[7],
            third_draw_balls=data_row[9],
            multiplier=data_row[3],
            jackpot=data_row[4],
        ).save()


@transaction.atomic
def seed_user_favorites(lottery_list):
    for lottery in lottery_list:
        UserFavorite(
            user=CustomUser.objects.get(id=1),
            lottery=LotteryMetadata.objects.get(id=lottery)
        ).save()


@transaction.atomic
def seed_user_account_setup():
    CustomUser(id=1,
               password="pbkdf2_sha256$600000$LD8ipDYfxeAeeUgyAGsvHu$Vb9xbtbJ8q5gCVrD4l5gX8oZ4n7SPuDEppGFqSakTHg=",
               last_login=None,
               is_superuser=False,
               username="Geoffrey",
               first_name="Geoffrey",
               last_name="Hart",
               email="hartjunkfilter@gmail.com",
               is_staff=False,
               is_active=True,
               date_joined="2023-10-20 21:27:07.351196 +00:00",
               display_name="That Guy").save()
    CustomUser(id=2,
               password="pbkdf2_sha256$600000$TwtUvlAUep1qCDA2BxHoKV$GIeZRtbkcCSOLHJHgXh2Yo8dP5z24EOJk2ZWi55w7Rs=",
               last_login="2023-10-23 03:40:57.339808 +00:00",
               is_superuser=True,
               username="Mr.Admin",
               first_name="",
               last_name="",
               email="hart.geoffrey@gmail.com",
               is_staff=True,
               is_active=True,
               date_joined="2023-10-23 03:40:57.339808 +00:00",
               display_name="").save()
    CustomUser(id=3,
               password="!InWB1rZtJ1P2tfCOSrDXv0QT28YmXiTzihpAz2Cc",
               last_login="2023-10-23 03:46:11.039751 +00:00",
               is_superuser=False,
               username="lotto",
               first_name="Lotto",
               last_name="Dude",
               email="lottodude007@gmail.com",
               is_staff=False,
               is_active=True,
               date_joined="2023-10-23 03:46:02.397000 +00:00",
               display_name="DudeMan").save()

    EmailAddress(id=1, email="hartjunkfilter@gmail.com", verified=True, primary=True, user_id=1).save()
    EmailAddress(id=2, email="hart.geoffrey@gmail.com", verified=True, primary=True, user_id=3).save()
    SocialAccount(id=1, provider="google", uid="116457393552935177499", last_login="2023-10-23 03:46:11.011238 +00:00",
                  date_joined="2023-10-23 03:46:11.011238 +00:00",
                  extra_data='{"iss": "https://accounts.google.com", "azp": '
                             '"544071216198-84co67e8paq4pa74sst3u1nag54mrkup.apps.googleusercontent.com", '
                             '"aud": "544071216198-84co67e8paq4pa74sst3u1nag54mrkup.apps.googleusercontent.com", '
                             '"sub": "116457393552935177499", "email": "lottodude007@gmail.com", "email_verified": '
                             'true, "at_hash": "TSZPi5HGSm3rcdsn7DrVxg", "name": "Lotto Dude", "picture": '
                             '"https://lh3.googleusercontent.com/a/ACg8ocLd4ZXNIxJfneXMO5v_mgNxTuZXPGIsmybh1_tpDaMp'
                             '=s96-c", "given_name": "Lotto", "family_name": "Dude", "locale": "en", '
                             '"iat": 1698032758, "exp": 1698036358}',
                  user_id=3).save()


@transaction.atomic
def seed_social_account_setup():
    site = Site.objects.filter(id=1)
    site.update(name="bullseyelotto.com", domain="bullseyelotto.com")
    SocialApp(id=1, provider="google", name="Google",
              client_id="544071216198-84co67e8paq4pa74sst3u1nag54mrkup.apps.googleusercontent.com",
              secret="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", settings="{}").save()
    SocialApp.objects.get(id=1).sites.add(1)


def get_lottery_date_list(lottery_id):
    dates = []
    results = HistoryData.objects.annotate(
        balls_len=Length('balls')).filter(balls_len__gt=0,
        lottery=lottery_id).order_by("-date")

    for x in range(5):
        dates.append(results[x].date)

    dates.append(LotteryMetadata.objects.filter(id=lottery_id).first().next_result_date)

    return dates

@transaction.atomic
def seed_user_picks(lottery_list):
    for lottery in lottery_list:
        dates = get_lottery_date_list(lottery)

        metadata = LotteryMetadata.objects.filter(id=lottery).first()

        for date in dates:
            for x in range(5):
                balls_list = []
                while len(balls_list) < metadata.number_of_balls:
                    new_ball = random.randint(metadata.ball_min_value, metadata.ball_max_value)
                    if metadata.ball_allow_repeats or new_ball not in balls_list:
                        balls_list.append(new_ball)

                sballs_list = []
                while len(sballs_list) < metadata.number_of_special_balls:
                    new_ball = random.randint(metadata.special_ball_min_value, metadata.special_ball_max_value)
                    if metadata.special_ball_allow_repeats or new_ball not in sballs_list:
                        sballs_list.append(new_ball)

                if not metadata.ball_allow_repeats:
                    balls_list.sort()
                if not metadata.special_ball_allow_repeats:
                    sballs_list.sort()
                UserHistory(
                    user=CustomUser.objects.get(id=1),
                    lottery=LotteryMetadata.objects.get(id=lottery),
                    date=date,
                    balls=str(balls_list)[1:-1],
                    special_balls=str(sballs_list)[1:-1]
                ).save()


def index_fixes():
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [EmailAddress, SocialAccount, CustomUser])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(options['mode'])
        self.stdout.write('DONE... SUCCESS...')


def clear_data():
    UserHistory.objects.all().delete()
    LotteryStateMapper.objects.all().delete()
    UserFavorite.objects.all().delete()
    UserFavorite.objects.all().delete()
    CustomUser.objects.all().delete()
    SocialAccount.objects.all().delete()
    EmailAddress.objects.all().delete()
    HistoryData.objects.all().delete()
    LotteryMetadata.objects.all().delete()
    State.objects.all().delete()
    Country.objects.all().delete()
    ActiveState.objects.all().delete()
    """Deletes all the table data"""


def run_seed(mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """

    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    print("Seeding Active State")
    seed_active_state()
    print("Seeding Country")
    seed_country()
    print("Seeding State")
    seed_state()
    print("Seeding Lottery Metadata")
    seed_lottery_metadata()
    print("Seeding History Data")
    seed_lottery_history(135)
    seed_lottery_history(227)
    seed_lottery_history(383)
    seed_lottery_history(362)
    print("Seed Social Account Setup")
    seed_social_account_setup()
    print("Seeding User Accounts")
    seed_user_account_setup()
    print("Seeding User Favorites")
    seed_user_favorites([227,135,383])
    print("Seeding Lottery State Mapper")
    seed_lottery_state_mapper_metadata()
    print("Seeding User Picks")
    seed_user_picks([135,227,383])
    print("Index corrections")
    index_fixes()
