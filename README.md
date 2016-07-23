## YTube-Downloader
<p>YTube-Downloader is a python based Youtube Audio, Video, Playlist downloader and live streamer for Youtube Audio and Video. It used Python modules Youtube-dl, pafy for downloading and livestreamer for live streaming video and audio</p>
**Requirements**<br />
	 Python27
	 
**Tested on**<br />
	 Windows 7/8<br />
	 Kali linux (2.0)
**Installation**
<p>You can download the latest version of YTube-Downloader by cloning the GitHub repository:</p>
<pre><code>git clone https://github.com/r0oth3x49/YTube-Downloader.git</pre></code>
<pre><code>
Author: Nasir khan (<a href="http://anonpakforce.blogspot.com/">r0ot h3x49</a>)
Options:
  General Options:
    -h, --help        Print this help text and exit
    -v, --version     Print program version and exit

  Downloader options:
    -a, --best-audio  Download best available audio
    -b, --best-video  Download best available resolution
    -l, --list        list available download streams
    -n, --stream-no   Download specific video by stream no. (prog -n 2 URL)

  Playlist options:
    --yes-playlist    Allow downloading playlist completely
    --no-playlist     Only download specific video available in a playlist
    --start-playlist  Specify playlist start. (prog --start-playlist 2 URL)
    --end-playlist    Specify playlist end. (prog --end-playlist 23 URL)

  Live streaming options:
    --video-stream    Live streaming of video on vlc player
    --audio-stream    Live streaming of audio on vlc player
  </code></pre>
  
**Listing all formats**
<pre><code>python YTube-Downloader.py -l https://www.youtube.com/watch?v=6TPcwWHZN_0</code></pre>
**Downloading best video**
<pre><code>python YTube-Downloader.py -b https://www.youtube.com/watch?v=6TPcwWHZN_0</code></pre>
**Downloading best audio**
<pre><code>python YTube-Downloader.py -a https://www.youtube.com/watch?v=6TPcwWHZN_0</code></pre>
**Downloading playlist**
<pre><code>Downloading the whole playlist:
	python YTube-Downloader.py --yes-playlist https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S

Downloading the playlist by specifying starting number:
	python YTube-Downloader.py --start-playlist 10 https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S
	
Downloading the playlist by specifying ending number:
	python YTube-Downloader.py --start-playlist 10 https://www.youtube.com/playlist?list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S

Downloading only the current indexed video in a playlist:
	python YTube-Downloader.py --no-playlist "https://www.youtube.com/watch?v=BadQWJW7yk4&list=PLEsfXFp6DpzRcd-q4vR5qAgOZUuz8041S&index=42"</code></pre>
**Live streaming**
<pre><code>Audio streaming:
	python YTube-Downloader.py --audio-stream https://www.youtube.com/watch?v=6TPcwWHZN_0
	
Video streaming:
	python YTube-Downloader.py --video-stream https://www.youtube.com/watch?v=6TPcwWHZN_0</code></pre>

**Note**
<pre><code>	
	1.	To stream audio video live YTube-Downloader uses python module "livestreamer" which by default it checks if it is installed or not, if not it will try to install if YTube-Downloader gets failed try manually for live streaming.
	2.	VideoLAN (VLC) player must be there in your machine.
	3.	if you are downloading the playlist that starts from any indexed video that ur must be used with in the double 	quotes (e.g:- "URL")</code></pre>
	
