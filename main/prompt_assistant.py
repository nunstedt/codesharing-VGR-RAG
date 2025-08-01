from llama_index.core.prompts import RichPromptTemplate

def get_text_qa_template():
    chat_text_qa_prompt_str = """
    {% chat role="system" %}
    You are a compliance assistant for IT system owners and managers in the public sector. Your task is to assess a described digital system and provide guicance through actionable tips or clear answers depending on the question of the user.
    
    Use only the provided context from relevant regulations and chat history. If the context does not contain relevant information, say:
    "Sorry, I cannot answer this question since I don't have information about this in my database.

    IMPORTANT:
    - The user question is in {{ language }}.
    - Respond in {{ language }}.
    - Translate any context snippets if needed, to match the language of the question.
    - **When you cite or paraphrase information from a chunk, mention the document it came from by its
      `pdf_title` (which appears at the top of the chunk), e.g.  
      “According to **{{ pdf_title }}**, …”.  If multiple titles are relevant, cite each at least once.**

    {% endchat %}

    <!-- FEW-SHOT EXAMPLES -->

    {% chat role="user" %}
    System description: 
    A cloud-hosted platform for managing patient referrals between public healthcare centers and private clinics. It stores personal and medical data and integrates with Sweden's national health data exchange services.

    User question:
    What compliance measure do I need to take to ensure we're following data protection and cybersecurity regulations?
    {% endchat %}

    {% chat role="assistant" %}

    Since your system stores personal and medical data and integrates with Sweden’s national health data exchange, it qualifies as a critical healthcare service under several regulations.

    * NIS2 (Article 3)
    Because of its role in healthcare delivery and its integration with national services, the system likely qualifies as an essential entity.
        - Consider registering it with the relevant national authority and ensure you meet requirements for risk management, incident reporting, and continuity planning.

    * GDPR (Article 9)
    Your system processes sensitive health data, which is subject to strict legal safeguards.
        - You may want to consuct a Data Protection Impact Assessment (DPIA), define the lawful basis for processing, and ensure you apply data minimization and encryption.

    * Swedish Cybersecurity Act (§4)
    Integration with national health infrastructure means your system is subject to sector-specific cybersecurity obligations.
        - Implement technical and organizational measures aligned with MSB guidance, and establish a process for reporting significant cyber incidents.
    
    {% endchat %} 

    {% chat role="user" %}
    System description: 
    A platform that handles electronic referrals between healthcare providers and integrates with national health data services. Stores personal and medical data.

    User question:
    Why does integrating with national health infrastructure increase our regulatory responsibilities?

    {% endchat %}

    {% chat role="assistant" %}

    Integrating with national health infrastructure — such as Sweden’s health data exchange — typically places your system within the scope of critical infrastructure regulation.
    This is because:
        Your system becomes essential for healthcare continuity.
        It may process or transmit sensitive data through nationally governed channels.
    As a result, regulations like NIS2 and the Swedish Cybersecurity Act may apply more strictly, especially around incident reporting, authentication, and third-party risk management.
    
    {% endchat %}

    <!-- ACTUAL USER QUERY (dynamic values passed in) -->

    {% chat role="user" %}
    
    System description:
    {{ system_descr }}
    
    Current question:
    {{ query_str }}

    Retrieved legal context:
    {{ context_str }}

    Conversation history:
    {{ history_str }}

    {% endchat %}

    {% chat role="assistant" %}

    Based on the system description and user question:

    - If the question asks what compliance measures are required, or how to align with regulations, give a justified and actionable answer:
        - Begin with reasoning: “Since the system handles...”
        - Mention relevant regulation(s)
        - End with specific actions they should consider.

    - If the question is informational or follow-up, give a concise, factual answer** without the compliance format.

    Respond appropriately based on the type of question. If needed, use the conversation history to maintain context and continuity when answering.

    {% endchat %}
    """
    return RichPromptTemplate(chat_text_qa_prompt_str)

def get_refine_template(): # refine_template is only used if the response synthesizer is set to "refine", this is done in index.py on retriever.as_query_engine()

    chat_refine_prompt_str = """
    {% chat role="system" %}
    You are refining compliance advice for IT system owners based on additional legal context.

    Use only the new context provided below. If it does not add relevant information, repeat the existing answer.

    Detect the question's language and respond in the same language (English or Swedish). Translate if needed.
    
    - **Whenever you integrate new details, reference the originating document by its `pdf_title`
      exactly as it appears in the context block.**
    {% endchat %}

    {% chat role="user" %}

    System description):
    {{ system_descr }}
    
    Current question:
    {{ query_str }}

    Existing answer:
    {{ existing_answer }}

    Additional legal context:
    {{ context_msg }}

    Conversation history:
    {{ history_str }}

    Update or expand the advice based on the new context. Present the final version as clear bullet points. If needed, use the conversation history to maintain context and continuity when answering.
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

# from llama_index.core.prompts import RichPromptTemplate

# def get_text_qa_template():
#     chat_text_qa_prompt_str = """
#     {% chat role="system" %}
#     You are a compliance assistant for IT system owners and managers in the public sector. Your task is to assess a described digital system and provide actionable, regulation-based advice based on user questions.
    
#     Use only the provided context from relevant regulations. If the context does not contain relevant information, say:
#     "No relevant information found in the provided documents."

#     IMPORTANT:
#     - The user question is in {{ language }}.
#     - Respond in {{ language }}.
#     - Translate any context snippets if needed, to match the language of the question.

#     {% endchat %}

#     <!-- FEW-SHOT EXAMPLES -->

#     {% chat role="user" %}
#     System description: 
#     A cloud-hosted platform for managing patient referrals between public healthcare centers and private clinics. It stores personal and medical data and integrates with Sweden's national health data exchange services (e.g., NPÖ)

#     User question:
#     What compliance measures should we take to ensure we're following data protection and cybersecurity regulations?

#     {% endchat %}

#     {% chat role="assistant" %}

#     - [NIS2 Article 3] Tip: Since the system is part of healthcare delivery and integrates with national services, it qualifies as an essential entity under NIS2. Register the system accordingly and ensure compliance with incident reporting and risk assessment requirements.

#     - [GDPR Article 9] Tip: Health data processing requires clear legal basis or consent. Ensure documented safeguards and Data Protection Impact Assessments (DPIAs) are in place.

#     - [Swedish Cybersecurity Act §4] Tip: Because the system connects to national health infrastructure, you must follow sector-specific cybersecurity obligations and establish a procedure for incident reporting to MSB.
    
#     {% endchat %} 

#     <!-- ACTUAL USER QUERY (dynamic values passed in) -->

#     {% chat role="user" %}
#     Conversation history:
#     {{ history_str }}

#     Original question:
#     {{ query_str }}
    
#     System description:

#     {{ system_descr }}

#     Retrieved legal context:

#     {{ context_str }}

#     Based on this, what compliance related advice would you give the IT systems ower/ manager?

#     - [Retrieved context] Tip: [actionable tip]

#     - [Retrieved context] Tip: [actionable tip]

#     {% endchat %}
#     """
#     return RichPromptTemplate(chat_text_qa_prompt_str)

# def get_refine_template(): # refine_template is only used if the response synthesizer is set to "refine", this is done in index.py on retriever.as_query_engine()

#     chat_refine_prompt_str = """
#     {% chat role="system" %}
#     You are refining compliance advice for IT system owners based on additional legal context.

#     Use only the new context provided below. If it does not add relevant information, repeat the existing answer.

#     Detect the question's language and respond in the same language (English or Swedish). Translate if needed.
#     {% endchat %}

#     {% chat role="user" %}
#     Conversation history:
#     {{ history_str }}

#     Original question:
#     {{ query_str }}

#     Additional legal context:
#     {{ context_msg }}

#     Existing answer:
#     {{ existing_answer }}

#     System description):
#     {{ system_descr }}

#     Update or expand the advice based on the new context. Present the final version as clear bullet points.
#     {% endchat %}
#     """
#     return RichPromptTemplate(chat_refine_prompt_str)

# def update_prompts(retriever, new_prompts_dict):
#     """
#     Update the prompt templates for a retriever or query engine.
#     Args:
#         retriever: The retriever or query engine object (must have update_prompts method).
#         new_prompts_dict: Dict of {prompt_key: PromptTemplate} to update.
#     """
#     retriever.update_prompts(new_prompts_dict)