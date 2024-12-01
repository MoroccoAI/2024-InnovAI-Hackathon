"use client";

import { Button } from "@/components/ui/button";
import { GithubIcon } from "lucide-react";
import { signIn } from "next-auth/react";

export default function GithubSigninButton() {
    return(
        <Button onClick={()=>signIn("github")}
            variant="outline" size="icon">
            <GithubIcon className=""/>
        </Button>
    )
}