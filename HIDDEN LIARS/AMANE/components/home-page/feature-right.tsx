// React and Next.js imports
import Link from "next/link";
import Image from "next/image";
import image from "../../public/farmer2.jpg"; // Updated image name

// UI component imports
import { Section, Container } from "@/components/craft";
import { Button } from "@/components/ui/button";

const FeatureRight = () => {
  return (
    <Section>
      <Container className="grid items-stretch md:grid-cols-2 md:gap-12">
        {/* Left Content */}
        <div className="flex flex-col gap-6 py-8">
          <h3 className="!my-0 text-5xl font-semibold text-gray-800 dark:text-gray-200">
            Real-Time Irrigation Insights
          </h3>
          <p className="text-lg font-medium leading-[1.6] text-gray-600 dark:text-gray-400">
            Our platform uses cutting-edge AI models to analyze
            real-time data from soil and weather sensors. By
            predicting irrigation needs, we help farmers monitor and
            manage water resources effectively. Gain a complete
            understanding of your field’s hydration status and ensure
            every drop counts toward better yields and sustainability.
          </p>
          {/* Buttons */}
          <div className="not-prose flex items-center gap-4">
            {/* <Button className="w-fit px-6 py-3 text-base font-semibold" asChild>
              <Link href="#">Get Started</Link>
            </Button> */}
            <Button
              className="w-fit px-6 py-3 text-base font-medium"
              variant="link"
              asChild
            >
              <Link href="#">Learn More →</Link>
            </Button>
          </div>
        </div>

        {/* Right Image */}
        <div className="not-prose relative flex h-96 overflow-hidden rounded-lg border border-gray-300 dark:border-gray-700 shadow-md">
          <Image
            src={image}
            alt="Farmer with irrigation system"
            className="object-cover"
            fill
          />
        </div>
      </Container>
    </Section>
  );
};

export default FeatureRight;
