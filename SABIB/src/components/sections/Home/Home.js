import React from 'react';
import Section from '../../../HOC/Section';
import Link from '../../UI/Link/Link';
import bgVideo from '../../../assets/videos/faststart.mp4';
import './Home.css'; 
const Home = () => {
  return (
    <Section id='home'>
      <div className='video-container'>
        <video autoPlay loop muted className='fullscreen-video'>
          <source src={bgVideo} type='video/mp4' />
          Your browser does not support the video tag.
        </video>
        <div className='content-overlay '>
          <div className='home-content p-5 text-center text-light m-5'>
            <h1 className='title'>Stay One Step Ahead of Water Damage</h1>
            <div className='p-0 position-relative z-index-1'>
            <Link to='about' classes='btn btn-primary rounded-0 mr-2' >
                Learn More
              </Link>
              <Link to='contact' classes='btn btn-light text-dark rounded-0' >
                Contact Us
              </Link>
    </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default Home;
