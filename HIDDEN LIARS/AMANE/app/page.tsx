import { Main, Section, Container, Box } from "@/components/craft";
import FeatureLeft from "@/components/home-page/feature-left";
import FeatureRight from "@/components/home-page/feature-right";
import FeatureRight2 from "@/components/home-page/feature-right2";
import FeatureLeft2 from "@/components/home-page/feature-left2";
import Hero from "@/components/home-page/hero";
import Services from "@/components/home-page/services";

export default async function Home() {
  // Remove the session check and redirection logic
  /* 
  const session = await getServerSession(authOptions);
  if (!session) {
    return redirect('/login');
  } else {
    return redirect('/home');
  }
  */

  // Return your landing page content directly
  return (
    <Main>
      <Section>
        <Container>
          <Hero/>
          <FeatureRight/>
           <FeatureLeft/>
           <FeatureRight2/>
           <FeatureLeft2/>
          <Services/>
        </Container>
      </Section>
    </Main>
  );
}
