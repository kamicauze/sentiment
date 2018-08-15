def video_comments(video_id, max_results=200):
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
    video_comments(searchterm2)
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

            comms.append({'comment': comnt, 'sent': prop})

        create_list()


youmagic()
ptweets = [comment for comment in comms if comment['sent'] == 'positive']

val1 = (100 * len(ptweets) / len(comms))
ntweets = [comment for comment in comms if comment['sent'] == 'negative']
val2 = 100 * len(ntweets) / len(comms)

newtweets = [comment for comment in comms if comment['sent'] == 'neutral']
val3 = 100 * len(newtweets) / len(comms)

vako = [val1, val2, val3]

return render_template("youtube.html", title='youtube', comments=comms, searchterm=searchterm2, vako=vako,
                       lables=lables, videos=videos)
