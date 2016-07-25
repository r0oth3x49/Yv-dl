# encoding: utf-8

from __future__ import unicode_literals

import os
import re
import sys

from .common import InfoExtractor
from .youtube import YoutubeIE
from ..compat import (
    compat_etree_fromstring,
    compat_urllib_parse_unquote,
    compat_urlparse,
    compat_xml_parse_error,
)
from ..utils import (
    determine_ext,
    ExtractorError,
    float_or_none,
    HEADRequest,
    is_html,
    orderedSet,
    sanitized_Request,
    smuggle_url,
    unescapeHTML,
    unified_strdate,
    unsmuggle_url,
    UnsupportedError,
    url_basename,
    xpath_text,
)

class GenericIE(InfoExtractor):
    IE_DESC = 'Generic downloader that works on some sites'
    _VALID_URL = r'.*'
    IE_NAME = 'generic'
    _TESTS = [
        # google redirect
        {
            'url': 'http://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CCUQtwIwAA&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DcmQHVoWB5FY&ei=F-sNU-LLCaXk4QT52ICQBQ&usg=AFQjCNEw4hL29zgOohLXvpJ-Bdh2bils1Q&bvm=bv.61965928,d.bGE',
            'info_dict': {
                'id': 'cmQHVoWB5FY',
                'ext': 'mp4',
                'upload_date': '20130224',
                'uploader_id': 'TheVerge',
                'description': 're:^Chris Ziegler takes a look at the\.*',
                'uploader': 'The Verge',
                'title': 'First Firefox OS phones side-by-side',
            },
            'params': {
                'skip_download': False,
            }
        },
        {
            # https://github.com/rg3/youtube-dl/issues/2253
            'url': 'http://bcove.me/i6nfkrc3',
            'md5': '0ba9446db037002366bab3b3eb30c88c',
            'info_dict': {
                'id': '3101154703001',
                'ext': 'mp4',
                'title': 'Still no power',
                'uploader': 'thestar.com',
                'description': 'Mississauga resident David Farmer is still out of power as a result of the ice storm a month ago. To keep the house warm, Farmer cuts wood from his property for a wood burning stove downstairs.',
            },
            'add_ie': ['BrightcoveLegacy'],
        },
        {
            'url': 'http://www.championat.com/video/football/v/87/87499.html',
            'md5': 'fb973ecf6e4a78a67453647444222983',
            'info_dict': {
                'id': '3414141473001',
                'ext': 'mp4',
                'title': 'Видео. Удаление Дзагоева (ЦСКА)',
                'description': 'Онлайн-трансляция матча ЦСКА - "Волга"',
                'uploader': 'Championat',
            },
        },
        {
            # https://github.com/rg3/youtube-dl/issues/3541
            'add_ie': ['BrightcoveLegacy'],
            'url': 'http://www.kijk.nl/sbs6/leermijvrouwenkennen/videos/jqMiXKAYan2S/aflevering-1',
            'info_dict': {
                'id': '3866516442001',
                'ext': 'mp4',
                'title': 'Leer mij vrouwen kennen: Aflevering 1',
                'description': 'Leer mij vrouwen kennen: Aflevering 1',
                'uploader': 'SBS Broadcasting',
            },
            'skip': 'Restricted to Netherlands',
            'params': {
                'skip_download': True,  # m3u8 download
            },
        },
        # embed.ly video
        {
            'url': 'http://www.tested.com/science/weird/460206-tested-grinding-coffee-2000-frames-second/',
            'info_dict': {
                'id': '9ODmcdjQcHQ',
                'ext': 'mp4',
                'title': 'Tested: Grinding Coffee at 2000 Frames Per Second',
                'upload_date': '20140225',
                'description': 'md5:06a40fbf30b220468f1e0957c0f558ff',
                'uploader': 'Tested',
                'uploader_id': 'testedcom',
            },
            # No need to test YoutubeIE here
            'params': {
                'skip_download': True,
            },
        },
        # YouTube embed
        {
            'url': 'http://www.badzine.de/ansicht/datum/2014/06/09/so-funktioniert-die-neue-englische-badminton-liga.html',
            'info_dict': {
                'id': 'FXRb4ykk4S0',
                'ext': 'mp4',
                'title': 'The NBL Auction 2014',
                'uploader': 'BADMINTON England',
                'uploader_id': 'BADMINTONEvents',
                'upload_date': '20140603',
                'description': 'md5:9ef128a69f1e262a700ed83edb163a73',
            },
            'add_ie': ['Youtube'],
            'params': {
                'skip_download': True,
            }
        },
        # YouTube embed via <data-embed-url="">
        {
            'url': 'https://play.google.com/store/apps/details?id=com.gameloft.android.ANMP.GloftA8HM',
            'info_dict': {
                'id': '4vAffPZIT44',
                'ext': 'mp4',
                'title': 'Asphalt 8: Airborne - Update - Welcome to Dubai!',
                'uploader': 'Gameloft',
                'uploader_id': 'gameloft',
                'upload_date': '20140828',
                'description': 'md5:c80da9ed3d83ae6d1876c834de03e1c4',
            },
            'params': {
                'skip_download': True,
            }
        },
        # Multiple brightcove videos
        # https://github.com/rg3/youtube-dl/issues/2283
        {
            'url': 'http://www.newyorker.com/online/blogs/newsdesk/2014/01/always-never-nuclear-command-and-control.html',
            'info_dict': {
                'id': 'always-never',
                'title': 'Always / Never - The New Yorker',
            },
            'playlist_count': 3,
            'params': {
                'extract_flat': False,
                'skip_download': True,
            }
        },
        # jwplayer YouTube
        {
            'url': 'http://media.nationalarchives.gov.uk/index.php/webinar-using-discovery-national-archives-online-catalogue/',
            'info_dict': {
                'id': 'Mrj4DVp2zeA',
                'ext': 'mp4',
                'upload_date': '20150212',
                'uploader': 'The National Archives UK',
                'description': 'md5:a236581cd2449dd2df4f93412f3f01c6',
                'uploader_id': 'NationalArchives08',
                'title': 'Webinar: Using Discovery, The National Archives’ online catalogue',
            },
        },
        # Wordpress "YouTube Video Importer" plugin
        {
            'url': 'http://www.lothype.com/blue-devils-drumline-stanford-lot-2016/',
            'md5': 'd16797741b560b485194eddda8121b48',
            'info_dict': {
                'id': 'HNTXWDXV9Is',
                'ext': 'mp4',
                'title': 'Blue Devils Drumline Stanford lot 2016',
                'upload_date': '20160627',
                'uploader_id': 'GENOCIDE8GENERAL10',
                'uploader': 'cylus cyrus',
            },
        },
    ]

    def report_following_redirect(self, new_url):
        """Report information extraction."""
        self._downloader.to_screen('[redirect] Following redirect to %s' % new_url)

    def _extract_rss(self, url, video_id, doc):
        playlist_title = doc.find('./channel/title').text
        playlist_desc_el = doc.find('./channel/description')
        playlist_desc = None if playlist_desc_el is None else playlist_desc_el.text

        entries = []
        for it in doc.findall('./channel/item'):
            next_url = xpath_text(it, 'link', fatal=False)
            if not next_url:
                enclosure_nodes = it.findall('./enclosure')
                for e in enclosure_nodes:
                    next_url = e.attrib.get('url')
                    if next_url:
                        break

            if not next_url:
                continue

            entries.append({
                '_type': 'url',
                'url': next_url,
                'title': it.find('title').text,
            })

        return {
            '_type': 'playlist',
            'id': url,
            'title': playlist_title,
            'description': playlist_desc,
            'entries': entries,
        }

    def _extract_camtasia(self, url, video_id, webpage):
        """ Returns None if no camtasia video can be found. """

        camtasia_cfg = self._search_regex(
            r'fo\.addVariable\(\s*"csConfigFile",\s*"([^"]+)"\s*\);',
            webpage, 'camtasia configuration file', default=None)
        if camtasia_cfg is None:
            return None

        title = self._html_search_meta('DC.title', webpage, fatal=True)

        camtasia_url = compat_urlparse.urljoin(url, camtasia_cfg)
        camtasia_cfg = self._download_xml(
            camtasia_url, video_id,
            note='Downloading camtasia configuration',
            errnote='Failed to download camtasia configuration')
        fileset_node = camtasia_cfg.find('./playlist/array/fileset')

        entries = []
        for n in fileset_node.getchildren():
            url_n = n.find('./uri')
            if url_n is None:
                continue

            entries.append({
                'id': os.path.splitext(url_n.text.rpartition('/')[2])[0],
                'title': '%s - %s' % (title, n.tag),
                'url': compat_urlparse.urljoin(url, url_n.text),
                'duration': float_or_none(n.find('./duration').text),
            })

        return {
            '_type': 'playlist',
            'entries': entries,
            'title': title,
        }

    def _real_extract(self, url):
        if url.startswith('//'):
            return {
                '_type': 'url',
                'url': self.http_scheme() + url,
            }

        parsed_url = compat_urlparse.urlparse(url)
        if not parsed_url.scheme:
            default_search = self._downloader.params.get('default_search')
            if default_search is None:
                default_search = 'fixup_error'

            if default_search in ('auto', 'auto_warning', 'fixup_error'):
                if '/' in url:
                    self._downloader.report_warning('The url doesn\'t specify the protocol, trying with http')
                    return self.url_result('http://' + url)
                elif default_search != 'fixup_error':
                    if default_search == 'auto_warning':
                        if re.match(r'^(?:url|URL)$', url):
                            raise ExtractorError(
                                'Invalid URL:  %r . Call youtube-dl like this:  youtube-dl -v "https://www.youtube.com/watch?v=BaW_jenozKc"  ' % url,
                                expected=True)
                        else:
                            self._downloader.report_warning(
                                'Falling back to youtube search for  %s . Set --default-search "auto" to suppress this warning.' % url)
                    return self.url_result('ytsearch:' + url)

            if default_search in ('error', 'fixup_error'):
                raise ExtractorError(
                    '%r is not a valid URL. '
                    'Set --default-search "ytsearch" (or run  youtube-dl "ytsearch:%s" ) to search YouTube'
                    % (url, url), expected=True)
            else:
                if ':' not in default_search:
                    default_search += ':'
                return self.url_result(default_search + url)

        url, smuggled_data = unsmuggle_url(url)
        force_videoid = None
        is_intentional = smuggled_data and smuggled_data.get('to_generic')
        if smuggled_data and 'force_videoid' in smuggled_data:
            force_videoid = smuggled_data['force_videoid']
            video_id = force_videoid
        else:
            video_id = compat_urllib_parse_unquote(os.path.splitext(url.rstrip('/').split('/')[-1])[0])

        self.to_screen('%s: Requesting header' % video_id)

        head_req = HEADRequest(url)
        head_response = self._request_webpage(
            head_req, video_id,
            note=False, errnote='Could not send HEAD request to %s' % url,
            fatal=False)

        if head_response is not False:
            # Check for redirect
            new_url = head_response.geturl()
            if url != new_url:
                self.report_following_redirect(new_url)
                if force_videoid:
                    new_url = smuggle_url(
                        new_url, {'force_videoid': force_videoid})
                return self.url_result(new_url)

        full_response = None
        if head_response is False:
            request = sanitized_Request(url)
            request.add_header('Accept-Encoding', '*')
            full_response = self._request_webpage(request, video_id)
            head_response = full_response

        info_dict = {
            'id': video_id,
            'title': compat_urllib_parse_unquote(os.path.splitext(url_basename(url))[0]),
            'upload_date': unified_strdate(head_response.headers.get('Last-Modified'))
        }

        # Check for direct link to a video
        content_type = head_response.headers.get('Content-Type', '').lower()
        m = re.match(r'^(?P<type>audio|video|application(?=/(?:ogg$|(?:vnd\.apple\.|x-)?mpegurl)))/(?P<format_id>[^;\s]+)', content_type)
        if m:
            format_id = m.group('format_id')
            if format_id.endswith('mpegurl'):
                formats = self._extract_m3u8_formats(url, video_id, 'mp4')
            elif format_id == 'f4m':
                formats = self._extract_f4m_formats(url, video_id)
            else:
                formats = [{
                    'format_id': m.group('format_id'),
                    'url': url,
                    'vcodec': 'none' if m.group('type') == 'audio' else None
                }]
                info_dict['direct'] = True
            self._sort_formats(formats)
            info_dict['formats'] = formats
            return info_dict

        if not self._downloader.params.get('test', False) and not is_intentional:
            force = self._downloader.params.get('force_generic_extractor', False)
            self._downloader.report_warning(
                '%s on generic information extractor.' % ('Forcing' if force else 'Falling back'))

        if not full_response:
            request = sanitized_Request(url)
            # Some webservers may serve compressed content of rather big size (e.g. gzipped flac)
            # making it impossible to download only chunk of the file (yet we need only 512kB to
            # test whether it's HTML or not). According to youtube-dl default Accept-Encoding
            # that will always result in downloading the whole file that is not desirable.
            # Therefore for extraction pass we have to override Accept-Encoding to any in order
            # to accept raw bytes and being able to download only a chunk.
            # It may probably better to solve this by checking Content-Type for application/octet-stream
            # after HEAD request finishes, but not sure if we can rely on this.
            request.add_header('Accept-Encoding', '*')
            full_response = self._request_webpage(request, video_id)

        first_bytes = full_response.read(512)

        # Is it an M3U playlist?
        if first_bytes.startswith(b'#EXTM3U'):
            info_dict['formats'] = self._extract_m3u8_formats(url, video_id, 'mp4')
            self._sort_formats(info_dict['formats'])
            return info_dict

        # Maybe it's a direct link to a video?
        # Be careful not to download the whole thing!
        if not is_html(first_bytes):
            self._downloader.report_warning(
                'URL could be a direct video link, returning it as such.')
            info_dict.update({
                'direct': True,
                'url': url,
            })
            return info_dict

        webpage = self._webpage_read_content(
            full_response, url, video_id, prefix=first_bytes)

        self.report_extraction(video_id)

        # Is it an RSS feed, a SMIL file, an XSPF playlist or a MPD manifest?
        try:
            doc = compat_etree_fromstring(webpage.encode('utf-8'))
            if doc.tag == 'rss':
                return self._extract_rss(url, video_id, doc)
            elif re.match(r'^(?:{[^}]+})?smil$', doc.tag):
                smil = self._parse_smil(doc, url, video_id)
                self._sort_formats(smil['formats'])
                return smil
            elif doc.tag == '{http://xspf.org/ns/0/}playlist':
                return self.playlist_result(self._parse_xspf(doc, video_id), video_id)
            elif re.match(r'(?i)^(?:{[^}]+})?MPD$', doc.tag):
                info_dict['formats'] = self._parse_mpd_formats(
                    doc, video_id, mpd_base_url=url.rpartition('/')[0])
                self._sort_formats(info_dict['formats'])
                return info_dict
            elif re.match(r'^{http://ns\.adobe\.com/f4m/[12]\.0}manifest$', doc.tag):
                info_dict['formats'] = self._parse_f4m_formats(doc, url, video_id)
                self._sort_formats(info_dict['formats'])
                return info_dict
        except compat_xml_parse_error:
            pass

        # Is it a Camtasia project?
        camtasia_res = self._extract_camtasia(url, video_id, webpage)
        if camtasia_res is not None:
            return camtasia_res

        # Sometimes embedded video player is hidden behind percent encoding
        # (e.g. https://github.com/rg3/youtube-dl/issues/2448)
        # Unescaping the whole page allows to handle those cases in a generic way
        webpage = compat_urllib_parse_unquote(webpage)

        # it's tempting to parse this further, but you would
        # have to take into account all the variations like
        #   Video Title - Site Name
        #   Site Name | Video Title
        #   Video Title - Tagline | Site Name
        # and so on and so forth; it's just not practical
        video_title = self._og_search_title(
            webpage, default=None) or self._html_search_regex(
            r'(?s)<title>(.*?)</title>', webpage, 'video title',
            default='video')

        # Try to detect age limit automatically
        age_limit = self._rta_search(webpage)
        # And then there are the jokers who advertise that they use RTA,
        # but actually don't.
        AGE_LIMIT_MARKERS = [
            r'Proudly Labeled <a href="http://www.rtalabel.org/" title="Restricted to Adults">RTA</a>',
        ]
        if any(re.search(marker, webpage) for marker in AGE_LIMIT_MARKERS):
            age_limit = 18

        # video uploader is domain name
        video_uploader = self._search_regex(
            r'^(?:https?://)?([^/]*)/.*', url, 'video uploader')

        video_description = self._og_search_description(webpage, default=None)
        video_thumbnail = self._og_search_thumbnail(webpage, default=None)

        # Helper method
        def _playlist_from_matches(matches, getter=None, ie=None):
            urlrs = orderedSet(
                self.url_result(self._proto_relative_url(getter(m) if getter else m), ie)
                for m in matches)
            return self.playlist_result(
                urlrs, playlist_id=video_id, playlist_title=video_title)

        # Look for Brightcove Legacy Studio embeds
        bc_urls = BrightcoveLegacyIE._extract_brightcove_urls(webpage)
        if bc_urls:
            self.to_screen('Brightcove video detected.')
            entries = [{
                '_type': 'url',
                'url': smuggle_url(bc_url, {'Referer': url}),
                'ie_key': 'BrightcoveLegacy'
            } for bc_url in bc_urls]

            return {
                '_type': 'playlist',
                'title': video_title,
                'id': video_id,
                'entries': entries,
            }

        # Look for embedded YouTube player
        matches = re.findall(r'''(?x)
            (?:
                <iframe[^>]+?src=|
                data-video-url=|
                <embed[^>]+?src=|
                embedSWF\(?:\s*|
                new\s+SWFObject\(
            )
            (["\'])
                (?P<url>(?:https?:)?//(?:www\.)?youtube(?:-nocookie)?\.com/
                (?:embed|v|p)/.+?)
            \1''', webpage)
        if matches:
            return _playlist_from_matches(
                matches, lambda m: unescapeHTML(m[1]))

        # Look for lazyYT YouTube embed
        matches = re.findall(
            r'class="lazyYT" data-youtube-id="([^"]+)"', webpage)
        if matches:
            return _playlist_from_matches(matches, lambda m: unescapeHTML(m))

        # Look for Wordpress "YouTube Video Importer" plugin
        matches = re.findall(r'''(?x)<div[^>]+
            class=(?P<q1>[\'"])[^\'"]*\byvii_single_video_player\b[^\'"]*(?P=q1)[^>]+
            data-video_id=(?P<q2>[\'"])([^\'"]+)(?P=q2)''', webpage)
        if matches:
            return _playlist_from_matches(matches, lambda m: m[-1])

        matches = DailymotionIE._extract_urls(webpage)
        if matches:
            return _playlist_from_matches(matches)

        # Looking for http://schema.org/VideoObject
        json_ld = self._search_json_ld(
            webpage, video_id, default=None, expected_type='VideoObject')
        if json_ld and json_ld.get('url'):
            info_dict.update({
                'title': video_title or info_dict['title'],
                'description': video_description,
                'thumbnail': video_thumbnail,
                'age_limit': age_limit
            })
            info_dict.update(json_ld)
            return info_dict

        def check_video(vurl):
            if YoutubeIE.suitable(vurl):
                return True
            vpath = compat_urlparse.urlparse(vurl).path
            vext = determine_ext(vpath)
            return '.' in vpath and vext not in ('swf', 'png', 'jpg', 'srt', 'sbv', 'sub', 'vtt', 'ttml')

        def filter_video(urls):
            return list(filter(check_video, urls))

        # Start with something easy: JW Player in SWFObject
        found = filter_video(re.findall(r'flashvars: [\'"](?:.*&)?file=(http[^\'"&]*)', webpage))
        if not found:
            # Look for gorilla-vid style embedding
            found = filter_video(re.findall(r'''(?sx)
                (?:
                    jw_plugins|
                    JWPlayerOptions|
                    jwplayer\s*\(\s*["'][^'"]+["']\s*\)\s*\.setup
                )
                .*?
                ['"]?file['"]?\s*:\s*["\'](.*?)["\']''', webpage))
        if not found:
            # Broaden the search a little bit
            found = filter_video(re.findall(r'[^A-Za-z0-9]?(?:file|source)=(http[^\'"&]*)', webpage))
        if not found:
            # Broaden the findall a little bit: JWPlayer JS loader
            found = filter_video(re.findall(
                r'[^A-Za-z0-9]?(?:file|video_url)["\']?:\s*["\'](http(?![^\'"]+\.[0-9]+[\'"])[^\'"]+)["\']', webpage))
        if not found:
            # Flow player
            found = filter_video(re.findall(r'''(?xs)
                flowplayer\("[^"]+",\s*
                    \{[^}]+?\}\s*,
                    \s*\{[^}]+? ["']?clip["']?\s*:\s*\{\s*
                        ["']?url["']?\s*:\s*["']([^"']+)["']
            ''', webpage))
        if not found:
            # Cinerama player
            found = re.findall(
                r"cinerama\.embedPlayer\(\s*\'[^']+\',\s*'([^']+)'", webpage)
        if not found:
            # Try to find twitter cards info
            # twitter:player:stream should be checked before twitter:player since
            # it is expected to contain a raw stream (see
            # https://dev.twitter.com/cards/types/player#On_twitter.com_via_desktop_browser)
            found = filter_video(re.findall(
                r'<meta (?:property|name)="twitter:player:stream" (?:content|value)="(.+?)"', webpage))
        if not found:
            # We look for Open Graph info:
            # We have to match any number spaces between elements, some sites try to align them (eg.: statigr.am)
            m_video_type = re.findall(r'<meta.*?property="og:video:type".*?content="video/(.*?)"', webpage)
            # We only look in og:video if the MIME type is a video, don't try if it's a Flash player:
            if m_video_type is not None:
                found = filter_video(re.findall(r'<meta.*?property="og:video".*?content="(.*?)"', webpage))
        if not found:
            # HTML5 video
            found = re.findall(r'(?s)<(?:video|audio)[^<]*(?:>.*?<source[^>]*)?\s+src=["\'](.*?)["\']', webpage)
        if not found:
            REDIRECT_REGEX = r'[0-9]{,2};\s*(?:URL|url)=\'?([^\'"]+)'
            found = re.search(
                r'(?i)<meta\s+(?=(?:[a-z-]+="[^"]+"\s+)*http-equiv="refresh")'
                r'(?:[a-z-]+="[^"]+"\s+)*?content="%s' % REDIRECT_REGEX,
                webpage)
            if not found:
                # Look also in Refresh HTTP header
                refresh_header = head_response.headers.get('Refresh')
                if refresh_header:
                    # In python 2 response HTTP headers are bytestrings
                    if sys.version_info < (3, 0) and isinstance(refresh_header, str):
                        refresh_header = refresh_header.decode('iso-8859-1')
                    found = re.search(REDIRECT_REGEX, refresh_header)
            if found:
                new_url = compat_urlparse.urljoin(url, unescapeHTML(found.group(1)))
                self.report_following_redirect(new_url)
                return {
                    '_type': 'url',
                    'url': new_url,
                }

        if not found:
            # twitter:player is a https URL to iframe player that may or may not
            # be supported by youtube-dl thus this is checked the very last (see
            # https://dev.twitter.com/cards/types/player#On_twitter.com_via_desktop_browser)
            embed_url = self._html_search_meta('twitter:player', webpage, default=None)
            if embed_url:
                return self.url_result(embed_url)

        if not found:
            raise UnsupportedError(url)

        entries = []
        for video_url in orderedSet(found):
            video_url = unescapeHTML(video_url)
            video_url = video_url.replace('\\/', '/')
            video_url = compat_urlparse.urljoin(url, video_url)
            video_id = compat_urllib_parse_unquote(os.path.basename(video_url))

            # Sometimes, jwplayer extraction will result in a YouTube URL
            if YoutubeIE.suitable(video_url):
                entries.append(self.url_result(video_url, 'Youtube'))
                continue

            # here's a fun little line of code for you:
            video_id = os.path.splitext(video_id)[0]

            entry_info_dict = {
                'id': video_id,
                'uploader': video_uploader,
                'title': video_title,
                'age_limit': age_limit,
            }

            ext = determine_ext(video_url)
            if ext == 'smil':
                entry_info_dict['formats'] = self._extract_smil_formats(video_url, video_id)
            elif ext == 'xspf':
                return self.playlist_result(self._extract_xspf_playlist(video_url, video_id), video_id)
            elif ext == 'm3u8':
                entry_info_dict['formats'] = self._extract_m3u8_formats(video_url, video_id, ext='mp4')
            elif ext == 'mpd':
                entry_info_dict['formats'] = self._extract_mpd_formats(video_url, video_id)
            elif ext == 'f4m':
                entry_info_dict['formats'] = self._extract_f4m_formats(video_url, video_id)
            else:
                entry_info_dict['url'] = video_url

            if entry_info_dict.get('formats'):
                self._sort_formats(entry_info_dict['formats'])

            entries.append(entry_info_dict)

        if len(entries) == 1:
            return entries[0]
        else:
            for num, e in enumerate(entries, start=1):
                # 'url' results don't have a title
                if e.get('title') is not None:
                    e['title'] = '%s (%d)' % (e['title'], num)
            return {
                '_type': 'playlist',
                'entries': entries,
            }
