import firebase from 'firebase/compat/app';
import 'firebase/compat/firestore';
import 'firebase/compat/auth';

import { useEffect, useState } from 'react';
import { useUser } from '@clerk/clerk-react';

export const    useDetails = () => {
    const clerkUser = useUser();
    const [details, setDetails] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const retriveDetails = async function ()  {
            try {
                const firebaseToken = await clerkUser.getToken("firebase");
                await firebase.auth().signInWithCustomToken(firebaseToken);

                const tempDetails = [];
                const db = firebase.firestore();
            
                const user_form = await db.collection("user_form").doc(clerkUser.id).get();
                user_form.forEach((detail) => {
                    tempDetails.push(detail.data());
                });


                setDetails(tempDetails);
            } catch (err){
                setError(err); 
            }
        };
        retriveDetails();
    }, []);
    return { details, error };
};