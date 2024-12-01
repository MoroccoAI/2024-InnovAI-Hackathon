import re
from html import escape
from pathlib import Path
import json

def convert_course_content(course_prop, output_directory="generated_html"):
    """
    Convert course content from a variable to HTML file.
    
    Args:
        course_prop (dict): Dictionary containing course content
        output_directory (str): Directory where HTML files will be saved
    
    Returns:
        str: Path to the generated HTML file
    """
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    def process_math(content):
        # Convert display math mode - use double backslashes for proper escaping
        content = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', content, flags=re.DOTALL)
        # Convert inline math mode
        content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
        return content

    def convert_latex_commands(content):
        # Process math environments first
        content = re.sub(r'\\begin{align\*}(.*?)\\end{align\*}', 
                        lambda m: '$$' + m.group(1).replace('\\\\', '\\') + '$$', 
                        content, flags=re.DOTALL)
        
        replacements = {
            r'\\section{(.*?)}': r'<h1>\1</h1>',
            r'\\subsection{(.*?)}': r'<h2>\1</h2>',
            r'\\subsubsection{(.*?)}': r'<h3>\1</h3>',
            r'\\paragraph{(.*?)}': r'<h4>\1</h4>',
            r'\\textbf{(.*?)}': r'<strong>\1</strong>',
            r'\\begin{itemize}': r'<ul>',
            r'\\end{itemize}': r'</ul>',
            r'\\item': r'<li>',
            r'\\begin{cases}': r'\\begin{cases}',  # Keep LaTeX cases environment
            r'\\end{cases}': r'\\end{cases}',
            r'\\text{([^}]*)}': r'\\text{\1}',  # Keep LaTeX \text command
            r'\\quad': r'\\quad',  # Keep LaTeX spacing
            r'\\rightarrow': r'\\rightarrow',  # Keep LaTeX arrows
            r'\\Rightarrow': r'\\Rightarrow',
            r'\\mathbb{R}': r'\\mathbb{R}',  # Keep LaTeX mathbb
            r'\\neg': r'\\neg',
            r'\\overline': r'\\overline',
            r'\\exists': r'\\exists',
            r'\\forall': r'\\forall',
            r'\\in': r'\\in',
            r'\\leq': r'\\leq',
            r'\\neq': r'\\neq',
            r'\\geq': r'\\geq'
        }
        
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
        
        return content

    def process_content(content):
        # Save math blocks
        math_blocks = []
        
        def save_math(match):
            math_blocks.append(match.group(0))
            return f"MATHBLOCK{len(math_blocks)-1}"
        
        # Save both display and inline math
        content = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)', save_math, content, flags=re.DOTALL)
        
        # Escape HTML except for allowed tags
        content = escape(content)
        content = content.replace('&lt;h1&gt;', '<h1>').replace('&lt;/h1&gt;', '</h1>')
        content = content.replace('&lt;h2&gt;', '<h2>').replace('&lt;/h2&gt;', '</h2>')
        content = content.replace('&lt;h3&gt;', '<h3>').replace('&lt;/h3&gt;', '</h3>')
        content = content.replace('&lt;h4&gt;', '<h4>').replace('&lt;/h4&gt;', '</h4>')
        content = content.replace('&lt;strong&gt;', '<strong>').replace('&lt;/strong&gt;', '</strong>')
        content = content.replace('&lt;ul&gt;', '<ul>').replace('&lt;/ul&gt;', '</ul>')
        content = content.replace('&lt;li&gt;', '<li>').replace('&lt;/li&gt;', '</li>')
        
        # Restore math blocks
        for i, block in enumerate(math_blocks):
            content = content.replace(f"MATHBLOCK{i}", block)
        
        content = convert_latex_commands(content)
        content = process_math(content)
        
        return content

    # Build the HTML document
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{escape(course_prop['Titre'])}</title>
        <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                packages: ['base', 'ams', 'noerrors', 'noundefined']
            }},
            svg: {{
                fontCache: 'global'
            }}
        }};
        </script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .mjx-chtml {{
                margin: 1em 0;
                overflow-x: auto;
                padding: 10px;
            }}
            ul {{
                margin-left: 20px;
                padding-left: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
                margin-top: 1.5em;
            }}
            h1 {{ border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid #2c3e50; padding-bottom: 5px; }}
            strong {{ color: #2c3e50; }}
        </style>
    </head>
    <body>
    """

    # Process the main content
    if 'Leçon proposée et exemples' in course_prop:
        content = process_content(course_prop['Leçon proposée et exemples'])
        html += content

    html += """
    </body>
    </html>
    """

    # Generate output filename based on title
    safe_title = "".join(x for x in course_prop['Titre'] if x.isalnum() or x in (' ', '-', '_')).rstrip()
    output_file_path = Path(output_directory) / f"{safe_title}.html"
    
    # Write HTML file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    
    return str(output_file_path)
# Your course content
course_prop = {
    "Titre": "III. Opérations sur les propositions : Négation et implications",
    "Leçon proposée et exemples": "\\section{III. Opérations sur les propositions : Négation et implications}\n\n\\subsection{Comprendre la négation des propositions}\n\nLa négation d'une proposition $P$ est notée $\\neg P$ ou $\\overline{P}$. Elle est vraie lorsque $P$ est fausse et fausse lorsque $P$ est vraie. La négation est essentielle en logique pour construire des raisonnements rigoureux, comme le raisonnement par contre-exemple.\n\n\\subsubsection{Exemple 1 : Négation d'un quantificateur universel}\nSoit $P(x)$ une fonction propositionnelle d'une variable $x \\in \\mathbb{R}$. La négation de la proposition \\((\\forall x \\in \\mathbb{R}) P(x)\\) est \\((\\exists x \\in \\mathbb{R}) \\neg P(x)\\).\n\n\\paragraph{Illustration}\nProposition : \\((\\forall x \\in \\mathbb{R}); x^2 + 1 \\geq 2\\).\n\n\\textbf{Négation} : \\((\\exists x \\in \\mathbb{R}); x^2 + 1 < 2\\).\n\nPour vérifier, cherchons un \\(x \\in \\mathbb{R}\\) qui satisfait $x^2 + 1 < 2$ :\n\\[x^2 < 1 \\Rightarrow x \\in ]-1, 1[.\\]\nCela confirme que la proposition originale est fausse car la négation est vraie.\n\n\\subsubsection{Exemple 2 : Négation d'un quantificateur existentiel}\nLa négation de \\((\\exists x \\in \\mathbb{R}) P(x)\\) est \\((\\forall x \\in \\mathbb{R}) \\neg P(x)\\).\n\n\\paragraph{Illustration}\nProposition : \\((\\exists x \\in \\mathbb{R}^+); x^2 - 4x + 3 = 0\\).\n\n\\textbf{Négation} : \\((\\forall x \\in \\mathbb{R}^+); x^2 - 4x + 3 \\neq 0\\).\n\nVérifions la proposition originale :\nRésolvons \\(x^2 - 4x + 3 = 0\\) :\n\\[x^2 - 4x + 3 = (x - 1)(x - 3) = 0 \\Rightarrow x = 1 \\text{ ou } x = 3.\\]\nPuisque des solutions existent dans $\\mathbb{R}^+$, la proposition originale est vraie.\n\n\\subsection{Applications des implications logiques}\n\nUne implication \\((P \\Rightarrow Q)\\) est une proposition vraie sauf si $P$ est vraie et $Q$ est fausse. On peut également écrire \\((P \\Rightarrow Q)\\) comme \\((\\neg P \\text{ ou } Q)\\).\n\n\\subsubsection{Exemple : Résolution d'équations}\nSoit $x, y \\in \\mathbb{R}$, les propositions suivantes :\n\\[P: 2x + 4y = 1, \\quad Q: x^2 + y^2 \\leq 20.\\]\n\nDémontrons que \\(P \\Rightarrow Q\\).\n\\begin{itemize}\n    \\item \\textbf{Hypothèse :} $P$ est vraie, donc $2x + 4y = 1$.\n    \\item \\textbf{Démonstration :} Isolons $y$ en fonction de $x$ :\n    \\[y = \\frac{1 - 2x}{4}.\\]\n    Substituons dans $x^2 + y^2$ :\n    \\[\n    x^2 + y^2 = x^2 + \\left(\\frac{1 - 2x}{4}\\right)^2 = x^2 + \\frac{(1 - 2x)^2}{16}.\n    \\]\n    Développons et simplifions :\n    \\[x^2 + \\frac{1 - 4x + 4x^2}{16} = \\frac{16x^2 + 1 - 4x + 4x^2}{16} = \\frac{20x^2 - 4x + 1}{16}.\\]\n    Pour que \\(x^2 + y^2 \\leq 20\\), vérifions les bornes de $x$ qui satisfont cette inégalité.\n\\end{itemize}\n\n\\subsection{Exercice pratique}\n\n\\textbf{Exercice 1 :} Montrer que la proposition \\((P \\text{ ou } \\neg P)\\) est toujours vraie.\n\n\\textbf{Exercice 2 :} Résolvez les systèmes suivants en utilisant les propriétés logiques :\n\\begin{align*}\n(S_1): &\\begin{cases}\n    x^2 - y^2 = 0, \\\\\n    2x^2 + y^2 = 3.\n\\end{cases} \\\\\n(S_2): &\\begin{cases}\n    xy - x + y = 1, \\\\\n    2x^2 - xy - y = 0.\n\\end{cases}\n\\end{align*}\n\nCe cours vise à renforcer la compréhension des négations et des implications tout en offrant des opportunités de pratique."
}

# Generate the HTML file
if __name__ == "__main__":
    try:
        output_path = convert_course_content(course_prop)
        print(f"Successfully generated HTML file at: {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")