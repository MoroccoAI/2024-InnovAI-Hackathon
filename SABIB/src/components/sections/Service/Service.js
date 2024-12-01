import React from 'react';

import Section from '../../../HOC/Section';
import how from '../../../assets/img/how.gif'
const Service = () => {
  return (
    <Section id='services'>
      <div className='container pt-2 pb-5'>
        <div className='section-header pt-5 pb-5 text-center'>
          <h3 className='section-title'>
            <span>Our </span>Services
          </h3>
          <h6 className='section-subtitle mr-auto ml-auto'>
            Individualized quality care that meets the total needs of the
            patient Individualized quality care that quality care that
            Individualized quality care that meets the total.
          </h6>
        </div>
        <div className='section-content'>
          <div className='row'>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-tachometer-alt' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>24/7 Leak Detection</h5>
                  <p className='service-description'>
                    Our latest FloSense™ 3.0 technology uses machine learning to better understand and analyze your water usage patterns. With more precise monitoring and leak detection accuracy, your Flo Smart Water Monitor and Shutoff
                    can better protect your home by sending timely, reliable alerts when it matters most.
                  </p>
                </div>
              </div>
            </div>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-power-off' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>Automatic Shutoff</h5>
                  <p className='service-description'>
                    Stop leaks in their tracks — even when you’re away from home — by setting your smart water
                    shutoff to automatically close your water valve when it detects a leak. You can even start and stop your water flow by closing the valve remotely through the app.
                  </p>
                </div>
              </div>
            </div>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-shield-alt' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>Proactive Protection</h5>
                  <p className='service-description'>
                  The best way to avoid water damage is to prevent it, and daily health tests automatically monitor your home to detect water leaks of all sizes. Once your device understands your water use, it can catch hidden 
                  leaks as small as a single drop per minute to protect your home and peace of mind.
                  </p>
                </div>
              </div>
            </div>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-bell' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>Real-Time Alerts</h5>
                  <p className='service-description'>
                  Receive real-time alerts via the app, texts or even a phone call when your device detects a leak, low temperatures or a running fixture.
                  </p>
                </div>
              </div>
            </div>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-chart-line' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>Conservation Goals</h5>
                  <p className='service-description'>
                  View your daily water consumption in the Moen Smart 
                  Water App to understand your water usage and set conservation goals to encourage water savings.
                  </p>
                </div>
              </div>
            </div>
            <div className='col-md-6 col-lg-4 mb-3'>
              <div className='service-box d-flex h-100'>
                <div className='service-icon mr-4'>
                  <i className='fas fa-headset' />
                </div>
                <div className='service-body'>
                  <h5 className='service-title'>Suppport Team</h5>
                  <p className='service-description'>
                  Our dedicated support team is here 24/7 to assist you with any questions or concerns you may have. 
                  Whether it's troubleshooting technical issues or providing guidance on maximizing the benefits of your smart water system, 
                  our knowledgeable team is just a call or message away.

                  </p>
                </div>
              </div>
            </div>
          </div>
          {/* <div className="flex flex-col items-center py-20 text-center bg-white bg-opacity-0">
            <h3 className="custom-color fw-bold mb-5 pt-5">
              How It Works
              <br />
            </h3>
            <div className="mt-20 text-4xl font-medium text-black max-md:mt-10 max-md:max-w-full mb-4">
              The Sabib Water Monitor and Shutoff is installed on your home’s main
              water supply line to proactively provide leak detection for your whole
              home.
            </div>
            <img
              src={how} alt='how it works'
              className="w-100"
            />
          </div> */}
        </div>
      </div>
    </Section>
  );
};

export default Service;
