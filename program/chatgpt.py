import json
import openai


def chatgpt_response(full_prompt):
    chatgpt_answer = ' '  
    status = '-- '
    explanation = ' '
    
    message=[{"role": "user", "content": full_prompt}]
    response = openai.chat.completions.create(
        model="gpt-4o",
        max_tokens=5000,
        temperature=0.5,
        messages = message
    )
    

    chatgpt_answer = response.choices[0].message.content

    secure_index = chatgpt_answer.lower().find('secure')
    insecure_index = chatgpt_answer.lower().find('insecure')
    inconclusive_index = chatgpt_answer.lower().find('inconclusive')

    if secure_index != -1 and ((insecure_index == -1 or secure_index < insecure_index) and (inconclusive_index == -1 or secure_index < inconclusive_index)):
        status = 'Secure'
    elif insecure_index != -1 and ((secure_index == -1 or insecure_index < secure_index) and (inconclusive_index == -1 or insecure_index < inconclusive_index)):
        status = 'Insecure'
    elif inconclusive_index != -1 and ((secure_index == -1 or inconclusive_index < secure_index) and (insecure_index == -1 or inconclusive_index < insecure_index)):
        status = 'Inconclusive'
    else:
        status = 'Not answered'
    
    return chatgpt_answer, status
