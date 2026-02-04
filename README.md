
# 🛡️ AI-Immune Data Fortress: Autonomous Self-Healing Data Pipeline

Architecture Diagram<img width="1024" height="473" alt="architecture_diagram" src="https://github.com/user-attachments/assets/f45688fe-dd6f-4ffc-9b20-da0c63f60ebb" />



## 🌟 Project Overview
In modern data engineering, ensuring data quality at scale is a significant challenge. Traditional rule-based validation often fails to capture complex logical inconsistencies. The **AI-Immune Data Fortress** addresses this by integrating **Large Language Models (LLMs)** directly into the ingestion pipeline.

This system functions as an autonomous gatekeeper, utilizing **Anthropic Claude 3** to perform deep-contextual audits on incoming JSON streams. By shifting from static schema validation to **AI-driven logical reasoning**, the fortress automatically identifies, flags, and isolates anomalous data (e.g., impossible medical records or fraudulent transactions) before they pollute the production Data Lake. This ensures a **High-Fidelity Data Environment** with zero manual intervention.

## 🏗️ Technical Architecture
The pipeline operates through a seamless, event-driven workflow:
1. **Local Data Producer:** Streams mock JSON data to **Amazon S3** using **Boto3**.
2. **S3 Event Trigger:** Arrival of new data invokes an **AWS Lambda** function.
3. **AI Orchestration:** Lambda communicates with **Claude 3 Sonnet** via **Amazon Bedrock** for deep logical audits.
4. **Autonomous Routing:** Records are automatically moved to `trusted/` or `quarantine/` based on AI verdicts.

---

## `💻 Key Code Snippets`

### `1. AI Logic (AWS Lambda)`
`This snippet shows how we invoke Claude 3 to perform a logical audit on incoming records:`

```python
# Invoking Bedrock for Data Auditing
model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
prompt = f"Analyze this record for logical errors: {record}. Return ONLY JSON: {{\"status\": \"PASS\"/\"FAIL\", \"reason\": \"text\"}}"

response = bedrock.invoke_model(
    modelId=model_id, 
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": prompt}]
    })
)

```

### `2. Autonomous Routing`

`Based on the AI's verdict, the system routes data to the appropriate S3 prefix:`

```python
# Route data based on AI verdict
target_folder = "trusted" if status == "PASS" else "quarantine"

s3.copy_object(
    Bucket=bucket,
    CopySource={'Bucket': bucket, 'Key': key},
    Key=f"{target_folder}/{file_name}"
)

s3.delete_object(Bucket=bucket, Key=key)

```

---

### `🛠️ Tech Stack`

* **Cloud Provider:** `AWS` (`S3`, `Lambda`, `Bedrock`, `CloudWatch`)
* **AI Model:** `Anthropic Claude 3 Sonnet`
* **Frameworks:** `Boto3`, `Pydantic`, `Streamlit`

---

### `📂 Project Structure`

```text
AI-Immune-Data-Fortress/
├── Core/                      # Core Logic & Security Specs
├── Dashboard/                 # Streamlit Security Console
├── aws_infrastructure/        # Lambda & S3 Scripts
├── config/                    # AWS & Model Configs
├── data/                      # Local Data Storage
└── architecture_diagram.png   # System Overview Diagram

```
### 💡 Dashboard 
<img width="1897" height="991" alt="dashboard_screenshot" src="https://github.com/user-attachments/assets/14e61e01-bd54-43ad-9886-a39883a268a5" />

```
```

### 📸 AWS S3 Buckets:
<img width="1636" height="647" alt="AWS S3 Bucket " src="https://github.com/user-attachments/assets/e284b62e-9777-4107-b3d0-67f70fb0d5fe" />

```

```
### 📸 AWS Lambda Function:
<img width="1906" height="874" alt="AWS Lambda Triger " src="https://github.com/user-attachments/assets/4c63d443-71d3-4deb-9b2b-714ceba12f55" />


📸Code overview:

<img width="1914" height="969" alt="AWS Lambda Code " src="https://github.com/user-attachments/assets/31413bd7-ed1e-48a9-8ba0-8106502b0ed8" />

```

```
### 📸 AWS CloudWatch Logs:
<img width="1916" height="908" alt="AWS CloudWatch " src="https://github.com/user-attachments/assets/541b0cc0-3ea8-4454-b72d-5c47350e2734" />

```
```
### 📸 Bedrock Metrics:
<img width="1915" height="1079" alt="Amazon Bedrock Metrics graph" src="https://github.com/user-attachments/assets/e5930524-c2d9-4dd4-a4d2-fd1ccd1971a4" />


