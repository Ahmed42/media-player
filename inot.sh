#!/bin/bash

inotifywait -m -e move -e create -e delete --format '%e %T %f' --timefmt '%s'  ~/music_lan/musiclan/audio/ | while read evnt scnds fil; do
	python manage.py update_song $evnt $scnds "$fil"
done
