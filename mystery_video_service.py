from os import path
from typing import Dict

import requests


class MysteryVideoService:
    def __init__(self, cdn_upload_url: str, root_url: str, access_token: str):
        self._access_token = access_token
        self._root_url = root_url
        self._cdn_upload_url = cdn_upload_url

    def upload_all(self, source_id: int, input_data: Dict[str, Dict[str, any]]) -> Dict[str, bool]:
        res = {}
        for lang in input_data:
            ok = self.upload_video(input_data[lang]['video_path'], source_id, lang)
            res[lang] = ok
        return res

    def upload_video(self, video_path: str, source_id: int, lang: str) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {self._access_token}"
            }
            body = {
                'sourceId': source_id,
                'metaData': {
                    'lang': lang
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
            print(f"Upload complete: {video_path}")
            return True
        except Exception as e:
            print(f"Error uploading video: {e}")
            return False

