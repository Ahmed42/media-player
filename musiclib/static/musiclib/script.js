
const track_buttons = document.querySelectorAll('.trackstree .track');
const addtoqueue_buttons = document.querySelectorAll('.addtoqueue'); 

const tracks_queue = document.querySelector('.queue ul');

const audio_player = document.querySelector('audio');

const track_playing_title = document.querySelector('h2.trackplaying');

var currently_playing = null;

function playTrack(track_element) {
	if(currently_playing) {
		currently_playing.classList.remove("playing");
	}
	currently_playing = track_element;
	currently_playing.classList.add("playing");

	track_button = currently_playing.querySelector(".track");
	track_url = track_button.getAttribute("data-trackurl");
	track_name = track_button.innerHTML

	track_playing_title.innerHTML = track_name;
	audio_player.src = track_url;
	audio_player.play()
	// TODO add artist and album
}

function addTrackToQueue(track_button) {
	new_queue_track = document.createElement("li");
	new_queue_track.classList.add("tracklistitem");
	
	// Reuse the track button
	new_track_button = track_button.cloneNode(true);

	new_track_button.addEventListener("click", event => {
		track_element = event.target.parentElement;
		playTrack(track_element);
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
		track_element = addTrackToQueue(track_button);

		playTrack(track_element);
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
	playTrack(next_track);
});

/////////////////////////
// Switch between album/artist view and directory view
function switchToDirView() {
	dir_view = document.querySelector(".dirview");
	artist_view = document.querySelector(".artistview");

	dir_view.style.visibility = "visible";
	artist_view.style.visibility = "hidden";
}

function switchToArtistAlbumView() {
	dir_view = document.querySelector(".dirview");
	artist_view = document.querySelector(".artistview");

	dir_view.style.visibility = "hidden";
	artist_view.style.visibility = "visible";
}

switch_to_dir_btn = document.querySelector(".artistview").querySelector(".switch");
switch_to_artist_btn = document.querySelector(".dirview").querySelector(".switch");

switch_to_dir_btn.addEventListener("click", event => switchToDirView());
switch_to_artist_btn.addEventListener("click", event => switchToArtistAlbumView());


var http_request = new XMLHttpRequest();
http_request.onreadystatechange = fetchAndPopulateDirView;
http_request.open('GET', songs_by_dirs_url);
http_request.setRequestHeader('Content-Type', 'application/json');
http_request.send();

function populateDirView(dir_name, tree, list_element) {
	if (tree['file_name'] == undefined) {
		// Display dir_name directory list item
		//console.log(list_element + "DIR: " + dir_name);
		dir_list_item = document.createElement("li");
		dir_list_item.classList.add("dirlistitem");
		dir_name_p = document.createElement("p");
		dir_name_p.innerHTML = dir_name;
		dir_list_item.appendChild(dir_name_p);

		list_element.appendChild(dir_list_item);
		// Create new list element for children
		children_list_element = document.createElement("ul");
		dir_list_item.appendChild(children_list_element);

		//children_list_element = list_element + "\t"
		for (child in tree) {
			populateDirView(child, tree[child], children_list_element);
		}

	} else {
		// Display track list item
		//console.log(list_element + "TRACK: " + tree['file_name']);
		track_list_item = document.createElement("li");
		track_list_item.classList.add("tracklistitem");
		track_list_item.innerHTML = dir_name;

		list_element.appendChild(track_list_item);
	}
}

function fetchAndPopulateDirView() {
	if(http_request.readyState == XMLHttpRequest.DONE) { 
		response = JSON.parse(http_request.responseText);
		dir_view_list = document.querySelector(".dirview").querySelector("ul");
		console.log("hi there");

		common_root = Object.keys(response)[0]

		populateDirView(common_root, response[common_root], dir_view_list);
	}
}

