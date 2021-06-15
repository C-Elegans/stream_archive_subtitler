# Stream Archive Subtitler

This program generates subtitles from a text file with timestamps or json files from [chat_downloader](https://github.com/xenova/chat-downloader/). This can be used for instance to create an archive of a stream in another language that has a live translator providing translations in the chat. See [Translating a Stream] for how to do this

## Installation
To use this program, you will need to have Python 3, and pip installed. It is also recommended to install [youtube-dl](https://github.com/ytdl-org/youtube-dl) and optionally [chat_downloader](https://github.com/xenova/chat-downloader/) to archive your stream and download the chat respectively.

Installation is as follows:

1. Clone the repository by doing the following

	``` console
	git clone https://github.com/C-Elegans/stream_archive_subtitler.git

	```
	OR downloading the [zip](https://github.com/C-Elegans/stream_archive_subtitler/archive/refs/heads/master.zip) and unzipping it somewhere convenient

1. It is recommended to install the program under a python virtual environment, as this means the program and dependencies aren't installed globally on the system. The downside is you'll need to activate the environment to use the program
   - Create the environment by doing the following in a convenient folder:

   ``` console
   python -m venv .env
   ```
   - Activate the environment by doing the following:

   ``` console
   . .env/bin/activate
   ```
   - Deactivate the environment by typing `deactivate` into the terminal



## Translating a stream
