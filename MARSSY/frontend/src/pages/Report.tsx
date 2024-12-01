import ReactMarkdown from 'react-markdown';
import rehypeKatex from 'rehype-katex';
import remarkMath from 'remark-math';
import 'katex/dist/katex.min.css'; // KaTeX styling for LaTeX rendering
import { useAppContext } from './AppContext';
import { useNavigate } from "react-router-dom"; 

const Report = () => {
    const { report, formData } = useAppContext();
    const navigate = useNavigate();

    const handleRedirect = () => {
        navigate("/customized-course"); 
    };

    if (!report || !report.analyse_des_lacunes_par_sous_cours) {
        return <p className="text-center text-gray-500">Chargement du rapport...</p>;
    }

    return (
        <div
      className="min-h-screen bg-gradient-to-br from-blue-100 to-white flex justify-center items-center"
    >
        <div className="max-w-3xl mx-auto p-6  my-6 bg-white shadow-md rounded-lg">
            <h1 className="text-3xl font-bold mb-6 text-center">Votre rapport personnalisé</h1>
            
            {/* Dynamic content */}
            <div>
                <h2 className="text-xl font-semibold mb-4">Analyse des lacunes</h2>
                <ul className="space-y-4">
                    {report.analyse_des_lacunes_par_sous_cours.map((sousCours, index) => (
                        <li key={index} className="p-4 border rounded-lg bg-gray-50">
                            <h3 className="text-lg font-bold text-blue-600">{sousCours.sous_cours_name}</h3>
                            <p className="text-gray-700 mt-2">{sousCours.analyse}</p>
                            <p className="text-gray-600 mt-1">
                                <span className="font-semibold">Questions incorrectes : </span>
                                {sousCours.nombre_questions_incorrectes_par} / {formData.num_questions}
                                
                            </p>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">Conclusion</h2>
                <ReactMarkdown
                    children={report.conclusion}
                    rehypePlugins={[rehypeKatex]}
                    remarkPlugins={[remarkMath]}
                    className="text-gray-700"
                />
            </div>

            <button
                onClick={handleRedirect}
                className="w-full py-3 mt-6 rounded text-white font-bold transition-colors bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
            >
                Marquer comme lu
            </button>
        </div></div>
    );
};

export default Report;
