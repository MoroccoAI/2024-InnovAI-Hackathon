import React from "react";

// Layout Components
import { Section, Container } from "@/components/craft";
import Balancer from "react-wrap-balancer";

// Icons
import { Droplet, Leaf, Sun } from "lucide-react";

type FeatureText = {
  icon: JSX.Element;
  title: string;
  description: string;
};

const featureText: FeatureText[] = [
  {
    icon: <Droplet className="h-7 w-7 text-blue-500" />, // Slightly larger icons
    title: "Optimal Water Management",
    description:
      "Monitor and control irrigation in real-time with smart sensors to reduce water waste.",
  },
  {
    icon: <Leaf className="h-7 w-7 text-green-500" />,
    title: "Support Sustainable Agriculture",
    description:
      "Our tools promote eco-friendly practices, enabling environmentally responsible farming.",
  },
  {
    icon: <Sun className="h-7 w-7 text-yellow-500" />,
    title: "Maximize Yields",
    description:
      "Analyze your crop needs and optimize resources to achieve maximum yields.",
  },
];

const Services = () => {
  return (
    <Section className="border-b">
      <Container className="not-prose">
        <div className="flex flex-col gap-8">
          {/* Title */}
          <h2 className="text-center text-6xl font-bold text-green-700 dark:text-green-400">
            <Balancer>Our Services</Balancer>
          </h2>

          {/* Subtitle */}
          <h3 className="text-center text-3xl font-semibold text-green-700 dark:text-green-400">
            <Balancer>
              Transform your water management with our innovative solutions
            </Balancer>
          </h3>

          {/* Supporting Text */}
          <h4 className="text-center text-2xl font-light text-gray-600 dark:text-gray-300">
            <Balancer>
              A sustainable and intelligent approach for high-performance
              agriculture
            </Balancer>
          </h4>

          {/* Features */}
          <div className="mt-6 grid gap-8 md:mt-12 md:grid-cols-3">
            {featureText.map(({ icon, title, description }, index) => (
              <div
                className="flex flex-col gap-4 border p-6 rounded-lg shadow-md hover:shadow-lg"
                key={index}
              >
                {icon}
                <h4 className="text-2xl font-semibold text-blue-600 dark:text-blue-400">
                  {title}
                </h4>
                <p className="text-lg text-gray-700 dark:text-gray-300 opacity-90">
                  {description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  );
};

export default Services;
