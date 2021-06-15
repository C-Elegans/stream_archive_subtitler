# Stream Archive Subtitler

This program generates subtitles from a text file with timestamps or json files from [chat_downloader](https://github.com/xenova/chat-downloader/). This can be used for instance to create an archive of a stream in another language that has a live translator providing translations in the chat. See [Usage](#usage) for how to do this

## Installation
To use this program, you will need to have Python 3, and pip installed. It is also recommended to install [youtube-dl](https://github.com/ytdl-org/youtube-dl) and optionally [chat_downloader](https://github.com/xenova/chat-downloader/) to archive your stream and download the chat respectively.

Installation is as follows:

1. Clone the repository by doing the following

	``` console
	$ git clone https://github.com/C-Elegans/stream_archive_subtitler.git

	```
	OR downloading the [zip](https://github.com/C-Elegans/stream_archive_subtitler/archive/refs/heads/master.zip) and unzipping it somewhere convenient

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

It will create a subtitle `.srt` file with a subtitle for each line in the text file. The `.srt` file can be used with ffmpeg as shown in (#adding-subtitles-to-a-video)

### Subtitling a Stream with chat_downloader


### Adding subtitles to a video
