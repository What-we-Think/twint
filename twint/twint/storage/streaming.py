import datetime, pandas as pd, warnings
from time import strftime, localtime
from twint.tweet import Tweet_formats
import json
import requests

weekdays = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
        }

_type = ""
def stream(object, config):
    global _type

    if object.__class__.__name__ == "tweet":
        _type = "tweet"
    elif object.__class__.__name__ == "user":
        _type = "user"
    elif object.__class__.__name__ == "dict":
        _type = config.Following*"following" + config.Followers*"followers"

    if _type == "tweet":
        Tweet = object
        datetime_ms = datetime.datetime.strptime(Tweet.datetime, Tweet_formats['datetime']).timestamp() * 1000
        day = weekdays[strftime("%A", localtime(datetime_ms/1000))]
        dt = f"{object.datestamp} {object.timestamp}"
        if not config.mini:
            _data = {
                "id": str(Tweet.id),
                "conversation_id": Tweet.conversation_id,
                "created_at": datetime_ms,
                "date": dt,
                "timezone": Tweet.timezone,
                "place": Tweet.place,
                "tweet": Tweet.tweet,
                "language": Tweet.lang,
                "hashtags": Tweet.hashtags,
                "cashtags": Tweet.cashtags,
                "user_id": Tweet.user_id,
                "user_id_str": Tweet.user_id_str,
                "username": Tweet.username,
                "name": Tweet.name,
                "day": day,
                "hour": strftime("%H", localtime(datetime_ms/1000)),
                "link": Tweet.link,
                "urls": Tweet.urls,
                "photos": Tweet.photos,
                "video": Tweet.video,
                "thumbnail": Tweet.thumbnail,
                "retweet": Tweet.retweet,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "quote_url": Tweet.quote_url,
                "search": str(config.Search),
                "near": Tweet.near,
                "geo": Tweet.geo,
                "source": Tweet.source,
                "user_rt_id": Tweet.user_rt_id,
                "user_rt": Tweet.user_rt,
                "retweet_id": Tweet.retweet_id,
                "reply_to": Tweet.reply_to,
                "retweet_date": Tweet.retweet_date,
                "translate": Tweet.translate,
                "trans_src": Tweet.trans_src,
                "trans_dest": Tweet.trans_dest
                }
        else:
            _data = {
                "tweet":Tweet.tweet,
                "hashtags":Tweet.hashtags,
                "language":Tweet.lang,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "is_retweet": Tweet.retweet,
            }
        req = requests.post(url=config.url,data=json.dumps(_data))
    elif _type == "user":
        user = object
        try:
            background_image = user.background_image
        except:
            background_image = ""
        if not config.mini:
            _data = {
                "id": str(Tweet.id),
                "conversation_id": Tweet.conversation_id,
                "created_at": datetime_ms,
                "date": dt,
                "timezone": Tweet.timezone,
                "place": Tweet.place,
                "tweet": Tweet.tweet,
                "language": Tweet.lang,
                "hashtags": Tweet.hashtags,
                "cashtags": Tweet.cashtags,
                "user_id": Tweet.user_id,
                "user_id_str": Tweet.user_id_str,
                "username": Tweet.username,
                "name": Tweet.name,
                "day": day,
                "hour": strftime("%H", localtime(datetime_ms/1000)),
                "link": Tweet.link,
                "urls": Tweet.urls,
                "photos": Tweet.photos,
                "video": Tweet.video,
                "thumbnail": Tweet.thumbnail,
                "retweet": Tweet.retweet,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "quote_url": Tweet.quote_url,
                "search": str(config.Search),
                "near": Tweet.near,
                "geo": Tweet.geo,
                "source": Tweet.source,
                "user_rt_id": Tweet.user_rt_id,
                "user_rt": Tweet.user_rt,
                "retweet_id": Tweet.retweet_id,
                "reply_to": Tweet.reply_to,
                "retweet_date": Tweet.retweet_date,
                "translate": Tweet.translate,
                "trans_src": Tweet.trans_src,
                "trans_dest": Tweet.trans_dest
                }
        else:
            _data = {
                "tweet":Tweet.tweet,
                "hashtags":Tweet.hashtags,
                "language":Tweet.lang,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "is_retweet": Tweet.retweet,
            }
        requests.post(url=config.url,data=json.dumps(_data))
    elif _type == "followers" or _type == "following":
        _data = {
            config.Following*"following" + config.Followers*"followers" :
                             {config.Username: object[_type]}
        }
        requests.post(url=config.url,data=json.dumps(_data))
    else:
        print("Wrong type of object passed!")