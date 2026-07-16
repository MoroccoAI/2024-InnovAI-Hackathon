import Section from "./Section";
import Heading from "./Heading";
import { check } from "../assets";
import stats from "../assets/stats.png";
import mascot from "../assets/mascot.png";
import wrld from "../assets/wrld.webp";
import { aabarServices } from "../constants";
import {
  PhotoChatMessage,
  Gradient,
  VideoChatMessage,
} from "./design/Services";

import Generating from "./Generating";

const Services = () => {
  return (
    <Section id="how-to-use">
      <div className="container">
        <Heading
          title="All your needs are fulfilled."
          text="Aabar unlocks the potential of AI-powered applications"
        />

        <div className="relative">
          <div className="relative z-1 flex items-center h-[39rem] mb-5 p-8 border border-n-1/10 rounded-3xl overflow-hidden lg:p-20 xl:h-[46rem]">
            <div className="absolute top-0 left-0 w-full h-full pointer-events-none md:w-3/5 xl:w-auto">
              <img
                className="w-full h-full object-cover md:object-right"
                width={800}
                alt="Monitor you wells"
                height={730}
                src={stats}
              />
            </div>

            <div className="relative z-1 max-w-[17rem] ml-auto">
              <h4 className="h4 mb-4">AabarMonitor. In real-time</h4>
              <p className="body-2 mb-[3rem] text-n-3">
                Monitor your wells in real-time with useful statistics
              </p>
              <ul className="body-2">
                {aabarServices.map((item, index) => (
                  <li
                    key={index}
                    className="flex items-start py-4 border-t border-n-6"
                  >
                    <img width={24} height={24} src={check} />
                    <p className="ml-4">{item}</p>
                  </li>
                ))}
              </ul>
            </div>

          </div>

          <div className="relative z-1 grid gap-5 lg:grid-cols-2">
            <div className="relative min-h-[39rem] border border-n-1/10 rounded-3xl overflow-hidden">
              <div className="absolute inset-0">
                <img
                  src={mascot}
                  className="h-full w-full object-cover translate-x-[40%]"
                  width={630}
                  height={750}
                  alt="robot"
                />
              </div>

              <div className="absolute inset-0 flex flex-col justify-end p-8 bg-gradient-to-b from-n-8/0 to-n-8/90 lg:p-15">
                <h4 className="h4 mb-4">AnzarChat</h4>
                <p className="body-2 mb-[3rem] text-n-3">
                  Chat with Anzar, a chatbot dedicated to help you on your digging journey
                </p>
                <Generating className="absolute left-4 right-4 bottom-4 border-n-1/10 border lg:left-1/2 lg-right-auto lg:bottom-8 lg:-translate-x-1/2" />

              </div>

              <PhotoChatMessage />
            </div>

            <div className="p-4 bg-n-7 rounded-3xl overflow-hidden lg:min-h-[46rem]">
              <div className="py-12 px-4 xl:px-8">
                <h4 className="h4 mb-4">AbaarPredict</h4>
                <p className="body-2 mb-[2rem] text-n-3">
                  Wanna know the best place to dig? Let's help you predict the place
                </p>
              </div>

              <div className="relative h-[20rem] bg-n-8 rounded-xl overflow-hidden md:h-[25rem]">
                <img
                  src={wrld}
                  className="w-full h-full object-cover"
                  width={520}
                  height={400}
                  alt="Scary robot"
                />

                <VideoChatMessage />
              </div>
            </div>
          </div>

          <Gradient />
        </div>
      </div>
    </Section>
  );
};

export default Services;
