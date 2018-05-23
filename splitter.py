import datetime, tbapy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import getAPIKey, db
from recorder import streamdb

tbap = tbapy.TBA(getAPIKey.Key.tba)


def get_start_time(event, day):
    with db.Session as session:
        start_time_db_result = session.query(streamdb).filter_by(eventkey=event, day=day).one_or_none()
        return start_time_db_result.starttime


def splitter(day, streamtime, i):
    matchtimestamp = i.actual_time + datetime.timezone.utcoffset()
    starttime = matchtimestamp - streamtime
    endtime = starttime + 180
    ffmpeg_extract_subclip('{}.mp4'.format(day), starttime, endtime, '{}.mp4'.format(i.key))


def split(event):
    matches = tbap.event_matches(event)
    for i in matches:
        try:
            open('{}.mp4'.format(i.key))
            print('{} already exists'.format(i.key))
            already_exists = True
        except FileNotFoundError:
            print("{} does not already exist".format(i.key))
            already_exists = False
        day = datetime.datetime.fromtimestamp(i.actual_time).weekday()
        time = get_start_time(event, day)
        if i.actual_time and not already_exists:
                splitter(day, time, i)
