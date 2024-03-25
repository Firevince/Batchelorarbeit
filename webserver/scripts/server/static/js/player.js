document.addEventListener('DOMContentLoaded', function() {
    const audio = document.getElementById('audio-player');
    let tracks = [];
    let currentTrackIndex = 0;
    let isTimerPlaying = true;

    // Elements from your HTML you'll interact with
    const playButton = document.querySelector('#play-button');
    const nextButton = document.querySelector('#next-button');
    const prevButton = document.querySelector('#prev-button');
    const transcriptButton = document.querySelector('#transcript-button');
    const progressBar = document.querySelector('#progress-bar');
    const progressIndicator = document.querySelector('#progress-indicator'); // This could be your barWidth or circleLeft
    const currentTimeDisplay = document.querySelector('#current-time');
    const durationDisplay = document.querySelector('#duration');
    const audioTitle = document.querySelector('#title');
    const audioArtist = document.querySelector('#artist');
    const audioCover = document.querySelector('#cover-image');
    const transcriptContainer = document.querySelector('#transcript-container');
    const transcriptText = document.querySelector('#transcript-text');

    function fetchTracks() {
        fetch('/tracks')
            .then(response => response.json())
            .then(data => {
                tracks = data;
                loadTrack(currentTrackIndex);
            });
    }

    function loadTrack(index) {
        const track = tracks[index];
        audio.src = track.source;
        audioArtist.textContent = track.artist;
        audioTitle.textContent = track.title;
        transcriptText.innerHTML = "";
        track.sentences.forEach((sentence, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = sentence;
            transcriptText.appendChild(listItem);
          });

        // Optional: Update UI with track title, cover, etc.
        resetPlayer();
    }

    function updateIcon(state) {
        let iconHref = state === 'pause' ? '#icon-play' : '#icon-pause';
        let svgHTML = `<svg class="icon"><use xlink:href="${iconHref}"></use></svg>`;

        playButton.innerHTML = svgHTML;
    }

    function playPause() {
        if (audio.paused) {
            audio.play();
            isTimerPlaying = true;
            updateIcon('play');
        } else {
            audio.pause();
            isTimerPlaying = false;
            updateIcon('pause');
        }
    }



    function nextTrack() {
        if (currentTrackIndex < tracks.length - 1) {
            currentTrackIndex++;
        } else {
            currentTrackIndex = 0;
        }
        loadTrack(currentTrackIndex);
    }

    function prevTrack() {
        if (currentTrackIndex > 0) {
            currentTrackIndex--;
        } else {
            currentTrackIndex = tracks.length - 1;
        }
        loadTrack(currentTrackIndex);
    }

    function expandTranscript(){
        if (transcriptContainer.style.display === "none") {
            transcriptContainer.style.display = "block";
        } else {
            transcriptContainer.style.display = "none";
        }
    }

    function resetPlayer() {
        audio.currentTime = 0;
        updateProgressBar();
    }

    function updateProgressBar() {
        const percentage = (audio.currentTime / audio.duration) * 100;
        progressIndicator.style.width = `${percentage}%`;
        currentTimeDisplay.textContent = formatTime(audio.currentTime);
        durationDisplay.textContent = formatTime(audio.duration);
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }

    // Event listeners
    playButton.addEventListener('click', playPause);
    nextButton.addEventListener('click', nextTrack);
    prevButton.addEventListener('click', prevTrack);
    transcriptButton.addEventListener('click', expandTranscript);
    audio.addEventListener('timeupdate', updateProgressBar);

    progressBar.addEventListener('click', function(e) {
        const clickPosition = (e.pageX - this.offsetLeft) / this.offsetWidth;
        const clickTime = clickPosition * audio.duration;
        audio.currentTime = clickTime;
    });

    // Initial track load and setup
    fetchTracks();
});
