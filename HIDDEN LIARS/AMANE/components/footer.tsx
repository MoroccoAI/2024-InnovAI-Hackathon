// React and Next.js imports
import Image from "next/image";
import Link from "next/link";

// Third-party library imports
import Balancer from "react-wrap-balancer";

// Local component imports
import { Section, Container } from "./craft";

// Asset imports
import Logo from "@/public/amane.svg"; // Updated logo path

export default function Footer() {
  return (
    <footer>
      <Section>
        <Container className="grid gap-12 md:grid-cols-[1.5fr_0.5fr_0.5fr]">
          <div className="grid gap-6">
            <Link href="/">
              <h3 className="sr-only">Amane</h3> {/* Updated company name */}
              <Image
                src={Logo}
                alt="Amane"
                width={150}
                height={40}
                className="transition-all hover:opacity-75 dark:invert"
              ></Image>
            </Link>
            <p>
              <Balancer>
                Amane is a service designed to assist farmers and agriculturalists by automating water management for their crops, ensuring optimal irrigation and resource efficiency.
              </Balancer>
            </p>
            <p className="text-muted-foreground">
              ©{" "}
              <a href="https://github.com/brijr/components">Amane</a> {/* Updated link */}
              . All rights reserved. 2024-present.
            </p>
          </div>
          <div className="flex flex-col gap-2">
            <h5>Website</h5>
            <Link href="/">Blog</Link>
            <Link href="/">Authors</Link>
            <Link href="/">Categories</Link>
          </div>
          <div className="flex flex-col gap-2">
            <h5>Legal</h5>
            <Link href="/privacy-policy">Privacy Policy</Link>
            <Link href="/terms-of-service">Terms of Service</Link>
            <Link href="/cookie-policy">Cookie Policy</Link>
          </div>
        </Container>
      </Section>
    </footer>
  );
}
