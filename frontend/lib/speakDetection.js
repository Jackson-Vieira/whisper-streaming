
export async function detectSpeechEnd({ onSpeechEnd, onSpeechStart, positiveSpeechThreshold = 0.5, negativeSpeechThreshold = 0.3 }) {
  const speechDetector = await vad.MicVAD.new({
    onSpeechStart,
    onSpeechEnd,
    positiveSpeechThreshold,
    negativeSpeechThreshold,
  })

  speechDetector.start()

  return () => {
    speechDetector.stop()
  }
}
