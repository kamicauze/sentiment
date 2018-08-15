from google.oauth2 import service_account
import googleapiclient.discovery
import time
import re

from  textblob import  TextBlob


DEVELOPER_KEY = "AIzaSyDh61htnqkFivC0eC62LUPslv4vdpjGonw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY )

comments = []
comms = []
videos = []
def video_comments(video_id, max_results=10):

    results = youtube.commentThreads().list(
        videoId=video_id,
        part="id,snippet",
        order="relevance",
        textFormat="plainText",
        maxResults=max_results % 101
    ).execute()



    for result in results['items']:
        comment = {}
        comment['id'] = result['id']
        comment['text'] = result['snippet']['topLevelComment']['snippet']['textOriginal']
        comment['likes'] = result['snippet']['topLevelComment']['snippet']['likeCount']
        comments.append(comment)

    return comments


def youmagic():

    video_comments('D8LFwC1nEpU')
    for comment in comments:
        comnt = comment['text']

        def clean_text(teext):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", teext).split())

        def get_comm_sentiment(teext):
            blob = TextBlob(clean_text(teext))
            if blob.sentiment.polarity > 0.0:
                return 'positive'
            elif blob.sentiment.polarity == 0.0:
                return 'neutral'
            else:
                return 'negative'

        prop = get_comm_sentiment(comnt)

        def create_list():

            comms.append({'comment':comnt, 'sent':prop})
            print comms
        create_list()

query = "short and sweet"

def youtube_search(query, max_count=5):
    search_results =youtube.search().list(

        q=query,
        part="id,snippet",
        type= "video",
        maxResults= max_count).execute()
    for result in search_results['items']:

        video = {}
        video['id'] = result['id']['videoId']
        video['title'] = result['snippet']['title']
        video['thumbnail'] = result['snippet']['thumbnails']

        videos.append(video)

    print videos


youtube_search(query)



