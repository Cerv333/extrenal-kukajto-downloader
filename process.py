import tempfile
import time

from config import config
from downloader import Downloader
from lib.spine import SpineMessanger, SpineError
from lib.spine.core import TaskSubProcessRecord, TaskSubProcessServiceRec
from mystery_video_service import MysteryVideoService


def run_process():
    while True:
        try:
            with SpineMessanger(config.SPINE_ACCESS_TOKEN, TaskSubProcessRecord('tigalo-movie-kukajto-scraper', 'tigalo-movie-kukajto-scraper-downloader')) as messanger:
                print(f"Connected to Spine server. Client id: {messanger.client_id}")
                service_provider = messanger.create_service(TaskSubProcessServiceRec('tigalo-movie-kukajto-scraper-downloader', True, 'tigalo-movie-kukajto-scraper', 'downloader'))
                print(f"Service provider. Service id: {service_provider.service_id}")
                for consumer in service_provider:
                    try:
                        data = consumer.receive_message(7200)
                        if data.get('msg_type') == 'request':
                            print(f"Received message: {data}")
                            video_data = data['video']
                            with tempfile.TemporaryDirectory() as temp_folder:
                                downloader = Downloader(temp_folder, video_data)
                                videos = downloader.download_all()

                                print(f"Downloaded videos: {videos}")
                                uploader = MysteryVideoService(config.CDN_UPLOAD_URL, config.MYSTERY_VIDEO_API_URL, config.MYSTERY_VIDEO_ACCESS_TOKEN, config.CDN_ACCESS_TOKEN)
                                uploaded_res = uploader.upload_all(video_data['source_id'], videos)
                                result_data = {
                                    'msg_type': 'response',
                                    'source_id': video_data['source_id'],
                                    'result': uploaded_res
                                }
                                consumer.send_message(result_data)
                                print(f"Sent response: {result_data}")
                    except SpineError as e:
                        print(f"Spine error: {e}")
                        consumer.close()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(6)
            print('Reconnecting...')
