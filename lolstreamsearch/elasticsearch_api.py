# elasticsearch_api.py
from typing import List
from .yt_es_documents import YtVideoDocument


class YtVideoElasticAPI:
    @staticmethod
    def get_all_videos(query) -> List[YtVideoDocument]:
        search = YtVideoDocument.search()
        response = search.execute()
        return response
