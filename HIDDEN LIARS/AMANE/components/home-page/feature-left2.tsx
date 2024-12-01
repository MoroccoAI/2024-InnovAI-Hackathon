// React and Next.js imports
import Image from "next/image";
import Link from "next/link";

// UI component imports
import * as Craft from "@/components/craft";
import { Button } from "@/components/ui/button";

// Asset imports
import farmerImage from "@/public/farmer.jpg"; // Updated image name

const FeatureLeft = () => {
  return (
    <Craft.Section>
      <Craft.Container className="grid items-stretch md:grid-cols-2 md:gap-12">
        {/* Left Image */}
        <div className="not-prose relative flex h-96 overflow-hidden rounded-lg border border-gray-300 dark:border-gray-700 shadow-md">
          <Image
            src={farmerImage}
            alt="Moroccan farmer using technology"
            className="object-cover"
            fill
          />
        </div>

        {/* Right Content */}
        <div className="flex flex-col gap-6 py-8">
          <h3 className="!my-0 text-5xl font-semibold text-gray-800 dark:text-gray-200">
            Empowering Moroccan Farmers with Technology
          </h3>
          <p className="text-lg font-medium leading-[1.6] text-gray-600 dark:text-gray-400">
            Our mission is to make advanced technology accessible to every farmer in Morocco. Whether you’re managing a large farm or a small plot, our app combines cutting-edge AI with a user-friendly design to give you the tools you need. From real-time data to interactive visualizations, we’re here to help you make the most of your resources for a sustainable agricultural future.
          </p>
          {/* Buttons */}
          <div className="not-prose flex items-center gap-4">
            <Button className="w-fit px-6 py-3 text-base font-semibold" asChild>
              <Link href="#">Get Started</Link>
            </Button>
            <Button
              className="w-fit px-6 py-3 text-base font-medium"
              variant="link"
              asChild
            >
              <Link href="#">Learn More →</Link>
            </Button>
          </div>
        </div>
      </Craft.Container>
    </Craft.Section>
  );
};

export default FeatureLeft;
