export interface Quiz {
  id: string;
  question: string;
  options: string[];
  correctAnswer: number;
}

export const getRandomQuizzes = (quizzes: Quiz[], count: number = 3): Quiz[] => {
  const shuffled = [...quizzes].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
};