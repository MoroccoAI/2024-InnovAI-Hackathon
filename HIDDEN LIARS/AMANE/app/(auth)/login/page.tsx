import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import GithubSignInButton from "@/app/components/GithubSigninButton";
import GoogleSignInButton from "@/app/components/GoogleSigninButton";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/utils/auth";
import { redirect } from "next/navigation";

export default async function Login() {
  const session = await getServerSession(authOptions);

  if (session) {
    return redirect("/home");
  }
  
  return (
    <div className="mt-24 rounded py-10 px-6 md:mt-0 md:max-w-sm md:px-14 ">
      <form method="post" action="/api/auth/signin">
        <h1 className="text-3xl font-semibold text-black">Log in</h1>
        <div className="space-y-4 mt-5">
          <Input
            type="email"
            name="email"
            placeholder="Email"
            className="bg-gray-100 placeholder:text-xs placeholder:text-gray-500 text-black w-full inline-block"
          />
          <Button
            type="submit"
            variant="default"
            className="w-full text-white"
          >
            Log in
          </Button>
        </div>
      </form>

      <div className="text-gray-700 text-sm mt-2">
        New to<span className="text-blue"> Amane</span>?{" "}
        <Link className="text-blue-600 hover:underline" href="/signup">
          Sign up now
        </Link>
      </div>

      <div className="flex w-full justify-center items-center gap-x-3 mt-6">
        <GithubSignInButton />
        <GoogleSignInButton />
      </div>
    </div>
  );
}
