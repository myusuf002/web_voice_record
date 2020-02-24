//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var skipButton = document.getElementById("skipButton");
var saveButton = document.getElementById("saveButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
saveButton.addEventListener("click", saveRecording);

function startRecording() {
	console.log("recordButton clicked");

	/*
		Simple constraints object, for more advanced audio features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	recordButton.classList.add("d-none");
	stopButton.classList.remove("d-none");

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format 
		document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

		/*  assign to gumStream for later use  */
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);

		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
	});
}

function stopRecording() {
	console.log("stopButton clicked");

	//disable the stop button, enable the record too allow for new recordings
	stopButton.classList.add("d-none");
	recordButton.classList.remove("d-none");
	saveButton.classList.remove("disabled");

	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createRecordResult)

}

function createRecordResult(blob) {
	var recordResult = document.getElementById("recordResult");
	while(recordResult.firstChild){
		recordResult.removeChild(recordResult.firstChild);
	}
	Recorder.forceDownload(blob, "Namafile.wav");
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');

	
	//add controls to the <audio> element
	au.controls = true;
	au.src = url;
	recordResult.appendChild(au);
	
}

function saveRecording(blob) {
	var recordResult = document.getElementById("recordResult");
	while(recordResult.firstChild){
		recordResult.removeChild(recordResult.firstChild);
	}
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	
	//add controls to the <audio> element
	au.controls = true;
	au.src = url;
	recordResult.appendChild(au);
	
}

