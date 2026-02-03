# 🛡️ AI-Immune Data Fortress: Autonomous Self-Healing Data Pipeline

![Architecture Diagram](architecture_diagram.png)

## 🌟 Project Overview
The **AI-Immune Data Fortress** is an enterprise-grade data engineering solution built on **AWS**. It utilizes **Generative AI** to autonomously audit and validate incoming data streams in real-time. By implementing a **Zero-Trust** architecture, the system ensures that only logically verified data enters the trusted environment.

## 🏗️ Technical Architecture
The pipeline operates through a seamless, event-driven workflow:
1. **Local Data Producer:** Streams mock JSON data to **Amazon S3** using **Boto3**.
2. **S3 Event Trigger:** Arrival of new data invokes an **AWS Lambda** function.
3. **AI Orchestration:** Lambda communicates with **Claude 3 Sonnet** via **Amazon Bedrock** for deep logical audits.
4. **Autonomous Routing:** Records are automatically moved to `trusted/` or `quarantine/` based on AI verdicts.

## 💻 Key Code Snippets

### 1. AI Logic (AWS Lambda)
This snippet shows how we invoke **Claude 3** to perform a logical audit on incoming records:

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




