import { Button } from "@/components/ui/button";
import { UserButton } from "@clerk/nextjs";
import Image from "next/image";
import DashboardHeader from "./dashboard/_components/DashboardHeader";
import FeatureCard from "@/app/featureCard";
import FeatureCardList from "@/app/featureCard";

export default function Home() {
  return (
   <div>
      <DashboardHeader/>
      <section className=" z-50 pt-10">
          <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">


              <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
                  <span className='text-primary'>Empower Your Learning Journey with </span><br></br> AI-Driven Study
                  Plans </h1>
              <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">Boost
                  your learning with personalized study plans, interactive quizzes, and AI-powered insights. Upload your
                  files and let our smart assistant guide you every step of the way!</p>


                    <FeatureCardList/>


              <div
                  className="flex flex-col mt-6 mb-8 lg:mb-16 space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                  <a href="/dashboard"
                     className="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-white rounded-lg bg-primary hover:bg-primary focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">
                      Get Started
                      <svg className="ml-2 -mr-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                           xmlns="http://www.w3.org/2000/svg">
                          <path fillRule="evenodd"
                                d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                                clipRule="evenodd"></path>
                      </svg>
                  </a>

              </div>


          </div>
      </section>

       <section className="flex items-center justify-center rounded-lg">


       </section>

   </div>
  );
}
