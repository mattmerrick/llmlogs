from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the analysis data from the request
        data = request.json
        analysis = data.get('analysis')
        
        # Create a prompt from the analysis data
        prompt = f"""Analyze this website's AI SEO data and provide specific recommendations:

URL: {analysis['url']}

Scores:
- Technical SEO: {analysis['scores']['technicalSEO']}
- Content Structure: {analysis['scores']['structure']}
- Semantic Markup: {analysis['scores']['semantic']}
- LLM Readiness: {analysis['scores']['llmReadiness']}
- Content Quality: {analysis['scores']['contentQuality']}

Key Findings:
{format_findings(analysis['findings'])}

Please provide a detailed action plan with:
1. Technical improvements for AI crawlers
2. Content structure optimization
3. Semantic markup enhancements
4. Citation and authority building
5. Specific opportunities for backlinks and AI-focused partnerships

Format each recommendation with priority level, implementation steps, and expected impact."""

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI SEO expert specializing in optimizing websites for language models and AI crawlers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Parse the response and format recommendations
        recommendations = parse_recommendations(response.choices[0].message.content)
        
        return jsonify({
            "success": True,
            "plans": recommendations
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def format_findings(findings):
    return "\n".join([f"- {finding['title']}: {finding['description']}" for finding in findings])

def parse_recommendations(content):
    # Split content into sections and format as action plans
    # This is a simple implementation - you might want to make it more robust
    plans = []
    sections = content.split('\n\n')
    
    for section in sections:
        if not section.strip():
            continue
            
        lines = section.split('\n')
        title = lines[0].strip().replace('#', '').strip()
        
        # Extract priority from content
        priority = 'medium'
        if 'high priority' in section.lower():
            priority = 'high'
        elif 'low priority' in section.lower():
            priority = 'low'
            
        # Extract steps
        steps = [line.strip('- ').strip() for line in lines if line.strip().startswith('-')]
        
        # Extract description
        description = next((line for line in lines if not line.startswith('#') and not line.startswith('-')), '')
        
        if title and steps:
            plans.append({
                'title': title,
                'priority': priority,
                'description': description.strip(),
                'steps': steps
            })
    
    return plans

if __name__ == '__main__':
    app.run(port=5000) 