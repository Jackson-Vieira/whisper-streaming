export function recordAudio({
  stream,
  onDataAvailable,
  onStop,
  onError,
}) {
  const mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = onDataAvailable;

  if (onStop) mediaRecorder.onstop = onStop;
  if (onError) mediaRecorder.onerror = onError;

  mediaRecorder.start();

  return () => {
    if (mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    }
  };
}
