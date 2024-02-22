from prompt_helper import doctor_template,math_template,computerscience_template,history_template


prompt_infos = [
    {
        "name": "doctor", 
        "description": "Good for answering questions about medical help", 
        "prompt_template": doctor_template
    },
    {
        "name": "math", 
        "description": "Good for answering math questions", 
        "prompt_template": math_template
    },
    {
        "name": "History", 
        "description": "Good for answering history questions", 
        "prompt_template": history_template
    },
    {
        "name": "computer science", 
        "description": "Good for answering computer science questions", 
        "prompt_template": computerscience_template
    }
]