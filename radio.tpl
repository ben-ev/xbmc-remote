<h1>Radio Stations</h1>

% for station in stations:
% if station['type'] == "song":
<a href="/play_radio/?station_file={{station['file']}}&station={{station['label']}}">{{station['label']}}</a><br>

% end
% end
