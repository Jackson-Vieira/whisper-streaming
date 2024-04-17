<script setup>
import { ref } from "vue"

const onAudio = async (buffer) => {
  const response = await fetch('http://localhost:8000/whisper', {
    method: 'POST',
    body: buffer
  });

  const data = await response.json();

  return { data }
}


let stream;
let audioContext;
let source;
let processor;

const startAudioCapture = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new (window.AudioContext || window.webkitAudioContext)({
      sampleRate: 16000,
    });
    source = audioContext.createMediaStreamSource(stream);
    processor = audioContext.createScriptProcessor(16384, 1, 1);

    source.connect(processor);
    processor.connect(audioContext.destination);

    processor.onaudioprocess = async (event) => {
      const audioData = event.inputBuffer.getChannelData(0);
      const buffer = new Float32Array(audioData);
      const { data } = await onAudio(buffer);
      console.log('transcription', data);
    };
  }

  catch (error) {
    console.error('Error', error);
  }

}

const handleGetUserMedia = async () => {

  await startAudioCapture();


}

function handleStopRecording() {
  recorder.stop();
}
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
  <button @click="handleStopRecording">
    Stop Media
  </button>
  <button @click="handleScreenshot">
    Screenshot Media
  </button>
  <button @click="takePhoto">
    Take Photo
  </button>
</template>

<style scoped></style>
