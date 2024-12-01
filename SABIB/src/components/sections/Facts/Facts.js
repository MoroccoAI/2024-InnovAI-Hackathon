import React from 'react';
import Section from '../../../HOC/Section';
import smartSprinkler from '../../../assets/img/smartSprinkler.png';
import { fontWeight } from '@mui/system';
import Link from '../../UI/Link/Link';

const Facts = () => {
  const containerStyle = {
    background: 'linear-gradient(180deg, #0A8EBF 0%, #054259 100%)',
    color: 'white',
    fontWeight: 'bold',
    paddingTop: '1.5rem',
    paddingBottom: '1.5rem', 
  };

  const imgStyle = {
    marginBottom: '-24px', 
  };

  const headingStyle = {
    fontSize: '3rem',
    fontWeight: 'bold'
  };

  const leadStyle = {
    fontSize: '1.25rem', 
  };

  return (
    <Section>
      <div className="container-fluid" style={containerStyle}>
        <div className="row justify-content-between align-items-start">
          <div className="col-lg-6 mt-3">
            <img
              src={smartSprinkler}
              alt="Background Image"
              className="img-fluid"
              style={imgStyle}
            />
          </div>
          <div className="col-lg-6">
            <div className="text-lg-start">
              <h1 style={headingStyle}>SABIB</h1> 
              <p className="lead" style={leadStyle}>Save Today Secure Tomorrow</p> 
              <h1>The Home's First Smart Water Network</h1> 
              <p className="mt-3 lead">
                With the Smart Water Network, you can now have complete control of
                the water both inside and outside of your home.
              </p>
              <Link  to="contact" classes="btn btn-light dark-text mt-3">Learn More</Link> 
            </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default Facts;
