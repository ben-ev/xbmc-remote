<h1><a href="/artists/">Add Music Playlist</a></h1>
<h1><a href="/radio/">Play Radio</a></h1>

<h2>Currently Playing:</h1> 
% if playlist is not None:
% position = offset
% for song in playlist:
<strong> {{song['title']}} </strong>
% if song['type'] == 'unknown':
Radio
% else:
{{song['artist'][0]}} 
% end
% if position != offset:
<!-- can't remove the top item -->
<a href="/remove/{{position}}">remove</a>
% else:
<a href="/skip/{{position}}">skip</a>
% end
<br>
% position += 1
% end
<br/>
<a href="/playpause">Play/Pause</a>
<br/>
<br/>
<a href="/volume/up">Volume Up</a> / <a href="/volume/down">Volume Down</a>
<br/>
<br/>
<a href="/shutdown">Shutdown</a>


