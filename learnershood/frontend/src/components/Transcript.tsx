import { motion } from 'framer-motion';

interface TranscriptProps {
  text: string;
}

function Transcript({ text }: TranscriptProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl p-6 shadow-lg"
    >
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Transcript</h2>
      <p className="text-gray-600 leading-relaxed whitespace-pre-line ">{text}</p>
    </motion.div>
  );
}

export default Transcript;