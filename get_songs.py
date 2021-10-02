from youtubesearchpython import VideosSearch


class GetSongs(VideosSearch):

    def get_from_youtube(self, text, song_result_limit=1):
        """
        Get Songs from youtube
        :param song_result_limit: To Query limitation to search
        :param text:
        :return:Song Link And Title
        """
        videos_search = VideosSearch(text, limit=song_result_limit)

        info = videos_search.result()["result"]

        for i in info:
            return [i["link"], i["title"]]
            # print(i["title"])
            # print(i["link"])
