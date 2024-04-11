import { detectSpeechEnd } from "./speakDetection";
import { recordAudio } from "./record";
import { Buffer } from "buffer"

function joinBase64Strings(base64Str1, base64Str2) {
  const bothData = Buffer.from(base64Str1, 'base64').toString('binary') + Buffer.from(base64Str2, 'base64').toString('binary');
  const joinedBase64Result = Buffer.from(bothData.toString(), 'binary').toString('base64');
  return joinedBase64Result;
}

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

async function blobsToBase64(blobs) {
  let base64String = '';
  for (const blob of blobs) {
    base64String = joinBase64Strings(base64String, await blobToBase64(blob));
  }
  return base64String;
}

export function captureAudio({
  stream,
  onAudio,
  minChunkDuration = 5_000,
}) {
  let startedAt;
  let chunks = [];
  let stopRecord;
  let releaseTimeout;

  const onDataAvailable = async (evt) => {
    clearTimeout(releaseTimeout);
    chunks.push(evt.data);

    if (Date.now() - startedAt > minChunkDuration) {
      releaseAudio();
      return;
    }

    releaseTimeout = setTimeout(releaseAudio, 500);
  };

  const releaseAudio = async () => {
    const base64 = await blobsToBase64(chunks);

    startedAt = 0;
    chunks = [];

    onAudio(base64);
  };

  const startRecord = () => {
    if (!startedAt) {
      startedAt = Date.now();
    }

    stopRecord = recordAudio({
      stream,
      onDataAvailable,
      onError: console.error,
    });
  };

  const stopSpeechDetect = detectSpeechEnd({
    onSpeechStart() {
      console.info("[Speech] started.");
      startRecord();
    },
    onSpeechEnd() {
      console.info("[Speech] end.");
      setTimeout(stopRecord, 30);
    },
  });

  return () => {
    stopSpeechDetect();
    stopRecord();
  };
}
