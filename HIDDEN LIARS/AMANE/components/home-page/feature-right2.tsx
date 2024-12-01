// React and Next.js imports
import Link from "next/link";
import Image from "next/image";
import image from "../../public/farmer3.jpg"; // Updated image name

// UI component imports
import { Section, Container } from "@/components/craft";
import { Button } from "@/components/ui/button";

const FeatureRight2 = () => {
  return (
    <Section>
      <Container className="grid items-stretch md:grid-cols-2 md:gap-12">
        {/* Left Content */}
        <div className="flex flex-col gap-6 py-8">
          <h3 className="!my-0 text-5xl font-semibold text-gray-800 dark:text-gray-200">
            Sustainability for Morocco’s Future
          </h3>
          <p className="text-lg font-medium leading-[1.6] text-gray-600 dark:text-gray-400">
            Water scarcity is one of Morocco’s biggest challenges.
            Our AI-powered platform is designed to help farmers
            reduce water waste and embrace sustainable farming
            practices. By optimizing water usage, we’re not only
            helping farms thrive but also contributing to the
            long-term health of Morocco’s ecosystems and
            communities.
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

        {/* Right Image */}
        <div className="not-prose relative flex h-96 overflow-hidden rounded-lg border border-gray-300 dark:border-gray-700 shadow-md">
          <Image
            src={image}
            alt="Farmer using sustainable irrigation"
            className="object-cover"
            fill
          />
        </div>
      </Container>
    </Section>
  );
};

export default FeatureRight2;
