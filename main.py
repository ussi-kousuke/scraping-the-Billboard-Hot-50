from bs4 import BeautifulSoup
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
import json
from pprint import pprint
# 6f8056bbc55f4712b910e27d344f03f9
# 7ed0191962844fab88773e75d15367d7
# CLIENT_SECRET = '7ed0191962844fab88773e75d15367d7'
# すべてのシステム変数を所得: Get-ChildItem env:
CLIENT_ID = os.environ.get('MY_UNIQUE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('MY_UNIQUE_CLIENT_SECRET')
# question = input('which year do you want to travel to? Type the date in this format YYYY-MM-DD:')

response = requests.get(url='https://www.uta-net.com/close_up/2021_ranking')
soup = BeautifulSoup(response.text, "html.parser")
get_title = soup.find_all(name='td', class_='songs_td1')
song_name = [title.getText() for title in get_title]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri='https://example.com/',
        show_dialog=True,
        cache_path="token.txt"

    )
)

user_id = sp.current_user()['id']
song_list = []
for song in song_name:
    results = sp.search(q=f"track:{song}", type='track')
    # print(results)

    try:
        music_url = results['tracks']['items'][0]['uri']
        song_list.append(music_url)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_list)

create_playlist = sp.user_playlist_create(user=user_id, name='2021 hit medley', public=False, collaborative=False)
print(create_playlist)
sp.playlist_add_items(playlist_id=create_playlist['id'], items=song_list)
