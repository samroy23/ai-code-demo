// recorder.ts
import Recorder from 'recorder-js';

const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
const audioContext = new AudioContext();
let recorder: Recorder | null = null;
let stream: MediaStream | null = null;

export const startRecording = async (): Promise<void> => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  recorder = new Recorder(audioContext);
  await recorder.init(stream);
  recorder.start();
};

export const stopRecording = async (): Promise<Blob> => {
  if (!recorder) throw new Error("Recorder is not initialized");
  const { blob } = await recorder.stop();
  if (stream) stream.getTracks().forEach(track => track.stop());
  return blob;
};
