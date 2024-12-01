import React from 'react';

import Section from '../../../HOC/Section';

import blogImage1 from '../../../assets/img/blog1.jpg';
import blogImage2 from '../../../assets/img/blog2.jpg';
import blogImage3 from '../../../assets/img/blog3.jpg';
import prec90 from '../../../assets/img/per90.gif';
import prec60 from '../../../assets/img/per60.gif';
import Blog4 from '../../../assets/img/blog4.png'; 
import Link from '../../UI/Link/Link';
import '../../../components/sections/Blog/Blog.css';
const Blog = () => {
  return (
    <Section id='blog'>
      <div className='container pt-2 pb-5 '>
        <div className='section-header pt-5 pb-5 text-center'>
          <h3 className='section-title'>
            <span>Our </span>Blog
          </h3>
          <h6 className='section-subtitle mr-auto ml-auto'>
            Individualized quality care that meets the total needs of the
            patient Individualized quality care that quality care that
            Individualized quality care that meets the total.
          </h6>
        </div>
        <div className='section-content'>
        <div className='row'>
  <div className='col-lg-4 mb-3'>
    <div className='card rounded-0'>
      <img src={blogImage1} className='card-img-top1' alt='Blog 1' />
      <div className='card-body'>
        <h5 className='card-title'>Smart Leak Detection</h5>
        <p className='card-text'>
          Learn how our smart water monitoring technology detects leaks in real-time, helping you prevent water wastage and avoid costly damage to your property.
        </p>
        <a href='/smart-leak-detection' className='btn btn-sm btn-primary'>
          Read More
        </a>
      </div>
    </div>
  </div>
  <div className='col-lg-4 mb-3'>
    <div className='card rounded-0'>
      <img src={blogImage2} className='card-img-top1' alt='Blog 2' />
      <div className='card-body'>
        <h5 className='card-title'>Water Conservation Tips</h5>
        <p className='card-text'>
          Discover practical tips and strategies to reduce your water consumption and contribute to environmental conservation while saving money on your water bills.
        </p>
        <a href='/water-conservation-tips' className='btn btn-sm btn-primary'>
          Read More
        </a>
      </div>
    </div>
  </div>
  <div className='col-lg-4 mb-3'>
    <div className='card rounded-0'>
      <img src={blogImage3} className='card-img-top1' alt='Blog 3' />
      <div className='card-body'>
        <h5 className='card-title'>The Importance of Timely Repairs</h5>
        <p className='card-text'>
          Learn why timely repairs of plumbing issues are crucial for preventing water wastage and maintaining the integrity of your water supply system.
        </p>
        <a href='/importance-of-timely-repairs' className='btn btn-sm btn-primary'>
          Read More
        </a>
      </div>
    </div>
  </div>
</div>

          <div className="flex flex-col pt-5 pb-20 bg-white">
      <h3 className="text-center custom-color fw-bold mb-5 pt-3">
        Start Saving Water And Money Today
      </h3>
  <div className="flex flex-col px-16 mt-20 w-full max-md:px-5 max-md:mt-10 max-md:max-w-full">
  <div className="flex gap-5 text-2xl font-bold text-center text-black max-md:flex-wrap max-md:mr-2.5 max-md:max-w-full">
    <div className="mt-20 text-4xl font-medium text-black max-md:mt-10 max-md:max-w-full mb-4">
      The SABIB Smart Water Monitor and Shutoff can reduce water usage by up to 90%.
    </div>
  </div>
</div>
    
    <div className="d-flex justify-content-around">
    <img src={prec90} className="percImg mb-5" alt="90% Reduction" />
    <img src={prec60} className="percImg mb-5" alt="60% Reduction" />
  </div>

        </div>
        </div>
        <div className='row pt-5 mt-5 bg-white'>
            <div className='col-lg-6 mb-3'>
              {/* Image */}
              <img src={Blog4} className='card-img-top' alt='Blog Image' />
            </div>
            <div className='col-lg-6 mb-3'>
              {/* Text and Button */}
              <div className='text-left'>
                <h2 className='text-info'>Real-Time Insight & Water Monitoring Mastery with Sabib</h2>
                <p className='fw-bold'>Sabib's technology can help organizations and communities make informed decisions about water management, conservation, and sustainability.</p>
                <button className='btn btn-primary rounded-0'>Read More</button>
              </div>
            </div>
          </div>
          <div className='row pt-5 mt-0 bg-white'>
            
            <div className='col-lg-6 mb-3'>
              {/* Text and Button */}
              <div className='text-left'>
                <h2 className='text-info'>Real-Time Insight & Water Monitoring Mastery with Sabib</h2>
                <p className='fw-bold'>Sabib's technology can help organizations and communities make informed decisions about water management, conservation, and sustainability.</p>
                <Link classes='btn btn-primary text-light rounded-0' >Read More</Link>
              </div>
            </div>
            <div className='col-lg-6 mb-3'>
              {/* Image */}
              <img src={Blog4} className='card-img-top' alt='Blog Image' />
            </div>
          </div>
      </div>
      
    </Section>
  );
};

export default Blog;
