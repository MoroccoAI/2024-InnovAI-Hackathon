import React from 'react';
import './TopBar.css'; // Import the CSS file

const TopBar = () => {
  return (
    <div className='top-bar'>
      <div className='container top-bar-container'>
        <div className='top-bar-content'>
          <div className='icon-container'>
            <i className='fas fa-phone-alt m-2'/>
            <small>+212 (0) 637765253</small>
          </div>
          <div className='icon-container'>
            <i className='fas fa-envelope m-2' />
            <small>sabib.team@gmail.com</small>
          </div>
        </div>
        <div className='top-bar-content'>
          <div className='social-media-container'>
            <a href='!#' className='text-light social-media-link'>
              <i className='fab fa-facebook-f' />
            </a>
            <a href='!#' className='text-light social-media-link'>
              <i className='fab fa-twitter' />
            </a>
            <a href='https://www.instagram.com/sabib.team/' className='text-light social-media-link'>
              <i className='fab fa-instagram' />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopBar;
