import React from 'react';

import Section from '../../../HOC/Section';

const contact = () => {
  return (
    <Section id='contact'>
      <div className='container pt-2 pb-5'>
        <div className='section-header pt-5 pb-5 text-center'>
          <h3 className='section-title'>
            <span>Contact </span>Us
          </h3>
          <h6 className='section-subtitle mr-auto ml-auto'>
            Individualized quality care that meets the total needs of the
            patient Individualized quality care that quality care that
            Individualized quality care that meets the total.
          </h6>
        </div>
        <div className='section-content'>
          <div className='row'>
            <div className='col-md-9 col-lg-7'>
              <form action='https://formsubmit.co/sabib.team@gmail.com' method='POST'>
                <div className='form-group pb-3'>
                  <input
                    type='text'
                    name='name'
                    className='form-control rounded-0'
                    aria-describedby='emailHelp'
                    placeholder='Name'
                  />
                </div>
                <div className='form-group pb-3'>
                  <input
                    type='email'
                    name='email'
                    className='form-control rounded-0'
                    aria-describedby='emailHelp'
                    placeholder='Email'
                  />
                </div>
                <div className='form-group pb-3'>
                  <textarea
                  name='message'
                    className='form-control rounded-0'
                    rows='5'
                    placeholder='Enter Message...'
                  />
                </div>
                <div className='form-group text-center mt-5'>
                  <button className='btn btn-block btn-primary rounded-0 mr-auto ml-auto'>
                    Send
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default contact;