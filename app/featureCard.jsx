import Image from 'next/image';
import React from 'react';

const cardData = [
    {
        id: 1,
        image: '/laptop.png',
        title: 'Boost Your Productivity',
        description: 'Discover tips and tools to maximize your efficiency and stay ahead.',
    },
    {
        id: 2,
        image: '/quiz.png',
        title: 'Data-Driven Insights',
        description: 'Analyze trends and make informed decisions with our AI-powered analytics.',
    },
    {
        id: 3,
        image: '/practice.png',
        title: 'Learn Anywhere, Anytime',
        description: 'Access high-quality educational content and resources on the go.',
    },
];

function FeatureCard({ image, title, description }) {
    return (
        <div className="border rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
            <div>
                <div className="flex">
                    <Image src={image} alt={title} width={50} height={50} />
                </div>
                <h2 className="mt-4 font-semibold text-lg text-left">{title}</h2>
                <p className="text-sm text-left text-gray-500 mt-2 line-clamp-3">{description}</p>
            </div>
        </div>
    );
}

function FeatureCardList() {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {cardData.map((card) => (
                <FeatureCard
                    key={card.id}
                    image={card.image}
                    title={card.title}
                    description={card.description}
                />
            ))}
        </div>
    );
}

export default FeatureCardList;
