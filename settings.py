import os
from typing import NamedTuple


from dotenv import find_dotenv, load_dotenv
from requests.models import HTTPError

load_dotenv(find_dotenv())

# Paths
BOT_DIR = os.path.dirname(__file__)
# PROJECT_ROOT = os.path.abspath(os.path.join(BOT_DIR, os.pardir)) /var


class API(NamedTuple):
    # Change to API Hosts Possibly
    static_host = os.environ.get('STATIC_HOST')
    flask_host = os.environ.get('FLASK_HOST')

    # Not a Setting, Needs Moved
    @classmethod
    def character(cls, name: str):
        try:
            return f'{cls.static_host}/character/Portrait_{name}.png'
        except HTTPError:
            return f'{cls.static_host}/character/Portrait_default.png'


# print(API.character('Venom'))

class Category(NamedTuple):
    character = "Character"
    general = "General"
    roster = "Roster"
    team = "Team"


class Client(NamedTuple):
    name = os.environ.get("NAME")
    guild = int(os.environ.get("BOT_GUILD"))
    prefix = os.environ.get("PREFIX")
    token = os.environ.get("BOT_TOKEN")
    debug = os.environ.get("DEBUG") == "TRUE"
    github_bot_repo = os.environ.get("GITHUB_BOT_REPO")
    log_channel = os.environ.get("LOG_CHANNEL")
    log_owner = os.environ.get("LOG_OWNER")


class Mongo(NamedTuple):
    mode = os.environ.get("MONGO_MODE")
    user = os.environ.get("MONGO_USER")
    passwd = os.environ.get("MONGO_PASSWD")
    host = os.environ.get("MONGO_HOST")
    db = os.environ.get("MONGO_DB")
    header = os.environ.get("MONGO_HEADER")
    uri = f'{mode}://{user}:{passwd}@{host}/{db}?{header}'


class Mysql(NamedTuple):
    host = os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQL_USER")
    db = os.environ.get("MYSQL_DB")
    passwd = os.environ.get("MYSQL_PASSWD")


class Msfgg (NamedTuple):
    key = os.environ.get("MSFGG_KEY")


class Filters(NamedTuple):
    roster = ['ros', 'rost', 'ro']
    favorite = ['favor', 'favorite', 'fa']
    gear = ['gear', 'gt', 'tier', 'gl']
    iso8 = ['iso8', 'is', 'i8']
    level = ['lv', 'level', 'lev']
    power = ['po', 'pwr', 'pow']
    redstar = ['red', 'rds', 'reds']
    t4 = ['tier4', 'or', 'ora', 'orange']
    trait = ['tra', 'trt', 'tt']
    yellowstar = ['yel', 'star', 'yellow']


TAGLINES = ['pay attention', 'pay close attention', 'take heed', 'listen to me', 'listen', 'heed', 'listen crefully', 'good listener', 'hear', 'lend an ear', 'hearing', 'watch closely', 'heard', 'great listener', 'look', 'turn your attention', 'pays any attention', 'your attention', 'call your attention', 'hear me out', 'watch', 'give your attendance', 'keep an eye on', 'give heed', 'notice', 'you listen well',
            'direct your attention', 'just pay attention', 'mark my words', 'attention', 'play', 'obey', 'listening', 'watch out', 'give ear to me', 'be careful', 'draw attention', 'draw your attention', 'bring to your attention', 'get an earful', 'draw to your attention', 'please pay attention', 'note', 'paying attention', 'you need to listen to me', 'excellent listener', 'i need to point out', 'they listened', 'just hear', 'just listen']
