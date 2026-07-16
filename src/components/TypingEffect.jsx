import React, { useState, useEffect } from 'react';

const TypingEffect = ({
  words,
  typingSpeed = 150,
  deletingSpeed = 100,
  delayBetweenWords = 1000,
}) => {
  const [text, setText] = useState('');
  const [wordIndex, setWordIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let timer;

    const type = () => {
      const currentWord = words[wordIndex];
      const shouldDelete = isDeleting ? 1 : 0;

      setText((prev) =>
        isDeleting
          ? currentWord.substring(0, prev.length - 1)
          : currentWord.substring(0, prev.length + 1)
      );

      if (!isDeleting && text === currentWord) {
        timer = setTimeout(() => setIsDeleting(true), delayBetweenWords);
      } else if (isDeleting && text === '') {
        setIsDeleting(false);
        setWordIndex((prev) => (prev + 1) % words.length);
      } else {
        timer = setTimeout(
          type,
          isDeleting ? deletingSpeed : typingSpeed
        );
      }
    };

    timer = setTimeout(type, typingSpeed);

    return () => clearTimeout(timer);
  }, [text, isDeleting, wordIndex, words, typingSpeed, deletingSpeed, delayBetweenWords]);

  return (
    <span className="bg-gradient-to-r from-purple-500 to-blue-500 text-transparent bg-clip-text">
      {text}
    </span>
  );
};

export default TypingEffect;

