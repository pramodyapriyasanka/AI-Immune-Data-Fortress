import os
import sys
import time
import json
import boto3
from dotenv import load_dotenv


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from Core.auditor import audit_record_with_ai
except ImportError:
    from core.auditor import audit_record_with_ai

load_dotenv()


s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "your-bucket-name") 

RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw_stream")

def process_files():
    print("🛡️ Fortress Watcher is active. Monitoring for new data...")
    if not os.path.exists(RAW_DIR):
        os.makedirs(RAW_DIR)
    
    while True:
        files = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
        
        for file_name in files:
            file_path = os.path.join(RAW_DIR, file_name)
            
            try:
                with open(file_path, 'r') as f:
                    record = json.load(f)
                
                print(f"🔍 Auditing: {file_name}")
                audit_result = audit_record_with_ai(record)
                if isinstance(audit_result, str):
                    audit_result = json.loads(audit_result)
                
                status = audit_result.get("status", "FAIL")
                target_folder = "trusted" if status == "PASS" else "quarantine"
                
                
                s3_key = f"{target_folder}/{file_name}"
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=s3_key,
                    Body=json.dumps({"original_data": record, "audit": audit_result})
                )
                
                print(f"📤 Moved to S3: {s3_key} | Decision: {status}")
                os.remove(file_path) 
                
            except Exception as e:
                print(f"❌ Error processing {file_name}: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    process_files()