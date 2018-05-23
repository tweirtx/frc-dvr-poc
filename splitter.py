import tbapi, datetime, tbapy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

tba = tbapi.TBAParser(api_key='5nxF8pYtXPy1rZELO68JhjwYZuJRkojuPNDUuEAXyysRn8A6SfL1GaAvbYskU6rj', cache=False)

tbap = tbapy.TBA('5nxF8pYtXPy1rZELO68JhjwYZuJRkojuPNDUuEAXyysRn8A6SfL1GaAvbYskU6rj')


def splitter(day, streamtime, i):
    matchtimestamp = i.actual_time + datetime.timezone.utcoffset()
    starttime = matchtimestamp - streamtime
    endtime = starttime + 180
    ffmpeg_extract_subclip('{}.mp4'.format(day), starttime, endtime, '{}.mp4'.format(i.key))


matches = tbap.event_matches('2018txsa')
for i in matches:
    print(i.actual_time < 1523077200)
    try:
        open('{}.mp4'.format(i.key))
        print('{} already exists'.format(i.key))
        already_exists = True
    except FileNotFoundError:
        print("{} does not already exist".format(i.key))
        already_exists = False
    if i.actual_time < 1523077200:
        day = 'friday'
        time = tw.videos.get_by_id(247255213)['created_at'].timestamp()
        if i.actual_time and not already_exists:
            splitter(day, time, i)
    else:
        day = 'saturday'
        time = tw.videos.get_by_id(247649045)['created_at'].timestamp()
        if i.actual_time and not already_exists:
            splitter(day, time, i)
