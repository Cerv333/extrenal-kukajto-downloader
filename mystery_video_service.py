from json import loads, dumps
from os import path
from typing import Dict, Optional, List

import requests


class MysteryVideoService:
    def __init__(self, cdn_upload_url: str, root_url: str, access_token: str, cdn_access_token: str):
        self._access_token = access_token
        self._root_url = root_url
        self._cdn_upload_url = cdn_upload_url

    def upload_all(self, source_id: int, input_data: Dict[str, Dict[str, any]]) -> Dict[str, bool]:
        res = {}
        for lang in input_data:
            lang_data = input_data[lang]
            video_id = self.upload_video(lang_data['video_path'], source_id, lang, list(lang_data['subtitles'].keys()))
            if video_id is not None:
                for subtitle_lang in lang_data['subtitles']:
                    self.upload_subtitle(video_id, lang_data['subtitles'][subtitle_lang], subtitle_lang)
            res[lang] = bool(video_id)
        return res

    def upload_video(self, video_path: str, source_id: int, lang: str, subtitle_langs: List[str]) -> Optional[int]:
        try:
            headers = {
                "Authorization": f"Bearer {self._access_token}"
            }
            body = {
                'sourceId': source_id,
                'metaData': {
                    'lang': lang,
                    'subtitles': subtitle_langs,
                }
            }
            res_video = requests.post(f"{self._root_url}/videos", headers=headers, json=body)
            res_video.raise_for_status()
            video = res_video.json()

            res_upload_rec = requests.get(f"{self._root_url}/videos/{video['id']}/upload", headers=headers)
            res_upload_rec.raise_for_status()
            upload_rec = res_upload_rec.json()

            data = {
                'nonce': upload_rec['nonce'],
                'params': upload_rec['params'],
                'project': upload_rec['project'],
                'response': upload_rec['response'],
                'signature': upload_rec['signature'],
            }

            res_upload = requests.post(self._cdn_upload_url, data=data, files={'file': (path.basename(video_path), open(video_path, 'rb'))})
            res_upload.raise_for_status()
            res_data = res_upload.json()
            print(f"Upload complete: {video_path}")
            return res_data['files'][0]
        except Exception as e:
            print(f"Error uploading video: {e}")
            return None

    def upload_subtitle(self, video_id: int, subtitle: str, lang: str) -> bool:
        headers = {
            'X-Auth-Token': self._access_token,
            'Content-Type': 'application/json'
        }
        body = dumps({'subtitle': subtitle})
        print(body)
        res = requests.post(f"https://api.premiumcdn.net/api/v1/files/{video_id}/subtitles/{lang}", headers=headers, data=body)
        ok = res.status_code == 200
        if not ok:
            print(f"Error uploading subtitle [{lang}]: {res.status_code} {res.text}")
        else:
            print(f"Subtitle [{lang}] uploaded successfully")
        return ok
