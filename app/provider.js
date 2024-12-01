"use client"
import { db } from '@/configs/db';
import { USER_TABLE } from '@/configs/schema';
import { useUser } from '@clerk/nextjs'
import axios from 'axios';
import { eq } from 'drizzle-orm';
import React, { useEffect } from 'react'

function Provider({ children }) {

    const { user } = useUser();

    useEffect(() => {
        user && CheckIsNewUser();
    }, [user])

    /**
     * Used to check is User is New or Not
     */
    const CheckIsNewUser = async () => {
        // Check Is User Already Exist
        const result = await db.select().from(USER_TABLE)
            .where(eq(USER_TABLE.email, user?.primaryEmailAddress?.emailAddress))

        if (result?.length == 0) {
            //If Not, Then add to DB
            const userResp = await db.insert(USER_TABLE).values({
                name: user?.primaryEmailAddress?.emailAddress.substring(7),
                email: user?.primaryEmailAddress?.emailAddress
            }).returning({ id: USER_TABLE.id })
        }

        // const resp=await axios.post('/api/create-user',{user:user});
        // console.log(resp.data);

    }

    return (
        <div>
            {children}
        </div>
    )
}

export default Provider