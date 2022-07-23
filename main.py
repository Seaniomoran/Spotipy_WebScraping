from bs4 import BeautifulSoup
import requests
import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


BILLBOARD_URL = "https://www.billboard.com/charts/hot-100"


date = input("What day would you like to travel to? enter in YYYY-MM-DD: ")
# date = "1966-08-28"


response = requests.get(f'{BILLBOARD_URL}/{date}')
soup = BeautifulSoup(response.text, "html.parser")
soup.encode("utf-8")

song_names_spans = soup.find_all("h3", id="title-of-a-story")
song_names = [song.getText().strip() for song in song_names_spans[6::4]]

print(song_names)

year = date.split("-")[0]

if len(song_names) < 95:
    song_names = [song.getText().strip() for song in song_names_spans[4::]]

duplicates = []
new_list = []

for i in song_names:
    if i not in new_list:
        new_list.append(i)
    else:
        duplicates.append(i)
for i in duplicates:
    try:
        new_list.remove(i)
    except ValueError:
        print(i)

song_names = new_list

print(song_names[99])
print(song_names)


artist_names_spans = soup.find_all("span", class_="c-label")
unedited_artist_list = [artist.getText().strip() for artist in artist_names_spans]
artist_names = []

#
for i in unedited_artist_list:
    try:
        int(i)
    except ValueError:
        if i != 'NEW' and i != '-':
            try:
                p = i.split("Featuring")
                i = p[0]
            finally:
                artist_names.append(i)

print(len(song_names))
print(song_names)
print(len(artist_names))



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback/",
        client_id=os.getenv("SPOTIPY_CLIENT-ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)
track_ids = []
missed_songs_index = []
year = date.split("-")[0]

for i in range(len(song_names)-1):
    if i < 100:
        track = song_names[i]
        try:
            artist = artist_names[i]
            track_id = sp.search(q=f"artist:{artist} track:{track}", type='track')
            track_ids.append(track_id["tracks"]["items"][0]["id"])
        except IndexError:
            missed_songs_index.append(i)

print(missed_songs_index)
print(len(track_ids))
for i in missed_songs_index:
    if i < 100:
        try:
            track = song_names[i]
            track_id = sp.search(q=f"track:{track} year:{year}", type='track')
            track_ids.append(track_id["tracks"]["items"][0]["id"])
        except ValueError or IndexError:
            print(track)
            print(artist_names[i])
            print(i)

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=track_ids)




