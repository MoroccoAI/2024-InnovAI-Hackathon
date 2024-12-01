import ReactMarkdown from 'react-markdown';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
import { MathJax, MathJaxContext } from 'better-react-mathjax'; // Import MathJax components
import 'katex/dist/katex.min.css'; // KaTeX styling for LaTeX rendering
import { useAppContext } from './AppContext';
import { useNavigate } from "react-router-dom";
import {config} from "../types/LatexConfig";

const CustomizedLesson = () => {
    const { customizedCourse } = useAppContext();
    const navigate = useNavigate();

    const handleRedirect = () => {
        navigate("/customized-qcm"); 
    };


    return (
        <MathJaxContext config={config}>
            <div
                className="min-h-screen bg-gradient-to-br from-blue-100 to-white flex justify-center items-center"
            >
                <div className="max-w-3xl mx-auto p-6 my-6 bg-white shadow-md rounded-lg">
                    <h1 className="text-3xl font-bold mb-6 text-center">Votre cours personnalisé</h1>
                    {customizedCourse.map((course: any, index: number) => (
                        <div
                            key={index}
                            className="mb-8 p-6 bg-white rounded-lg border border-gray-400"
                        >
                            <h2 className="text-2xl font-bold mb-4">{course.sub_title}</h2>
                            {/* Render Markdown with MathJax */}
                            <MathJax>
                                <ReactMarkdown
                                    children={course.content}
                                    remarkPlugins={[remarkMath]}
                                    rehypePlugins={[rehypeKatex]}
                                    components={{
                                        h1: ({ node, ...props }) => (
                                            <h1 className="text-xl font-semibold mt-4 mb-2" {...props} />
                                        ),
                                        h2: ({ node, ...props }) => (
                                            <h2 className="text-lg font-semibold mt-4 mb-2" {...props} />
                                        ),
                                        h3: ({ node, ...props }) => (
                                            <h3 className="text-base font-semibold mt-3 mb-1" {...props} />
                                        ),
                                        p: ({ node, ...props }) => (
                                            <p className="text-base mb-2" {...props} />
                                        ),
                                        ul: ({ node, ...props }) => (
                                            <ul className="list-disc list-inside mb-4" {...props} />
                                        ),
                                        ol: ({ node, ...props }) => (
                                            <ol className="list-decimal list-inside mb-4" {...props} />
                                        ),
                                    }}
                                />
                            </MathJax>
                        </div>
                    ))}
                    <button
                        onClick={handleRedirect}
                        className={`w-full py-3 rounded text-white font-bold transition-colors bg-blue-600 hover:bg-blue-700 active:bg-blue-800`}
                    >
                        Marquer comme lu
                    </button>
                </div>
            </div>
        </MathJaxContext>
    );
};

export default CustomizedLesson;
