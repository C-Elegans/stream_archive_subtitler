# Stream Archive Subtitler

This program generates subtitles from a text file with timestamps or json files from [chat_downloader](https://github.com/xenova/chat-downloader/). This can be used for instance to create an archive of a stream in another language that has a live translator providing translations in the chat. See [Usage](#usage) for how to do this

## Installation
To use this program, you will need to have Python 3 and pip installed. It is also recommended to install [youtube-dl](https://github.com/ytdl-org/youtube-dl), [ffmpeg](https://ffmpeg.org/), and optionally [chat_downloader](https://github.com/xenova/chat-downloader/) to archive your stream and download the chat respectively.

Installation is as follows:

#### Recommended - Pip

Install via pip

Run the following in the terminal:

``` console
pip install stream_archive_subtitle
stream_archive_subtitle -h
```

#### Alternative - Build from source

1. Clone the repository by doing the following

	``` console
	$ git clone https://github.com/C-Elegans/stream_archive_subtitler.git

	```
	OR by downloading the [zip](https://github.com/C-Elegans/stream_archive_subtitler/archive/refs/heads/master.zip) and unzipping it somewhere convenient

	Note: using `git` is recommended as it makes updating easier

1. It is recommended to install the program under a python virtual environment, as this means the program and dependencies aren't installed globally on the system. The downside is you'll need to activate the environment to use the program
   - Create the environment by doing the following in a convenient folder:

   ``` console
   $ python -m venv .env
   ```
   Note: depending on the age of your system, you may need to replace `python` with `python3`
   - Activate the environment by doing the following:

   ``` console
   $ . .env/bin/activate
   ```
   - Deactivate the environment by typing `deactivate` into the terminal

1. Install the program's dependencies by doing the following:

   ``` console
   $ pip install -e .
   ```
   Note: depending on the age of your system, you may need to replace `pip` with `pip3`
1. Install the program by doing the following:

   ``` console
   $ python setup.py install
   ```
   Note: depending on the age of your system, you may need to replace `python` with `python3`
1. Test that the program has been installed correctly by running the following:

   ``` console
   $ stream_archive_subtitle -h
   ```
   It should output something like this:

   ```
   usage: stream_archive_subtitle [-h] -o OUTPUT [-t TRANSLATOR_FILTER] [-s START] files [files ...]

   Create a subtitle .srt file from korotagger or chat_downloader output

   positional arguments:
     files                 The korotagger or chat_downloader files to parse

   optional arguments:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
   						The subtitle file to write to
     -t TRANSLATOR_FILTER, --translator-filter TRANSLATOR_FILTER
   						A regex to filter out translator messages (default: "\[[eE][nN]\]")
     -s START, --start START
   						Timestamp to control when the subtitles start from for archives that start in the middle of a stream
   						(default: 00:00:00)
   ```

## Usage

### Downloading a stream

If the stream you want to download is public, and assuming you have `youtube-dl` installed, all you need to do is:

``` console
$ youtube-dl 'https://youtube.com/whatever-your-stream-url-is'
```

However, if the stream is members-only, downloading the stream is a little more complicated. For full instructions see [this pastebin](https://pastebin.com/YkTzVNUK)

### Subtitling a Stream with Korotagger or a text file
Some live translators type their translations in discord, and use a bot like KoroTagger to collect their translations a couple of messages on discord. The messages look something like this:

```
some translated text here 1m50s
more translated text  2m10s
a long time later there's some more translated text here 1h32m10s
```

You can of course also manually create a text file like this if you want to manually subtitle a video.

To use this type of translation with this tool, copy and paste the discord messages into a file with the extension `.txt` such as `stream_translation.txt`.

Next run the tool like so:

``` console
$ stream_archive_subtitle -o subtitlefile.srt your_txt_file_here.txt

```

It will create a subtitle `.srt` file with a subtitle for each line in the text file. The `.srt` file can be used with ffmpeg as shown in [Adding Subtitles to a Video](#adding-subtitles-to-a-video)

By default, Korotagger subtracts 20 seconds from the tag timestamp, so that when you click the link in the tag output, you'll jump to the stream archive 20s before the event in question actually happens. This is great for using the tag output to find where in the stream something interesting happened, but not so good for subtitling. 

This tool by default will add 20s to Korotagger time stamps to make them line up better with what is actually happening in the stream. To change this, pass the `-k` flag and your desired offset time to the tool like so:

``` console
$ stream_archive_subtitle -o subtitlefile.srt -k 00:00:45 korotagger_file.txt
```

### Subtitling a Stream with chat_downloader

Some live translators will provide translations directly in stream chat, prefixed with a tag like "[EN]" or "[ru]" or similar. This stream chat can be downloaded using [chat_downloader](https://github.com/xenova/chat-downloader/) by doing the following:

``` console
$ chat_downloader -o filename.json 'https://youtube.com/the-stream-url'
```

If your stream is a members' only one, you'll need to follow the procedure in [Downloading a Stream](#downloading-a-stream) to get the cookies.txt file, and pass it to `chat_downloader` like you did with `youtube-dl`:
``` console
$ chat_downloader -c cookies.txt -o filename.json 'https://youtube.com/the-stream-url'
```

Be patient, it takes a while, particularly if chat is particularly active

Once you have this `.json` file downloaded, generate the subtitle file by:
``` console
$ stream_archive_subtitle -o subtitlefile.srt your_txt_file_here.json

```

Note, since `stream_archive_subtitle` needs to filter needs to filter out only live translation comments for the subtitles to be properly generated. By default it looks for the regex "\[[eE][nN]\]" which will match the following tags: "[EN]", "[En]", "[eN]", and "[en]". If the tags in your stream look different (either because you want a different language or your live translator uses a different tag), you'll need to change the regular expression like so:

``` console
$ stream_archive_subtitle -o subtitlefile.srt --translator-filter '\[[rR][uU]\]' your_txt_file_here.json

```

In this case I changed it to match all of the RU tags instead of EN.

Note also that if you have both KoroTagger and chat_downloader translations and you want to combine them, just pass both files to the tool like so:

``` console
$ stream_archive_subtitle -o subtitlefile.srt chat_downloader_output.json korotagger_output.txt

```

It will automatically sort the subtitles by timestamp, giving you translations from both files at the appropriate times.

### Subtitling a Stream with a Luna's Translations log file

There is a Discord bot called "Luna's Translations" that can automatically capture all of the live translations in the stream chat. At the end of the stream, the bot will collate all of the live translations it captured into a log file that can be downloaded. These log filed can be used with this tool to provide subtitles as an alternative to downloading the chat with chat_downloader (if for instance, the live chat is turned off in the archive).

1. First download the translation log from the bot, and change the file extension from `.txt` to `.log` (this is important, as otherwise this tool will think the file is a KoroTagger file).

2. Pass the log file to this tool like so:

``` console
$ stream_archive_subtitle -o subtitlefile.srt luna_translation_file.log
```

Note: just like with chat_downloader, you can provide both a Luna's translations `.log` file and a Korotagger `.txt` file and the tool will automatically sort the subtitles by timestamp, giving you translations from both files.

### Adding subtitles to a video

Once you have a video downloaded and a subtitle `.srt` file generated, you can add the subtitles to the video like so:

``` console
$ ffmpeg -i videofile.mov -i subtitles.srt -c copy -c:s mov_text videofile_out.mp4
```

If you have an archive downloaded that starts partway through the stream (say you started your download of a live stream a little late, or you downloaded only the second half of a youtube stream archive), and you still want subtitles, you will need to tell `stream_archive_subtitle` when your video started relative to the source video for the subtitles to line up. For instance, say I have an archive that starts 31 minutes and 53 seconds after the streamer began streaming. I would then pass an extra parameter `-s 00:31:53` to `stream_archive_subtitle` like so:

``` console
$ stream_archive_subtitle -s 00:31:53 -o subtitlefile.srt chat_downloader_output.json

```

The generated file can then be used to subtitle your video using `ffmpeg` as above.
