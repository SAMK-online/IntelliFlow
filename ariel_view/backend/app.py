from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from analyzer import TopicAnalyzer

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Validate required API keys are set
required_keys = ['OPENAI_API_KEY', 'TRAVERSAAL_ARES_API_KEY', 'PERPLEXITY_API_KEY']
for key in required_keys:
    if not os.environ.get(key):
        raise ValueError(f"Required environment variable {key} is not set")

# Initialize Flask app
app = Flask(__name__)
# Enable CORS with specific origins for security
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # React development server
            "http://127.0.0.1:3000",
            "https://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize analyzer
analyzer = TopicAnalyzer()

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_topic():
    """
    Analyze a topic using Ariel View
    Expects JSON: {
        "topic": "Topic to analyze",
        "options": {
            "depth": "deep" | "quick"  # Optional: analysis depth
        }
    }
    Maximum 8 videos will be returned by default.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        print("Received request:", request.get_json())
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        topic = data.get('topic')
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        options = data.get('options', {})
        depth = options.get('depth', 'quick')
        print(f"Analyzing topic: {topic} with depth: {depth}")

        # Analyze the topic
        try:
            raw_result = analyzer.analyze_topic(topic, depth)
            print("Analysis completed successfully")
        except Exception as analysis_error:
            print(f"Analysis error: {str(analysis_error)}")
            return jsonify({'error': f'Analysis failed: {str(analysis_error)}'}), 500

        # Just return the raw result
        result = raw_result

        print("Sending response:", result)
        return jsonify(result)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'apis': {
            'perplexity': bool(os.getenv('PERPLEXITY_API_KEY')),
            'openai': bool(os.getenv('OPENAI_API_KEY'))
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
