// React and Next.js imports
import Link from "next/link";
import Image from "next/image";

// Third-party library imports
import Balancer from "react-wrap-balancer";
import { Droplet, Leaf } from "lucide-react";

// Local component imports
import { Section, Container } from "@/components/craft";
import { Button } from "@/components/ui/button";

// Asset imports
import Logo from "@/public/amane.svg";

const Hero = () => {
  return (
    <Section>
      <Container className="flex flex-col items-center text-center">
        <Image
          src={Logo}
          width={262}
          height={72}
          alt="Amane Logo"
          className="not-prose mb-6 dark:invert md:mb-8"
        />
        <h1 className="!mb-0 text-green-700 dark:text-green-400">
          <Balancer>
            Optimize water management for sustainable agriculture.
          </Balancer>
        </h1>
        <h3 className="text-muted-foreground text-gray-600 dark:text-gray-300">
          <Balancer>
            Our connected solution helps you save water while maximizing your agricultural yields.
          </Balancer>
        </h3>
        <div className="not-prose mt-6 flex gap-2 md:mt-12">
          <Button variant={"default"} asChild>
            <Link href="/">
              <Droplet className="mr-2" />
              Discover the Solution
            </Link>
          </Button>
          <Button variant={"ghost"} asChild>
            <Link href="/posts">
              Learn More <Leaf className="ml-1" />
            </Link>
          </Button>
        </div>
      </Container>
    </Section>
  );
};

export default Hero;
