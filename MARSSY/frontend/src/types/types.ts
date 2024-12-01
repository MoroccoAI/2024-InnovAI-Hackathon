export type QCMData = Array<{
    sous_cours_name: string;
    content: Array<{
      question: string;
      options: string[];
      correct_answer: string;
    }>;
  }>;


  export type Level = "Lycée" | "Collège" | "Primaire";
  export type Difficulty = "Facile" | "Moyen" | "Difficile";
  
  export interface FormData {
    level: Level | "";
    year: string | "";
    branch: string;
    subject: string;
    lesson: string;
    difficulty: Difficulty | "";
    num_questions: number;
  }

  export interface SousPartieCours {
    sub_title: string;
    content: string;
}

export interface Report {
  analyse_des_lacunes_par_sous_cours: Array<any>;
  conclusion: string;
}