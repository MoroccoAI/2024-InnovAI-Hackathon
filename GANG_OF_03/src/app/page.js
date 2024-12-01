import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  CheckCircle,
  ArrowRight,
  BarChart,
  BrainCircuit,
  TrendingUp,
  Heart,
  Moon,
  Footprints,
  Star,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container px-4 py-4 mx-auto">
          <nav className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold">
              Burnout Predictor
            </Link>
            <div className="space-x-4">
              <Button variant="ghost" asChild>
                <Link href="#features">Features</Link>
              </Button>
              <Button variant="ghost" asChild>
                <Link href="#pricing">Pricing</Link>
              </Button>
              <Button asChild>
                <Link href="/login">Login</Link>
              </Button>
              <Button variant="outline" asChild>
                <Link href="/signup">Sign Up</Link>
              </Button>
            </div>
          </nav>
        </div>
      </header>

      <main>
        <section className="px-4 py-20 bg-gradient-to-b from-background to-muted">
          <div className="container mx-auto text-center">
            <h2 className="mb-4 text-5xl font-extrabold leading-tight">
              Predict and Prevent Burnout
              <br />
              <span className="text-primary">Before It Happens</span>
            </h2>
            <p className="max-w-2xl mx-auto mb-8 text-xl text-muted-foreground">
              Harness the power of your smartwatch data to stay healthy,
              productive, and balanced. Join thousands of professionals taking
              control of their well-being.
            </p>
            <Button size="lg" asChild className="mr-4">
              <Link href="/signup">
                Start Free Trial <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="#features">See How It Works</Link>
            </Button>
          </div>
        </section>

        <section id="features" className="py-20">
          <div className="container px-4 mx-auto">
            <h3 className="mb-12 text-4xl font-bold text-center">
              Powerful Features to Keep You Balanced
            </h3>
            <div className="grid gap-8 md:grid-cols-3">
              <Card className="transition-all duration-300 hover:shadow-lg">
                <CardHeader>
                  <BarChart className="w-10 h-10 mb-2 text-primary" />
                  <CardTitle>Real-time Monitoring</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>
                    Track vital metrics like heart rate, sleep patterns, and
                    activity levels in real-time to assess your burnout risk
                    accurately.
                  </p>
                </CardContent>
              </Card>
              <Card className="transition-all duration-300 hover:shadow-lg">
                <CardHeader>
                  <BrainCircuit className="w-10 h-10 mb-2 text-primary" />
                  <CardTitle>AI-Powered Insights</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>
                    Receive personalized recommendations based on advanced AI
                    analysis of your data to improve well-being and
                    productivity.
                  </p>
                </CardContent>
              </Card>
              <Card className="transition-all duration-300 hover:shadow-lg">
                <CardHeader>
                  <TrendingUp className="w-10 h-10 mb-2 text-primary" />
                  <CardTitle>Trend Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>
                    Visualize your burnout risk over time and identify patterns
                    to make informed lifestyle changes and track improvements.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/50">
          <div className="container px-4 mx-auto">
            <h3 className="mb-12 text-4xl font-bold text-center">
              How Burnout Predictor Works
            </h3>
            <div className="grid gap-8 md:grid-cols-4">
              {[
                {
                  icon: Heart,
                  title: "Connect",
                  description: "Link your smartwatch to our secure platform",
                },
                {
                  icon: BrainCircuit,
                  title: "Analyze",
                  description:
                    "We process your data using advanced AI algorithms",
                },
                {
                  icon: BarChart,
                  title: "Assess",
                  description: "Get real-time burnout risk assessments",
                },
                {
                  icon: TrendingUp,
                  title: "Improve",
                  description:
                    "Follow personalized recommendations and track progress",
                },
              ].map((step, index) => (
                <Card
                  key={index}
                  className="transition-all duration-300 hover:shadow-lg"
                >
                  <CardHeader>
                    <step.icon className="w-10 h-10 mb-2 text-primary" />
                    <CardTitle>{step.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p>{step.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section id="pricing" className="py-20">
          <div className="container px-4 mx-auto">
            <h3 className="mb-12 text-4xl font-bold text-center">
              Simple, Transparent Pricing
            </h3>
            <div className="grid gap-8 md:grid-cols-3">
              {[
                {
                  title: "Basic",
                  price: "$9.99",
                  features: [
                    "Real-time monitoring",
                    "Basic AI insights",
                    "7-day data history",
                    "Email support",
                  ],
                },
                {
                  title: "Pro",
                  price: "$19.99",
                  features: [
                    "All Basic features",
                    "Advanced AI insights",
                    "30-day data history",
                    "Priority email support",
                    "Personalized recommendations",
                  ],
                },
                {
                  title: "Enterprise",
                  price: "Custom",
                  features: [
                    "All Pro features",
                    "Unlimited data history",
                    "24/7 phone support",
                    "Custom integrations",
                    "Team management",
                  ],
                },
              ].map((plan, index) => (
                <Card
                  key={index}
                  className="transition-all duration-300 hover:shadow-lg"
                >
                  <CardHeader>
                    <CardTitle className="text-2xl">{plan.title}</CardTitle>
                    <CardDescription className="text-3xl font-bold">
                      {plan.price}
                      {plan.price !== "Custom" && (
                        <span className="text-sm font-normal">/month</span>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-center">
                          <CheckCircle className="w-5 h-5 mr-2 text-primary" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                    <Button className="w-full mt-6" asChild>
                      <Link href="/signup">Choose Plan</Link>
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted/50">
          <div className="container px-4 mx-auto">
            <h3 className="mb-12 text-4xl font-bold text-center">
              What Our Users Say
            </h3>
            <div className="grid gap-8 md:grid-cols-3">
              {[
                {
                  name: "Sarah K.",
                  role: "Software Engineer",
                  quote:
                    "Burnout Predictor has been a game-changer for my work-life balance. I feel more in control of my well-being than ever before.",
                },
                {
                  name: "Michael R.",
                  role: "Marketing Manager",
                  quote:
                    "The personalized insights have helped me make small but impactful changes to my daily routine. I'm more productive and less stressed.",
                },
                {
                  name: "Emily T.",
                  role: "Healthcare Professional",
                  quote:
                    "As someone who works long shifts, this app has been crucial in helping me manage my energy levels and prevent burnout.",
                },
              ].map((testimonial, index) => (
                <Card
                  key={index}
                  className="transition-all duration-300 hover:shadow-lg"
                >
                  <CardHeader>
                    <CardTitle>{testimonial.name}</CardTitle>
                    <CardDescription>{testimonial.role}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="italic">"{testimonial.quote}"</p>
                    <div className="flex mt-4">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className="w-5 h-5 text-yellow-400 fill-current"
                        />
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20">
          <div className="container px-4 mx-auto text-center">
            <h3 className="mb-4 text-4xl font-bold">
              Ready to take control of your well-being?
            </h3>
            <p className="max-w-2xl mx-auto mb-8 text-xl text-muted-foreground">
              Join thousands of professionals who are already benefiting from
              Burnout Predictor. Start your journey to a balanced, productive
              life today.
            </p>
            <Button size="lg" asChild>
              <Link href="/signup">
                Start Your Free 14-Day Trial{" "}
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </Button>
            <p className="mt-4 text-sm text-muted-foreground">
              No credit card required
            </p>
          </div>
        </section>
      </main>

      <footer className="py-12 bg-muted">
        <div className="container px-4 mx-auto">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <h4 className="mb-4 text-lg font-bold">Burnout Predictor</h4>
              <p className="text-muted-foreground">
                Empowering you to take control of your well-being and
                productivity.
              </p>
            </div>
            <div>
              <h4 className="mb-4 text-lg font-bold">Product</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="#features"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Features
                  </Link>
                </li>
                <li>
                  <Link
                    href="#pricing"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Pricing
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    FAQ
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4 text-lg font-bold">Company</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    About Us
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Careers
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="mb-4 text-lg font-bold">Legal</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-muted-foreground hover:text-primary"
                  >
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="pt-8 mt-8 text-center border-t text-muted-foreground">
            <p>&copy; 2024 Burnout Predictor. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
