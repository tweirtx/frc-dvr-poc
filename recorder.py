import streamlink, tbapi, datetime
import getAPIKey, db
from time import sleep

tba = tbapi.TBAParser(api_key=getAPIKey.key.tba, cache=False)


class streamdb(db.DatabaseObject):
	__tablename__ = 'streamstarts'
	eventkey = db.Column(db.String)
	starttime = db.Column(db.String)
	primary_key = db.Column(db.Integer, primary_key=True, autoincrement=True)


db.DatabaseObject.metadata.create_all()
debug = True
if debug:
	eventkey = '2018txlu'
else:
	eventkey = input("Please enter the event key as it appears in TBA: ")
try:
	eventtba = tba.get_event(event_key=eventkey)
except tbapi.InvalidKeyError:
	raise ValueError('That event does not exist!')
webcast = eventtba.webcasts[0]
if debug:
	print(webcast)

stream = streamlink.Streamlink()


def logstart():
	with db.Session() as session:
		starting = streamdb(eventkey=eventkey, starttime='{}:{}:{}'.format(datetime.datetime.now().hour,
																		datetime.datetime.now().minute,
																		   datetime.datetime.now().second))
		session.add(starting)


def checkiflive():
	streams = stream.streams(url)
	try:
		streams['best']
		return True
	except KeyError:
		return False


def waituntillive():
	while True:
		is_live = checkiflive()
		if is_live:
			break
		print("Stream is not live yet, waiting 30 seconds and retrying")
		sleep(30)


if webcast.type == 'twitch':
	url = 'https://twitch.tv/{}'.format(webcast.channel)
elif webcast.type == 'dacast':
	print("Sorry, we can't work with this streaming provider due to required info being behind a paywall. Please bug FiM to stop using DaCast.")
	exit(0)
else:
	print("This event's stream is currently unsupported")
	exit()
if debug:
	url = 'https://twitch.tv/tweirtx' # Debug only, remove before production use!

waituntillive()
print("Now live!")
streams = stream.streams(url)
stream_file = streams['best'].open()
with open('{}.mp4'.format(eventkey), 'wb') as f:
	while True:
		f.write(stream_file.read(1024))
		# if not checkiflive():
		# 	break
