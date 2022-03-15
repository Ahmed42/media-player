#!/bin/bash

inotifywait -r -m -e move -e create -e delete --format '%e|%T|%f|%w' --timefmt '%s'  ~/music_lan/musiclan/audio/ | while IFS='|' read event seconds filename fullpath; do
	#printf "Hello!\n"
	#printf "Event: %s\nSeconds: %s\nFile1: %s\nFile2%s\n\n" $evnt $scnds $fil $fil2
	python manage.py update_song $event $seconds "$filename" "$fullpath"
done
