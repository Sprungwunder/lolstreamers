import json
import os

import requests
from typing import List, Dict


def load_initial_data() -> List[Dict]:
    with open('../api/initial_data.json', 'r') as file:
        return json.load(file)


def index_documents(documents: List[Dict], es_host: str, index_name: str, api_key) -> None:
    """
    Index documents into Elasticsearch
    """
    headers = {'Content-Type': 'application/json',
               'Authorization': f'ApiKey {api_key}'}

    for doc in documents:
        doc_id = doc['video_url'].split('watch?v=')[1].split('&')[0]  # Extract YouTube video ID
        url = f"{es_host}/{index_name}/_doc/"

        try:
            response = requests.post(url, headers=headers, json=doc, verify=False)
            if response.status_code in (200, 201):
                print(f"Successfully indexed document with ID: {doc_id}")
            else:
                print(f"Failed to index document {doc_id}. Status: {response.status_code}")
                print(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error indexing document {doc_id}: {str(e)}")


def main():
    # Configuration
    es_host = os.getenv("ELASTIC_HOST")
    api_key = os.getenv("ELASTIC_BULK_API_KEY")
    verify_certs = False,
    index_name = "lolstreamsearch_yt_videos"

    # Load documents
    documents = load_initial_data()

    # Index documents
    index_documents(documents, es_host, index_name, api_key)


if __name__ == "__main__":
    main()
