import json

def grade_answer(question, correct_answer, student_answer,llm):
    """Grade the students answers to the quiz.
    """
    prompt = f"""
        You are a German language teacher grading a student's answer.

        Question:
        {question}

        Correct Answer:
        {correct_answer}

        Student Answer:
        {student_answer}

        Evaluate the student's answer.

        Return ONLY JSON:

        {{
        "score": "correct | almost | wrong",
        "feedback": "short explanation",
        "correction": "corrected sentence if needed"
        }}

        Rules:
        correct → same meaning
        almost → small grammar mistake
        wrong → incorrect meaning
        """

    response = llm.invoke(prompt)

    text = response.content

    try:
        return json.loads(text)
    except:

        return {
            "score": "wrong",
            "feedback": "Could not parse grading result",
            "correction": correct_answer
        }