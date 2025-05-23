from os import path
from typing import Dict

import yt_dlp
from requests import Session

from const import MIME_TYPE_M3U8_APPLE, MIME_TYPE_MP4, mime_to_ext, MIME_TYPE_VTT
from lib.error import WorkerError


class Downloader:
    def __init__(self, temp_folder: str, input_data: dict):
        self._temp_folder = temp_folder
        self._input_data = input_data
        zombie = input_data.get('zombie')
        self._filename = input_data.get('filename')
        self._proxy = zombie.get('proxy') if zombie else None
        self._zombie_id = zombie.get('id') if zombie else None

    def download_all(self) -> dict:
        videos = {}
        for lang_video in self._input_data['lang_videos']:
            stream_rec = lang_video['stream_rec']
            if stream_rec:
                try:
                    lang_video_res = {
                        'video_path': self.download_video(lang_video['stream_rec'], lang_video['lang'])
                    }
                    subtitle_dict: Dict[str, str] = {}

                    for subtitle in lang_video['subtitles']:
                        subtitle_dict[subtitle['lang']] = self.download_subtitle(subtitle['stream_rec'])
                    lang_video_res['subtitles'] = subtitle_dict

                    videos[lang_video['lang']] = lang_video_res
                except Exception as e:
                    print(f"Error downloading video for language {lang_video['lang']}: {e}")

        return videos

    def get_filename(self, lang: str, extension: str) -> str:
        return path.join(self._temp_folder, f"{self._filename.format(lang.upper())}.{extension}")

    def download_video(self, stream_rec: dict, lang: str) -> str:
        mime_type = stream_rec['mime_type']
        if mime_type == MIME_TYPE_M3U8_APPLE:
            return self.download_m3u8(stream_rec, lang)
        elif mime_type == MIME_TYPE_MP4:
            return self.download_file(stream_rec, lang)
        else:
            raise WorkerError(f'Unsupported mime type for video: {mime_type}')

    def download_m3u8(self, stream_rec: dict, lang: str) -> str:
        filename = self.get_filename(lang, 'mp4')

        options = {
            'outtmpl': filename,
            'noplaylist': True,
            'merge_output_format': 'mp4',
            'format': 'best',
            'proxy': self._proxy,
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([stream_rec['url']])

        return filename

    def download_file(self, stream_rec: dict, lang: str) -> str:
        chunk_size = 2 * 1024 * 1024
        total = 0
        output_path = self.get_filename(lang, mime_to_ext[stream_rec['mime_type']])

        http_session = Session()
        http_session.proxies = {
            'http': self._proxy,
            'https': self._proxy
        }

        print(f"Downloading file from {stream_rec['url']} to {output_path}")
        with http_session.get(stream_rec['url'], stream=True) as response:
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        total += len(chunk)
                        print(f"Downloaded {total / (1024 * 1024):.2f} MB", end="\r")
        print(f"Downloaded to: {output_path}")
        return output_path

    def download_subtitle(self, stream_rec: dict) -> str:
        mime_type = stream_rec['mime_type']
        if mime_type == MIME_TYPE_VTT:
            http_session = Session()
            http_session.proxies = {
                'http': self._proxy,
                'https': self._proxy
            }
            response = http_session.get(stream_rec['url'])
            response.raise_for_status()
            print(f"Downloaded subtitle from {stream_rec['url']}")
            return response.text
        else:
            raise WorkerError(f'Unsupported mime type for video: {mime_type}')


