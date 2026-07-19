// In-memory cache for loaded images
const imageCache = new Map<string, Promise<void>>();

export const preloadImage = (src: string): Promise<void> => {
  if (imageCache.has(src)) {
    return imageCache.get(src)!;
  }

  const promise = new Promise<void>((resolve, reject) => {
    const img = new Image();
    img.src = src;
    img.onload = () => resolve();
    img.onerror = reject;
  });

  imageCache.set(src, promise);
  return promise;
};

export const preloadImages = async (srcs: string[]): Promise<void> => {
  await Promise.all(srcs.map(preloadImage));
};