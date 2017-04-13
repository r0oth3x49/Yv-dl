#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pafy import *
from banner import banner
from vimeo import new as vmnew
from Output import *
from sys import *
from urlparse import *
from os.path import expanduser
import optparse, re
import os,time,subprocess

class YoutubeDownloader:

    def __init__(self, video, playlist):
        self.video = video
        self.playlist = playlist

    def _generate_dirname(self, title):
        ok = re.compile(r'[^/]')

        if os.name == "nt":
            ok = re.compile(r'[^\\/:*?"<>|]')

        dirname = "".join(x if ok.match(x) else "_" for x in title)
        return dirname

    # Source taken from  http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    def printProgress(self, iteration, total, fileSize='' , downloaded = '' , rate = '' ,suffix = '', barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = format(100.00 * (iteration / float(total)), '.2f')
        bar             = fc + sd + ('█' if os.name is 'posix' else '#') * filledLength + fw + sd +'-' * (barLength - filledLength)
        stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + str(fileSize) + '/' + str(downloaded) + ' ' + percents + '% |' + bar + fg + sb + '| ' + str(rate) + ' ' + str(suffix) + 's ETA \r')
        stdout.flush()

    def DownloadNow(self, total, recvd, ratio, rate, eta):
        TotalSize = round(float(total) / 1048576, 2)
        Receiving = round(float(recvd) / 1048576, 2)
        Size = format(TotalSize if TotalSize < 1024.00 else TotalSize/1024.00, '.2f')
        Received = format(Receiving if Receiving < 1024.00 else Receiving/1024.00,'.2f')
        SGb_SMb = 'MB' if TotalSize < 1024.00 else 'GB'
        RGb_RMb = 'MB ' if Receiving < 1024.00 else 'GB '
        Dl_Speed = round(float(rate) , 2)
        dls = format(Dl_Speed if Dl_Speed < 1024.00 else Dl_Speed/1024.00, '.2f')
        Mb_kB = 'kB/s ' if Dl_Speed < 1024.00 else 'MB/s '
        (mins, secs) = divmod(eta, 60)
        (hours, mins) = divmod(mins, 60)
        if hours > 99:
            eta = "--:--:--"
        if hours == 0:
            eta = "%02d:%02d" % (mins, secs)
        else:
            eta = "%02d:%02d:%02d" % (hours, mins, secs)
        self.printProgress(Receiving, TotalSize, fileSize = str(Size) + str(SGb_SMb) , downloaded = str(Received) + str(RGb_RMb), rate = str(dls) + str(Mb_kB), suffix = str(eta), barLength = 40)
        
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

        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = v.title
        dur = v.duration
        vid = v.videoid
        print fc + sb + "\n-------------------------------------------------------------"
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print fc + sb + "-------------------------------------------------------------\n"
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = bestvideo.download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"

    def AllVideoQuality(self):

        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        vid = v.videoid
        title = v.title
        allStreams = v.allstreams
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fy + sb + "Available streams for video id [" + fm + sb + str(vid)+ fy + sb + "].."
        time.sleep(0.4)
        print  fy + sb + "\n+--------------------------------------------------------+"
        print  fy + sb + "|     {:<6} {:<8} {:<7} {:<12} {:<14}|".format("Stream", "Type", "Format", "Quality", "Size")
        print  fy + sb + "|     {:<6} {:<8} {:<7} {:<10} {:<16}|".format("------", "-----", "------", "-------", "--------")
        sid = 0
        for s in allStreams:
            sid += 1
            size = round(float(s.get_filesize()) / 1048576, 2)
            sz = size if size < 1024.00 else round(size/1024.00,2)
            in_MB = "MB " if size < 1024.00 else 'GB '
            media = s.mediatype
            quality = s.quality
            Format = s.extension
            bar = v.getbest()
            repbar = str(bar)
            best = repbar.replace('normal:mp4@', '') if repbar is not None else repbar.replace('normal:webm@', '')
            if best in quality and 'mp4' in Format and 'normal' in media:
                in_MB = in_MB + fc + sb + "(Best)" + fg + sd
            else:
                pass
            print  fy + sb + "|" + fg + sd + "     {:<6} {:<8} {:<7} {:<10} {:<7}{:<9}{}{}|".format(sid, media, Format , quality, sz, in_MB, fy, sb)

        print  fy + sb + "+--------------------------------------------------------+\n"

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
    	print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = new(self.video)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = bestvideo.download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"

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
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = Streams[stream_no].download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"


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

        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading Audio information webpage .."
        a = new(self.video)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting Audio information.."
        time.sleep(0.4)
        bestaudio = a.getbestaudio()
        title = a.title
        print fc + sb + "\n-------------------------------------------------------------"
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = bestaudio.download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "-------------------------------------------------------------\n"

    def PlayList(self, start, end):
    	plist = get_playlist(self.playlist)
    	p = plist["title"]
    	plistTitle = self._generate_dirname(p)
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

    	print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading playist webpage"
        time.sleep(0.4)
    	print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting playlist information"
    	print  fc + sb + "-------------------------------------------------------------"
    	print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading playlist %s " % plistTitle
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Playlist %s: Downloading %d videos " % (plistTitle, vcount)
    	print  fc + sb + "-------------------------------------------------------------\n"
        time.sleep(0.4)
        if temp >= TotalVideos:
            print fc + sd + "[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "Specified wrong starting/ending point of playlist please check the URL "
        else:
            pass
    	while temp < TotalVideos:
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video %d of %d " % (s, e)
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage"
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information"
            best = plist['items'][temp]['pafy'].getbest()
            title = best.title
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
            retVal = best.download(quiet=True, callback=self.DownloadNow)
            if 'EXISTS' in retVal:
                time.sleep(0.4)
                print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
            else:
                print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
            temp += 1
            s += 1
            print  fc + sb + "-------------------------------------------------------------\n"

    def LiveStreamAudio(self):
        v = new(self.video)
        Streams = v.allstreams
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading audio information webpage .."
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting audio information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting (mp4/webm) audio stream info.."
        if os.name == "posix":
            CheckStreamsCmd = "livestreamer " + str(self.video) + " --yes-run-as-root"
        else:
            CheckStreamsCmd = "livestreamer " + str(self.video)
        AvailableStream = subprocess.check_output(CheckStreamsCmd, shell=True)
        SetAudioStream = "audio_webm" if "audio_webm" in AvailableStream and os.name == "nt"  else "audio_mp4"
        if SetAudioStream == "audio_webm":
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Openning webm audio stream : (audio_webm ==> http).."
        else:
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Openning mp4 audio stream : (audio_mp4 ==> http).."

        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Starting live audio stream for %s" % title.encode('latin-1','ignore')
        if os.name == "posix":
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetAudioStream) + " --yes-run-as-root"
        else:
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetAudioStream)
        player = subprocess.check_output(StartStreamingCmd, shell=True)
        if "Player closed" in player:
            print  fc + sd + "[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "Player closed by user."
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Audio stream ended."
        else:
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Audio stream completed."
        print  fc + sb + "-------------------------------------------------------------\n"

    def LiveStreamVideo(self, args):
        v = new(self.video)
        Streams = v.allstreams
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.videoid
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting (hd/normal) video stream info.."
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
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Opening normal video stream : (360p ==> http).."
        else:
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Opening hd video stream :  (720p ==> http).."

        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Starting live video stream for %s" % title.encode('latin-1','ignore')
        if os.name == "posix":
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetVideoStream) + " --yes-run-as-root"
        else:
            StartStreamingCmd = "livestreamer " + str(self.video) + " " + str(SetVideoStream)
        player = subprocess.check_output(StartStreamingCmd, shell=True)
        if "Player closed" in player:
            print  fc + sd + "[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "Player closed by user."
            print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Video stream ended."
        else:
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Video stream completed."
        print  fc + sb + "-------------------------------------------------------------\n"


class VimeoDownloader(object):
    
    def __init__(self, video, playlist):
        self.video = video
        self.playlist = playlist

    def printProgress(self, iteration, total, fileSize='' , downloaded = '' , rate = '' ,suffix = '', barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = format(100.00 * (iteration / float(total)), '.2f')
        bar             = fc + sd + ('█' if os.name is 'posix' else '#') * filledLength + fw + sd +'-' * (barLength - filledLength)
        stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + str(fileSize) + '/' + str(downloaded) + ' ' + percents + '% |' + bar + fg + sb + '| ' + str(rate) + ' ' + str(suffix) + 's ETA \r')
        stdout.flush()

    def DownloadNow(self, total, recvd, ratio, rate, eta):
        TotalSize = round(float(total) / 1048576, 2)
        Receiving = round(float(recvd) / 1048576, 2)
        Size = format(TotalSize if TotalSize < 1024.00 else TotalSize/1024.00, '.2f')
        Received = format(Receiving if Receiving < 1024.00 else Receiving/1024.00,'.2f')
        SGb_SMb = 'MB' if TotalSize < 1024.00 else 'GB'
        RGb_RMb = 'MB ' if Receiving < 1024.00 else 'GB '
        Dl_Speed = round(float(rate) , 2)
        dls = format(Dl_Speed if Dl_Speed < 1024.00 else Dl_Speed/1024.00, '.2f')
        Mb_kB = 'kB/s ' if Dl_Speed < 1024.00 else 'MB/s '
        (mins, secs) = divmod(eta, 60)
        (hours, mins) = divmod(mins, 60)
        if hours > 99:
            eta = "--:--:--"
        if hours == 0:
            eta = "%02d:%02d" % (mins, secs)
        else:
            eta = "%02d:%02d:%02d" % (hours, mins, secs)
        self.printProgress(Receiving, TotalSize, fileSize = str(Size) + str(SGb_SMb) , downloaded = str(Received) + str(RGb_RMb), rate = str(dls) + str(Mb_kB), suffix = str(eta), barLength = 40)
        
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

        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = vmnew(self.video)
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = v.title
        dur = v.duration
        vid = v.video_id
        print fc + sb + "\n-------------------------------------------------------------"
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print fc + sb + "-------------------------------------------------------------\n"
        print fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = bestvideo.download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"

    def AllVideoQuality(self):

        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = vmnew(self.video)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        vid = v.video_id
        title = v.title
        allStreams = v.streams
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fy + sb + "Available streams for video id [" + fm + sb + str(vid)+ fy + sb + "].."
        time.sleep(0.4)
        print  fy + sb + "\n+--------------------------------------------------------+"
        print  fy + sb + "|     {:<6} {:<8} {:<7} {:<12} {:<14}|".format("Stream", "Type", "Format", "Quality", "Size")
        print  fy + sb + "|     {:<6} {:<8} {:<7} {:<10} {:<16}|".format("------", "-----", "------", "-------", "--------")
        sid = 0
        for s in allStreams:
            sid += 1
            size = round(float(s.get_filesize()) / 1048576, 2)
            sz = size if size < 1024.00 else round(size/1024.00,2)
            in_MB = "MB " if size < 1024.00 else 'GB '
            media = s.mediatype
            quality = s.quality
            Format = s.extension
            bar = v.getbest()
            repbar = str(bar)
            best = repbar.replace('normal:mp4@', '') if repbar is not None else repbar.replace('normal:webm@', '')
            if best in quality and 'mp4' in Format and 'normal' in media:
                in_MB = in_MB + fc + sb + "(Best)" + fg + sd
            else:
                pass
            print  fy + sb + "|" + fg + sd + "     {:<6} {:<8} {:<7} {:<10} {:<7}{:<9}{}{}|".format(sid, media, Format , quality, sz, in_MB, fy, sb)

        print  fy + sb + "+--------------------------------------------------------+\n"

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
    	print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        v = vmnew(self.video)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        bestvideo = v.getbest()
        title = v.title
        dur = v.duration
        vid = v.video_id
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = bestvideo.download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"

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

    	v = vmnew(self.video)
        Streams = v.streams
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage.."
        time.sleep(0.4)
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading video information webpage .."
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting video information.."
        time.sleep(0.4)
        title = v.title
        dur = v.duration
        vid = v.video_id
        print  fc + sb + "\n-------------------------------------------------------------"
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Title     : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Duration  : " + fg + sd + "%s " % dur
        print  fc + sd + "[" + fm + sb + "+" + fc + sd + "]" + fy + sb + " Video Id  : " + fg + sd + "%s " % vid
        print  fc + sb + "-------------------------------------------------------------\n"
        print  fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        retVal = Streams[stream_no].download(quiet=True, callback=self.DownloadNow)
        if 'EXISTS' in retVal:
            time.sleep(0.4)
            print  fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore') + fy + sb  + " (already downloaded)"
        else:
            print  fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "%s " % title.encode('latin-1','ignore')
        print fc + sb + "\n-------------------------------------------------------------\n"


def Main():
    print banner
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
        r0oth3xYTD = path + "\\Yv-Downloads" 
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
    version = "%prog version 1.2"
    parser = optparse.OptionParser(usage=us,version=version,conflict_handler="resolve")

    general = optparse.OptionGroup(parser, 'General')
    general.add_option(
        '-h', '--help',
        action='help',
        help='Print this help text and exit')
    general.add_option(
        '-v', '--version',
        action='version',
    help='Print program version and exit')

    downloader = optparse.OptionGroup(parser, "Downloader")
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
    downloader.add_option(
        "-f", "--file", 
        action='store_true', 
        dest='fileDown',\
        help="Download videos/playlists by proving file (e.g :- prog -b/--yes-palylist -f file.txt).")

    playlist = optparse.OptionGroup(parser, "Playlist")
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

    livestream = optparse.OptionGroup(parser, "Streaming")
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
            if 'vimeo' in url:
                url = args[0]
                download = VimeoDownloader(url, None)
                download.AllVideoQuality()
            else:
                if options.fileDown:
                    f = args[0]
                    f_in = open(f)
                    ListOfvids = list(line for line in (l.strip() for l in f_in) if line)
                    for u in ListOfvids:
                        plurl = (u.split("v=")[-1])[0:11]
                        vid = plurl
                        url = "https://www.youtube.com/watch?v=%s" % vid
                        download = YoutubeDownloader(url, None)
                        download.AllVideoQuality()
                else:
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
            if 'vimeo' in url:
                url = args[0]
                download = VimeoDownloader(url, None)
                download.BestVidoeQuality()
            else:
                if options.fileDown:
                    f = args[0]
                    f_in = open(f)
                    ListOfvids = list(line for line in (l.strip() for l in f_in) if line)
                    for u in ListOfvids:
                        plurl = (u.split("v=")[-1])[0:11]
                        vid = plurl
                        url = "https://www.youtube.com/watch?v=%s" % vid
                        download = YoutubeDownloader(url, None)
                        download.BestVidoeQuality()
                else:
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
            if options.fileDown:
                f = args[0]
                f_in = open(f)
                ListOfvids = list(line for line in (l.strip() for l in f_in) if line)
                for u in ListOfvids:
                    plurl = (u.split("v=")[-1])[0:11]
                    vid = plurl
                    url = "https://www.youtube.com/watch?v=%s" % vid
                    download = YoutubeDownloader(url, None)
                    download.BestAudioQuality()
            else:
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
            if options.fileDown:
                f = args[0]
                f_in = open(f)
                ListOfplvids = list(line for line in (l.strip() for l in f_in) if line)
                for url in ListOfplvids:
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
                        plurl = url
                        start = 1
                        end = None
                        download = YoutubeDownloader(None, plurl)
                        download.PlayList(start, end)
                
            else:
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
            if 'vimeo' in url:
                sid = int(streamno) - 1
                download = VimeoDownloader(url, None)
                download.UserDefineStreamDownload(sid)
            else:
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
        if 'vimeo' in url:
            url = args[0]
            download = VimeoDownloader(url, None)
            download.BestVidoeQuality()
        else:
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
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "User Interrupted.."
    except IndexError:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "You forgot to specify the link."
    except IOError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except ValueError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except TypeError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except NameError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except OSError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except subprocess.CalledProcessError:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "It Seems this link don't have any live stream try with another link."
    except UnicodeEncodeError as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
    except Exception as e:
        print fc + sd + "\n[" + fm + sb + "-" + fc + sd + "] : " + fr + sb + "%s" % e
