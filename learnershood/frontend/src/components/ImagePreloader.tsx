import { useState, useEffect } from 'react';

interface ImagePreloaderProps {
  images: string[];
  onLoad: () => void;
  children: React.ReactNode;
}

function ImagePreloader({ images, onLoad, children }: ImagePreloaderProps) {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let loadedCount = 0;
    const totalImages = images.length;

    const preloadImage = (src: string) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.src = src;
        img.onload = resolve;
        img.onerror = reject;
      });
    };

    Promise.all(images.map(preloadImage))
      .then(() => {
        setLoaded(true);
        onLoad();
      })
      .catch((error) => {
        console.error('Error preloading images:', error);
        setLoaded(true); // Show content anyway
        onLoad();
      });
  }, [images, onLoad]);

  if (!loaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="space-y-4 text-center">
          <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-gray-600">Loading story asset...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}

export default ImagePreloader;