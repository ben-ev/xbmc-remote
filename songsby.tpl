<h1>{{artist}}</h1>
<h2>Albums:</h2>
% for album in albums:
<a href="/play_album/{{album['albumid']}}"> {{album['label']}} </a><br>
% end
<h2>Songs</h2>
% for song in songs:
<a href="/play/{{song['songid']}}"> {{song['label']}} </a> / <a href="/download/{{song['songid']}}">Download</a> <br>
% end
