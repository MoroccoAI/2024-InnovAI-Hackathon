import { ipcMain } from 'electron';
import ytdl from '@distube/ytdl-core';

const GetvideoStreamlink = async (vidoId: string) => {
    const url = `https://www.youtube.com/watch?v=${vidoId}`;
    
    try {
		const audioFormat = await ytdl.getInfo(url).then(info => {
			return info.formats;
		});
		const highestAudioFormat = audioFormat.find(format => 
			format.mimeType?.includes('audio/mp4') && format.audioBitrate
		);
		if (!highestAudioFormat) {
			throw new Error('No audio format found');
		}
	        return {
            url: highestAudioFormat.url,
            contentLength: highestAudioFormat.contentLength
        };
    } catch (error) {
        console.error('Error fetching video info:', error);
        throw error;
    }
};

ipcMain.handle('GetvideoStreamlink', async (_, videoId: string) => {
	try {
		const stream = await GetvideoStreamlink(videoId);
		return stream;
	} catch (error) {
		throw error;
	}
});
export default GetvideoStreamlink;