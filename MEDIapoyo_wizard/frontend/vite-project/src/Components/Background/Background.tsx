import React from 'react';
import './Background.css';
import v from '../../assets/vid1.mp4';
import f from '../../assets/f.jpg';
import s from '../../assets/s.jpg';
import t from '../../assets/t.jpg';

// Définir les types des props
interface BackgroundProps {
  playStatus: boolean;  // 'playStatus' est un booléen
  heroCount: number;    // 'heroCount' est un nombre
}

// Composant fonctionnel avec des types définis pour les props
const Background: React.FC<BackgroundProps> = ({ playStatus, heroCount }) => {
  // Si le jeu est en cours (playStatus est true), afficher la vidéo
  if (playStatus) {
    return (
      <video className="background fade-in" autoPlay loop muted>
        <source src={v} type="video/mp4" />
      </video>
    );
  }

  // Si le nombre de héros est égal à 0, afficher l'image 't.jpg'
  else if (heroCount === 0) {
    return <img src={t} className="background fade-in" alt="Aucun héros" />;
  }

  // Si le nombre de héros est égal à 1, afficher l'image 's.jpg'
  else if (heroCount === 1) {
    return <img src={s} className="background fade-in" alt="Un héros" />;
  }

  // Si le nombre de héros est égal à 2, afficher l'image 'f.jpg'
  else if (heroCount === 2) {
    return <img src={f} className="background fade-in" alt="Deux héros" />;
  }

  // Retourne rien si aucune condition n'est remplie
  return null;
};

export default Background;
