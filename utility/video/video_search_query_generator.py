from openai import OpenAI
import os
import json
import re
from datetime import datetime
from utility.utils import log_response,LOG_TYPE_GPT

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "llama3-70b-8192"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    model = "gpt-4o"
    OPENAI_API_KEY = os.environ.get('OPENAI_KEY')
    client = OpenAI(api_key=OPENAI_API_KEY)

log_directory = ".logs/gpt_logs"

prompt = """# Instructions

Given the following video script and timed captions, extract three visually concrete and specific keywords for each time segment that can be used to search for background videos. The keywords should be short and capture the main essence of the sentence. They can be synonyms or related terms. If a caption is vague or general, consider the next timed caption for more context. If a keyword is a single word, try to return a two-word keyword that is visually concrete. If a time frame contains two or more important pieces of information, divide it into shorter time frames with one keyword each. Ensure that the time periods are strictly consecutive and cover the entire length of the video. Each keyword should cover between 2-4 seconds. The output should be in JSON format, like this: [[[t1, t2], ["keyword1", "keyword2", "keyword3"]], [[t2, t3], ["keyword4", "keyword5", "keyword6"]], ...]. Please handle all edge cases, such as overlapping time segments, vague or general captions, and single-word keywords.

For example, if the caption is 'The cheetah is the fastest land animal, capable of running at speeds up to 75 mph', the keywords should include 'cheetah running', 'fastest animal', and '75 mph'. Similarly, for 'The Great Wall of China is one of the most iconic landmarks in the world', the keywords should be 'Great Wall of China', 'iconic landmark', and 'China landmark'.

Important Guidelines:

Use only English in your text queries.
Each search string must depict something visual.
The depictions have to be extremely visually concrete, like rainy street, or cat sleeping.
'emotional moment' <= BAD, because it doesn't depict something visually.
'crying child' <= GOOD, because it depicts something visual.
The list must always contain the most relevant and appropriate query searches.
['Car', 'Car driving', 'Car racing', 'Car parked'] <= BAD, because it's 4 strings.
['Fast car'] <= GOOD, because it's 1 string.
['Un chien', 'une voiture rapide', 'une maison rouge'] <= BAD, because the text query is NOT in English.

Note: Your response should be the response only and no extra text or data.
  """

def fix_json(json_str):
    # Replace typographical apostrophes with straight quotes
    json_str = json_str.replace("’", "'")
    # Replace any incorrect quotes (e.g., mixed single and double quotes)
    json_str = json_str.replace("“", "\"").replace("”", "\"").replace("‘", "\"").replace("’", "\"")
    # Add escaping for quotes within the strings
    json_str = json_str.replace('"you didn"t"', '"you didn\'t"')
    return json_str

def getVideoSearchQueriesTimed(script, captions_timed):
    try:
        # Get response from OpenAI
        response_text = call_OpenAI(script, captions_timed)
        
        # Clean up the response text
        # Remove the "```json" and "```" markers
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Clean up any content: prefix
        if 'content:' in response_text:
            response_text = response_text.split('content:')[-1].strip()
        
        # Parse the JSON array
        import json
        search_terms = json.loads(response_text)
        
        # Convert the search terms into the expected format
        formatted_terms = []
        for time_range, prompts in search_terms:
            start_time, end_time = time_range
            formatted_terms.append([[float(start_time), float(end_time)], prompts])
        
        return formatted_terms
    except Exception as e:
        print(f"error in response {str(e)}")
        return None

def call_OpenAI(script,captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script,"".join(map(str,captions_timed)))
    print("Content", user_content)
    
    response = client.chat.completions.create(
        model= model,
        temperature=1,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]
    )
    
    text = response.choices[0].message.content.strip()
    text = re.sub('\s+', ' ', text)
    print("Text", text)
    log_response(LOG_TYPE_GPT,script,text)
    return text