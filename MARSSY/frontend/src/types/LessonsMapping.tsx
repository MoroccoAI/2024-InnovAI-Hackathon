import { Difficulty } from "./types"


export const levels: string[] = ["Lycée", "Collège (Bientôt disponible)", "Primaire (Bientôt disponible)"];
export const years: Record<string, string[]> = {
  "Lycée": ["Tronc Commun (Bientôt disponible)", "1ère Bac", "2ème Bac (Bientôt disponible)"],
  "Collège (Bientôt disponible)": ["1ère année", "2ère année", "3ère année"],
  "Primaire (Bientôt disponible)": ["1ère année", "2ère année", "3ère année","4ère année", "5ère année", "6ère année"],
};
export const branches: Record<string, Record<string, string[]>> = {
  // branches for lycée are not complete
  "Lycée": {
    "1ère Bac": ["Sciences Mathématiques", "Sciences Expérimentales (Bientôt disponible)","Sciences Économiques et Gestion (Bientôt disponible)"],
    "2ème Bac": ["Sciences Mathématiques A", "Sciences Mathématiques B", "Sciences Physiques"],
    "Tronc Commun": ["Sciences","Technologies", "Lettres et Sciences Humaines"],
  },
  "Collège (Bientôt disponible)": {
    "1ère année": ["Commun"],
    "2ère année": ["Commun"],
    "3ère année": ["Commun"],
  },
  "Primaire (Bientôt disponible)": {
    "1ère année": ["Commun"],
    "2ère année": ["Commun"],
    "3ère année": ["Commun"],
    "4ère année": ["Commun"],
    "5ère année": ["Commun"],
    "6ère année": ["Commun"],
  },
};

export const subjects: Record<string, string[]> = {
  // Lycée
  "Lycée-1ère Bac-Sciences Mathématiques": ["Mathématiques", "Français (Bientôt disponible)", "Physiques (Bientôt disponible)"],
  "Lycée-1ère Bac-Sciences Expérimentales (Bientôt disponible)": ["Mathématiques", "Français", "Physiques"],
  "Lycée-1ère Bac-Sciences Économiques et Gestion (Bientôt disponible)": ["Mathématiques", "Français", "Physiques"],
  "Lycée-2ème Bac-Sciences Mathématiques A": ["Mathématiques", "Français", "Physiques"],
  "Lycée-2ème Bac-Sciences Mathématiques B": ["Mathématiques", "Français", "Physiques"],
  "Lycée-2ème Bac-Sciences Physiques": ["Mathématiques", "Français", "Physiques"],
  "Lycée-Tronc Commun-Sciences": ["Mathématiques", "Français", "Physiques"],
  "Lycée-Tronc Commun-Technologies": ["Mathématiques", "Français", "Physiques"],
  "Lycée-Tronc Commun-Lettres et Sciences Humaines": ["Mathématiques", "Français", "Physiques"],
  
  // Collège (Bientôt disponible)
  "Collège (Bientôt disponible)-1ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Collège (Bientôt disponible)-2ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Collège (Bientôt disponible)-3ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  
  // Primaire (Bientôt disponible)
  "Primaire (Bientôt disponible)-1ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Primaire (Bientôt disponible)-2ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Primaire (Bientôt disponible)-3ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Primaire (Bientôt disponible)-4ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Primaire (Bientôt disponible)-5ère année-Commun": ["Mathématiques", "Français", "Physiques"],
  "Primaire (Bientôt disponible)-6ère année-Commun": ["Mathématiques", "Français", "Physiques"],
};


export const difficulties: Difficulty[] = ["Facile", "Moyen", "Difficile"];

export const lessons: Record<string, string[]> = {
  // Lycée
  "Lycée-1ère Bac-Sciences Mathématiques-Mathématiques": ["Notion de logique", "Ensembles (Bientôt disponible)", "Autres (Bientôt disponible)"],
  "Lycée-1ère Bac-Sciences Mathématiques-Français": [],
  "Lycée-1ère Bac-Sciences Mathématiques-Physiques": [],
  "Lycée-1ère Bac-Sciences Expérimentales (Bientôt disponible)-Mathématiques": [],
  "Lycée-1ère Bac-Sciences Expérimentales (Bientôt disponible)-Français": [],
  "Lycée-1ère Bac-Sciences Expérimentales (Bientôt disponible)-Physiques": [],
  "Lycée-1ère Bac-Sciences Économiques et Gestion (Bientôt disponible)-Mathématiques": [],
  "Lycée-1ère Bac-Sciences Économiques et Gestion (Bientôt disponible)-Français": [],
  "Lycée-1ère Bac-Sciences Économiques et Gestion (Bientôt disponible)-Physiques": [],
  "Lycée-2ème Bac-Sciences Mathématiques A-Mathématiques": [],
  "Lycée-2ème Bac-Sciences Mathématiques A-Français": [],
  "Lycée-2ème Bac-Sciences Mathématiques A-Physiques": [],
  "Lycée-2ème Bac-Sciences Mathématiques B-Mathématiques": [],
  "Lycée-2ème Bac-Sciences Mathématiques B-Français": [],
  "Lycée-2ème Bac-Sciences Mathématiques B-Physiques": [],
  "Lycée-2ème Bac-Sciences Physiques-Mathématiques": [],
  "Lycée-2ème Bac-Sciences Physiques-Français": [],
  "Lycée-2ème Bac-Sciences Physiques-Physiques": [],
  "Lycée-Tronc Commun-Sciences-Mathématiques": [],
  "Lycée-Tronc Commun-Sciences-Français": [],
  "Lycée-Tronc Commun-Sciences-Physiques": [],
  "Lycée-Tronc Commun-Technologies-Mathématiques": [],
  "Lycée-Tronc Commun-Technologies-Français": [],
  "Lycée-Tronc Commun-Technologies-Physiques": [],
  "Lycée-Tronc Commun-Lettres et Sciences Humaines-Mathématiques": [],
  "Lycée-Tronc Commun-Lettres et Sciences Humaines-Français": [],
  "Lycée-Tronc Commun-Lettres et Sciences Humaines-Physiques": [],

  // Collège (Bientôt disponible)
  "Collège (Bientôt disponible)-1ère année-Commun-Mathématiques": [],
  "Collège (Bientôt disponible)-1ère année-Commun-Français": [],
  "Collège (Bientôt disponible)-1ère année-Commun-Physiques": [],
  "Collège (Bientôt disponible)-2ère année-Commun-Mathématiques": [],
  "Collège (Bientôt disponible)-2ère année-Commun-Français": [],
  "Collège (Bientôt disponible)-2ère année-Commun-Physiques": [],
  "Collège (Bientôt disponible)-3ère année-Commun-Mathématiques": [],
  "Collège (Bientôt disponible)-3ère année-Commun-Français": [],
  "Collège (Bientôt disponible)-3ère année-Commun-Physiques": [],

  // Primaire (Bientôt disponible)
  "Primaire (Bientôt disponible)-1ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-1ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-1ère année-Commun-Physiques": [],
  "Primaire (Bientôt disponible)-2ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-2ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-2ère année-Commun-Physiques": [],
  "Primaire (Bientôt disponible)-3ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-3ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-3ère année-Commun-Physiques": [],
  "Primaire (Bientôt disponible)-4ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-4ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-4ère année-Commun-Physiques": [],
  "Primaire (Bientôt disponible)-5ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-5ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-5ère année-Commun-Physiques": [],
  "Primaire (Bientôt disponible)-6ère année-Commun-Mathématiques": [],
  "Primaire (Bientôt disponible)-6ère année-Commun-Français": [],
  "Primaire (Bientôt disponible)-6ère année-Commun-Physiques": [],
};
