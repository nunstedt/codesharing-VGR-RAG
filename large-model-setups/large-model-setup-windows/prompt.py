from llama_index.core.prompts import RichPromptTemplate

def get_text_qa_template():
    chat_text_qa_prompt_str = """
    {% chat role="system" %}
    You are a compliance assistant for IT system owners and managers in the public sector. Use only the provided context to answer the user's question. If the context does not contain relevant information, do not attempt to guess or describe the documents simply reply: "No relevant information found in the provided documents."
    
    IMPORTANT: Before answering, detect the language of the question. Respond in the same language: use English if the question is in English, and Swedish if the question is in Swedish. Translate the answer to the language os the question if necessary.
    {% endchat %}

    {% chat role="user" %}
    The following is some retrieved context:

    {{ context_str }}

    Based on this context, answer the following question in a clear, concise, and actionable way for system owners and managers:

    {{ query_str }}
    {% endchat %}
    """
    return RichPromptTemplate(chat_text_qa_prompt_str)

def get_refine_template(): # refine_template is only used if the response synthesizer is set to "refine", this is done in index.py on retriever.as_query_engine()

    chat_refine_prompt_str = """
    {% chat role="system" %}
    You are a compliance assistant for IT system owners and managers. Use only the provided context. If the context does not contain relevant information, do not attempt to guess or describe the documents simply reply: "No additional relevant information found in the provided documents."
    IMPORTANT: Before answering, detect the language of the question. Respond in the same language: use English if the question is in English, and Swedish if the question is in Swedish. Answers should be equally detailed regardless of the language. Translate the answer to the language os the question if necessary.
    {% endchat %}
 
    {% chat role="user" %}
    The following is some new retrieved context:

    {{ context_msg }}

    Here is an existing answer to the user's question:

    {{ existing_answer }}

    Using both the new context and the existing answer, update or improve the answer for system owners and managers, ensuring clarity and actionable guidance. If the new context does not add relevant information, repeat the existing answer.

    Question:
    {{ query_str }}
    {% endchat %}
    """
    return RichPromptTemplate(chat_refine_prompt_str)

def update_prompts(retriever, new_prompts_dict):
    """
    Update the prompt templates for a retriever or query engine.
    Args:
        retriever: The retriever or query engine object (must have update_prompts method).
        new_prompts_dict: Dict of {prompt_key: PromptTemplate} to update.
    """
    retriever.update_prompts(new_prompts_dict)