#!/usr/bin/python
""" !/home/yo/.virtualenvs/sacrebleu/bin/python """
from sacrecommon import post_video, post_to_wall
from moviecommon import push_video, render_video
from cloudsmovement import last_hour_plot
from sunsetplotter import brightness_plot
import time
import os

# Find newest dir (hopefuly with photos)
dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]
newest = max(dirs, key = os.path.getmtime)

# Upload to Youtube
render_video(newest)
video_id = push_video(newest)

# Publish with current date as a message
message = '_' + time.strftime('%d %B %Y, %H:%M') 
post_video(video_id, message)

# Movement detection whole day plot
plotname = last_hour_plot(newest, hour_only = False)
post_to_wall(plotname, ' ')
os.remove(plotname)

# Brightness plot
suntrace = brightness_plot(newest)
post_to_wall(suntrace, ' ')
os.remove(suntrace)
