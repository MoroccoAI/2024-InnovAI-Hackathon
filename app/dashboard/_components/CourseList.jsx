"use client"
import { useUser } from '@clerk/nextjs'
import axios from 'axios'
import React, { useContext, useEffect, useState } from 'react'
import CourseCardItem from './CourseCardItem';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';
import { CourseCountContext } from '@/app/_context/CourseCountContext';

function CourseList() {
    const { user } = useUser();
    const [courseList, setCourseList] = useState([]);
    const [loading, setLoading] = useState(false);
    const { totalCourse, setTotalCourse } = useContext(CourseCountContext);

    useEffect(() => {
        user && GetCourseList();
    }, [user]);

    const GetCourseList = async () => {
        setLoading(true);
        try {
            const result = await axios.post('/api/courses', {
                createdBy: user?.primaryEmailAddress?.emailAddress,
            });
            console.log(result);
            setCourseList(result.data.result);
            setTotalCourse(result.data.result?.length || 0);
        } catch (error) {
            console.error("Error fetching course list:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-10">
            <h2 className="font-bold text-2xl flex justify-between items-center">
                Your Study Material
                <Button
                    variant="outline"
                    onClick={GetCourseList}
                    className="border-primary text-primary"
                >
                    <RefreshCw /> Refresh
                </Button>
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-3 mt-2 gap-5">
                {loading ? (
                    // Skeleton loaders during loading state
                    [1, 2, 3, 4, 5, 6].map((item, index) => (
                        <div key={index} className="h-56 w-full bg-slate-200 rounded-lg animate-pulse"></div>
                    ))
                ) : courseList.length > 0 ? (
                    // Display the list of courses
                    courseList.map((course, index) => (
                        <CourseCardItem course={course} key={index} />
                    ))
                ) : (
                    // Message when there are no courses
                    <div className="col-span-full text-center text-gray-500 mt-5">
                        <p className="text-lg">You have not created any course yet.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default CourseList;
