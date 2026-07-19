from groq import Groq

# Replace with your actual API key
client = Groq(
    api_key="YOUR_API_KEY"
)

def ask_groq(prompt):
    """
    Sends a prompt to Groq and returns the response text.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"
    
    