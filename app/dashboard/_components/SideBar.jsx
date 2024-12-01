"use client"
import { CourseCountContext } from '@/app/_context/CourseCountContext'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { LayoutDashboard, Shield, UserCircle, Book , Zap , FilePlus , MessageCircleQuestion} from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import React, { useContext } from 'react'

function SideBar() {
    const MenuList=[
        {
            name:'Dashboard',
            icon:LayoutDashboard,
            path:'/dashboard'
        },

        {
            name:'Study Plan',
            icon:Book,
            path:'/create'
        },


        {
            name:'Study Plan from file',
            icon:Zap,
            path:'/create-file'
        },


        {
            name:'Chat with file',
            icon:MessageCircleQuestion,
            path:'/dashboard/profile'
        },
        {
            name:'About Us',
            icon:FilePlus,
            path:'/dashboard/about_us'
        },
        // {
        //     name:'Upgrade',
        //     icon:Shield,
        //     path:'/dashboard/upgrade'
        // },
        {
            name:'Profile',
            icon:UserCircle,
            path:'/dashboard/profile'
        },

    ]

    //const {totalCourse,setTotalCourse}=useContext(CourseCountContext);
    const path=usePathname();
  return (
    <div className='h-screen shadow-md p-5'>
        <Link href="/" passHref>
            <div className="flex gap-2 items-center cursor-pointer">
                <Image src="/Fsdm_it_club_logo.png" alt="logo" width={40} height={40} />
                <h2 className="font-bold text-2xl">Smart Study</h2>
            </div>
        </Link>

            <div className='mt-10'>
                {/*<Link href={'/create'} className="w-full">*/}
                {/*<Button className="w-full" disabled={totalCourse>=5}>+ Create New</Button>*/}
                {/*</Link>*/}

                <div className='mt-5'>
                    {MenuList.map((menu,index)=>(
                        <Link href={menu.path} key={index} >
                        <div 
                        className={`flex gap-5 items-center p-3
                        hover:bg-slate-200 rounded-lg cursor-pointer mt-3
                        ${path==menu.path&&'bg-slate-200'}`}>
                            <menu.icon/>
                            <h2>{menu.name}</h2>
                        </div>
                        </Link>
                    ))}
                </div>
            </div>

        {/* <div className='border p-3 bg-slate-100 rounded-lg
            absolute bottom-10 w-[85%]'>
                <h2 className='text-lg mb-2'>Available Credits : {(5-totalCourse)}</h2>
                <Progress value={(totalCourse/5)*100} />
                <h2 className='text-sm'>{totalCourse} Out of 5 Credits Used</h2>

                <Link href={'/dashboard/upgrade'} className='text-primary text-xs mt-3'>Upgrade to create more</Link>
            </div>*/}
    </div>
  )
}

export default SideBar