import Stories from "@/model/Stories";
import connectMongo from '@/lib/db-connect';
import Cors from 'cors';
import initMiddleware from '@/lib/init-middleware';

const cors = initMiddleware(
  Cors({
    methods: ['GET', 'POST', 'OPTIONS'], 
    origin: "*", 
  })
);

const CreateStory = async (req, res) => {
  await cors(req, res);
  
  if (req.method !== "POST") {
    res.status(405).appendHeader("Allow", "POST").json({
      status: false,
      error: "Only POST request is allowed",
    });
    return;
  }

  try {
    await connectMongo().catch((error) => res.json({ status: false, error: "Database connection failed." }));
    const {
      title,
      transcript,
      images,
      audio,
      quiz
    } = req.body;

//     const title = "The Story of Muritala Muhammed"
//     const transcript = `Gather around, dear children, as the sun sets over our village, and let me tell you the captivating story of Muritala Muhammed, a tale full of bravery, wisdom, and honor. Born in a humble town in Nigeria, young Muritala was no ordinary child. From a tender age, he exhibited exceptional intelligence and a fervent desire to bring about justice and fairness. His mother would often say, 'This boy is destined for greatness!', and how right she was. His eyes sparkled with dreams of a better world, and those dreams soon began to take shape. 

// As Muritala grew, he became known for his boundless energy and unyielding commitment to helping others. Now, imagine a busy market square; bustling with traders and animals, and at the center of it all, there stands young Muritala, negotiating peace between two quarreling merchants. 'There must be a way for both of you to be happy,' he would declare, and through his sheer will and charm, conflicts were always resolved. The people began to see him not just as a boy but as a beacon of hope and wisdom. 

// Years went by, and Muritala's reputation spread far and wide. He joined the Nigerian military with the vision of serving his people. His valiant efforts did not go unnoticed, and he quickly rose through the ranks. Was it easy? Oh, no, children – the journey was fraught with danger and challenges. Late one moonlit night during a treacherous mission, his platoon was surrounded by enemies. With a heart full of courage, Muritala led his men through the darkness, using his sharp mind and keen instincts to guide them to safety. 'Stay close, trust your instincts,' he would whisper, and his men trusted him with their lives. 

// Muritala's bravery and skills in leadership earned him the highest respect, and he eventually became the Head of State. Imagine that, children – a boy from a small town leading an entire nation! But with great power comes great responsibility. One day, he decided to tackle the corruption that had plagued his beloved country. His voice echoed through the halls of power, 'We must rid our land of this cancer!' With every step, he instilled the values of integrity and justice, and the people saw him as a true guardian. 

// But not everyone appreciated his efforts. There were whispers in the shadows, plots to bring him down. One fateful day, as he traveled with his trusted aides, they were ambushed. The tale takes a dark turn here, for even a hero is not invincible. Though Muritala fought bravely, he was tragically killed. The nation mourned, and his legacy became etched in the hearts of millions. 'A hero's light may fade, but his deeds will always shine,' the elders would say. His spirit of courage and integrity continues to inspire generations. 

// And so, dear children, as you sit under the starry sky listening to this tale, remember the lessons of Muritala Muhammed. Be brave, be just, and never shy away from standing up for what is right. Life may present you with challenges, but with a heart full of determination and a mind brimming with wisdom, you too can make a difference. Now, what will you do tomorrow to be a little more like Muritala? Think about it as you drift off to sleep, dreaming of your own adventures and the hero within you.`
//     const images = [
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/bbf758fe-09ff-4c2d-8f97-a9fbdbd148ca",
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/e9b53922-e61a-46bc-a419-a1084afad268",
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/aa158061-9f60-4299-80e6-a90f90f6605d",
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/dcc6abc7-3f11-4666-8d35-a61e869cd0ef",
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/eefa2b99-ebb1-499d-a8f7-9f2790e026d3",
//       "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/6b0869ad-8d3f-4e02-a132-dce96686af1e"
//     ]
//     const audio =  "https://jambo-llama.s3.eu-central-1.amazonaws.com/95cc6111-a46c-4c47-b05f-014da8ea8b38/6b0869ad-8d3f-4e02-a132-dce96686af1e"
//     const quiz = [
//       {
//         id: 0,
//         question: 'Where was Muritala Muhammed born?',
//         options: [ 'Ghana', 'Nigeria', 'Kenya', 'Egypt' ],
//         correctAnswer: 1
//       },
//       {
//         id: 1,
//         question: "What did Muritala's mother believe about him?",
//         options: [
//           'He would become wealthy',
//           'He would travel the world',
//           'He was destined for greatness',
//           'He would become a teacher'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 2,
//         question: 'What was Muritala known for as a child?',
//         options: [
//           'Exceptional intelligence',
//           'Shyness',
//           'Artistic skills',
//           'Athleticism'
//         ],
//         correctAnswer: 0
//       },
//       {
//         id: 3,
//         question: 'Where did Muritala often resolve conflicts as a young boy?',
//         options: [
//           'In school',
//           'In his home',
//           'In the market square',
//           'On the playground'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 4,
//         question: "What was Muritala's main goal when he joined the Nigerian military?",
//         options: [
//           'To become the richest man',
//           'To travel abroad',
//           'To serve his people',
//           'To learn new skills'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 5,
//         question: 'How did Muritala lead his men to safety during a treacherous mission?',
//         options: [
//           'By bribing the enemies',
//           'By negotiating with the enemies',
//           'Using his sharp mind and keen instincts',
//           'By hiding until the enemies left'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 6,
//         question: 'What rank did Muritala eventually achieve?',
//         options: [ 'Major General', 'Head of State', 'Colonel', 'Lieutenant' ],
//         correctAnswer: 1
//       },
//       {
//         id: 7,
//         question: 'What problem did Muritala focus on tackling as Head of State?',
//         options: [ 'Poverty', 'Corruption', 'Education', 'Healthcare' ],
//         correctAnswer: 1
//       },
//       {
//         id: 8,
//         question: 'What did Muritala proclaim about corruption?',
//         options: [
//           'We must accept corruption',
//           'We must avoid discussing corruption',
//           'We must rid our land of this cancer',
//           'Corruption is not a major issue'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 9,
//         question: 'How did Muritala inspire others?',
//         options: [
//           'Through his wealth',
//           'Through his integrity and justice',
//           'By being popular on social media',
//           'By writing books'
//         ],
//         correctAnswer: 1
//       },
//       {
//         id: 10,
//         question: 'What ultimately happened to Muritala?',
//         options: [
//           'He retired peacefully',
//           'He moved to another country',
//           'He was tragically killed',
//           'He became a teacher'
//         ],
//         correctAnswer: 2
//       },
//       {
//         id: 11,
//         question: 'What did the nation do after Muritala was killed?',
//         options: [
//           'Held a festival',
//           'Mourned his loss',
//           'Forgot about him',
//           'Declared war'
//         ],
//         correctAnswer: 1
//       },
//       {
//         id: 12,
//         question: "What is the lesson from Muritala's story?",
//         options: [
//           'Be wealthy and powerful',
//           'Be brave, just, and stand up for what is right',
//           'Avoid conflicts',
//           'Focus on personal success only'
//         ],
//         correctAnswer: 1
//       }
//     ]

    const newStories = await Stories.create({
      title,
      transcript,
      images,
      audio,
      quiz
    });

    res.status(201).json({
      status: true,
      data: newStories._id,
    });


  } catch (error) {
    res
      .status(500)
      .json({ status: false, error: "Error occurred! Please try again." });
  }
};

export default CreateStory;
