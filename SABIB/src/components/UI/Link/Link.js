// link.js
import React from 'react';
import { Link as ScrollLink } from 'react-scroll';
import { Link as RouterLink } from 'react-router-dom';

const Link = (props) => {
  const { to, isExternal, ...rest } = props;

  if (isExternal) {
    // Render external link using react-router-dom Link component
    return (
      <RouterLink to={to} className={props.classes} {...rest}>
        {props.children}
      </RouterLink>
    );
  } else {
    // Render internal smooth scroll link using react-scroll Link component
    return (
      <ScrollLink
        className={props.classes}
        style={{ cursor: 'pointer' }}
        activeClass='active'
        to={to}
        spy={true}
        smooth={true}
        offset={props.offset || -45}
        duration={500}
      >
        {props.children}
      </ScrollLink>
    );
  }
};

export default Link;
