from xbmcjson import XBMC
from bottle import route, run, template, redirect, static_file, request
import os

#TODO
#start on correct ip (pass as argument?)
#add head info to templates

#config
hostname = "0.0.0.0"
hostport = 8000
path_for_files = ""
#endconfig

xbmc = XBMC("http://192.168.0.5/jsonrpc", "xbmc", "xbmc")

def get_playlistid():
	player = xbmc.Player.GetActivePlayers()
	if len(player['result']) > 0:
		playlist_data = xbmc.Player.GetProperties({"playerid":0, "properties":["playlistid"]})
		if len(playlist_data['result']) > 0 and "playlistid" in playlist_data['result'].keys():
			return playlist_data['result']['playlistid']

	return -1

def get_playlist():
	playlistid = get_playlistid()
	if playlistid >= 0:
		data = xbmc.Playlist.GetItems({"playlistid":playlistid, "properties": ["title", "album", "artist", "file"]})
		position_data = xbmc.Player.GetProperties({"playerid":0, 'properties':["position"]})
		position = int(position_data['result']['position'])
		return data['result']['items'][position:], position
	return [], -1

def get_artists():
	data = xbmc.AudioLibrary.GetArtists()
	return data['result']['artists']

def get_artist_name(id):
	for artist in get_artists():
		if artist['artistid'] == int(id):
			return artist['label']

def get_songs(id):
	data = xbmc.AudioLibrary.GetSongs({"filter":{"artistid":int(id)}})
	return data['result']['songs']

def get_albums(id):
	data = xbmc.AudioLibrary.GetAlbums({"filter":{"artistid":int(id)}})
	return data['result']['albums']

def remove_duplicates(playlistid):
	songs = []
	position = 0
	playlist, not_needed = get_playlist()
	for song in playlist:
		if song['file'] in songs:
			xbmc.Playlist.Remove({"playlistid":int(playlistid), "position":int(position)})
		songs.append(song['file'])
		position = position + 1

@route('/juke')
#need to add check for radio -- this could be in template -- or just add skip
def index():
	current_playlist, position = get_playlist()
	return template('list', playlist=current_playlist, offset = position)

@route('/artists/')
def index():
	return template('artists', artists=get_artists())

@route('/songsby/<id>')
def index(id):
	return template('songsby', artist=get_artist_name(id), songs=get_songs(id), albums=get_albums(id))

@route('/remove/<position>')
def index(position):
	playlistid = get_playlistid()
	if playlistid >= 0:
		xbmc.Playlist.Remove({'playlistid':int(playlistid), 'position':int(position)})
	redirect("/juke")

@route('/playpause')
def index():
	player = xbmc.Player.GetActivePlayers()
	if len(player['result']) > 0:
		xbmc.Player.PlayPause({'playerid':0})
	redirect("/juke")

@route('/play/<id>')
def index(id):
	playlistid = get_playlistid()
	playlist, not_needed= get_playlist()
	#if nothing playing or if currently playing radio, clear the playlist
	if playlistid < 0 or playlist[0]['type'] == 'unknown':
		xbmc.Playlist.Clear({"playlistid":0})
		xbmc.Playlist.Add({"playlistid":0, "item":{"songid":int(id)}})
		xbmc.Player.open({"item":{"playlistid":0}})
		playlistid = 0
	else:
		xbmc.Playlist.Add({"playlistid":playlistid, "item":{"songid":int(id)}})

	remove_duplicates(playlistid)
	redirect("/juke")

@route('/skip/<position>')
def index(position):
	print xbmc.Player.GoTo({'playerid':0, 'to':'next'})
	redirect("/juke")

@route('/play_album/<id>')
def index(id):
	playlistid = get_playlistid()
	playlist, not_needed = get_playlist()
	#if nothing playing or if currently playing radio, clear the playlist
	if playlistid < 0 or playlist[0]['type'] == 'unknown':
		xbmc.Playlist.Clear({"playlistid":0})
		xbmc.Playlist.Add({"playlistid":0, "item":{"albumid":int(id)}})
		xbmc.Player.open({"item":{"playlistid":0}})
		playlistid = 0
	else:
		xbmc.Playlist.Add({"playlistid":playlistid, "item":{"albumid":int(id)}})

	remove_duplicates(playlistid)
	redirect("/juke")

@route('/shutdown')
def index():
	return static_file('shutdown.html', root=".")

#change to a put or post so that it doesn't auto-reload
@route('/shutdown_really')
def index():
#nb. redirect so that when you reopen the browser, it doesn't automatically shut down xbmc
	xbmc.System.Shutdown()
	redirect("/juke")


@route('/volume/<change>')
def index(change):
	if change == "up":
		xbmc.Application.SetVolume({"volume":"increment"})
	elif change == "down":
		xbmc.Application.SetVolume({"volume":"decrement"})
	redirect("/juke")

@route('/radio/')
def index():
	my_stations = xbmc.Files.GetDirectory({"directory":"plugin://plugin.audio.radio_de/stations/my/", "properties":["title","thumbnail","playcount","artist","album","episode","season","showtitle"]})
	if 'result' in my_stations.keys():
		return template('radio', stations=my_stations['result']['files'])
	else:
		return template('error', error='radio')

@route('/play_radio/')
def index():
#note -- always clear playlist
	station_file = request.query.station_file
	xbmc.Playlist.Clear({"playlistid":0})
	xbmc.Playlist.Add({"item":{"file":station_file},"playlistid":0})
	xbmc.Player.open({"item":{"playlistid":0}})
#change this ti juke and let it detect radio
	return redirect("/juke")
	

#need to take post parameters I think. 
	

@route('/download/<id>')
def index(id):
	data = xbmc.AudioLibrary.GetSongDetails({"songid":int(id), "properties":["file"]})
	full_filename = data['result']['songdetails']['file']
	path, filename = os.path.split(full_filename)
	
	return static_file(filename, root=path, download=True)
	

run(host=hostname, port=hostport, server="paste")

