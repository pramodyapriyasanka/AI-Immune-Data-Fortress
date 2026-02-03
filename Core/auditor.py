import boto3
import json
import os
from dotenv import load_dotenv


load_dotenv()
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

def audit_record_with_ai(data_record):
    """Sends the data to Amazon Bedrock (Claude 3 Sonnet) to check for logical errors."""
    
  
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.1,
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this record for logical errors (e.g., impossible age, fake locations): {data_record}. Return ONLY JSON: {{\"status\": \"PASS\"/\"FAIL\", \"reason\": \"text\", \"confidence_score\": 0.0-1.0}}"
            }
        ]
    })

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=body
        )
        
        response_body = json.loads(response.get('body').read())
        raw_text = response_body['content'][0]['text']
        return json.loads(raw_text) 
    
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}


if __name__ == "__main__":
    test_data = {"user_id": 1234, "age": 250, "location": "Colombo"}
    result = audit_record_with_ai(test_data)
    print(f"AI Audit Result: {result}")