import google.generativeai as genai
import time

def gemini_response(full_prompt):
    

    gemini_answer = ''
    status = '-- '
    
    time.sleep(10) # to get rid off  Resource has been exhausted (e.g. check quota).
    
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(full_prompt)
        gemini_answer = response.text
        
        # Analyze the content for status keywords
        secure_index = gemini_answer.lower().find('secure')
        insecure_index = gemini_answer.lower().find('insecure')
        inconclusive_index = gemini_answer.lower().find('inconclusive')

        if secure_index != -1 and ((insecure_index == -1 or secure_index < insecure_index) and (inconclusive_index == -1 or secure_index < inconclusive_index)):
            status = 'Secure'
        elif insecure_index != -1 and ((secure_index == -1 or insecure_index < secure_index) and (inconclusive_index == -1 or insecure_index < inconclusive_index)):
            status = 'Insecure'
        elif inconclusive_index != -1 and ((secure_index == -1 or inconclusive_index < secure_index) and (insecure_index == -1 or inconclusive_index < insecure_index)):
            status = 'Inconclusive'
        else:
            status = 'Not answered'
    
    except Exception as e:
        # Handle any exceptions that occur during the request
        print(f"Error during Gemini response generation: {e}")
        gemini_answer = "Error generating response"
        status = "Error"
    
    return gemini_answer, status


