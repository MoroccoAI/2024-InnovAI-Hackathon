"use client"
import { Button } from '@/components/ui/button'
import { UserButton } from '@clerk/nextjs'
import Image from 'next/image'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import React from 'react'

function DashboardHeader() {
    const path = usePathname();

    return (
        <div className={`p-5 shadow-md flex ${path === '/dashboard' ? 'justify-end' : 'justify-between'}`}>
            {path !== '/dashboard' && (
                <Link href={'/'}>
                    <div className='flex gap-2 items-center'>
                        <Image src={'/Fsdm_it_club_logo.png'} alt='logo' width={30} height={30} />
                        <h2 className="font-bold text-xl">Smart Study</h2>
                    </div>
                </Link>
            )}

            {/* Dashboard Button updated */}
            <div className='flex items-center gap-3'>
                <UserButton />
                <Link href={path === '/' ? '/dashboard' : '/dashboard'}>
                    <Button>{path === '/' ? 'Get Started' : 'Dashboard'}</Button>
                </Link>
            </div>
        </div>
    );
}

export default DashboardHeader;
