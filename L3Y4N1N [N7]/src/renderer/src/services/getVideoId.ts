const getYouTubeVideoId = (url: string | undefined): string | null => {
    if (!url) return null;
    
    try {
      const urlObj = new URL(url);
      const searchParams = new URLSearchParams(urlObj.search);
      return searchParams.get('v');
    } catch {
      const match = url.match(/(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/watch\?.+&v=))([^"&?\/\s]{11})/);
      return match ? match[1] : null;
    }
  };


  export default getYouTubeVideoId;