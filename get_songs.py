from youtubesearchpython import VideosSearch


def get_from_youtube(text, song_result_limit=1):
    """
    Get Songs from youtube
    :param text:
    :return:
    """
    videosSearch = VideosSearch(text, limit=song_result_limit)

    info = videosSearch.result()["result"]

    for i in info:
        return [i["link"], i["title"]]
        # print(i["title"])
        # print(i["link"])
