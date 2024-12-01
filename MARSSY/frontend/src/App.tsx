import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import QCMApp from "./pages/QCM";
import GeneralQCMForm from "./pages/GeneralQCMForm";
import CustomQCMApp from "./pages/CustomizedQCM";
import { AppProvider } from "./pages/AppContext";
import CustomizedLesson from "./pages/CustomizedLesson";
import Report from "./pages/Report";







const App = () => {
  return (
    <AppProvider>
    <Router>
      <Routes>
        <Route path="/" element={<GeneralQCMForm/>} />
        <Route path="/qcm" element={<QCMApp />} />
        <Route path="/report" element={<Report />} />
        <Route path="/customized-course" element={<CustomizedLesson />} />
        <Route path="/customized-qcm" element={<CustomQCMApp />} />
      </Routes>
    </Router>
    </AppProvider>
  );
};

export default App;