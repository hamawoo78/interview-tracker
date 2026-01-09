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
    Send company detail to OpenAI and return extracted data as dict.
    Uses chat.completions API (correct method).
    Returns dict with extracted fields or error info.
    """


    prompt = f"""Extract company/job details from the email below.
        Return ONLY valid JSON with these fields (use null for unknown values):

        Fields:
        - company_name
        - position_title
        - location
        - website_url
        - salary_min
        - salary_max
        - job_description_url

        Rules:
        - Do NOT guess missing values
        - Use null for unknown fields
        - Return ONLY JSON, no extra text


        Email:
        \"\"\"
        {email_text}
        \"\"\"
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts company/ job details from emails. Always return valid JSON."},
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

