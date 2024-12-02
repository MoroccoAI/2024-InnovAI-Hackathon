const ffmpeg = require('fluent-ffmpeg');

const ffmpegPath = require('ffmpeg-static').replace(
    'app.asar',
    'app.asar.unpacked'
);
console.log(ffmpegPath)

const ffprobePath = require('ffprobe-static').path.replace(
    'app.asar',
    'app.asar.unpacked'
);

ffmpeg.setFfmpegPath(ffmpegPath);
ffmpeg.setFfprobePath(ffprobePath);


export default ffmpeg;