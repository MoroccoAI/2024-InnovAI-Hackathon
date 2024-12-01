import React, { useState } from 'react';
import { Book, Dna ,TestTube ,FlaskRound, BarChart, Brain, DollarSign, Globe, Heart, PlusCircle, Monitor } from 'lucide-react'; // Import des icônes nécessaires

function SelectOption({ selectedStudyType }) {
    const Options = [
        {
            name: 'Physics',
            icon: <FlaskRound size={40} /> // Icon "Flask" for Physics
        },
        {
            name: 'Mathematics',
            icon: <BarChart size={40} /> // Icon "BarChart" for Mathematics
        },
        {
            name: 'Chemistry',
            icon: <TestTube size={40} /> // Icon "Flask" for Chemistry
        },
        {
            name: 'Biology',
            icon: <Dna size={40} /> // Icon "DNA" for Biology
        },
        {
            name: 'Psychology',
            icon: <Brain size={40} /> // Icon "Brain" for Psychology
        },
        {
            name: 'Economics',
            icon: <DollarSign size={40} /> // Icon "DollarSign" for Economics
        },
        {
            name: 'History',
            icon: <Globe size={40} /> // Icon "Globe" for History
        },
        {
            name: 'Medicine',
            icon: <Heart size={40} /> // Icon "Heart" for Medicine
        },
        {
            name: 'Computer Science',
            icon: <Monitor size={40} /> // Icon "Monitor" for Computer Science
        },
        {
            name: 'Other',
            icon: <PlusCircle size={40} /> // Generic icon for "Other"
        }

    ];

    const [selectedOption, setSelectedOption] = useState();

    return (
        <div>
            <div className='grid grid-cols-2 mt-5 md:grid-cols-3 lg:grid-cols-5 gap-5'>
                {Options.map((option, index) => (
                    <div
                        key={index}
                        className={`p-4 flex flex-col items-center justify-center 
                        border rounded-xl hover:border-primary cursor-pointer
                        ${option?.name === selectedOption && 'border-primary'}`}
                        onClick={() => {
                            setSelectedOption(option.name);
                            selectedStudyType(option.name);
                        }}
                    >
                        <div className="mb-2">{option.icon}</div> {/* Icône affichée ici */}
                        <h2 className='text-sm mt-2'>{option.name}</h2>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default SelectOption;
