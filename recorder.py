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

if webcast.type == 'twitch':
	url = 'https://twitch.tv/{}'.format(webcast.channel)
	with db.Session() as session:
		starting = streamdb(eventkey=eventkey, starttime='{}:{}:{}'.format(datetime.datetime.now().hour,
																		datetime.datetime.now().minute,
																		   datetime.datetime.now().second))
		session.add(starting)

	def checkiflive():
		print('do some twitch api stuff to see if they\'re live')
		return True

	def waituntillive():
		while True:
			print("Stream is not live yet, waiting 30 seconds and retrying")
			sleep(30)
			is_live = checkiflive()
			if is_live:
				break

else:
	print("This event's stream is currently unsupported")
	exit()
if debug:
	url = 'https://twitch.tv/tweirtx' # Debug only, remove before production use!
waituntillive()
stream = streamlink.Streamlink()
streams = stream.streams(url)
stream_file = streams['best'].open()
with open('{}.mp4'.format(eventkey), 'wb') as f:
	while True:
		f.write(stream_file.read(1024))
		is_live = checkiflive()
		if not is_live:
			break

