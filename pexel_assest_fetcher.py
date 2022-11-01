import os
from pexelsapi.pexels                import Pexels
from dotenv import load_dotenv


from extract_keywords_for_each_sentence import our_keyword_extractor
load_dotenv()

def pexel_searcher(para):
    '''
    for given para , uses nlp to find keywords and gets relevent assets from pixel
    para: String
    Output: list[Dict]
    '''

    # para='there is a decline in bitcoin price nowadays. This is due to ongoing war between russia and ukraine. The market is also taking a toll. The dollar is facing inflation. Alleluia praise the Lord.'
    # para = "They decided to settle the argument with a race. They agreed on a route and started off the race. The rabbit shot ahead and ran briskly for some time. Then seeing that he was far ahead of the tortoise, he thought he'd sit under a tree for some time and relax before continuing the race. He sat under the tree and soon fell asleep."
    # para = "The last goal doesn’t matter. The last victory, already forgotten. Yesterday is gone. Lost, in the record books. But today is up for grabs. Unpredictable. Unwritten. Undecided. “Now” is ours. Do something and be remembered. Or do nothing and be forgotten. No one owns today. Take it"
    print(para)
    keyphrases_list,sentences = our_keyword_extractor(para=para)
    pexels_api_key          = os.getenv("PEXELS_API_KEY")
    api                     = Pexels(pexels_api_key)
    pexel_videos = []

    for sentence_index, keyword in enumerate(keyphrases_list):
        hd_file = None    
        search_videos = api.search_videos(
            query           = keyword,
            orientation     = '', size='', color='', locale='', page=1,
            per_page        = 1
        )
        for index, video in enumerate(search_videos.get('videos')):
            videos  = video.get('video_files')
            for entry in videos:
                if entry.get('height') == 720 or entry.get('width') == 1920:
                    hd_file = entry
            if hd_file is None:
                hd_file = videos[0]
            hd_file['keyword_queried'] = keyword
            hd_file["keyword_caption"] = sentences[sentence_index]
        print(f"DEBUG: {hd_file} \n")
        pexel_videos.append(hd_file)
    return pexel_videos

if __name__ == "__main__":
    para = "They decided to settle the argument with a race. They agreed on a route and started off the race. The rabbit shot ahead and ran briskly for some time. Then seeing that he was far ahead of the tortoise, he thought he'd sit under a tree for some time and relax before continuing the race. He sat under the tree and soon fell asleep."
    var = pexel_searcher(para)
    print(var)
    