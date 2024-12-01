"use client";

import { cn } from "@/lib/utils";
import { MenuIcon } from "lucide-react";
import Link from "next/link";
import * as React from "react";
import { Dialog, DialogClose } from "./ui/dialog";
import { Button } from "./ui/button";
import Logo from "@/public/amane.svg";
import Image from "next/image";
import {
  NavigationMenu,
  NavigationMenuLink,
  NavigationMenuList,
} from "./ui/navigation-menu";
import {
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "./ui/sheet";

export function NavBar() {
  return (
    <div className="flex items-center min-w-full w-full fixed justify-center p-3 z-[50]">
      <div className="flex justify-between lg:w-[900px] md:w-[800px] w-[95%] border dark:border-zinc-900 dark:bg-black bg-opacity-10 relative backdrop-filter backdrop-blur-lg bg-white border-white border-opacity-20 rounded-xl p-5 shadow-lg h-20">
        {/* Mobile Menu */}
        <Dialog>
          <SheetTrigger className="min-[825px]:hidden p-3 transition">
            <MenuIcon size={24} />
          </SheetTrigger>
          <SheetContent side="left">
            <SheetHeader>
              <Image
                src={Logo}
                alt="Amane"
                width={130}
                height={30}
                className="transition-all hover:opacity-75 dark:invert"
              />
              <SheetDescription className="text-lg text-gray-600 dark:text-gray-400">
                Learn more about us or get in touch with our team.
              </SheetDescription>
            </SheetHeader>
            <div className="flex flex-col space-y-4 mt-6 z-[99]">
              <DialogClose asChild>
                <Link href="/">
                  <Button variant="outline" className="w-full text-lg">
                    Home
                  </Button>
                </Link>
              </DialogClose>
              <DialogClose asChild>
                <Link href="/about">
                  <Button variant="outline" className="w-full text-lg">
                    About Us
                  </Button>
                </Link>
              </DialogClose>
              <DialogClose asChild>
                <Link href="/contact">
                  <Button variant="outline" className="w-full text-lg">
                    Contact Us
                  </Button>
                </Link>
              </DialogClose>
              <DialogClose asChild>
                <Link href="/login">
                  <Button variant="outline" className="w-full text-lg">
                    Login
                  </Button>
                </Link>
              </DialogClose>
              <DialogClose asChild>
                <Link href="/signup">
                  <Button variant="outline" className="w-full text-lg">
                    Sign Up
                  </Button>
                </Link>
              </DialogClose>
            </div>
          </SheetContent>
        </Dialog>

        {/* Desktop Navigation */}
        <NavigationMenu>
          <NavigationMenuList className="max-[825px]:hidden ">
            <Link href="/" className="pl-3">
              <Image
                src={Logo}
                alt="Amane"
                width={110}
                height={30}
                className="transition-all hover:opacity-75 dark:invert"
              />
            </Link>
          </NavigationMenuList>
        </NavigationMenu>
        <div className="flex items-center gap-4 max-[825px]:hidden">
          <Link href="/">
            <Button variant="ghost" className="text-lg">
              Home
            </Button>
          </Link>
          <Link href="/about">
            <Button variant="ghost" className="text-lg">
              About Us
            </Button>
          </Link>
          <Link href="/contact">
            <Button variant="ghost" className="text-lg">
              Contact Us
            </Button>
          </Link>
          <Link href="/login">
            <Button variant="outline" className="text-lg">
              Login
            </Button>
          </Link>
          <Link href="/signup">
            <Button variant="default" className="text-lg">
              Sign Up
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}

// Updated ListItem Component
const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-2 rounded-lg p-4 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className
          )}
          {...props}
        >
          <div className="text-lg font-semibold leading-tight">{title}</div>
          <p className="line-clamp-2 text-base leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  );
});
ListItem.displayName = "ListItem";
