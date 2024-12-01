"use client"
import { Button } from '@/components/ui/button'
import { db } from '@/configs/db'
import { USER_TABLE } from '@/configs/schema'
import { useUser } from '@clerk/nextjs'
import axios from 'axios'
import { eq } from 'drizzle-orm'
import React, { useEffect, useState } from 'react'

function Upgrade() {

  const {user}=useUser();
  const [userDetail,setUserDetail]=useState();

  useEffect(()=>{
    user&&GetUserDetail();
  },[user])

  const GetUserDetail=async()=>{

    const result=await db.select().from(USER_TABLE)
    .where(eq(USER_TABLE.email,user?.primaryEmailAddress?.emailAddress));

    setUserDetail(result[0]);

  }

  const OnCheckoutClick=async()=>{
    const result=await axios.post('/api/payment/checkout',{
      priceId:process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_MONTHLY
    });

    console.log(result.data);
    window.open(result.data?.url)
  }

  const onPaymentMange=async()=>{
    const result=await axios.post('/api/payment/manage-payment',{
      customerId:userDetail?.customerId
    })

    console.log(result.data);
    window.open(result.data?.url)

  }
  return (
    <div>
    <h2 className='font-medium text-3xl'>Plans</h2>
    <p>Update your plan to generate unlimted courses for your exam</p>
  
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8">
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:items-center md:gap-8">


  <div className="rounded-2xl border border-gray-200 p-6 shadow-sm sm:px-8 lg:p-12">
    <div className="text-center">
      <h2 className="text-lg font-medium text-gray-900">
        Free
        <span className="sr-only">Plan</span>
      </h2>

      <p className="mt-2 sm:mt-4">
        <strong className="text-3xl font-bold text-gray-900 sm:text-4xl"> 0$ </strong>

        <span className="text-sm font-medium text-gray-700">/month</span>
      </p>
    </div>

    <ul className="mt-6 space-y-2">
      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> 5 Course Generate </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Limited Support </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Email support </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Help center access </span>
      </li>
    </ul>

    <Button variant="ghost" className="w-full mt-5 text-primary">
        Current Plan
        </Button>
  </div>
  <div className="rounded-2xl border border-gray-200 p-6 shadow-sm sm:px-8 lg:p-12">
    <div className="text-center">
      <h2 className="text-lg font-medium text-gray-900">
        Montly
        <span className="sr-only">Plan</span>
      </h2>

      <p className="mt-2 sm:mt-4">
        <strong className="text-3xl font-bold text-gray-900 sm:text-4xl"> 9.99$ </strong>

        <span className="text-sm font-medium text-gray-700">/Montly</span>
      </p>
    </div>

    <ul className="mt-6 space-y-2">
      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Unlimted Course Generate </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Unlimted Flashcard, Quiz </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Email support </span>
      </li>

      <li className="flex items-center gap-1">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
          className="size-5 text-indigo-700"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>

        <span className="text-gray-700"> Help center access </span>
      </li>
    </ul>

   {userDetail?.isMember==false? <Button
      onClick={OnCheckoutClick}
      className="w-full mt-5"
    >
      Get Started
    </Button>:

<Button
onClick={onPaymentMange}
className="w-full mt-5"
>
Manage Payment
</Button>}
 
  </div>
</div>
</div></div>
  )
}

export default Upgrade