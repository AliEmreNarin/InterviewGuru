import openai

openai.api_key = "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"

job = ""
company = ""
additionalinfo = ""
count = 0
messages = []

def CustomChatGPT(user_input):
    global count
    global messages

    if count == 0:
        system_message = (
            f"You are an interviewer, and your job is to ask questions. "
            f"Only ask one question. Avoid making repetitions and refrain from using "
            f"'let's start our interview' or similar phrases during the process. "
            f"Try to be kind when asking questions. The interviewee is applying for a "
            f"{job} position at {company}. Here is more information about the company "
            f"and job position: {additionalinfo}. Begin the interview now."
        )
        messages = [{"role": "system", "content": system_message}]
    
    if count < 1:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        question = response["choices"][0]["message"]["content"]
        
        messages.append({"role": "user", "content": user_input})  
        messages.append({"role": "user", "content": question})
        
        count += 1
        return question
    else:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "system", "content": "Thank you for your time. This concludes the interview."})
        count = 0
        return "Thank you for your time. This concludes the interview."
    

