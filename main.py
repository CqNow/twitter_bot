import tweepy
from dhooks import Webhook, Embed
from googletrans import Translator
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
hook = Webhook(url=config['Twitter']['discord_url_webhook'], username=config['Twitter']['twitter_name'],
               avatar_url="https://assets.primagames.com/media/files/true-colors-emblem-destiny-2.jpg")

class Listener(tweepy.Stream):

    def on_status(self, status):
        if from_creator(status):
            if hasattr(status, "extended_tweet"):
                tweet_text = status.extended_tweet['full_text']
            else:
                tweet_text = status.text
        URL_tweet = f'https://twitter.com/{config["Twitter"]["twitter_name"]}/status/' + status.id_str
        embed = create_embed(trans(tweet_text))
        hook.send(URL_tweet)
        hook.send(embed=embed)

def authentication():
    CONSUMER_KEY = config['Twitter']['consumer_key']
    CONSUMER_SECRET = config['Twitter']['consumer_secret']
    ACCESS_TOKEN = config['Twitter']['access_token']
    ACCESS_SECRET_TOKEN = config['Twitter']['access_secret_token']
	
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    api = tweepy.API(auth)
    USER_ID = api.get_user(screen_name=config['Twitter']['twitter_name']).id
    stream_tweet = Listener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    stream_tweet.filter(follow=[USER_ID])

def trans(origin_text):
    return Translator().translate(origin_text, dest="ru", src="en").text

def create_embed(translated_text):
    embed = Embed(description=translated_text,
                  color=0xFF0000,
                  timestamp="now")
    embed.set_author(name="Embed name")
    embed.add_field(name="Field name 1")
    embed.add_field(name="Field name 2")
    return embed

def from_creator(status):
    if hasattr(status, "retweeted_status"):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def main():
    authentication()

if __name__ == '__main__':
    main()