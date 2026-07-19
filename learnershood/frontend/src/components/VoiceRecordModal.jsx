import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, X, Loader2 } from 'lucide-react';

function VoiceRecordModal({ isOpen, onClose, onTranscription }) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioContext, setAudioContext] = useState(null);
  const [analyser, setAnalyser] = useState(null);
  const [dataArray, setDataArray] = useState(null);
  const canvasRef = useRef(null);
  const animationFrameRef = useRef();
  const mediaRecorderRef = useRef(null);

  useEffect(() => {
    if (isRecording && canvasRef.current && analyser && dataArray) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const height = canvas.height;
      
      const draw = () => {
        if (!analyser || !dataArray) return;
        
        analyser.getByteTimeDomainData(dataArray);
        
        ctx.fillStyle = 'rgb(249, 250, 251)';
        ctx.fillRect(0, 0, width, height);
        
        ctx.lineWidth = 2;
        ctx.strokeStyle = 'rgb(79, 70, 229)';
        ctx.beginPath();
        
        const sliceWidth = width / dataArray.length;
        let x = 0;
        
        for (let i = 0; i < dataArray.length; i++) {
          const v = dataArray[i] / 128.0;
          const y = v * height / 2;
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
          
          x += sliceWidth;
        }
        
        ctx.lineTo(width, height / 2);
        ctx.stroke();
        
        animationFrameRef.current = requestAnimationFrame(draw);
      };
      
      draw();
      
      return () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
      };
    }
  }, [isRecording, analyser, dataArray]);

  const transcribeAudio = async (audioBlob) => {
    try {
      const url = `${import.meta.env.VITE_BACKEND_ENDPOINT}/api/transcribe-audio`;

      const formData = new FormData();
      formData.append("file", audioBlob, "record.webm");

      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setIsProcessing(false);
      
      if (data.error) {
        throw new Error(data.error);
      }

      onTranscription(data.data);
      onClose();

    } catch (error) {
      setIsProcessing(false);
      console.error('API Error:', error);
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const audioCtx = new AudioContext();
      const source = audioCtx.createMediaStreamSource(stream);
      const analyserNode = audioCtx.createAnalyser();
      
      analyserNode.fftSize = 2048;
      const bufferLength = analyserNode.frequencyBinCount;
      const dataArr = new Uint8Array(bufferLength);
      
      source.connect(analyserNode);
      
      setAudioContext(audioCtx);
      setAnalyser(analyserNode);
      setDataArray(dataArr);
      
      const mediaRecorder = new MediaRecorder(stream,  { mimeType: 'audio/webm;codecs=opus' });
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.start();
      setIsRecording(true);
      
      const chunks = [];
      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        setIsProcessing(true);
        const blob = new Blob(chunks, { type: 'audio/webm' });
        
        // await transcribeAudio(blob)

        setTimeout(() => {
          setIsProcessing(false);
          onTranscription("Demo Text: Tell me about Hanno the Navigator");
          onClose();
        }, 2000);
      };
    } catch (err) {
      console.error('Error accessing microphone:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
    if (audioContext) {
      audioContext.close();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center px-4 bg-black/50 backdrop-blur-sm"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-2xl w-full max-w-sm p-6 shadow-xl"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-800">
                Voice Search
              </h2>
              <button
                onClick={onClose}
                className="text-gray-500 hover:text-gray-700"
                disabled={isProcessing}
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <p className="text-gray-600 mb-6">
              What African story do you want to learn?
            </p>

            <div className="flex flex-col items-center space-y-6">
              <canvas
                ref={canvasRef}
                width={300}
                height={100}
                className="w-full bg-gray-50 rounded-lg"
              />

              {isProcessing ? (
                <div className="flex flex-col items-center space-y-2">
                  <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
                  <p className="text-sm text-gray-500">Processing your recording...</p>
                </div>
              ) : (
                <>
                  <button
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isProcessing}
                    className={`p-6 rounded-full transition-all ${
                      isRecording
                        ? 'bg-red-500 animate-pulse'
                        : 'bg-indigo-600'
                    } text-white hover:scale-110`}
                  >
                    <Mic className="w-8 h-8" />
                  </button>
                  <p className="text-sm text-gray-500">
                    {isRecording ? 'Tap to stop recording' : 'Tap to start recording'}
                  </p>
                </>
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export default VoiceRecordModal;