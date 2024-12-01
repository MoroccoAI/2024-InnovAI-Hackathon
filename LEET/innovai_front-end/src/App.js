import "./App.css";
import React, { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import Popup from "./Popup";



function App() {
    const [fileName, setFileName] = React.useState("");
    const [isPopupVisible, setIsPopupVisible] = useState(false);
    const [popupContent, setPopupContent] = useState("");
    const [jobDescription, setJobDescription] = useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileName(file.name);
        }
    };

    const handleJobDescriptionChange = (e) => {
        setJobDescription(e.target.value);
    };

    const handleSubmit = async () => {
        const fileInput = document.getElementById("fileUpload");
        const file = fileInput?.files[0];
    
        if (!file) {
            setPopupContent("Please upload a resume file.");
            setIsPopupVisible(true);
            return;
        }
    
        if (!jobDescription) {
            setPopupContent("Please enter the job description.");
            setIsPopupVisible(true);
            return;
        }
    
        const formData = new FormData();
        formData.append("file", file);
        formData.append("job_offer_text", jobDescription);
    
        try {
            const response = await fetch("http://localhost:8000/submit", {
                method: "POST",
                body: formData,
            });
    
            if (!response.ok) {
                const errorText = await response.text();
                try {
                    const errorData = JSON.parse(errorText);
                    setPopupContent(errorData.error || "An error occurred while submitting the data.");
                } catch {
                    setPopupContent(errorText || "An unknown error occurred.");
                }
                setIsPopupVisible(true);
                return;
            }
    
            const responseText = await response.text();
            try {
                const data = JSON.parse(responseText);
                setPopupContent(data.response || "Submission successful!");
            } catch {
                setPopupContent("Error parsing response from server.");
            }
            setIsPopupVisible(true);
        } catch (error) {
            setPopupContent("An error occurred. Please try again.");
            setIsPopupVisible(true);
        }
    };
    

    const closePopup = () => {
        setIsPopupVisible(false);
    };


    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-[#ced4da] w-[80%] h-[80vh] text-center flex justify-center items-center relative rounded-xl container-shadow">
                <div>
                    <img
                        src="logo.png"
                        alt="logo"
                        className="w-36 h-36 absolute left-0 top-0 rounded-xl"
                    />
                </div>
                <div className="flex flex-col w-1/2">
                    <p className="mb-4 text-lg text-neutral text-justify">
                        Upload your resume (PDF format) and paste a job offer
                        description to discover what skills, experiences, or
                        tools might be missing from your resume.
                    </p>
                    <hr className="border-secondary" />
                    <label
                        htmlFor="jobDescription"
                        className="text-gray-500 text-lg font-semibold mt-2 mb-1 text-left"
                    >
                        Job Description <span className="text-red-500">*</span>
                    </label>
                    <TextareaAutosize
                        minRows={2}
                        maxRows={8}
                        id="jobDescription"
                        className="textarea textarea-primary text-base caret-secondary"
                        placeholder="Enter job description here"
                        value={jobDescription}
                        onChange={handleJobDescriptionChange}
                    />
                    <div className="flex mt-4">
                        <button
                            className="btn btn-primary mr-3"
                            type="submit"
                            value="Submit"
                            onClick={handleSubmit}
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                strokeWidth={1.5}
                                stroke="currentColor"
                                className="size-6"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
                                />
                            </svg>
                            <span className="font-semibold text-base">
                                Submit
                            </span>
                        </button>
                        <label
                            htmlFor="fileUpload"
                            className="btn btn-secondary"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                                strokeWidth="1.5"
                                stroke="currentColor"
                                className="size-5"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13"
                                />
                            </svg>
                            <span className="font-semibold text-base">
                                Upload Resume
                            </span>
                        </label>
                        <input
                            id="fileUpload"
                            type="file"
                            className="hidden"
                            onChange={handleFileChange}
                        />
                        {fileName && (
                            <p className="text text-gray-500 ml-2 mt-3">
                                {fileName}
                            </p>
                        )}
                    </div>
                </div>
            </div>
            {isPopupVisible && (
                <Popup onClose={closePopup}>
                    <p>{popupContent}</p>
                </Popup>
            )}
        </div>
    );

    // return (
    //     <div className="flex justify-center items-center h-screen">
    //         <div className="bg-[#ced4da] w-[80%] h-[80vh] text-center flex justify-center items-center relative rounded-xl container-shadow">
    //             <div>
    //                 <img
    //                     src="logo.png"
    //                     alt="logo"
    //                     className="w-36 h-36 absolute left-0 top-0 rounded-xl"
    //                 />
    //             </div>
    //             <div className="flex flex-col w-1/2">
    //                 <p className="mb-4 text-lg text-neutral text-justify">
    //                     Upload your resume (PDF format) and paste a job offer
    //                     description to discover what skills, experiences, or
    //                     tools might be missing from your resume
    //                 </p>
    //                 <hr className="border-secondary" />
    //                 <label
    //                     htmlFor="jobDescription"
    //                     className="text-gray-500 text-lg font-semibold mt-2 mb-1 text-left"
    //                 >
    //                     Job Description <span className="text-red-500">*</span>
    //                 </label>
    //                 <TextareaAutosize
    //                     minRows={2}
    //                     maxRows={8}
    //                     id="jobDescription"
    //                     className="textarea textarea-primary text-base caret-secondary"
    //                     placeholder="Enter job description here"
    //                 />
    //                 <div className="flex mt-4">
    //                     <button
    //                         className="btn btn-primary mr-3"
    //                         type="submit"
    //                         value="Submit"
    //                         onClick={handleSubmit}
    //                     >
    //                         <svg
    //                             xmlns="http://www.w3.org/2000/svg"
    //                             fill="none"
    //                             viewBox="0 0 24 24"
    //                             strokeWidth={1.5}
    //                             stroke="currentColor"
    //                             className="size-6"
    //                         >
    //                             <path
    //                                 strokeLinecap="round"
    //                                 strokeLinejoin="round"
    //                                 d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
    //                             />
    //                         </svg>
    //                         <span className="font-semibold text-base">
    //                             Submit
    //                         </span>
    //                     </button>
    //                     <label
    //                         htmlFor="fileUpload"
    //                         className="btn btn-secondary"
    //                     >
    //                         <svg
    //                             xmlns="http://www.w3.org/2000/svg"
    //                             fill="none"
    //                             viewBox="0 0 24 24"
    //                             stroke-width="1.5"
    //                             stroke="currentColor"
    //                             class="size-5"
    //                         >
    //                             <path
    //                                 stroke-linecap="round"
    //                                 stroke-linejoin="round"
    //                                 d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13"
    //                             />
    //                         </svg>
    //                         <span className="font-semibold text-base">
    //                             Upload Resume
    //                         </span>
    //                     </label>
    //                     <input
    //                         id="fileUpload"
    //                         type="file"
    //                         className="hidden"
    //                         onChange={handleFileChange}
    //                     />
    //                     {fileName && (
    //                         <p className="text text-gray-500 ml-2 mt-3">
    //                             {fileName}
    //                         </p>
    //                     )}
    //                 </div>
    //             </div>
    //         </div>
    //         {isPopupVisible && (
    //             <Popup
    //                 onClose={closePopup}
    //             >
	// 				<p>
	// 				&emsp;&emsp;Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
	// 				</p>
	// 				<br/>
	// 				<p>
	// 				&emsp;&emsp;Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
	// 				</p>
	// 			</Popup>
    //         )}
    //     </div>
    // );
}

export default App;
