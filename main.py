from urllib import response
from dotenv import load_dotenv
import shotstack_sdk as shotstack
import os
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.title_asset import TitleAsset
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.model.transition  import Transition
from shotstack_sdk.model.html_asset  import HtmlAsset
from shotstack_sdk.model.audio_asset import AudioAsset

from pexel_assest_fetcher import pexel_searcher
load_dotenv()

shotstack_url           = os.getenv("SHOTSTACK_HOST")
shotstack_api_key       = os.getenv("SHOTSTACK_API_KEY")
shotstack_assets_url    = os.getenv("SHOTSTACK_ASSETS_URL")
configuration = shotstack.Configuration(host = shotstack_url)
configuration.api_key['DeveloperKey'] = shotstack_api_key

mcferin_mp3 ="https://feeds.soundcloud.com/stream/824693758-unminus-majesty.mp3"

def submit(data):
    pexel_videos = pexel_searcher(data.get('input_text'))
    min_clips   = 4.0
    max_clips   = 8.0
    clip_length = 4.0
    video_start = 4.0

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)
        video_clips  = []
        Caption_clips = []
        audio_clips = []

        title_asset = TitleAsset(
            text        = data.get('title'),
            style       = "minimal",
            size        = "small"
        )

        title_transition = Transition(
            _in="fade",
            out="fade"
        )

        title_clip = Clip(
            asset       = title_asset,
            length      = video_start,
            start       = 0.0,
            transition  = title_transition,
            effect      = "zoomIn"
        )

        for index, video in enumerate(pexel_videos):
            # if index >= max_clips:
            #     break
            
            hd_file = None
            videos  = pexel_videos

            # for entry in videos:
            #     if entry.get('height') == 720 or entry.get('width') == 1920:
            #         hd_file = entry

            if hd_file is None:
                hd_file = videos[index]
            
            # ---CAPTIONS---------------
            # htmlAsset = HtmlAsset(
            # html      = f'<p>{video["keyword_caption"]}</p>',
            # css       = 'p { color: #FFFF00; }',
            # # width     = 800,
            # # height    = 100,
            # background= 'transparent',
            # position  = 'bottom'
            # )

            title_asset = TitleAsset(
            text        = video["keyword_caption"],
            style       = "subtitle",
            size        = "small",
            color      = '#FFFF00',
            position   = 'bottom',
            background = '#000000',
            )


            Caption_clip = Clip(
                asset     = title_asset,
                start = video_start + (index * clip_length),
                length    = clip_length,
                fit       = 'crop',
                scale     = 0.0,
                position  = 'bottom',
                opacity   = 1.0,
            )

            Caption_clips.append(Caption_clip)
            
            #---------audio_per-clip---------
            audio_asset = AudioAsset(
                src= mcferin_mp3,
                trim= 2.0
            )
            audio_clip = Clip(
                asset = audio_asset,
                start = video_start + (index * clip_length),
                length= clip_length
            )

            audio_clips.append(audio_clip)

            #-------VIDEO----------------
            video_asset = VideoAsset(
                src = hd_file.get('link'),
                trim= 2.0
            )

            video_clip = Clip(
                asset = video_asset,
                start = video_start + (index * clip_length),
                length= clip_length
            )

            video_clips.append(video_clip)

            title_transition = Transition(
                _in="fade",
                out="fade"
            )

        soundtrack = Soundtrack(
            volume      = 0.25,
            # src         = f"{shotstack_assets_url}music/{data.get('soundtrack')}.mp3",
            src         = data.get('soundtrack'),
            # src         = "https://feeds.soundcloud.com/stream/824693758-unminus-majesty.mp3",
            effect      = "fadeOut"
        )

        timeline = Timeline(
            background  = "#000000",
            soundtrack  = soundtrack,
            tracks      = [Track(clips=Caption_clips),Track(clips=video_clips),Track(clips=[title_clip]),Track(clips=audio_clips)]
        )

        output = Output(
            format      = "mp4",
            resolution  = "sd"
        )

        edit = Edit(
            timeline    = timeline,
            output      = output
        )

        return api_instance.post_render(edit)['response']

def status(render_id):
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)
        return api_instance.get_render(render_id, data=True, merged=True)['response']


if __name__ == '__main__':
    # import time
    # para = "Rabbit & tortoise decided to settle the argument with a race. They agreed on a route and started off the race. The rabbit shot ahead and ran briskly for some time. Then seeing that he was far ahead of the tortoise, he thought he'd sit under a tree for some time and relax before continuing the race. He sat under a tree and soon fell asleep."
    # request = {'title': 'Rabbit & tortoise', 'soundtrack': "https://feeds.soundcloud.com/stream/824693758-unminus-majesty.mp3",
    # 'input_text':para}
    # response = submit(request)
    # print(response)
    # time.sleep(60)
    # print(status(response.id))
    print(status('c226e6fc-9909-4005-8391-db3a48cf0d09'))
    # # print(status("b319fa2f-ad66-4274-a7c5-bf99d2b1bad3"))
    # var = pexel_searcher('asd')
    # print(var)
    