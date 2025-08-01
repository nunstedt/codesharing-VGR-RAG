# Code for generating training data to fine-tune the embedding model, currently using the all-MiniLM-L6-v2 model
# Also foundation to generate data for evaluation using the evaluation_sv and evaluation_eng prompts.
# Pipeline to train model:
# 1. Generate data using this script.
# 2. Fine-tune the embedding model using the generated data.
# 3. Export the model to ONNX format.
# 4. Use the ONNX model in the Docker container by changing the docker compose file and change the model name in the index.py file.
# Kept seperate from the main script.


import os
import random
from typing import List, Dict
import json
import requests
import google.generativeai as genai
from llama_index.core import VectorStoreIndex
from index import get_vector_index
from ingest import parse_and_get_nodes
from sklearn.metrics.pairwise import cosine_similarity
from llama_index.embeddings.text_embeddings_inference import TextEmbeddingsInference
import numpy as np
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings
)
from ingest import parse_and_get_nodes

PROMPTS = {"default":"""Given the following regulation text, generate 4 specific questions which can be answered using the text. 

Text: {context}
The questions must:

1. Be answerable using ONLY the exact information contained in the excerpt - do not assume or require any external knowledge
2. Not ask about information that may be typical in legal documents but isn't explicitly stated in this excerpt
3. Focus on concrete facts rather than requiring interpretation
4. Have a clear, unambiguous answer found directly in the text

Output Format:
{{
  "questions": [
    {{
      "id": 1,
      "question": "[question text]",
      "location": "Exact sentence or phrase from the text that contains the answer"
    }}
  ]
}}

Example of a good question:
If excerpt contains: "Providers of high-risk AI systems shall ensure that their systems are designed and developed to allow for human oversight during the period in which the AI system is in use."
Question: "What must providers of high-risk AI systems ensure regarding human oversight?"
Location: "Providers of high-risk AI systems shall ensure that their systems are designed and developed to allow for human oversight during the period in which the AI system is in use."

Example of a bad question:
If excerpt contains: "By improving prediction, optimising operations and resource allocation, and personalising digital solutions available for individuals and organisations."
Question: "What is the definition of a high-risk AI system?"
(Bad because the excerpt doesn't provide any definition)""",


"evaluation_sv": """Given the following regulation text, generate 1 specific **natural question in swedish** using the given text.


Text: {context}


Generate questions that:
1. Ask about specific facts, definitions or specific requirements
2. Require understanding the practical application of the regulation
3. Test the model's ability to find relevant compliance requirements
4. Have clear answers found directly in the text, never assume or require external knowledge


Output Format:
{{
 "questions": [
   {{
     "id": 1,
     "question": "[specific compliance question in Swedish]",
     "location": "Exact sentence or phrase containing the answer"
   }}
 ]
}}


Examples of good specific questions:
- "Fram till vilket datum har kommissionen befogenhet att anta delegerade akter enligt artikel 5(1)?"
- "Vilka rättigheter har kritiska enheter, såsom skyddet av affärs- och företagshemligheter, enligt denna bestämmelse?"
- "När uppdaterades CER direktivet?""",

"evaluation_eng": """Given the following regulation text, generate 1 general **natural question in english** that a responsible IT systems owner might ask about the given text.


Text: {context}


Generate questions that:
1. Ask about specific compliance requirements or actions
2. Require understanding the practical application of the regulation
3. Test the model's ability to find relevant compliance requirements
4. Have clear answers found directly in the text, never assume or require external knowledge


Output Format:
{{
 "questions": [
   {{
     "id": 1,
     "question": "[general compliance question in English]",
     "location": "Exact sentence or phrase containing the answer"
   }}
 ]
}}


Examples of good specific questions:
- "What should I do if I need to ensure human oversight of my AI system?"
- "What si said about critical entitites?"
- "What steps must I take to meet the security standards described?"""}


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# set up embedding model to use Docker embeddor
Settings.embed_model = TextEmbeddingsInference(
    #model_name="sentence-transformers/all-MiniLM-L6-v2"
    model_name="export_models",
    base_url="http://localhost:5080"
)

# Generate questions based on given context and give the location of the answer in the text
def generate_question(context: str, prompt_template_key: str) -> str:
    """Generate a natural question from the given context."""
    model = genai.GenerativeModel('gemini-2.0-flash')

    try:
        generation_config = {
            "temperature": 0.3, 
            "top_p": 0.8,
            "top_k": 40
        }
        
        # Generate response
        prompt_template = PROMPTS.get(prompt_template_key)
        prompt_content = prompt_template.format(context=context)
        response = model.generate_content(
            prompt_content, generation_config=generation_config)
        
        
     
        response_text = response.text.strip()
        
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            try:
                result = json.loads(json_str)
                return json.dumps(result, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                pass
        #Fallback
        lines = [line.strip() for line in response_text.split('\n') if '?' in line]
        questions = {
            "questions": [
                {
                    "id": i+1,
                    "question": line.strip(),
                    "location": context  # Using full context as fallback
                }
                for i, line in enumerate(lines)
            ]
        }
        return json.dumps(questions, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error generating question: {e}")
        return None

def filter_similar_questions(questions_data: dict, similarity_threshold: float = 0.85) -> dict:

    """
    Filter out similar questions using a similarity matrix.
    
    Args:
        questions_data: Dictionary containing questions and their locations
        similarity_threshold: Threshold for considering questions as similar
    
    Returns:
        dict: Filtered questions data
    """

    #Extract all generated questions
    questions = [q["question"] for q in questions_data["questions"]]

    #Extract all generated locations (for evaluaiton data set)
    #questions = [q["location"] for q in questions_data["questions"]]

    if not questions:
        return questions_data
    
    try:
        embedder = Settings.embed_model
        embeddings = embedder.get_text_embedding_batch(questions)
        embeddings = np.array(embeddings)

    #Compute similarity matrix to find redundant questions
        similarity_matrix = cosine_similarity(embeddings)

        unique_indices= []
        used_indices = set()

        for i in range(len(questions)):
            if i not in used_indices:
                unique_indices.append(i)
                similar_indices = np.where(similarity_matrix[i] > similarity_threshold)[0]
                used_indices.update(similar_indices)
            

        filtered_questions = {
            "questions": [
                questions_data["questions"][i] 
                for i in unique_indices
            ]
        }
        
        return filtered_questions
        
    except Exception as e:
        print(f"Error in similarity computation: {e}")
        return questions_data
    

def create_training_tuples(questions_data: dict, full_context: str) -> List[Dict]:
    """
    Create training tuples from generated questions.
    Each tuple contains: (question, positive_context, negative_context)
    """
    training_tuples = []
    
    #Has to be changed when using the actual data
    sentences = [s.strip() + '.' for s in full_context.split('.') if s.strip()]

    for q in questions_data.get("questions", []):
        question = q["question"]
        positive_context = q["location"]
        
        # Sample negative context (different from positive)
        negative_candidates = [
            sent for sent in sentences 
            if sent != positive_context
        ]
        
        if negative_candidates:
            negative_context = random.choice(negative_candidates)
            
            tuple_data = {
                "anchor": question,
                "positive": positive_context,
                "negative": negative_context
            }

            # Print the tuple
            print("\nGenerated tuple:")
            print(f"ANCHOR (Question): {question}")
            print(f"POSITIVE (Answer): {positive_context}")
            print(f"NEGATIVE (Non-answer): {negative_context}")
            print("-" * 80)

            training_tuples.append(tuple_data)
    

    return training_tuples

def save_tuples(tuples: List[Dict], output_file: str = "training_tuples.json"):
    """Save the training tuples to a JSON file."""
    data_dir = os.path.join(os.path.dirname(__file__), 'training_data')
    os.makedirs(data_dir, exist_ok=True)

    # Ensure the output file path is correct
    output_file = os.path.join(data_dir, output_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tuples, f, ensure_ascii=False, indent=2)


def process_raw_documents(raw_documents):
    """Process raw documents and return valid Document objects."""
    valid_docs = []
    for doc, success, path in raw_documents:
        if success and isinstance(doc, Document):
            valid_docs.append(doc)
    return valid_docs

def main():


    # Test context in Swedish to test the generation function, will be replaced with actual data
    # test_context = """
    # Den digitala assistenten implementerades i tre kommuner under 2023. 
    # Kostnaden för implementering var 500 000 kronor per kommun. 
    # Resultaten visade en effektivisering där handläggningstiden minskade med 35%. 
    # Medarbetarna rapporterade högre arbetstillfredsställelse och bättre service till medborgarna.
    # """
    print("Loading and chunking relevant documents...")
    data_dir = os.path.join(os.path.dirname(__file__), 'data/')
    print(f"Looking for documents in: {data_dir}")
    
    try:
        nodes = parse_and_get_nodes(data_dir)
        print(f"Successfully created {len(nodes)} chunks from documents")
            
        all_tuples = []
        for i, node in enumerate(nodes, 1):
            context = node.get_content()
            if len(context.split()) < 10:
                print(f"Skipping chunk {i} (too short)")
                continue

            print(f"\nProcessing chunk nr: {i+1}/{len(nodes)}")
            print("-" * 80)
            print("\nGenerating questions...")
            questions_result = generate_question(context, "default")

            #Generate questions for actual data
            if questions_result:
                try:
                    questions_data = json.loads(questions_result)
                    print(f"Generated {len(questions_data['questions'])} questions")

                    #Filter similar questions
                    filtered_questions = filter_similar_questions(questions_data)
                    print(f"Filtered to {len(filtered_questions['questions'])} questions")

                    #Create the tuples by adding non-answers
                    chunk_tuples = create_training_tuples(filtered_questions, context)
                    all_tuples.extend(chunk_tuples)
                    print(f"Created {len(chunk_tuples)} training tuples for data set")
                except json.JSONDecodeError as e:
                    print(f"Error parsing questions for chunk {i}: {e}")
                    continue

        if all_tuples:
            save_tuples(all_tuples)
            print("Saved generated tuples to training data folder")
        else:
            print("No training tuples were generated:(")

    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
    #Previous code for test content
    # if questions_result:
    #     questions_data = json.loads(questions_result)
    #     print(json.dumps(questions_data, ensure_ascii=False, indent=2))
        
    #     # Filter similar questions
    #     print("\nFiltering similar questions...")
    #     filtered_questions = filter_similar_questions(questions_data)
    #     print("\nQuestions after filtering:")
    #     print(json.dumps(filtered_questions, ensure_ascii=False, indent=2))

    #     # Create training tuples
    #     print("\nCreating training tuples...")
    #     training_tuples = create_training_tuples(filtered_questions, test_context)
        
    #     # Save tuples
    #     save_tuples(training_tuples)
        
    #     print("\nGenerated tuples:")
    #     print("-" * 80)
    #     print(json.dumps(training_tuples, ensure_ascii=False, indent=2))
    #     print(f"\nSaved {len(training_tuples)} training tuples to training_tuples.json")
    # else:
    #     print("Failed to generate questions")

if __name__ == "__main__":
    main()
