import { Schema, model, models } from 'mongoose';

const storySchema = new Schema({
  title : {
		type: String,
	},
  transcript : {
		type: String,
	},
  images : {
		type: [String],
		blackbox: true,
	},
  audio: {
		type: String,
	},
  quiz: {
		type: Array,
		blackbox: true,
	}
}, {
	timestamps: true
});

const Stories = models.story || model('story', storySchema);

export default Stories;