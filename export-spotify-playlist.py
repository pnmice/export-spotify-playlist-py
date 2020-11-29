#!/usr/local/bin/python3.9

from __future__ import print_function
import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def show_tracks():

    # Message to show something is really happening
    # Print to stderr so it does not end up in > redirected output
    print("Processing batch of tracks (stderr msg)", file=sys.stderr)

    for i, item in enumerate(tracks['items']):
        
        track = item['track']
        
        # Secondary query for album details
        album = sp.album(track['album']['uri'])
        
        output = ["{:s}".format(track['artists'][0]['name']),
                  "{:s}".format(album['name']),
                  "{:s}".format(track['name']),
                  "{:02d}".format(track['track_number']),
                  "{:02d}".format(track['disc_number']),
                  "{:d}".format(track['duration_ms']),
                  "{:s}".format(album['release_date']),
                  "{:s}".format(album['release_date_precision']),
                  ]
        
        # Form and print the ; separated string
        print(";".join(output))


if __name__ == '__main__':

    if len(sys.argv) != 2: 
        print("Whoops, need exactly one argument ...")
        print("usage: python export-spotify-playlist.py playlist_uri")
        sys.exit()
    else:
        playlist_uri = sys.argv[1]
        playlist_id = playlist_uri.split(':')[2]

    # Spotipy login
    token = SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                     client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])

    if token:
        sp = spotipy.Spotify(auth_manager=token)
        # return spotify
        fields = "tracks,next"
       
        # Primary query for tracks in playlist
        results = sp.playlist(playlist_id, fields=fields)

        tracks = results['tracks']
      
        # Process tracks as long as there are more tracks
        # One request per track to get album date
        show_tracks()
        while tracks['next']:
            
            # Get next batch of tracks
            tracks = sp.next(tracks)
            show_tracks()
        
    else:

        print("Can't get token for (can't login) ")
