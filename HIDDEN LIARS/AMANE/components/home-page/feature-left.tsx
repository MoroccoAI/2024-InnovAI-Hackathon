// React and Next.js imports
import Image from "next/image";
import Link from "next/link";

// UI component imports
import * as Craft from "@/components/craft";
import { Button } from "@/components/ui/button";

// Asset imports
import image from "@/public/farme.jpg"; // Updated image name

const FeatureLeft = () => {
  return (
    <Craft.Section>
      <Craft.Container className="grid items-stretch md:grid-cols-2 md:gap-12">
        {/* Left Image */}
        <div className="not-prose relative flex h-96 overflow-hidden rounded-lg border border-gray-300 dark:border-gray-700 shadow-md">
          <Image
            src={image}
            alt="Farmer using smart irrigation"
            className="object-cover"
            fill
          />
        </div>

        {/* Right Content */}
        <div className="flex flex-col gap-6 py-8">
          <h3 className="!my-0 text-5xl font-semibold text-gray-800 dark:text-gray-200">
            Smart Irrigation Planning
          </h3>
          <p className="text-lg font-medium leading-[1.6] text-gray-600 dark:text-gray-400">
            With precise insights tailored to your field conditions, our
            system provides actionable advice for optimizing irrigation
            schedules. By integrating weather forecasts and soil data,
            you can minimize water wastage and maximize crop growth. Our
            AI tools make it easy for everyone—from small-scale farmers to
            agricultural experts—to achieve sustainable farming practices.
          </p>
          {/* Buttons */}
          <div className="not-prose flex items-center gap-4">
            <Button className="w-fit px-6 py-3 text-base font-semibold" asChild>
              <Link href="#">Get Started</Link>
            </Button>
            {/* <Button
              className="w-fit px-6 py-3 text-base font-medium"
              variant="link"
              asChild
            >
              <Link href="#">Learn More →</Link>
            </Button> */}
          </div>
        </div>
      </Craft.Container>
    </Craft.Section>
  );
};

export default FeatureLeft;
