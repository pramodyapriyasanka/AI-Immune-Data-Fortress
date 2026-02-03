import os
import json
import time
import random
import boto3  
from datetime import datetime, timezone
from pydantic import BaseModel


BUCKET_NAME = 'ai-data-fortress-pramodya-2026' 
s3_client = boto3.client('s3')

class UserRecord(BaseModel):
    user_id: int
    user_name: str
    age: int
    location: str
    timestamp: str

def generate_mock_data():
    """AI creta the random data record simulating user info."""
    users = ["Kasun", "Nimmi", "John", "Sarah", "Pramodya", "Anura"]
    locations = ["Colombo", "Kandy", "Dubai", "New York", "London"]
    
    
    return UserRecord(
        user_id=random.randint(1000, 9999),
        user_name=random.choice(users),
        age=random.choice([22, 250, -5, 45, 30, 150]), 
        location=random.choice(locations),
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def start_streaming_to_s3():
    print(f"🚀 AI Data Fortress: Streaming to S3 started.")
    print(f"📦 Target Bucket: {BUCKET_NAME}")
    
    try:
        while True:
            record = generate_mock_data()
            file_name = f"record_{record.user_id}_{int(time.time())}.json"
            
            s3_key = f"data/raw_stream/{file_name}"
            
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=record.json(),
                ContentType='application/json'
            )
            
            print(f"✅ Successful Upload: {s3_key} | User: {record.user_name}")
            time.sleep(5) 
            
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("💡 Hint: Make sure you have run 'aws configure' and installed 'boto3'")

if __name__ == "__main__":
    start_streaming_to_s3()