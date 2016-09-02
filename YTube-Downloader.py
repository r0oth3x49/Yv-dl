#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pafy import *
from Output import *
from sys import *
from urlparse import *
from os.path import expanduser
import optparse
import os,time,subprocess

class YoutubeDownloader:

    def __init__(self, video, playlist):
        self.video = video
        self.playlist = playlist

    def printProgress(self, iteration, total, prefix = '' , fileSize='' , downloaded = '' , rate = '' ,suffix = '', decimals = 2, barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = round(100.00 * (iteration / float(total)), decimals)
        bar             = fr + sd + '█' * filledLength + fg + sd +'-' * (barLength - filledLength)
        stdout.write(fg + sb + str(prefix) + str(fileSize) + '/' + str(downloaded) + ' ' + str(round(percents, 1)) + '% |' + bar + fg + sb + '| ' + str(rate) + ' ' + str(suffix) + 's ETA \r')
        stdout.flush()

    def DownloadNow(self, total, recvd, ratio, rate, eta):
        TotalSize = round(float(total) / 1048576, 2)
        Receiving = round(float(recvd) / 1048576, 2)
        Size = TotalSize if TotalSize < 1024.00 else round(TotalSize/1024.00, 2)
        Received = Receiving if Receiving < 1024.00 else round(Receiving/1024.00, 2)
        SGb_SMb = 'MB' if TotalSize < 1024.00 else 'GB'
        RGb_RMb = 'MB ' if Receiving < 1024.00 else 'GB '
        Dl_Speed = round(float(rate) , 2)
        dls = Dl_Speed if Dl_Speed < 1024.00 else round(Dl_Speed/1024.00, 2)
        Mb_kB = 'kB/s ' if Dl_Speed < 1024.00 else 'MB/s '
        m, s = divmod(eta, 60)
        h, m = divmod(m, 60)
        eta = "%02d:%02d:%02d" % (h, m, s)
        self.printProgress(Receiving, TotalSize, prefix = '[DOWNLOADING] : ', fileSize = str(Size) + str(SGb_SMb) , downloaded = str(Received) + str(RGb_RMb), rate = str(dls) + str(Mb_kB), suffix = str(eta), barLength = 40)
        
    def BestVidoeQuality(self):

        if os.name == "posix":
            if os.path.exists(Video):
                os.chdir(Video)
            else:
                pass
        else:
            if os.path.exists(Video):
                os.chdir(Video)
            else:
                pass

        print fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = "%s" % (v.title)
        dur = v.duration
        vid = v.videoid
        print fc + sb + "\n------------------------------------------------"
        try:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title
        print fw + sd + "[DURATION] : " + fg + sd + "%s " % dur
        print fw + sd + "[VIDEOID]  : " + fg + sd + "%s " % vid
        print fc + sb + "------------------------------------------------\n"
        try:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title
        bestvideo.download(quiet=True, callback=self.DownloadNow)
        try:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title
        print fc + sb + "\n------------------------------------------------\n"

    def AllVideoQuality(self):

        print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        vid = v.videoid
        allStreams = v.allstreams
        print  fw + sb + "[INFORMATION] : " + fw + sd + "Available streams for video id [%s].." % vid
        time.sleep(0.4)
        print  fg + sd + "\n+--------------------------------------------------------+"
        print  fg + sd + "|     {:<6} {:<8} {:<7} {:<12} {:<14}|".format("Stream", "Type", "Format", "Quality", "Size")
        print  fg + sd + "|     {:<6} {:<8} {:<7} {:<10} {:<16}|".format("------", "-----", "------", "-------", "--------")
        sid = 0
        for s in allStreams:
            sid += 1
            size = round(float(s.get_filesize()) / 1048576, 2)
            sz = size if size < 1024.00 else round(size/1024.00,2)
            in_MB = "MB " if size < 1024.00 else 'GB '
            media = s.mediatype
            quality = s.quality
            Format = s.extension
            if '1280x720' in quality and 'mp4' in Format and 'normal' in media:
                in_MB = in_MB + fc + sb + "(Best)" + fg + sd
            else:
                pass
            print  fg + sd + "|     {:<6} {:<8} {:<7} {:<10} {:<7}{:<9}|".format(sid, media, Format , quality, sz, in_MB)

        print  fg + sd + "+--------------------------------------------------------+\n"

    def DownloadDefaultQuality(self):

        if os.name == "posix":
            if os.path.exists(Video):
                os.chdir(Video)
            else:
                pass
        else:
            if os.path.exists(Video):
                os.chdir(Video)
            else:
                pass
    	print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = "%s" % (v.title)
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n------------------------------------------------"
        try:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title
        print  fw + sd + "[DURATION] : " + fg + sd + "%s " % dur
        print  fw + sd + "[VIDEOID]  : " + fg + sd + "%s " % vid
        print  fc + sb + "------------------------------------------------\n"
        try:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title
        bestvideo.download(quiet=True, callback=self.DownloadNow)
        try:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title
        print fc + sb + "\n------------------------------------------------\n"

    def UserDefineStreamDownload(self, stream_no):

        if os.name == "posix":
            if os.path.exists(OtherStreams):
                os.chdir(OtherStreams)
            else:
                pass
        else:
            if os.path.exists(OtherStreams):
                os.chdir(OtherStreams)
            else:
                pass

    	v = new(self.video)
        Streams = v.allstreams
        print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        title = "%s" % (v.title)
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n------------------------------------------------"
        try:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[TITLE]    : " + fg + sd + "%s " % title
        print  fw + sd + "[DURATION] : " + fg + sd + "%s " % dur
        print  fw + sd + "[VIDEOID]  : " + fg + sd + "%s " % vid
        print  fc + sb + "------------------------------------------------\n"
        try:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title
        Streams[stream_no].download(quiet=True, callback=self.DownloadNow)
        try:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title
        print fc + sb + "\n------------------------------------------------\n"


    def BestAudioQuality(self):
        if os.name == "posix":
            if os.path.exists(Audio):
                os.chdir(Audio)
            else:
                pass
        else:
            if os.path.exists(Audio):
                os.chdir(Audio)
            else:
                pass

        print fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print fg + sb + "[INFORMATION] : " + fg + sd + "Downloading Audio information webpage .."
        a = new(self.video)
        print fg + sb + "[INFORMATION] : " + fg + sd + "Extracting Audio information.."
        time.sleep(0.4)
        bestvideo = a.getbestaudio()
        title = "%s" % (a.title)
        print fc + sb + "\n------------------------------------------------"
        try:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title
        bestvideo.download(quiet=True, callback=self.DownloadNow)
        try:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title.encode("latin-1","ignore")
        except UnicodeDecodeError:
            print fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title
        print fc + sb + "------------------------------------------------\n"

    def PlayList(self, start, end):
    	plist = get_playlist(self.playlist)
    	plistTitle = plist["title"]
        plistCount = len(plist['items'])
        if os.name == 'posix':
            if os.path.exists(Playlist):
                plname = Playlist + "/" + plistTitle
                try:
                    os.mkdir(str(plname))
                except (OSError, Exception, TypeError, IOError, IndexError, ValueError) as e:
                    if os.path.exists(plname):
                        os.chdir(plname)
                    else:
                        pass
                else:
                    if os.path.exists(plname):
                        os.chdir(plname)
                    else:
                        pass
            else:
                pass
        else:
            if os.path.exists(Playlist):
                plname = Playlist + '\\' + plistTitle
                try:
                    os.mkdir(str(plname))
                except (WindowsError, Exception, TypeError, IOError, IndexError) as e:
                    if os.path.exists(plname):
                        os.chdir(plname)
                    else:
                        pass
                else:
                    if os.path.exists(plname):
                        os.chdir(plname)
                    else:
                        pass
            else:
                pass

        if not end:
            s = 1
            temp = int(start) - 1
            TotalVideos = plistCount
            vcount = TotalVideos - int(start) + 1
            e = vcount

        elif int(end) > plistCount:
            s = 1
            temp = int(start) - 1
            TotalVideos = plistCount
            vcount = TotalVideos - int(start) + 1
            e = vcount

        else:
            s = 1
            temp = int(start) - 1
            TotalVideos = int(end)
            vcount = TotalVideos - int(start) + 1
            e = vcount

        if vcount < 0:
            vcount = 0
        else:
            vcount = vcount

    	print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading playist webpage"
        time.sleep(0.4)
    	print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting playlist information"
    	print  fc + sb + "------------------------------------------------"
    	print  fw + sd + "[INFORMATION] : " + fg + sd + "Downloading playlist %s " % plistTitle
        print  fw + sd + "[INFORMATION] : " + fg + sd + "Playlist %s: Downloading %d videos " % (plistTitle, vcount)
    	print  fc + sb + "------------------------------------------------\n"
        time.sleep(0.4)
        if temp >= TotalVideos:
            print fr + sb + "[ERROR] : Specified wrong starting/ending point of playlist please check the URL "
        else:
            pass
    	while temp < TotalVideos:
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video %d of %d " % (s, e)
            time.sleep(0.4)
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading webpage"
            time.sleep(0.4)
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
            time.sleep(0.4)
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information"
            time.sleep(0.4)
            best = plist['items'][temp]['pafy'].getbest()
            title = "%s" % (best.title)
            try:
                print  fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
            except UnicodeDecodeError:
                print  fw + sd + "[DOWNLOADING] : " + fg + sd + "%s " % title
            best.download(quiet=True, callback=self.DownloadNow)
            try:
                print  fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title.encode('latin-1','ignore')
            except UnicodeDecodeError:
                print  fw + sd + "\n[COMPLETED]   : " + fg + sd + "%s " % title
            temp += 1
            s += 1
            print  fc + sb + "------------------------------------------------"

    def LiveStreamAudio(self):
        v = new(self.video)
        Streams = v.allstreams
        print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading audio information webpage .."
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting audio information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n------------------------------------------------"
        print  fw + sd + "[TITLE]    : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fw + sd + "[DURATION] : " + fg + sd + "%s " % dur
        print  fw + sd + "[VIDEOID]  : " + fg + sd + "%s " % vid
        print  fc + sb + "------------------------------------------------\n"
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting (mp4/webm) audio stream info.."
        if os.name == "posix":
            CheckStreamsCmd = "livestreamer " + str(self.video) + " --yes-run-as-root"
        else:
            CheckStreamsCmd = "livestreamer " + str(self.video)
        AvailableStream = subprocess.check_output(CheckStreamsCmd, shell=True)
        SetAudioStream = "audio_webm" if "audio_webm" in AvailableStream and os.name == "nt"  else "audio_mp4"
        if SetAudioStream == "audio_webm":
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Openning webm audio stream : (audio_webm ==> http).."
        else:
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Openning mp4 audio stream : (audio_mp4 ==> http).."

        print  fg + sb + "[STARTSTREAM] : " + fg + sd + "Starting live audio stream for %s" % title.encode('latin-1','ignore')
        if os.name == "posix":
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetAudioStream) + " --yes-run-as-root"
        else:
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetAudioStream)
        player = subprocess.check_output(StartStreamingCmd, shell=True)
        if "Player closed" in player:
            print  fg + sb + "[INFORMATION] : " + fr + sb + "Player closed by user."
            print  fg + sb + "[ENDOFSTREAM] : " + fg + sd + "Audio stream ended."
        else:
            print  fg + sb + "[ENDOFSTREAM] : " + fg + sd + "Audio stream completed."
        print  fc + sb + "------------------------------------------------\n"

    def LiveStreamVideo(self, args):
        v = new(self.video)
        Streams = v.allstreams
        print  fg + sb + "\n[INFORMATION] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Downloading video information webpage .."
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n------------------------------------------------"
        print  fw + sd + "[TITLE]    : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fw + sd + "[DURATION] : " + fg + sd + "%s " % dur
        print  fw + sd + "[VIDEOID]  : " + fg + sd + "%s " % vid
        print  fc + sb + "------------------------------------------------\n"
        print  fg + sb + "[INFORMATION] : " + fg + sd + "Extracting (hd/normal) video stream info.."
        if os.name == "posix":
            CheckStreamsCmd = "livestreamer " + str(self.video) + " --yes-run-as-root"
        else:
            CheckStreamsCmd = "livestreamer " + str(self.video)
        AvailableStream = subprocess.check_output(CheckStreamsCmd, shell=True)
        if not args:
        	SetVideoStream = "360p" if "360p" in AvailableStream else "best"
        else:
        	SetVideoStream = args
        if SetVideoStream == "360p":
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Opening normal video stream : (360p ==> http).."
        else:
            print  fg + sb + "[INFORMATION] : " + fg + sd + "Opening hd video stream :  (720p ==> http).."

        print  fg + sb + "[STARTSTREAM] : " + fg + sd + "Starting live video stream for %s" % title.encode('latin-1','ignore')
        if os.name == "posix":
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetVideoStream) + " --yes-run-as-root"
        else:
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetVideoStream)
        player = subprocess.check_output(StartStreamingCmd, shell=True)
        if "Player closed" in player:
            print  fg + sb + "[INFORMATION] : " + fr + sb + "Player closed by user."
            print  fg + sb + "[ENDOFSTREAM] : " + fg + sd + "Video stream ended."
        else:
            print  fg + sb + "[ENDOFSTREAM] : " + fg + sd + "Video stream completed."
        print  fc + sb + "------------------------------------------------\n"




def Main():
    print fc + sb + """+----------------------------------------+
|          Youtube Downloader            |
|   Coded By: Nasir Khan (r0ot h3x49)    |
+----------------------------------------+\n"""
    global ret,Audio,Video,Playlist,OtherStreams
    dirAudio = 'Audio'
    dirVideos = 'Video'
    dirPlaylist = 'Playlists'
    dirOtherStream = "Other Streams"
    if os.name == 'posix':
        path = expanduser("~") + "/Downloads"
        r0oth3xYTD = path + "/YTube-Downloads"
        Audio = r0oth3xYTD + "/" + dirAudio
        Video = r0oth3xYTD + "/" + dirVideos
        Playlist = r0oth3xYTD + "/" + dirPlaylist
        OtherStreams = r0oth3xYTD + "/Other-Streams"
        if os.path.exists(path):
            try:
                os.mkdir(r0oth3xYTD)
            except (OSError, Exception, TypeError, IOError, IndexError, ValueError) as e:
                pass
            else:
                if os.path.exists(r0oth3xYTD):
                    try:
                        os.mkdir(str(Audio))
                        os.mkdir(str(Video))
                        os.mkdir(str(Playlist))
                        os.mkdir(str(OtherStreams))
                    except (OSError, Exception, TypeError, IOError, IndexError, ValueError) as e:
                        pass
                else:
                    pass
        else:
            pass

    else:
        path = os.environ['USERPROFILE'] + '\\Downloads'
        r0oth3xYTD = path + "\\Youtube Downloads" 
        Audio = r0oth3xYTD + '\\' + dirAudio
        Video = r0oth3xYTD + '\\' + dirVideos
        Playlist = r0oth3xYTD + '\\' + dirPlaylist
        OtherStreams = r0oth3xYTD + '\\' + dirOtherStream
        if os.path.exists(path):
            try:
                os.mkdir(str(r0oth3xYTD))
            except (WindowsError, Exception, TypeError, IOError, IndexError) as e:
                pass
            else:
                if os.path.exists(r0oth3xYTD):
                    try:
                        os.mkdir(str(Audio))
                        os.mkdir(str(Video))
                        os.mkdir(str(Playlist))
                        os.mkdir(str(OtherStreams))
                    except (WindowsError, Exception, TypeError, IOError, IndexError) as e:
                        pass
                else:
                    pass
        else:
            pass

    us = "%prog [OPTIONS] URL"
    version = "%prog version 1.0"
    parser = optparse.OptionParser(usage=us,version=version,conflict_handler="resolve")

    general = optparse.OptionGroup(parser, 'General Options')
    general.add_option(
        '-h', '--help',
        action='help',
        help='Print this help text and exit')
    general.add_option(
        '-v', '--version',
        action='version',
    help='Print program version and exit')

    downloader = optparse.OptionGroup(parser, "Downloader options")
    downloader.add_option(
        "-a", "--best-audio", 
        action='store_const', 
        const='audio', 
        dest='element',\
        help="Download best available audio")
    downloader.add_option(
        "-b", "--best-video", 
        action='store_const', 
        const='video', 
        dest='element',\
        help="Download best available resolution")
    downloader.add_option(
        "-l", "--list", 
        action='store_const', 
        const='listdown', 
        dest='element',\
        help="list available download streams")
    downloader.add_option(
        "-n", "--stream-no", 
        action='store_const', 
        const='strno', 
        dest='element',\
        help="Download specific video by stream no. (prog -n 2 URL)")

    playlist = optparse.OptionGroup(parser, "Playlist options")
    playlist.add_option(
        "--yes-playlist", 
        action='store_const', 
        const='YesPlaylist', 
        dest='element',\
        help="Allow downloading playlist completely")
    playlist.add_option(
        "--no-playlist", 
        action='store_const', 
        const='NoPlaylist', 
        dest='element',\
        help="Only download specific video available in a playlist")
    playlist.add_option(
        "--start-playlist", 
        action='store_const', 
        const='StartPlaylist', 
        dest='element',\
        help="Specify playlist start. (prog --start-playlist 2 URL)")
    playlist.add_option(
        "--end-playlist", 
        action='store_const', 
        const='EndPlaylist', 
        dest='element',\
        help="Specify playlist end. (prog --end-playlist 23 URL)")

    livestream = optparse.OptionGroup(parser, "Live streaming options")
    livestream.add_option(
        "--video-stream", 
        action='store_const', 
        const='VideoStream', 
        dest='element',\
        help="Live streaming of video on vlc player")
    livestream.add_option(
        "--audio-stream", 
        action='store_const', 
        const='AudioStream', 
        dest='element',\
        help="Live streaming of audio on vlc player")
    livestream.add_option(
        "--best-stream", 
        action='store_const', 
        const='BestStream', 
        dest='element',\
        help="Best video (720p) streaming")

    
    parser.add_option_group(general)
    parser.add_option_group(downloader)
    parser.add_option_group(playlist)
    parser.add_option_group(livestream)

    
    (options, args) = parser.parse_args()
    ret = options.element
    
    if not ret and len(args) != 1:
        parser.print_usage()

    elif ret:
        if ret == "listdown":
            url = args[0]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

                for v in query.values():
                    l.append(v[0])

                vid = l[2]
                url = "https://www.youtube.com/watch?v=%s" % vid
                download = YoutubeDownloader(url, None)
                download.AllVideoQuality()

            else:
                url = args[0]
                download = YoutubeDownloader(url, None)
                download.AllVideoQuality()

        elif ret == "video":
            url = args[0]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

                for v in query.values():
                    l.append(v[0])

                vid = l[2]
                url = "https://www.youtube.com/watch?v=%s" % vid
                download = YoutubeDownloader(url, None)
                download.BestVidoeQuality()

            else:
                url = args[0]
                download = YoutubeDownloader(url, None)
                download.BestVidoeQuality()

        elif ret == "audio":
            url = args[0]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

                for v in query.values():
                    l.append(v[0])

                aid = l[2]
                url = "https://www.youtube.com/watch?v=%s" % aid
                download = YoutubeDownloader(url, None)
                download.BestAudioQuality()

            else:
                url = args[0]
                download = YoutubeDownloader(url, None)
                download.BestAudioQuality()


        elif ret == "YesPlaylist":
            url = args[0]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

            # Starts downloading from default index in playlist url and ends and the END

                for v in query.values():
                    l.append(v[0])

                start = l[0]
                plist = l[1]
                end = None
                plurl = "https://www.youtube.com/playlist?list=%s" % plist
                download = YoutubeDownloader(None, plurl)
                download.PlayList(start, end)

            else:
                plurl = args[0]
            	start = 1
                end = None
            	download = YoutubeDownloader(None, plurl)
            	download.PlayList(start, end)

        elif ret == "NoPlaylist":
            url = args[0]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

                for v in query.values():
                    l.append(v[0])

                vid = l[2]
                url = "https://www.youtube.com/watch?v=%s" % vid
                download = YoutubeDownloader(url, None)
                download.BestVidoeQuality()

            else:
                url = args[0]
                download = YoutubeDownloader(url, None)
                download.BestVidoeQuality()

        elif ret == "StartPlaylist":
            start = args[0]
            url = args[1]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

            # Starts downloading from given args without looking to the index in playlist url

                for v in query.values():
                    l.append(v[0])

                plist = l[1]
                end = None
                plurl = "https://www.youtube.com/playlist?list=%s" % plist
                download = YoutubeDownloader(None, plurl)
                download.PlayList(start, end)

            else:
                plurl = args[1]
                end = None
                download = YoutubeDownloader(None, plurl)
                download.PlayList(start, end)

        elif ret == "strno":
        	streamno = args[0]
        	url = args[1]
        	sid = int(streamno) - 1
        	download = YoutubeDownloader(url, None)
        	download.UserDefineStreamDownload(sid)

        elif ret == "EndPlaylist":
            end = args[0]
            url = args[1]
            l = []
            plurl = urlparse(url)
            query = parse_qs(plurl.query)
            if len(query) > 1:

            # Starts downloading from default index in url and Ends on givens args

                for v in query.values():
                    l.append(v[0])

                start = l[0]
                plist = l[1]
                plurl = "https://www.youtube.com/playlist?list=%s" % plist
                download = YoutubeDownloader(None, plurl)
                download.PlayList(start, end)

            else:
                start = 1
                plurl = args[1]
                download = YoutubeDownloader(None, plurl)
                download.PlayList(start, end)

        elif ret == "VideoStream":
            try:
                import livestreamer
            except ImportError:
                print fr + sb + "[ERROR] : Live streaming module not found installing...\n"
                if os.name == "posix":
                    subprocess.call("sudo pip install livestreamer", shell=True)
                    time.sleep(1)
                else:
                    subprocess.call("pip install livestreamer", shell=True)
                    subprocess.call("PAUSE", shell=True)
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(None)

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(None)
            else:
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(None)

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(None)

        elif ret == "BestStream":
            try:
                import livestreamer
            except ImportError:
                print fr + sb + "[ERROR] : Live streaming module not found installing...\n"
                if os.name == "posix":
                    subprocess.call("sudo pip install livestreamer", shell=True)
                    time.sleep(1)
                else:
                    subprocess.call("pip install livestreamer", shell=True)
                    subprocess.call("PAUSE", shell=True)
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    s = "best"
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(s)

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(s)
            else:
            	s = "best"
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(s)

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamVideo(s)

        elif ret == "AudioStream":
            try:
                import livestreamer
            except ImportError:
                print fr + sb + "[ERROR] : Live streaming module not found installing...\n"
                if os.name == "posix":
                    subprocess.call("sudo pip install livestreamer", shell=True)
                    time.sleep(1)
                else:
                    subprocess.call("pip install livestreamer", shell=True)
                    subprocess.call("PAUSE", shell=True)
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamAudio()

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamAudio()
            else:
                url = args[0]
                l = []
                plurl = urlparse(url)
                query = parse_qs(plurl.query)
                if len(query) > 1:
                    for v in query.values():
                        l.append(v[0])

                    vid = l[2]
                    end = None
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamAudio()

                else:
                    url = args[0]
                    download = YoutubeDownloader(url, None)
                    download.LiveStreamAudio()


        else:
            pass
    else:
        url = args[0]
        l = []
        plurl = urlparse(url)
        query = parse_qs(plurl.query)
        if len(query) > 1:

            for v in query.values():
                l.append(v[0])

            vid = l[2]
            url = "https://www.youtube.com/watch?v=%s" % vid
            download = YoutubeDownloader(url, None)
            download.DownloadDefaultQuality()

        else:
            url = args[0]
            download = YoutubeDownloader(url, None)
            download.DownloadDefaultQuality()
    
if __name__ == "__main__":
    try:
        Main()
    except KeyboardInterrupt:
        print fr + sb + "\n\n[ERROR] : User Interrupted."
    except IndexError:
        print fr + sb + "\n[ERROR] : URL not specified"
    except IOError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except ValueError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except TypeError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except NameError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except OSError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except subprocess.CalledProcessError:
        print fr + sb + "\n[ERROR] : Failed to Extract stream info provide other URL for required stream"
    except UnicodeEncodeError as e:
        print fr + sb + "\n[ERROR] : %s" % e
    except Exception as e:
        print fr + sb + "\n[ERROR] : %s" % e
