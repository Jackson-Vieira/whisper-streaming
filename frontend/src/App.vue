<script setup>
import { ref } from "vue"
import { captureAudio } from "../lib";

// Task
// [X] - Screenshot a video stream and show it in img element in screen'
// [ ] - Take a photo from the video stream and show it in img element in screen
// [ ] - Improve this code to make more compartible with other browsers 
// [ ] - Test this using vitest
// [ ] - Transform this in a compousable and send a PR to VueUse library (useScreenshot)

// [ ] -   

import { RecordRTCPromisesHandler, StereoAudioRecorder } from "recordrtc";

let mediaStream;
const mediaStreamElm = ref(null);
const screenshotElm = ref(null);
const audioCtx = new AudioContext();

// const handleDataAvailable = async (event) => {
//   if (event.size > 0) {
//     const base64 = await blobToBase64(event);

//     const response = await fetch('http://localhost:8000/whisper', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ chunk: base64 })
//     });

//     const data = await response.json();
//     console.log('Data', data);
//   }
// };

function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64String = reader.result.split(',')[1];
      resolve(base64String);
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(blob);
  });
}

const bitMapToBase64 = (bitmap) => {
  const canvas = document.createElement('canvas');
  canvas.width = bitmap.width;
  canvas.height = bitmap.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(bitmap, 0, 0);
  return canvas.toDataURL('image/png');
};

const screenshot = async () => {
  const track = mediaStream.getVideoTracks()[0];
  // https://developer.mozilla.org/en-US/docs/Web/API/ImageCapture/track
  const imageCapture = new ImageCapture(track);
  const bitmap = await imageCapture.grabFrame();
  return bitmap;
};

const takePhoto = async () => {
  const track = mediaStream.getVideoTracks()[0]
  const imageCapture = new ImageCapture(track)
  const blob = await imageCapture.takePhoto()
  const base64 = await blobToBase64(blob)
  console.log('URL', URL.createObjectURL(blob))
  screenshotElm.value.src = `data:image/png;base64,${base64}`
  return base64
}

const onAudio = async (base64) => {
  const response = await fetch('http://localhost:8000/whisper', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ chunk: base64 })
  });

  const data = await response.json();
  console.log('Data', data);
}

const handleScreenshot = async () => {
  const bitmap = await screenshot();
  screenshotElm.value.src = bitMapToBase64(bitmap);
};

const handleGetUserMedia = async () => {
  // try {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: false,
    audio: true
  });

  mediaStream = stream;
  mediaStreamElm.value.srcObject = stream;
  const stopCaptureAudio = captureAudio({ stream, onAudio });
  // await detectSpeechEnd()
  // console.log('Stop Capture Audio', stopCaptureAudio);

  // let recorder = new RecordRTCPromisesHandler(stream, {
  //   type: 'audio',
  //   recorderType: StereoAudioRecorder,
  //   mimeType: 'audio/wav',
  //   timeSlice: 500,
  //   desiredSampRate: 16000,
  //   numberOfAudioChannels: 1,
  //   ondataavailable: handleDataAvailable
  // });

  // recorder.startRecording();

  // } catch (error) {
  // console.error(error);
}
// };
</script>

<template>
  <h1>Media Stream</h1>
  <div>
    <h2>Video</h2>
    <video ref="mediaStreamElm" autoplay muted playsinline></video>
  </div>
  <div>
    <h2>Screenshot</h2>
    <img ref="screenshotElm" />
  </div>

  <button @click="handleGetUserMedia">
    Start Media
  </button>
  <button @click="handleScreenshot">
    Screenshot Media
  </button>
  <button @click="takePhoto">
    Take Photo
  </button>
</template>

<style scoped></style>
