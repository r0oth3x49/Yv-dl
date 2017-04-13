## Yv-dl
Yv-dl is a python based Youtube Audio, Video, Playlist downloader and live streamer for Youtube Audio and Video and now supports downloading vidoes from **vimeo.com** and you can also provide a file containing links of videos or playlist (both should be kept in separate file.txt). It uses Python modules Youtube-dl, pafy for downloading and livestreamer for live streaming video and audio and vimeo_dl for downloading videos from vimeo.com.

[![youtube.png](https://s28.postimg.org/n9z05fh65/youtube.png)](https://postimg.org/image/6m7i2xmeh/)

**Requirements**
- Python27
- python-pip
- VideoLAN (VLC) player (for live streaming (youtube only))
	 
**Tested on**
- Windows 7/8
- Kali linux (2.0) (tested with root user)
- Ubuntu 14.04.4 LTS
	 
**Installation**
You can download the latest version of YTube-Downloader by cloning the GitHub repository.

	git clone https://github.com/r0oth3x49/Yv-dl.git

<pre><code>
Author: Nasir khan (<a href="http://r0oth3x49.herokuapp.com/">r0ot h3x49</a>)
Options:
  General Options:
    -h, --help        Print this help text and exit
    -v, --version     Print program version and exit

  Downloader options:
    -a, --best-audio  Download best available audio
    -b, --best-video  Download best available resolution
    -l, --list        list available download streams
    -n, --stream-no   Download specific video by stream no. (prog -n 2 URL)
    -f, --file        Download videos/playlists by proving file (e.g :- prog -b/--yes-palylist -f file.txt).

  Playlist options:
    --yes-playlist    Allow downloading playlist completely
    --no-playlist     Only download specific video available in a playlist
    --start-playlist  Specify playlist start. (prog --start-playlist 2 URL)
    --end-playlist    Specify playlist end. (prog --end-playlist 23 URL)

  Live streaming options:
    --video-stream    Live streaming of video on vlc player
    --audio-stream    Live streaming of audio on vlc player
    --best-stream     Best video (720p) streaming
 
 </code></pre>
 
**Downloading Using File option**
For videos downloading from file

	python Yv-dl.py -b -f VIDEOS_FILENAME.txt

For playlist downloading from file

	python Yv-dl.py --yes-playlist -f PLAYLIST_FILENAME.txt

**Listing all formats**

	python Yv-dl.py -l https://www.youtube.com/watch?v=6TPcwWHZN_0

**Downloading best video**

	python Yv-dl.py -b https://www.youtube.com/watch?v=6TPcwWHZN_0
	
**Downloading best audio**

	python Yv-dl.py -a https://www.youtube.com/watch?v=6TPcwWHZN_0
	
**Downloading playlist**
````
Downloading the whole playlist:
	python Yv-dl.py --yes-playlist https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S

Downloading the playlist by specifying starting number:
	python Yv-dl.py --start-playlist 10 https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S
	
Downloading the playlist by specifying ending number:
	python Yv-dl.py --start-playlist 10 https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S

Downloading only the current indexed video in a playlist:
	python Yv-dl.py --no-playlist "https://www.youtube.com/watch?v=BadQWJW7yk4&list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S&index=42"
````


**Live streaming**

````
Audio streaming:
   python Yv-dl.py --audio-stream https://www.youtube.com/watch?v=6TPcwWHZN_0
	
Video streaming:
   python Yv-dl.py --video-stream https://www.youtube.com/watch?v=6TPcwWHZN_0
	
Best video streaming:
   python Yv-dl.py --best-stream https://www.youtube.com/watch?v=6TPcwWHZN_0
   
````

**Note**

	1.	To stream audio video live Yv-Downloader uses python module "livestreamer" which by default it checks if it is installed or not, if not it will try to install if Yv-dl gets failed try manually for live streaming.
	2.	VideoLAN (VLC) player must be there in your machine.
	3.	if you are downloading the playlist that starts from any indexed video that ur must be used with in the double 	quotes (e.g:- "URL")
	
