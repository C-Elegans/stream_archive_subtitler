import srt
import time
from datetime import datetime, timedelta
import re

txt_file='minecraft_stream.txt'
time_initial = datetime.strptime("00:00:00", "%H:%M:%S")
video_offset='0:0:0'
video_offset_time=datetime.strptime(video_offset, "%H:%M:%S")
video_offset_time-=time_initial # convert to time delta


def parse_korotagger_txt(input_file):
    # Read in all of the lines from the text file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Korotagger outputs tags in the form of "tag text timestamp"
    # where timestamp can look like any of: "37s", "10m5s", or
    # "1h27m55s"

    # This regex parses out the tag field as well as the hours minutes and seconds fields
    time_regex = re.compile(r'^(.*) (([0-9]+)h)?(([0-9]+)m)?(([0-9]+)s)$')

    subtitle_lines = []

    for line in lines:
        # Remove the ending newline
        line = line.strip()

        # Try to match against the regex above
        match = time_regex.search(line)
        # If it doesn't match, we can't use this as a subtitle
        if not match:
            continue

        # Extract out the different fields from the regex match result
        text = match.group(1)
        hours = int(match.group(3) or '0')
        minutes = int(match.group(5) or '0')
        seconds = int(match.group(7) or '0')

        # Convert the hours minutes and seconds into a timedelta object
        time_delta = timedelta(seconds=seconds, minutes=minutes, hours=hours)    
        # Subtract the time delta from the start time of the video
        time_delta -= video_offset_time
        # print(f'{time_delta}: {text}')
        # Discard a subtitle if it has a negative time value
        if time_delta.total_seconds() < 0:
            continue
        # Append it to the array
        subtitle_lines.append((time_delta, text))
    return subtitle_lines

def convert_subtitles(subtitle_lines):
    # fix lines not being in chronological order in the file
    subtitle_lines = sorted(subtitle_lines, key=lambda x: x[0])

    subs = []
    for subtitle, next_subtitle in zip(subtitle_lines, subtitle_lines[1:]):
        sub = srt.Subtitle(index=1, start=subtitle[0], end=next_subtitle[0], content=subtitle[1])
        subs.append(sub)
    # Fix the above not including the last subtitle because we're
    # iterating over the current and next subtitle
    last_sub = subtitle_lines[-1]
    subs.append(srt.Subtitle(index=1, start=last_sub[0], end=timedelta(seconds=59, minutes=59, hours=23, days=6), content=last_sub[1]))
    return subs

def write_subs_to_file(subs, output_file):
    data = srt.compose(subs, reindex=True)
    with open(output_file, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    sub_data = parse_korotagger_txt('minecraft_stream.txt')
    subs = convert_subtitles(sub_data)
    write_subs_to_file(subs, 'subtitles.srt')
    
