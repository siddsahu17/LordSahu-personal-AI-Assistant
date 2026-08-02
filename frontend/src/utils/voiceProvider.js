/**
 * Pluggable Voice Provider Abstraction Layer for LordSahu AI OS.
 * Decouples speech synthesis (TTS) & recognition (STT) from UI components.
 * Supports Web Speech API with female voice selection, and is extensible for ElevenLabs, Deepgram, or Whisper APIs.
 */

class WebSpeechVoiceProvider {
  constructor() {
    this.synthesis = typeof window !== 'undefined' ? window.speechSynthesis : null;
    this.recognition = null;
    this.initRecognition();
  }

  initRecognition() {
    if (typeof window === 'undefined') return;
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = 'en-US';
      this.recognition = rec;
    }
  }

  speak(text, options = {}) {
    if (!this.synthesis || options.isMuted) return;
    this.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    const voices = this.synthesis.getVoices();

    const femaleVoice = voices.find((v) =>
      v.name.includes('Female') ||
      v.name.includes('Samantha') ||
      v.name.includes('Zira') ||
      v.name.includes('Victoria') ||
      v.name.includes('Karen') ||
      v.name.includes('Google UK English Female') ||
      v.name.includes('Google US English')
    );

    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }
    utterance.pitch = options.pitch || 1.1;
    utterance.rate = options.rate || 1.0;
    this.synthesis.speak(utterance);
  }

  listen(onResult, onError, onEnd) {
    if (!this.recognition) {
      if (onError) onError('Speech recognition is not supported in this browser.');
      return false;
    }

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      if (onResult) onResult(transcript);
    };

    this.recognition.onerror = (err) => {
      if (onError) onError(err);
    };

    this.recognition.onend = () => {
      if (onEnd) onEnd();
    };

    this.recognition.start();
    return true;
  }

  stopListening() {
    if (this.recognition) {
      this.recognition.stop();
    }
  }
}

export const voiceProvider = new WebSpeechVoiceProvider();
