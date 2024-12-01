import React, { createContext, useContext, useState, ReactNode } from "react";
import {FormData, QCMData, SousPartieCours, Report} from "../types/types"
// Define types for Level, Difficulty, and FormData


// Define the context type
interface AppContextType {
  customQcmData: QCMData; // Replace `any` with a more specific type if possible
  setCustomQcmData: React.Dispatch<React.SetStateAction<QCMData>>;
  qcmData: QCMData; // Replace `any` with a more specific type if possible
  setQcmData: React.Dispatch<React.SetStateAction<QCMData>>;
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
  customizedCourse: Array<SousPartieCours>;
  setCustomizedCourse: React.Dispatch<React.SetStateAction<Array<SousPartieCours>>>;
  report: Report; // Replace `any` with a more specific type if possible
  setReport: React.Dispatch<React.SetStateAction<Report>>;
}

// Define default values for formData
const defaultFormData: FormData = {
    level: "Lycée",
    year: "1ère Bac",
    branch: "Sciences Mathématiques",
    subject: "Mathématiques",
    lesson: "Notion de logique",
    difficulty: "Moyen",
    num_questions: 1,
  };

  const defaultReport: Report = {
    analyse_des_lacunes_par_sous_cours: [],
    conclusion: "",
  };
  // Create the context with default values
  const AppContext = createContext<AppContextType>({
    customQcmData: [],
    setCustomQcmData: () => {},
    qcmData: [],
    setQcmData: () => {}, // Default is a no-op function
    formData: defaultFormData,
    setFormData: () => {}, // Default is a no-op function
    customizedCourse: [],
    setCustomizedCourse: () => {}, // Default is a no-op function
    report: defaultReport, 
    setReport: () => {},
  });



// Provider component
export const AppProvider = ({ children }: { children: ReactNode }) => {
  // State for QCM data
  const [qcmData, setQcmData] = useState<QCMData>([]);
  const [customQcmData, setCustomQcmData] = useState<QCMData>([]);

  // State for form data
  const [formData, setFormData] = useState<FormData>(defaultFormData);
  const [report, setReport] = useState<Report>(defaultReport);
  const [customizedCourse, setCustomizedCourse] = useState<Array<SousPartieCours>>([]);

  return (
    <AppContext.Provider value={{ qcmData, setQcmData, formData, setFormData, customizedCourse, setCustomizedCourse, report, setReport, customQcmData, setCustomQcmData}}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook to use the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within a AppProvider");
  }
  return context;
};
