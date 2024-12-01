// Nav.js
import React, { useState, useEffect } from 'react';
import Logo from '../../../assets/img/sabib.png';
import './Nav.css';
import Link from '../Link/Link';
import { UserButton } from '@clerk/clerk-react';

const Nav = () => {
  const [navClass, setNavClass] = useState('');
  const [toggledNav, setToggledNav] = useState(false);

  const toggleNav = () => {
    setToggledNav(!toggledNav);
  };

  useEffect(() => {
    const handleScroll = () => {
      const newNavClass = window.scrollY >= 200 ? 'scrolled' : '';
      setNavClass(newNavClass);
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <nav className={`navbar navbar-expand-md navbar-light bg-light ${navClass}`}>
      <div className='container'>
        <Link to='/' isExternal={false} classes='navbar-brand'>
          <img src={Logo} className='logo-img' alt='logo' />
        </Link>
        <button
          className={`navbar-toggler ${toggledNav ? 'collapsed' : ''}`}
          type='button'
          aria-expanded={toggledNav ? 'true' : 'false'}
          aria-label='Toggle navigation'
          onClick={toggleNav}
        >
          <span className='navbar-toggler-icon' />
        </button>

        <div className={`collapse navbar-collapse ${toggledNav ? 'show' : ''}`}>
          <ul className='navbar-nav ms-auto'>
            <li className='nav-item'>
              <Link to='home' classes='nav-link'>
                Home
              </Link>
            </li>
            <li className='nav-item'>
              <Link to='about' classes='nav-link'>
                About
              </Link>
            </li>
            <li className='nav-item'>
              <Link to='services' classes='nav-link'>
                Services
              </Link>
            </li>
            <li className='nav-item'>
              <Link to='blog' classes='nav-link'>
                Blog
              </Link>
            </li>
            <li className='nav-item'>
              <Link to='contact' classes='nav-link'>
                Contact
              </Link>
            </li>
            <li className='nav-item'>
              <Link to='/login' isExternal={true} classes='nav-link'>
                Dashboard
              </Link>
            </li>
            <UserButton />
          </ul>

        </div>

      </div>
      
    </nav>
  );
};

export default Nav;
