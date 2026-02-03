import json
import boto3
import os

s3 = boto3.client('s3')
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        response = s3.get_object(Bucket=bucket, Key=key)
        record_content = response['Body'].read().decode('utf-8')
        record = json.loads(record_content)

        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        prompt_body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this record for logical errors (e.g., impossible age, fake locations): {record}. Return ONLY JSON: {{\"status\": \"PASS\"/\"FAIL\", \"reason\": \"text\"}}"
                }
            ]
        })

        res = bedrock.invoke_model(modelId=model_id, body=prompt_body)
        res_body = json.loads(res.get('body').read())
        audit_result = json.loads(res_body['content'][0]['text'])
        
        status = audit_result.get("status", "FAIL")
        target_folder = "trusted" if status == "PASS" else "quarantine"
        file_name = key.split('/')[-1]
        target_key = f"{target_folder}/{file_name}"
        
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': key},
            Key=target_key
        )
        
    
        s3.delete_object(Bucket=bucket, Key=key)
        
        print(f"✅ Successfully audited: {file_name} -> {target_folder}")
        return {"status": 200, "message": "Success"}

    except Exception as e:
        print(f"❌ Error auditing data: {str(e)}")
        return {"status": 500, "error": str(e)}