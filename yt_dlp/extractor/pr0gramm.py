from .common import InfoExtractor


class Pr0grammIE(InfoExtractor):
    _VALID_URL = r'(?:https?://)?(?:www\.)?pr0gramm\.com/top(?:/[a-zA-Z0-9 üöäß?]+)?/(?P<id>[0-9]+)'
    _TESTS = [{
        'url': 'https://pr0gramm.com/top/4993614',
        'md5': '96c12f89839979af834b7420136b505f',
        'info_dict': {
            'id': '4993614',
            'ext': 'mp4',
            'title': '4993614',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # TODO: We'll probably need this in the future to extact tags and comments.
        # webpage = self._download_webpage(url, video_id)

        api_response = self.get_from_api(video_id)

        image_path = api_response.get('image')
        thumbnail_path = api_response.get('thumb')

        return {
            'id': video_id,
            'title': video_id,  # TODO: There is no title for Pr0gramm videos. Maybe we just use the video id?
            'description': "video description",  # TODO: There is also no description for Pr0gramm videos...

            # TODO: These should probably be None if the paths are not set at all.
            'url': f"https://vid.pr0gramm.com/{image_path}",
            'thumbnail': f"https://thumb.pr0gramm.com/{thumbnail_path}",

            'uploader_id': api_response.get('userId'),

            # This does not work right now, because the page does not contain the user if there is no JS to load the content.
            # 'uploader': self._search_regex(r'<a [^>]+class="user[^>]+>([a-zA-Z0-9]+)</a>', webpage, 'uploader', fatal=False, default=None),

            'timestamp': api_response.get('created'),

            # TODO: more properties (see yt_dlp/extractor/common.py)
            # comments, comment_count, tags, upload_date
        }

    def get_from_api(self, id):
        full_api_result = self._download_json(f"https://pr0gramm.com/api/items/get?id={id}", id)
        return next((r for r in full_api_result["items"] if r["id"] == int(id)), None)
