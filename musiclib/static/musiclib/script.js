
const track_buttons = document.querySelectorAll('.trackstree .track');
const addtoqueue_buttons = document.querySelectorAll('.addtoqueue'); 

const tracks_queue = document.querySelector('.queue ul');

const audio_player = document.querySelector('audio');

const trackpplaying = document.querySelector('.trackplaying');

var currently_playing = null;

function addTrackToQueue(track_button) {
	new_queue_track = document.createElement("li");
	new_queue_track.classList.add("tracklistitem");
	
	// Reuse the track button
	new_track_button = track_button.cloneNode(true);

	new_track_button.addEventListener("click", event => {
		if(currently_playing) {
			currently_playing.classList.remove("playing");
		}
		currently_playing = event.target.parentElement;
		currently_playing.classList.add("playing");

		track_url = event.target.getAttribute("data-trackurl");
		audio_player.src = track_url;
		audio_player.play();
	});

	remove_button = document.createElement("button");
	remove_button.appendChild(document.createTextNode("Remove"));
	remove_button.classList.add("remove");
	remove_button.addEventListener(
		"click", 
		event => event.target.parentElement.remove());

	new_queue_track.appendChild(new_track_button);
	new_queue_track.appendChild(remove_button);

	tracks_queue.appendChild(new_queue_track);
	return new_queue_track;
}

// When a track is clicked, clear queue, add track to queue, and  set up the player.
track_buttons.forEach(track_button => track_button.addEventListener(
	'click', 
	event => {
		tracks_queue.textContent = "";
		
		if(currently_playing) {
			currently_playing.classList.remove("playing");
		}

		currently_playing = addTrackToQueue(track_button);

		track_url = event.target.getAttribute("data-trackurl");

		//currently_playing = event.target.parentElement;
		currently_playing.classList.add("playing");
		
		audio_player.src = track_url;
		audio_player.play();
	}));


// Add the track to the currently playing queue
addtoqueue_buttons.forEach(addtoqueue_button => addtoqueue_button.addEventListener(
	'click',
	event => {
		track_button = addtoqueue_button.parentElement.querySelector(".track");
		addTrackToQueue(track_button); 
	}
));


// When the player finishes a track, go to the next. 
audio_player.addEventListener('ended', event => {
	next_track = currently_playing.nextSibling;
	if(next_track) {
		currently_playing.classList.remove("playing");
		next_track.classList.add("playing");
		currently_playing = next_track;

		track_url = currently_playing.querySelector(".track").getAttribute("data-trackurl");
		event.target.src = track_url;
		event.target.play();
	//	tracks_queue.querySelector();
	}
});

