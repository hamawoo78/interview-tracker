import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_interview_details(email_text: str) -> dict:
    """
    Send interview email text to OpenAI and return extracted data as dict.
    Uses chat.completions API (correct method).
    Returns dict with extracted fields or error info.
    """
    
    # Get current year for context
    current_year = datetime.now().year

    prompt = f"""Extract interview details from the email below.
        Current year is {current_year}.
        Return ONLY valid JSON with these fields (use null for unknown values):


        Fields:
        - interview_link
        - interviewer_name
        - interview_type (one of: phone, technical, onsite, hr, other, online)
        - start_datetime_iso (ISO 8601 format, e.g., "2025-01-15T14:00:00")
        - meeting_link

        Rules:
        - Do NOT guess missing values
        - Use null for unknown fields
        - Return ONLY JSON, no extra text
        - For notes, generate a short summary of the email content.
            Include interview tips ONLY if they are explicitly mentioned in the email.
            Do not add new advice or assumptions.
        - If the email specifies a month and day but does not mention a year,
            assume the current year ({current_year}) unless the date would be in the past.
            If it would be in the past, use the next calendar year.


        Email:
        \"\"\"
        {email_text}
        \"\"\"
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts interview details from emails. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        # Extract JSON from response
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSONs
        extracted_data = json.loads(response_text)
        print(extracted_data)
        return extracted_data
        
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response as JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}


def extract_company_details(email_text: str) -> dict:
    """
    Extract company job posting details from email using OpenAI.
    Returns dict with extracted company fields or error info.
    """


    prompt = f"""Extract company job posting details from the email below.

        Return ONLY valid JSON with these fields (use null for unknown values):

        Fields:
        - company_name
        - position_title
        - location
        - website_url
        - salary_min (numeric only, no currency symbol)
        - salary_max (numeric only, no currency symbol)
        - job_description_url

        Rules:
        - Do NOT guess missing values
        - Use null for unknown fields
        - Return ONLY JSON, no extra text
        - For salary, extract only numeric value (e.g., 100000 not "$100,000")
        - If salary range given, use min and max separately

        Email:
        \"\"\"
        {email_text}
        \"\"\"
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts company job posting details from emails. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        # Extract JSON from response
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON
        extracted_data = json.loads(response_text)
        print(extracted_data)
        return extracted_data
        
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response as JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}



def rate_prep_answers(prep_answers: dict, job_description: str) -> dict:
    """
    Rate interview prep answers using OpenAI based on job description.
    
    Args:
        prep_answers: dict with keys: self_intro, why_apply, questions_to_ask, additional_notes
        job_description: job description text for context
    
    Returns:
        dict with ratings for each field: {field_name: {"score": 8, "feedback": "..."}}
    """
    
    if not job_description:
        return {"error": "Job Description is missing"}

    prompt = f"""You are an interview coach. Rate the following interview prep answers based on the job description.

Job Description:
\"\"\"
{job_description}
\"\"\"

If the job description above is a URL (starts with http), please fetch and read that URL to understand the job requirements.
If it's a file path, analyze based on the description provided.
If it says "No job description provided", rate based on general interview best practices.

First, provide a brief summary of the job description (2-3 sentences max).
Then rate each prep answer.

Prep Answers to Rate:
1. Self-Introduction: {prep_answers.get('self_intro', 'Not provided')}
2. Why I Applied: {prep_answers.get('why_apply', 'Not provided')}

4. Additional Notes: {prep_answers.get('additional_notes', 'Not provided')}

Rate each answer on a scale of 1-10 based on:
- Relevance to the job description/requirements
- Clarity and professionalism
- Specificity and detail
- Likelihood to impress interviewer

Return ONLY valid JSON with this exact format:
{{
    "job_summary": "Brief 2-3 sentence summary of the job description and key requirements",
    "self_intro": {{"score": X, "feedback": "message"}},
    "why_apply": {{"score": X, "feedback": "Smessage"}},

    "additional_notes": {{"score": X, "feedback": "message"}}
}}

Rules:
- Score must be 1-10 integer
- Feedback must be 1-2 sentences max
- Be constructive and encouraging
- Return ONLY JSON, no extra text
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are an expert interview coach. Rate prep answers fairly and provide constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        
        # Extract JSON from response
        response_text = response.choices[0].message.content.strip()
        
        # Parse JSON
        ratings = json.loads(response_text)
        print(ratings)
        return ratings
        
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse AI response as JSON: {str(e)}"}
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}
