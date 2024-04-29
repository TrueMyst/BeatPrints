import requests


class Lyrics:
    def __init__(self, MXM_USERTOKEN, LF_USERTOKEN):
        self.mxm_base_url = (
            "https://apic-desktop.musixmatch.com/ws/1.1/macro.subtitles.get?"
        )
        self.lf_base_url = "https://lyrics.lyricfind.com/api/v1/search?"
        self.mxm_usertoken = MXM_USERTOKEN
        self.lf_usertoken = LF_USERTOKEN

    def get_lyrics(self, track_name: str, artist_name: str):

        mxm_params = {
            "format": "json",
            "namespace": "lyrics_synched",
            "app_id": "web-desktop-app-v1.0",
            "subtitle_format": "mxm",
            "q_track": track_name,
            "q_artist": artist_name,
            "usertoken": self.mxm_usertoken,
        }

        mxm_response = requests.get(self.mxm_base_url, params=mxm_params)
        mxm_data = (
            mxm_response.json()
            .get("message", {})
            .get("body", {})
            .get("macro_calls", {}))

        lf_params = {
            "reqtype": "default",
            "territory": "BD",
            "searchtype": "track",
            "all": f"{artist_name} {track_name} ",
            "all-tracks": "no",
            "limit": 1,
            "output": "json",
        }

        lf_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Authorization": f"Bearer {self.lf_usertoken}",
        }

        lf_response = requests.get(
            self.lf_base_url, params=lf_params, headers=lf_headers
        )

        lf_data = lf_response.json().get("tracks", [])

        try:
            if mxm_data:
                mxm_lyrics = (
                    mxm_data.get("track.lyrics.get", {})
                    .get("message", {})
                    .get("body", {})
                    .get("lyrics", {})
                )

                lyrics = mxm_lyrics.get("lyrics_body", "")

                return lyrics

            elif lf_data:
                lf_track = lf_data[0].get("slug")
                lf_track_url = f"https://lyrics.lyricfind.com/_next/data/K8lnjb_309zmz7XOhQHFu/en-US/lyrics/{lf_track}.json?songSlug={lf_track}"
                lf_response = requests.get(lf_track_url, headers=lf_headers)
                lf_json = lf_response.json().get("pageProps", {}).get("songData", {})

                lyrics = lf_json.get("track", {}).get("lyrics", "")

                return lyrics

        except Exception:
            raise Exception
