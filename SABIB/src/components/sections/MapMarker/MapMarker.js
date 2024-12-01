import React from 'react';
import Section from '../../../HOC/Section';

const mapMarker = () => {
  return (
    <Section id='map'>
      <div>
        <iframe
          title='mapMarker'
          src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3441.131654315704!2d-9.532903324561211!3d30.40400637474445!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xdb3c833de96eea5%3A0x5a539c7b2017bc32!2sUniversiapolis%20-%20Universit%C3%A9%20Internationale%20d&#39;Agadir!5e0!3m2!1sfr!2sma!4v1714162937248!5m2!1sfr!2sma'
          width='100%'
          height='450'
          frameBorder='0'
          style={{ border: 0, marginBottom: '-7px' }}
          allowFullScreen
        />
      </div>
    </Section>
  );
};

export default mapMarker;
