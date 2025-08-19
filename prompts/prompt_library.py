from langchain_core.prompts import ChatPromptTemplate 


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

Input documents:

{combined_docs}

Your response should follow this format:

{format_instructions}                                                              
""")

PROMPT_REGISTRY = {
    "document_analysis": document_analysis_prompt,
    "document_compare": document_compare_prompt
}



