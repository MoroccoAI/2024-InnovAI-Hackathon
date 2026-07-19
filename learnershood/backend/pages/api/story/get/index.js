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

const GetStories = async (req, res) => {
  await cors(req, res);

  try {
    await connectMongo().catch((error) => res.json({ status: false, error: "Database connection failed." }));

    const allStories = await Stories.find({});

    res.status(201).json({
      status: true,
      data: allStories,
    });
  } catch (error) {
    res
      .status(500)
      .json({ status: false, error: "Error occurred! Please try again." });
  }
};

export default  GetStories;
