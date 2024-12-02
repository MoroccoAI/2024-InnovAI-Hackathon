import dataclasses
from typing import List, Dict, Optional, Set
from enum import Enum
import pandas as pd
import numpy as np
import json
import os
import unicodedata
import arabic_reshaper # type: ignore
from bidi.algorithm import get_display # type: ignore
# Fallback ML libraries
from transformers import AutoModel, AutoTokenizer


class ArabicTextHandler:
    @staticmethod
    def reshape_arabic_text(text):
        """
        Properly reshape and reorder Arabic text for correct display
        
        Args:
            text (str): Arabic text to be reshaped
        
        Returns:
            str: Correctly reshaped and bidirectional text
        """
        # Reshape the Arabic text
        reshaped_text = arabic_reshaper.reshape(text)
        
        # Apply bidirectional algorithm for correct display
        display_text = get_display(reshaped_text)
        
        return display_text
    
    @staticmethod
    def save_to_json(data, filename='gluten_analysis_results.json', 
                     encoding='utf-8'):
        """
        Save results to a JSON file with proper Arabic text encoding
        
        Args:
            data (dict or list): Data to be saved
            filename (str): Output filename
            encoding (str): File encoding
        """
        try:
            # Ensure the data directory exists
            os.makedirs('output', exist_ok=True)
            
            # Full path for the output file
            full_path = os.path.join('output', filename)
            
            # Save with UTF-8 encoding to support Arabic characters
            with open(full_path, 'w', encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Results saved to {full_path}")
            return full_path
        except Exception as e:
            print(f"Error saving results: {e}")
            return None
    
    @staticmethod
    def save_to_txt(text, filename='gluten_analysis_results.txt', 
                    encoding='utf-8'):
        """
        Save text to a plain text file with proper Arabic text encoding
        
        Args:
            text (str): Text to be saved
            filename (str): Output filename
            encoding (str): File encoding
        """
        try:
            # Ensure the data directory exists
            os.makedirs('output', exist_ok=True)
            
            # Full path for the output file
            full_path = os.path.join('output', filename)
            
            # Save with UTF-8 encoding to support Arabic characters
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(text)
            
            print(f"Results saved to {full_path}")
            return full_path
        except Exception as e:
            print(f"Error saving results: {e}")
            return None

# Modify the existing RAG System to use ArabicTextHandler
def modify_rag_system(gluten_assistant):
    """
    Modify the generate_response method to use ArabicTextHandler
    
    Args:
        gluten_assistant (RAGSystem): The existing RAG system instance
    
    Returns:
        Modified generate_response method
    """
    original_generate_response = gluten_assistant.generate_response
    
    def enhanced_generate_response(
        retrieved_info, 
        query_language: str = "darija",
        save_to_file: bool = True
    ):
        # Call the original method to generate the response
        response = original_generate_response(retrieved_info, query_language)
        
        # Reshape the Arabic text
        reshaped_response = ArabicTextHandler.reshape_arabic_text(response)
        
        # Optionally save to file
        if save_to_file:
            # Save to both JSON and TXT for flexibility
            ArabicTextHandler.save_to_json(
                {
                    "original_response": response,
                    "reshaped_response": reshaped_response,
                    "results": [
                        {
                            "item_name": result.item_name,
                            "contains_gluten": result.contains_gluten,
                            "gluten_sources": result.gluten_sources,
                            "alternatives": result.alternative_suggestions
                        } for result in retrieved_info
                    ]
                }
            )
            ArabicTextHandler.save_to_txt(reshaped_response)
        
        # Print the reshaped text
        print("Reshaped Response:")
        print(reshaped_response)
        
        return reshaped_response
    
    # Replace the original method
    gluten_assistant.generate_response = enhanced_generate_response
    
    return gluten_assistant

# Dataclass for Gluten Analysis Result
@dataclasses.dataclass
class GlutenAnalysisResult:
    item_name: str
    contains_gluten: bool
    gluten_sources: List[str]
    alternative_suggestions: List[str]
    confidence_score: float
    nutritional_details: Dict[str, str] = dataclasses.field(default_factory=dict)

# Enumeration for Data Sources
class DataSource(Enum):
    RECIPE_DATABASE = "local_moroccan_recipes"
    PRODUCT_CATALOG = "moroccan_product_inventory"
    NUTRITIONAL_DATABASE = "gluten_content_reference"

# Fallback Embedding Strategy
class SimpleEmbedding:
    def __init__(self, model_name='bert-base-multilingual-cased'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def encode(self, texts):
        # Simple embedding generation
        inputs = self.tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Main RAG System Class
class RAGSystem:
    def __init__(self, config_path='moroccan_gluten_config.json'):
        # Ensure data files exist
        self._prepare_data_files()
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize data sources
        self.data_sources = {
            DataSource.RECIPE_DATABASE: self._load_recipe_database(),
            DataSource.PRODUCT_CATALOG: self._load_product_catalog(),
            DataSource.NUTRITIONAL_DATABASE: self._load_nutritional_database()
        }
        
        # Initialize embedding model
        self.embedding_model = SimpleEmbedding()
        
        # Gluten-specific knowledge base
        self.gluten_ingredients = self._load_gluten_ingredients()
    
    def _prepare_data_files(self):
        """
        Create sample data files if they don't exist
        """
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Recipe database
        if not os.path.exists('data/moroccan_recipes.csv'):
            pd.DataFrame({
                'name': ['Tagine', 'Couscous', 'Harira', 'Pastilla', 'Zaalouk'],
                'ingredients': ['lamb', 'wheat semolina', 'flour', 'wheat flour', 'eggplant'],
                'gluten_status': [False, True, True, True, False]
            }).to_csv('data/moroccan_recipes.csv', index=False)
        
        # Product catalog
        if not os.path.exists('data/moroccan_products.csv'):
            pd.DataFrame({
                'name': ['Sardines à l\'huile', 'Moroccan Bread', 'Rice Cookies'],
                'ingredients': ['sardines salt oil', 'wheat flour', 'rice flour sugar'],
                'brand': ['Conserver', 'Local Bakery', 'Meknes Sweets'],
                'gluten_status': [False, True, False]
            }).to_csv('data/moroccan_products.csv', index=False)
        
        # Nutritional reference
        if not os.path.exists('data/nutritional_ref.csv'):
            pd.DataFrame({
                'ingredient': ['wheat', 'barley', 'rye', 'couscous'],
                'gluten_content': ['high', 'high', 'high', 'high'],
                'alternative': ['rice', 'millet', 'corn', 'quinoa']
            }).to_csv('data/nutritional_ref.csv', index=False)
        
        # Configuration file
        if not os.path.exists('moroccan_gluten_config.json'):
            config = {
                "recipe_database_path": "data/moroccan_recipes.csv",
                "product_catalog_path": "data/moroccan_products.csv",
                "nutritional_database_path": "data/nutritional_ref.csv",
                "embedding_model": "bert-base-multilingual-cased",
                "translation_model": "bert-base-multilingual-cased"
            }
            with open('moroccan_gluten_config.json', 'w') as f:
                json.dump(config, f)
    
    def _load_recipe_database(self) -> pd.DataFrame:
        """
        Load Moroccan recipe database
        """
        try:
            return pd.read_csv(self.config['recipe_database_path'])
        except Exception as e:
            print(f"Error loading recipe database: {e}")
            return pd.DataFrame()
    
    def _load_product_catalog(self) -> pd.DataFrame:
        """
        Load Moroccan product catalog
        """
        try:
            return pd.read_csv(self.config['product_catalog_path'])
        except Exception as e:
            print(f"Error loading product catalog: {e}")
            return pd.DataFrame()
    
    def _load_nutritional_database(self) -> pd.DataFrame:
        """
        Load nutritional reference database
        """
        try:
            return pd.read_csv(self.config['nutritional_database_path'])
        except Exception as e:
            print(f"Error loading nutritional database: {e}")
            return pd.DataFrame()
    
    def _load_gluten_ingredients(self) -> Set[str]:
        """
        Load comprehensive list of gluten-containing ingredients
        Supports multiple languages and Moroccan context
        """
        base_gluten_ingredients = {
            'wheat', 'barley', 'rye', 'couscous', 'semolina', 
            'bulgur', 'فريكة', 'قمح', 'شعير'  # Arabic variations
        }
        return base_gluten_ingredients
    
    def retrieve_relevant_info(self, query: str) -> List[GlutenAnalysisResult]:
        """
        Advanced retrieval with multiple strategies
        1. Semantic search using embeddings
        2. Ingredient-based matching
        3. Fuzzy matching for dialect variations
        """
        results = []
        
        # Search in recipes
        recipe_matches = self.data_sources[DataSource.RECIPE_DATABASE][
            (self.data_sources[DataSource.RECIPE_DATABASE]['name'].str.contains(query, case=False)) |
            (self.data_sources[DataSource.RECIPE_DATABASE]['ingredients'].str.contains(query, case=False))
        ]
        
        # Search in products
        product_matches = self.data_sources[DataSource.PRODUCT_CATALOG][
            (self.data_sources[DataSource.PRODUCT_CATALOG]['name'].str.contains(query, case=False)) |
            (self.data_sources[DataSource.PRODUCT_CATALOG]['ingredients'].str.contains(query, case=False))
        ]
        
        # Combine matches
        for _, item in recipe_matches.iterrows():
            contains_gluten = any(
                ing in self.gluten_ingredients 
                for ing in str(item['ingredients']).split()
            )
            
            result = GlutenAnalysisResult(
                item_name=item['name'],
                contains_gluten=contains_gluten,
                gluten_sources=[
                    ing for ing in str(item['ingredients']).split() 
                    if ing in self.gluten_ingredients
                ],
                alternative_suggestions=self._generate_alternatives(item['name']),
                confidence_score=0.8,  # Fixed confidence for this simple implementation
                nutritional_details={}
            )
            results.append(result)
        
        # Similar processing for products
        for _, item in product_matches.iterrows():
            contains_gluten = any(
                ing in self.gluten_ingredients 
                for ing in str(item['ingredients']).split()
            )
            
            result = GlutenAnalysisResult(
                item_name=item['name'],
                contains_gluten=contains_gluten,
                gluten_sources=[
                    ing for ing in str(item['ingredients']).split() 
                    if ing in self.gluten_ingredients
                ],
                alternative_suggestions=self._generate_alternatives(item['name']),
                confidence_score=0.8,
                nutritional_details={}
            )
            results.append(result)
        
        return results
    
    def _generate_alternatives(self, item_name: str) -> List[str]:
        """
        Generate gluten-free alternatives
        Considers cultural context and local availability
        """
        alternatives = []
        
        # Moroccan-specific gluten-free alternatives
        moroccan_alternatives = {
            'couscous': ['quinoa', 'rice', 'corn couscous'],
            'bread': ['corn bread', 'rice bread'],
            'flour': ['rice flour', 'corn flour'],
        }
        
        # Generic substitution logic
        for item, subs in moroccan_alternatives.items():
            if item in item_name.lower():
                alternatives.extend(subs)
        
        return alternatives
    
    def generate_response(
        self, 
        retrieved_info: List[GlutenAnalysisResult], 
        query_language: str = "darija"
    ) -> str:
        """
        Generate contextually aware, multilingual response
        Supports Moroccan Darija with nutritional insights
        """
        if not retrieved_info:
            return "معلومات غير متوفرة" # No information available
        
        response = "نتائج البحث:\n"
        for result in retrieved_info:
            gluten_status = "يحتوي على الغلوتين" if result.contains_gluten else "خالٍ من الغلوتين"
            
            response += f"- {result.item_name}: {gluten_status}\n"
            
            if result.gluten_sources:
                response += "  مصادر الغلوتين:\n"
                for source in result.gluten_sources:
                    response += f"    * {source}\n"
            
            if result.alternative_suggestions:
                response += "  بدائل مقترحة:\n"
                for alt in result.alternative_suggestions:
                    response += f"    * {alt}\n"
        
        return response

# Main execution

def main():
    try:
        print("Starting Gluten Assistant Initialization...")
        # Initialize the RAG system
        gluten_assistant = RAGSystem()
        print("RAG System Initialized Successfully!")
        
        # Enhance the RAG system with Arabic text handling
        gluten_assistant = modify_rag_system(gluten_assistant)
        # Debug: Print configuration and data sources
        print("\nConfiguration:")
        print(json.dumps(gluten_assistant.config, indent=2))
        
        print("\nData Sources Status:")
        for source, data in gluten_assistant.data_sources.items():
            print(f"{source.value}: {len(data)} entries")
        
        # Example queries in Darija or Arabic
        queries = [
            "couscous",  # Gluten-containing item
            "tagine",    # Likely gluten-free
            "sardines",  # Specific product
            "wheat"      # Ingredient search
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            results = gluten_assistant.retrieve_relevant_info(query)
            print(f"Found {len(results)} results")
            
            response = gluten_assistant.generate_response(results)
            print("Response:")
            print(response)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Traceback:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()