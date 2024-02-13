from typing import Optional

import requests


def get_playlist_items(id: str, key: str) -> Optional[list[str]]:
    ids: list[str] = []

    nextPageToken: Optional[str] = None

    url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?playlistId={id}&part=contentDetails&maxResults=50&key={key}"

    while True:
        response = requests.get(url if not nextPageToken else url +
                                f"&pageToken={nextPageToken}")

        data: dict = response.json()

        if response.status_code != 200:
            raise ValueError(f"Error: {data}")

        for video in data["items"]:
            ids.append(video["contentDetails"]["videoId"])

        nextPageToken = data.get("nextPageToken", None)
        if not nextPageToken:
            # done
            return ids
