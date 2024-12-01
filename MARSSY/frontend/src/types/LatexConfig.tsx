// export const config = {
//     loader: {
//         load: ['input/tex', 'output/chtml'], // Load input/output processors
//         paths: { mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5' }, // CDN path
//         startupTypeset: true, // Automatically typeset content at startup
//     },
//     tex: {
//         inlineMath: [['$', '$'], ['\\(', '\\)']], // Inline math delimiters
//         displayMath: [['$$', '$$'], ['\\[', '\\]']], // Block math delimiters
//         processEscapes: true, // Allow \$ to escape dollar signs
//         processEnvironments: true, // Enable LaTeX environments like align or equation
//         tags: 'all', // Automatic equation numbering
//         tagSide: 'right', // Place equation numbers on the right side
//         tagIndent: '0.8em', // Indentation for equation numbers
//         macros: {
//             // Define custom macros for shorthand
//             RR: '\\mathbb{R}', // Real number symbol
//             bold: ['{\\bf #1}', 1], // Bold text
//             color: ['{\\color{#1} #2}', 2], // Colored text
//         },
//     },
//     chtml: {
//         scale: 1, // Scale for output (1 = 100%)
//         mtextInheritFont: true, // Use inherited font for <mtext>
//         merrorInheritFont: true, // Use inherited font for <merror>
//         matchFontHeight: true, // Match font height with surrounding text
//     },
//     svg: {
//         scale: 1, // Scale for output (1 = 100%)
//         fontCache: 'global', // Use a global font cache
//     },
// };

export const config = {
    loader: { load: ['input/tex', 'output/chtml'] },
    tex: { inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']] },
};