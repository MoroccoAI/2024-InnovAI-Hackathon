import React, { useRef } from "react";
import { heroBackground } from "../assets";
import mascot from "../assets/mascot.png";
import Button from "./Button";
import Section from "./Section";
import { BackgroundCircles, BottomLine } from "./design/Hero";
import { heroIcons } from "../constants";
import { ScrollParallax } from "react-just-parallax";
import Generating from "./Generating";
import Notification from "./Notification";
import CompanyLogos from "./CompanyLogos";
import TypingEffect from "./TypingEffect";

const Hero = () => {
  const parallaxRef = useRef(null);

  return (
    <Section
      className="pt-[12rem] -mt-[5.25rem]"
      crosses
      crossesOffset="lg:translate-y-[5.25rem]"
      customPaddings
      id="hero"
    >
      <div className="container relative" ref={parallaxRef}>
        <div className="flex flex-col lg:flex-row items-center justify-between">
          <div className="relative z-1 max-w-[31rem] mb-[3.875rem] md:mb-20 lg:mb-0 lg:mr-8">
            <h1 className="h1 mb-6">
              Revolutionize Your{" "}
              <span className="inline-block relative">
                Well Management{" "}
              </span>
              <br />
              with{" "}
              <TypingEffect
                words={[
                  "Smart Analytics",
                  "Real-time Monitoring",
                  "Predictive Maintenance",
                  "Efficient Operations",
                ]}
              />
            </h1>
            <p className="body-1 mb-6 text-n-2 lg:mb-8">
              Empower your national well management system with cutting-edge AI technology. 
              Optimize productivity, reduce costs, and ensure sustainable resource management 
              with our comprehensive solution.
            </p>
            <Button href="http://localhost:8501/" white>
              Go to dashboard
            </Button>
          </div>
          
          <div className="relative max-w-[23rem] mx-auto md:max-w-[30rem] lg:max-w-[35rem] xl:max-w-[40rem]">
            <div className="relative z-1 p-0.5 rounded-2xl bg-conic-gradient">
              <div className="relative bg-n-8 rounded-[1rem]">
                <div className="h-[1.4rem] bg-n-10 rounded-t-[0.9rem]" />

                <div className="aspect-[33/40] rounded-b-[0.9rem] overflow-hidden md:aspect-[688/490] lg:aspect-[1024/490]">
                  <img
                    src={mascot}
                    className="w-full scale-[1] translate-y-[16%] md:scale-[0.3] md:-translate-y-[20%] lg:-translate-y-[35%]"
                    width={1300}
                    height={1300}
                    alt="AI-powered well management system"
                  />

                  <Generating className="absolute left-4 right-4 bottom-5 md:left-1/2 md:right-auto md:bottom-8 md:w-[31rem] md:-translate-x-1/2" />

                  <ScrollParallax isAbsolutelyPositioned>
                    <ul className="hidden absolute -left-[5.5rem] bottom-[7.5rem] px-1 py-1 bg-n-9/40 backdrop-blur border border-n-1/10 rounded-2xl xl:flex">
                      {heroIcons.map((icon, index) => (
                        <li className="p-5" key={index}>
                          <img src={icon} width={24} height={25} alt={`Well management feature ${index + 1}`} />
                        </li>
                      ))}
                    </ul>
                  </ScrollParallax>

                  <ScrollParallax isAbsolutelyPositioned>
                    <Notification
                      className="hidden absolute -right-[5.5rem] bottom-[11rem] w-[18rem] xl:flex"
                      title="Well Well Well"
                    />
                  </ScrollParallax>
                </div>
              </div>

            </div>
            <div className="absolute -top-[54%] left-1/2 w-[234%] -translate-x-1/2 md:-top-[46%] md:w-[138%] lg:-top-[104%]">
              <img
                src={heroBackground}
                className="w-full"
                width={1440}
                height={1800}
                alt="National well management system background"
              />
            </div>

            <BackgroundCircles />
          </div>
        </div>
      </div>

      <BottomLine />
    </Section>
  );
};

export default Hero;

