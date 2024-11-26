import requests
from bs4 import BeautifulSoup
import json

url_for_test = "https://open.spotify.com/playlist/6SHh1LkdNz0be2NIGIb11Q"

# for songs data-encore-id="listRowTitle"
# for songs artist data-encore-id="listRowSubtitle"

import threading

class playlist:

    def __init__(self, link):
        self.link = link
        self.plist = []
        self.tag = []
        self.cover = []

    def extract_tag(self, track_id):
        # listrow-title-track-spotify:track:5zT5cMnMKoyruPj13TQXGx-1
        ans = ""
        slash_check = False
        for i in range(len(track_id) - 1, 0, -1):
            if track_id[i] == ":":
                break
            if slash_check == True:
                ans = ans + track_id[i]
            if slash_check == False and track_id[i] == "-":
                slash_check = True
        return ans[::-1]

    def print_html(self):
        respone = requests.get(self.link)
        if respone.status_code == 200:
            soup = BeautifulSoup(respone.text)
            print(soup.prettify())
        else:
            print("there is a problem in the respone", respone.status_code)

    def get_playlist(self):
        respone = requests.get(self.link)
        self.respone = respone
        if respone.status_code == 200:
            soup = BeautifulSoup(respone.text, "html.parser")
            elements = soup.find_all("p", attrs={"data-encore-id": "listRowTitle"})
            for e in elements:
                self.plist.append(e.find("span").text)
                self.tag.append(self.extract_tag(e["id"]))
            elements = soup.find_all("img", attrs={"data-encore-id": "image"})
            for e in elements:
                self.cover.append(e["src"])
        else:
            print(
                "there is an ERROR generating playlist check the link and the tag/id for the playlist"
            )

    def validate_link(self):
        respone = requests.get(self.link)
        if respone.status_code == 200:
            return True
        else:
            return False

    def get_playlist_json(self):
        if len(self.plist) == 0:
            print("playlist is not generated running the get_playlist now")
            self.get_playlist()
        playlist_dict = dict(zip(self.plist, self.tag))
        print(playlist_dict)
        json_file = json.dumps(playlist_dict, indent=4)
        return json_file

    def print_list(self):
        if len(self.plist) == 0:
            print("List is Empty")
        for song in self.plist:
            print(song)
        for tag in self.tag:
            print(tag)

    def print_covers(self):
        if len(self.cover) != 0:
            for i in self.cover:
                print(i)

    def get_song(self, rank):
        print(self.plist[rank])
        print(self.tag[rank])


def main():
    main_runner = playlist(url_for_test)
    main_runner.get_playlist_json()
    main_runner.print_covers()


if __name__ == "__main__":
    main()
