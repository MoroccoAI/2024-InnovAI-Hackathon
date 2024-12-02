import ffmpeg from 'fluent-ffmpeg';
import GetvideoStreamlink from './youtubeDownloader';

async function getAudioStream(id: string , start :number): Promise<File> {
    try {
        const streamInfo = await GetvideoStreamlink(id);
        if (!streamInfo || !streamInfo.url) {
            throw new Error('Stream URL not found');
        }

        return new Promise((resolve, reject) => {
            const chunks: Buffer[] = [];
            ffmpeg(streamInfo.url)
            .setStartTime(start)
            .toFormat('mp3')
            .noVideo()
            .on('end', () => {
                const buffer = Buffer.concat(chunks);
                const arrayBuffer = buffer.buffer.slice(
                buffer.byteOffset,
                buffer.byteOffset + buffer.byteLength
                );
                const file = new File([arrayBuffer], `${id}.mp3`, { type: 'audio/mp3' });
                resolve(file);
            })
            .on('error', (err) => {
                console.error('FFmpeg error:', err);
                reject(err);
            })
            .pipe()
            .on('data', (chunk: Buffer) => {
                chunks.push(chunk);
            });
        });
    } catch (error) {
        console.error('Error in getVideoDurationFromReadableStream:', error);
        throw error;
    }
}
export default getAudioStream;


