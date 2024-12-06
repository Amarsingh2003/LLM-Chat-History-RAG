
# from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# import google.generativeai as genai
# import os
# import cohere
# from flask_cors import CORS
# from supabase import create_client, Client
# import numpy as np
# import ast 
# # Load environment variables
# load_dotenv()

# # Initialize Supabase
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
# cohere_client = cohere.Client(COHERE_API_KEY)

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Initialize Gemini models
# genai.configure(api_key=os.getenv("GEMINI_API_KEY_1"))
# model1 = genai.GenerativeModel("gemini-1.0-pro")

# genai.configure(api_key=os.getenv("GEMINI_API_KEY_2"))
# model2 = genai.GenerativeModel("gemini-1.0-pro")

# # Initialize chat
# chat = model1.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )

# def get_embedding(text):
#     """Generate embeddings using Cohere"""
#     response = cohere_client.embed(
#         texts=[text],
#         model='embed-english-v3.0',  # or 'embed-multilingual-v3.0' for multiple languages
#         input_type='search_query'
#     )
#     return response.embeddings[0]

# def cosine_similarity(a, b):
#     """Calculate cosine similarity between two vectors"""
    
#     # Check if b is a string representing a list, and convert it
#     if isinstance(b, str):
#         b = ast.literal_eval(b)  # Convert string like '[1.0, 2.0, 3.0]' to a list of floats
    
#     # Convert both a and b to numpy arrays of type float32
#     a = np.array(a, dtype=np.float32)
#     b = np.array(b, dtype=np.float32)
    
#     # Calculate cosine similarity
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def find_similar_queries(query_embedding, k=2):
#     """Find similar queries using Cohere embeddings stored in Supabase"""
#     # Get all stored embeddings from Supabase
#     stored_data = supabase.table("QueryEmbeddings").select("*").execute()
#     # print("stored data---------------")
#     # print(stored_data)
#     if not stored_data.data:
#         return []
    
#     # Calculate similarities
#     similarities = []
#     for item in stored_data.data:
#         stored_embedding = item['embedding']
#         similarity = cosine_similarity(query_embedding, stored_embedding)
#         similarities.append({
#             'id': item['id'],
#             'similarity': similarity
#         })
    
#     # Sort by similarity and get top k
#     similarities.sort(key=lambda x: x['similarity'], reverse=True)
#     return similarities[:k]

# def create_simple_prompt(response_data, query):
#     if response_data and len(response_data) > 0:
#         context = "\n".join([
#             f"Similar query: {item['query']}\nResponse: {item['response']}"
#             for item in response_data
#         ])
#     else:
#         context = "No prior context available."
#     prompt = (
        
#         f"Similar Past Interactions:\n{context}\n\n"
#         f"Instructions:\n"
#         "- Maintain context from the conversation history\n"
#         "- Use relevant information from similar queries\n"
#         "- Provide consistent responses based on known user information\n\n"
#         f"Current Query: {query}\n"
#         f"Assistant:"
#     )
#     # prompt = (
#     #     f"The AI references similar queries and responses from the provided history to answer the user's query if relevant.\n"
#     #     f"If the current query is not related to the history, the AI will generate a standalone response.\n\n"
#     #     f"History:\n{context}\n\n"
#     #     f"Current User Query: {query}\n"
#     #     f"AI:"
#     # )
#     return prompt


# def create_chat_with_history(similar_queries_data):
#     """Create a new chat with history from similar queries"""
#     history = []
    
#     if similar_queries_data:
#         for item in similar_queries_data:
#             # Add each similar query and its response as a history item
#             history.append({
#                 "role": "user",
#                 "parts": item['query']
#             })
#             history.append({
#                 "role": "model",
#                 "parts": item['response']
#             })
    
#     # Initialize chat with the constructed history
#     return model2.start_chat(history=history)

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     print(request.json)
#     user_query = request.json.get('query')
#     print(user_query)
    
#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400

#     response = chat.send_message(user_query)
#     response_text = response.text
#     print(response_text)
    
#     return jsonify({"response": response_text})

# @app.route('/get_improved_response', methods=['POST'])
# def get_improved_response():
#     user_query = request.json.get('query')
    
#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400

#     # Generate embedding for the query
#     query_embedding = get_embedding(user_query)
    
#     # Find similar queries
#     similar_queries = find_similar_queries(query_embedding)
    
#     # Get response data for similar queries
#     similar_queries_data = []
#     if similar_queries:
#         ids_to_fetch = [item['id'] for item in similar_queries]
#         response_data = supabase.table("QueryResponse").select("query", "response").in_("id", ids_to_fetch).execute()
#         similar_queries_data = response_data.data

#     # Create prompt with context
#     prompt = create_simple_prompt(similar_queries_data, user_query)
#     print("Generated prompt:", prompt)

#     # Generate response
#     response = model2.generate_content(prompt)
#     # print(response)
#     response_text = response.text

#     # Get next ID
#     next_id_result = supabase.table("QueryEmbeddings").select("id").order('id', desc=True).limit(1).execute()
#     next_id = 1 if not next_id_result.data else next_id_result.data[0]['id'] + 1

#     # Store embedding in Supabase
    

#     # print(len(query_embedding))
#     supabase.table('QueryEmbeddings').insert([
#         {"id": next_id, "embedding": query_embedding}
#     ]).execute()

#     # Store query and response in Supabase
#     supabase.table('QueryResponse').insert([
#         {"id": next_id, "query": user_query, "response": response_text}
#     ]).execute()
    
#     return jsonify({"response": response_text})


# if __name__ == '__main__':
#    app.run(debug=True)

# @app.route('/get_improved_response', methods=['POST'])
# def get_improved_response():
#     user_query = request.json.get('query')
    
#     if not user_query:
#         return jsonify({"error": "No query provided"}), 400

#     # Generate embedding for the query
#     query_embedding = get_embedding(user_query)
    
#     # Find similar queries
#     similar_queries = find_similar_queries(query_embedding)
    
#     # Get response data for similar queries
#     similar_queries_data = []
#     if similar_queries:
#         ids_to_fetch = [item['id'] for item in similar_queries]
#         response_data = supabase.table("QueryResponse").select("query", "response").in_("id", ids_to_fetch).execute()
#         similar_queries_data = response_data.data

#     print(similar_queries_data)
#     # Create a new chat with similar queries as history
#     chat_with_history = create_chat_with_history(similar_queries_data)
    
#     # Generate response using the chat with history
#     response = chat_with_history.send_message(user_query)
#     response_text = response.text

#     # Get next ID
#     next_id_result = supabase.table("QueryEmbeddings").select("id").order('id', desc=True).limit(1).execute()
#     next_id = 1 if not next_id_result.data else next_id_result.data[0]['id'] + 1

#     # Store embedding in Supabase
#     supabase.table('QueryEmbeddings').insert([
#         {"id": next_id, "embedding": query_embedding}
#     ]).execute()

#     # Store query and response in Supabase
#     supabase.table('QueryResponse').insert([
#         {"id": next_id, "query": user_query, "response": response_text}
#     ]).execute()
    
#     return jsonify({"response": response_text})

# # Route to check the number of stored embeddings
# @app.route('/get_stats', methods=['GET'])
# def get_stats():
#     result = supabase.table("QueryEmbeddings").select("count").execute()
#     count = len(result.data) if result.data else 0
#     return jsonify({
#         "total_embeddings": count
#     })

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os
import cohere
from flask_cors import CORS
from supabase import create_client, Client
import numpy as np
import ast 

# Load environment variables
load_dotenv()

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
cohere_client = cohere.Client(COHERE_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Gemini models
genai.configure(api_key=os.getenv("GEMINI_API_KEY_1"))
model1 = genai.GenerativeModel("gemini-1.0-pro")

genai.configure(api_key=os.getenv("GEMINI_API_KEY_2"))
model2 = genai.GenerativeModel("gemini-1.0-pro")

# Initialize chat for model1
chat = model1.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

def get_embedding(text):
    """Generate embeddings using Cohere"""
    response = cohere_client.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    if isinstance(b, str):
        b = ast.literal_eval(b)
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_similar_queries(query_embedding, k=2):
    """Find similar queries using Cohere embeddings stored in Supabase"""
    stored_data = supabase.table("QueryEmbeddings").select("*").execute()
    if not stored_data.data:
        return []
    
    similarities = []
    for item in stored_data.data:
        stored_embedding = item['embedding']
        similarity = cosine_similarity(query_embedding, stored_embedding)
        similarities.append({
            'id': item['id'],
            'similarity': similarity
        })
    
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    return similarities[:k]


@app.route('/get_response', methods=['POST'])
def get_response():
    print(request.json)
    user_query = request.json.get('query')
    print(user_query)
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    response = chat.send_message(user_query)
    response_text = response.text
    print(response_text)
    
    return jsonify({"response": response_text})

def extract_user_information(similar_queries_data):
    """
    Extracts explicit user information from conversation history
    """
    user_info = []
    
    # Keywords that indicate user statements about themselves
    identity_phrases = ["i am", "i'm", "i am a", "i'm a"]
    
    for item in similar_queries_data:
        query_lower = item['query'].lower()
        for phrase in identity_phrases:
            if phrase in query_lower:
                # Extract the statement after the identity phrase
                info = query_lower.split(phrase)[1].strip()
                if info:
                    user_info.append(info)
    
    return list(set(user_info))  # Remove duplicates

def create_chat_style_prompt(similar_queries_data, current_query):
    """
    Creates a chat-style prompt with explicit user information section
    """
    # Extract user information from history
    user_info = extract_user_information(similar_queries_data)
    
    # Create a stronger system prompt that emphasizes maintaining user information
    system_prompt = """You are a helpful AI assistant that must:
1. REMEMBER and UTILIZE the user information provided below
2. Maintain consistency with known user facts throughout the conversation
3. Reference this information when answering questions about the user
4. Provide clear, contextual responses based on known user information"""

    # Start building the formatted prompt
    formatted_prompt = f"System: {system_prompt}\n\n"
    
    # Add explicit user information section if any exists
    if user_info:
        formatted_prompt += "Known User Information:\n"
        for info in user_info:
            formatted_prompt += f"- User is {info}\n"
        formatted_prompt += "\n"
    
    # Add conversation history
    if similar_queries_data:
        formatted_prompt += "Previous Conversation:\n"
        for item in similar_queries_data:
            formatted_prompt += f"Human: {item['query']}\n"
            formatted_prompt += f"Assistant: {item['response']}\n\n"
    
    # Add current query
    formatted_prompt += f"Human: {current_query}\n"
    formatted_prompt += "Assistant:"
    
    return formatted_prompt

@app.route('/get_improved_response', methods=['POST'])
def get_improved_response():
    user_query = request.json.get('query')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Generate embedding for the query
    query_embedding = get_embedding(user_query)
    
    # Find similar queries
    similar_queries = find_similar_queries(query_embedding)
    
    # Get response data for similar queries
    similar_queries_data = []
    if similar_queries:
        ids_to_fetch = [item['id'] for item in similar_queries]
        response_data = supabase.table("QueryResponse").select("query", "response").in_("id", ids_to_fetch).execute()
        similar_queries_data = response_data.data

    # Create improved chat-style prompt with explicit user information
    prompt = create_chat_style_prompt(similar_queries_data, user_query)
    print("Generated prompt:", prompt)

    # Generate response using model2
    response = model2.generate_content(prompt)
    response_text = response.text

    # Store data in Supabase as before...
    next_id_result = supabase.table("QueryEmbeddings").select("id").order('id', desc=True).limit(1).execute()
    next_id = 1 if not next_id_result.data else next_id_result.data[0]['id'] + 1

    supabase.table('QueryEmbeddings').insert([
        {"id": next_id, "embedding": query_embedding}
    ]).execute()

    supabase.table('QueryResponse').insert([
        {"id": next_id, "query": user_query, "response": response_text}
    ]).execute()
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
   app.run(debug=True)