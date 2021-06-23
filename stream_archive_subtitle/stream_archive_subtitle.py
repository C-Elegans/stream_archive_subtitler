import srt
import time
from datetime import datetime, timedelta
import re
import json
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description='Create a subtitle .srt file from korotagger or chat_downloader output')
    parser.add_argument('files', nargs='+', help='The korotagger or chat_downloader files to parse')
    parser.add_argument('-o', '--output', required=True, help='The subtitle file to write to')
    parser.add_argument('-t', '--translator-filter', help='A regex to filter out translator messages (default: "%(default)s")', default='\\[[eE][nN]\\]')
    parser.add_argument('-s', '--start', default='00:00:00', help='Timestamp to control when the subtitles start from for archives that start in the middle of a stream (default: %(default)s)')
    parser.add_argument('-k', '--korotagger-offset', default='00:00:20', help='Korotagger default tag offset (default: %(default)s)')
    parser.add_argument('--spread', type=int, default=7, help='Amount to spread out subtitles by (default: %(default)s)')
    return parser.parse_args()




def parse_korotagger_txt(input_file, video_offset_time, korotagger_offset_time):
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

        # Add an offset to correct for KoroTagger placing the tag
        # timestamps ~20s ahead of when the event actually occurs
        time_delta += korotagger_offset_time
        # print(f'{time_delta}: {text}')
        # Discard a subtitle if it has a negative time value
        if time_delta.total_seconds() < 0:
            continue
        # Append it to the array
        subtitle_lines.append((time_delta, text))
    return subtitle_lines

def parse_json(json_file, video_offset_time, translator_filter):
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    subtitle_lines = []
    for item in json_data:
        # Filter out all non-chat things
        if item['action_type'] != 'add_chat_item':
            continue
        # Extract the message from the JSON
        message = item['message']
        match = translator_filter.match(message)
        # if the message does not match the translator filter, skip it
        if not match:
            continue

        message = translator_filter.sub('', message).strip().lstrip()
        # Extract the message timestamp
        time_secs = item['time_in_seconds']
        # Convert to time delta
        time_delta = timedelta(seconds=time_secs)    
        # Subtract off the video start time offset
        time_delta -= video_offset_time
        # If the message came before the video offset, discard it
        if time_delta.total_seconds() < 0:
            continue
        # print(message, time_delta)
        # Append it to the array
        subtitle_lines.append((time_delta, message))
    return subtitle_lines

def parse_luna(luna_log_file, video_offset_time, time_initial):
    # Read in all of the lines from the text file
    with open(luna_log_file, 'r') as f:
        lines = f.readlines()

    subtitle_lines = []

    sub_regex = re.compile('^(\d+:\d+:\d+)\s+\(\w+\)\s+\[\w\w\]\s+(.*)$')

    for line in lines:
        match = sub_regex.search(line)
        if not match:
            continue
        time_str = match.group(1)
        message = match.group(2)
        time = datetime.strptime(time_str, "%H:%M:%S")
        time -= time_initial
        time -= video_offset_time
        if time.total_seconds() < 0:
            continue

        subtitle_lines.append((time, message))
    
    return subtitle_lines

def convert_subtitles(subtitle_lines):
    # fix lines not being in chronological order in the file

    subs = []
    for subtitle, next_subtitle in zip(subtitle_lines, subtitle_lines[1:]):
        sub = srt.Subtitle(index=1, start=subtitle[0], end=next_subtitle[0], content=subtitle[1])
        subs.append(sub)
    # Fix the above not including the last subtitle because we're
    # iterating over the current and next subtitle
    last_sub = subtitle_lines[-1]
    subs.append(srt.Subtitle(index=1, start=last_sub[0], end=timedelta(seconds=59, minutes=59, hours=23, days=6), content=last_sub[1]))
    return subs

def spread_out_subs(subtitle_lines, spread_out_factor):
    last_timestamp = timedelta(seconds=-10)
    new_subtitles = []
    for line in subtitle_lines:
        cur_timestamp = line[0]
        text = line[1]
        if (cur_timestamp - last_timestamp).total_seconds() < spread_out_factor:
            cur_timestamp = last_timestamp + timedelta(seconds=spread_out_factor)
            print(f'spreading {line[1]} from {line[0]} to {cur_timestamp}')

        new_subtitles.append((cur_timestamp, text))
        last_timestamp = cur_timestamp
    return new_subtitles

    

def write_subs_to_file(subs, output_file):
    data = srt.compose(subs, reindex=True)
    with open(output_file, 'w') as f:
        f.write(data)


def main():
    args = parse_args()
    print(args)
    time_initial = datetime.strptime("00:00:00", "%H:%M:%S")
    video_offset_time=datetime.strptime(args.start, "%H:%M:%S")
    video_offset_time-=time_initial # convert to time delta
    korotagger_offset_time = datetime.strptime(args.korotagger_offset, "%H:%M:%S")
    korotagger_offset_time -= time_initial # convert to time delta

    translator_filter = re.compile(args.translator_filter)
    sub_data = []
    for name in args.files:
        extension = os.path.splitext(name)[1]
        if extension == '.txt':
            koro_subs = parse_korotagger_txt(name, video_offset_time, korotagger_offset_time)
            print(f'Generated {len(koro_subs)} subtitles from korotagger txt')
            sub_data.extend(koro_subs)
        elif extension == '.json':
            chat_subs = parse_json(name, video_offset_time, translator_filter)
            print(f'Generated {len(chat_subs)} subtitles from chat json')
            sub_data.extend(chat_subs)
        elif extension == '.log':
            luna_subs = parse_luna(name, video_offset_time, time_initial)
            print(f'Generated {len(luna_subs)} subtitles from Luna log')
            sub_data.extend(luna_subs)

    sub_data = sorted(sub_data, key=lambda x: x[0])

    sub_data = spread_out_subs(sub_data, args.spread)
            
    if sub_data:
        subs = convert_subtitles(sub_data)
        write_subs_to_file(subs, args.output)
    

if __name__ == '__main__':
    main()
