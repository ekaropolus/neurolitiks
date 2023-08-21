const chunks = [];
let mediaRecorder;
let mediaStream;

const startRecord = async () => {
  const mimeType = 'audio/webm; codecs=opus';

  if (!MediaRecorder.isTypeSupported(mimeType)) {
    alert('Opus mime type is not supported');
    return;
  }

  const options = {
    audioBitsPerSecond: 128000,
    mimeType
  };

  try {
    mediaStream = await getLocalMediaStream();
  } catch (error) {
    console.log(`Error accessing microphone: ${error}`);
    return;
  }

  mediaRecorder = new MediaRecorder(mediaStream, options);

  setListeners();

  mediaRecorder.start();
  console.log('Recording started');
};

const stopRecord = async () => {
  if (!mediaRecorder) return;

  mediaRecorder.stop();
  console.log('Recording stopped');

  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
  }
};

const getLocalMediaStream = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    return stream;
  } catch (error) {
    console.log(`Error accessing microphone: ${error}`);
    throw error;
  }
};

const setListeners = () => {
  mediaRecorder.ondataavailable = handleOnDataAvailable;
  mediaRecorder.onstop = handleOnStop;
};

const handleOnStop = () => {
  saveFile();

  destroyListeners();
  mediaRecorder = undefined;
};

const destroyListeners = () => {
  mediaRecorder.ondataavailable = undefined;
  mediaRecorder.onstop = undefined;
};

const handleOnDataAvailable = ({ data }) => {
  if (data.size > 0) {
    chunks.push(data);
  }
};

const saveFile = async () => {
  const blob = new Blob(chunks, { type: 'audio/wav' });

  const formData = new FormData();
  formData.append('audio', blob, 'recorded_file.wav');

  try {
    const response = await fetch('/opinions_plus/process_audio/', {
      method: 'POST',
      body: formData
    });
    console.log('Audio data sent:', response);
  } catch (error) {
    console.log('Error sending audio data:', error);
  }

//   window.URL.revokeObjectURL(blobUrl);
  chunks.length = 0;
};


// Get the SVG path element
var wavePath = document.querySelector('.wave-path');

// Set up the animation properties
var animation = {
  amplitude: 20,
  frequency: 0.03,
  offset: 0,
  speed: 2,
  duration: 10000,
};

// Define the animation function
function animateWave(timestamp) {
  // Calculate the new path data
  var pathData = '';
  for (var x = 0; x <= 100; x++) {
    var y = animation.amplitude * Math.sin(animation.frequency * (x + animation.offset));
    pathData += x + ',' + (50 + y) + ' ';
  }
  wavePath.setAttribute('d', 'M ' + pathData);

  // Update the animation properties
  animation.offset += animation.speed;
  if (timestamp < animation.startTime + animation.duration) {
    window.requestAnimationFrame(animateWave);
  }
}

// Start the animation when the page is loaded
animation.startTime = window.performance.now();
window.requestAnimationFrame(animateWave);
