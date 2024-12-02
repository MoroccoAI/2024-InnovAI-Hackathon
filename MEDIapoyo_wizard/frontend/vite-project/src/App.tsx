import { useEffect, useState } from "react";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Background from "./Components/Background/Background";
import Navbar from "./Components/Navbar/Navbar";
import Hero from "./Components/Hero/Hero";
import Annotation from "./pages/Annotation";
import Signin from "./pages/Signin";
import Login from "./pages/login";
import ApiData from "./pages/ApiData";
import "./App.css";

const App = () => {
  let heroData = [
    { text1: "Your", text2: "..." },
    { text1: "Care ", text2: "starts here" },
    { text1: " Ask", text2: " learn, heal" },
  ];
  const [heroCount, setHeroCount] = useState(0);
  const [playStatus, setPlayStatus] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setHeroCount((count) => (count === 2 ? 0 : count + 1));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <BrowserRouter>
      <div>
        <Background playStatus={playStatus} heroCount={heroCount} />
        <Navbar />
        <Routes>
          <Route
            path="/"
            element={
              <Hero
                setPlayStatus={setPlayStatus}
                heroData={heroData}
                heroCount={heroCount}
                setHeroCount={setHeroCount}
                playStatus={playStatus}
              />
            }
          />
          <Route path="/annotation" element={<Annotation />} />
          <Route path="/Signin" element={<Signin />} />
          <Route path="/login" element={<Login />} />
          <Route path="/api-data" element={<ApiData />} />{" "}
          {/* Ensure this route is here */}
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
