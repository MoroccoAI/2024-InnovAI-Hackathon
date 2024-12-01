"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import TopicInput from "./_components/TopicInput";
import { v4 as uuidv4 } from "uuid";
import axios from "axios";
import { useUser } from "@clerk/nextjs";
import { Loader } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import SelectOption from "@/app/create/_components/SelectOption";
import DashboardHeader from "@/app/dashboard/_components/DashboardHeader";
import SideBar from "@/app/dashboard/_components/SideBar";

function Create() {
    const [formData, setFormData] = useState({});
    const { user } = useUser();
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleUserInput = (fieldName, fieldValue) => {
        setFormData((prev) => ({
            ...prev,
            [fieldName]: fieldValue,
        }));
        console.log(formData);
    };

    /**
     * Used to Save User Input and Generate Course Layout using AI
     */
    const GenerateCourseOutline = async () => {
        const courseId = uuidv4();
        setLoading(true);
        try {
            const result = await axios.post("/api/generate-course-outline", {
                courseId: courseId,
                ...formData,
                createdBy: user?.primaryEmailAddress?.emailAddress,
            });
            toast("Your course content is generating. Click on the Refresh Button.");
            console.log(result.data.result.resp);
            router.replace("/dashboard");
        } catch (error) {
            console.error("Error generating course outline:", error);
            toast.error("An error occurred while generating the course outline.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <DashboardHeader/>
            <div className='md:w-64 hidden md:block fixed'>
                <SideBar/>
            </div>
            <div className="flex flex-col items-center p-5 md:px-24 lg:px-36 mt-10">
                <h2 className="font-bold text-4xl text-primary">
                    Create Your Personalized Study Material
                </h2>
                <p className="text-gray-500 text-lg">
                    Provide all the necessary details to generate study material tailored
                    to your needs.
                </p>
                <SelectOption selectedStudyType={(value) => handleUserInput('courseType', value)}/>

                <div className="mt-2">
                    <TopicInput
                        setTopic={(value) => handleUserInput("topic", value)}
                        setDifficultyLevel={(value) => handleUserInput("difficultyLevel", value)}
                    />
                </div>

                <div className="flex justify-center w-full mt-12">
                    <Button onClick={GenerateCourseOutline} disabled={loading}>
                        {loading ? <Loader className="animate-spin"/> : "Generate"}
                    </Button>
                </div>
            </div>
        </>
    );
}

export default Create;
