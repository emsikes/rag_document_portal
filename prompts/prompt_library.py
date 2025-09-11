from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


document_analysis_prompt = ChatPromptTemplate.from_template("""
You are a highly capable assistant trained to analyze and summarize documents.
Return ONLY valid JSON matching the exact schema below.

{format_instructions}

Analyze this document:
{document_text}                                                                                                                                                                                            
""")

document_compare_prompt = ChatPromptTemplate.from_template(""" 
You will be provided with contet form two PDFs.  Your tasks are as follows:

1. Compare the content in two PDFs
2. Identify the differnce in PDF and note down the page number
3. The output you provide must be a page wise comparisin of the content
4. If any page does not have any change, simply state 'No Change'                                                                                                                                                                                                                                                                                                          

Input documents:,

{combined_docs}

Your response should follow this format:

{format_instructions}                                                              
""")

# Prompt for contextual question rewriting
contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for answering based on context
context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an assistant designed to answer questions using the provided context. Rely only on the retrieved "
        "information to form your response. If the answer is not found in the context, respond with 'I don't know.' "
        "Keep your answer concise and no longer than three sentences.\n\n{context}"
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_compare": document_compare_prompt,
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt,
}
