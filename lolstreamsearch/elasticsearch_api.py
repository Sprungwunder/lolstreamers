# elasticsearch_api.py
from .yt_es_documents import YtVideoDocument


class YtVideoElasticAPI:
    @staticmethod
    def get_all_videos(query):
        # Führe eine Suche mit dem YtVideoDocument durch
        search = YtVideoDocument.search()
        response = search.execute()
        return response
