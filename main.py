import tweepy
from dhooks import Webhook, Embed
from googletrans import Translator
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
hook = Webhook(url=config['Twitter']['discord_url_webhook'], username=config['Twitter']['twitter_name'], avatar_url="https://assets.primagames.com/media/files/true-colors-emblem-destiny-2.jpg")

class Listener(tweepy.Stream):

	def on_status(self, status):
		hook.send(status.text)

def authentication(config):
	CONSUMER_KEY = config['Twitter']['consumer_key']
	CONSUMER_SECRET = config['Twitter']['consumer_secret']
	ACCESS_TOKEN = config['Twitter']['access_token']
	ACCESS_SECRET_TOKEN = config['Twitter']['access_secret_token']
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
	api = tweepy.API(auth)
	USER_ID = api.get_user(screen_name=config['Twitter']['twitter_name']).id
	stream_tweet = Listener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
	stream_tweet.filter(follow=[USER_ID])


def main():
	authentication(config)

if __name__ == '__main__':
	main()