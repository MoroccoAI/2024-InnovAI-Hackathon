import { useNavigate } from "react-router-dom";
import "./Hero.css";
import arrow_btn from "../../assets/arrow_btn.png";
import play_icon from "../../assets/play_icon.png";
import pause_icon from "../../assets/pause_icon.png";

// Définition des types des props
interface HeroProps {
  heroData: { text1: string; text2: string }[]; // tableau d'objets avec deux chaînes
  setHeroCount: (count: number) => void; // fonction pour mettre à jour heroCount
  heroCount: number; // index du héros
  setPlayStatus: (status: boolean) => void; // fonction pour mettre à jour playStatus
  playStatus: boolean; // état de lecture
}

const Hero: React.FC<HeroProps> = ({
  heroData,
  setHeroCount,
  heroCount,
  setPlayStatus,
  playStatus,
}) => {
  const navigate = useNavigate(); // Initialize the hook

  const handleArrowClick = () => {
    navigate("/api-data"); // Utilise navigate pour rediriger vers /api-data
  };

  return (
    <div className="hero">
      <div className="hero-text">
        <p>{heroData[heroCount].text1}</p>
        <p>{heroData[heroCount].text2}</p>
      </div>
      <div className="hero-explore" onClick={handleArrowClick}>
        <p>Chatbot</p>
        <img src={arrow_btn} alt="arrow button" />
      </div>
      <div className="hero-dot-play">
        <ul className="hero-dots">
          <li
            onClick={() => setHeroCount(0)}
            className={heroCount === 0 ? "hero-dot orange" : "hero-dot"}
          ></li>
          <li
            onClick={() => setHeroCount(1)}
            className={heroCount === 1 ? "hero-dot orange" : "hero-dot"}
          ></li>
          <li
            onClick={() => setHeroCount(2)}
            className={heroCount === 2 ? "hero-dot orange" : "hero-dot"}
          ></li>
        </ul>
        <div className="hero-play">
          <img
            onClick={() => setPlayStatus(!playStatus)}
            src={playStatus ? pause_icon : play_icon}
            alt=""
          />
          <p>See the video</p>
        </div>
      </div>
    </div>
  );
};

export default Hero;
