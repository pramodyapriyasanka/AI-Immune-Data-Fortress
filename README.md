
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


