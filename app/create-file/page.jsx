"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

const FileUpload = () => {
    const [uploading, setUploading] = useState(false);
    const [feedbackMessage, setFeedbackMessage] = useState("");
    const [extractedText, setExtractedText] = useState("");

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFeedbackMessage("File selected: " + file.name);
        }
    };

    const handleUpload = async () => {
        const fileInput = document.getElementById("file");
        const selectedFile = fileInput.files[0];

        if (!selectedFile) {
            setFeedbackMessage("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        setUploading(true);

        try {
            const response = await fetch("https://api.pdf.co/v1/pdf/convert/to/text", {
                method: "POST",
                headers: {
                    "x-api-key":process.env.CO_PDF_API_KEY ,
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to extract text from the file.");
            }

            const result = await response.json();

            if (result.body) {
                setExtractedText(result.body); // API returns extracted text in the 'body' field
                setFeedbackMessage("File processed successfully!");
            } else {
                setFeedbackMessage("File processed but no text extracted.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            setFeedbackMessage("Failed to process the file.");
        } finally {
            setUploading(false); // Hide the loader
        }
    };

    return (
        <>
            <div className="flex flex-col items-center p-5 md:px-24 lg:px-36 mt-20">
                <h2 className="font-bold text-4xl text-primary">
                    Create Your Personalized Study Plans
                </h2>
                <p className="text-gray-500 text-lg">
                    Provide your file to generate study material tailored to your needs.
                </p>
            </div>
            <div className="flex flex-col items-center justify-center p-5 md:px-24 lg:px-36 mt-10">
                <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
                    <div className="space-y-4">
                        <h3 className="text-gray-700 text-sm font-medium">
                            Upload Study Plan File
                        </h3>
                        <Input
                            type="file"
                            id="file"
                            onChange={handleFileChange}
                            className="w-full"
                            accept=".pdf" // Restrict to PDF only as per requirements
                        />
                        {feedbackMessage && (
                            <p className={`text-sm ${uploading ? "text-gray-500" : "text-red-500"}`}>
                                {feedbackMessage}
                            </p>
                        )}
                        <Button
                            onClick={handleUpload}
                            disabled={uploading}
                            className="w-full mt-5"
                            variant={uploading ? "secondary" : "default"}
                        >
                            {uploading ? (
                                <div className="flex items-center justify-center space-x-2">
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span>Uploading...</span>
                                </div>
                            ) : (
                                "Upload and Extract Text"
                            )}
                        </Button>
                        {extractedText && (
                            <div className="mt-4 p-4 bg-gray-100 rounded">
                                <h4 className="font-bold text-gray-700">Extracted Text:</h4>
                                <p className="text-gray-600 text-sm whitespace-pre-wrap">
                                    {extractedText}
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};

export default FileUpload;
