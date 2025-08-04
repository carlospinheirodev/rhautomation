import os
import json
import base64
import requests
from dotenv import load_dotenv

def analysis_with_n8n(job_description: str):
    url = "https://webhook.ograndelider.com.br/webhook/analyse-available-candidates"
    username = os.getenv('N8N_AUTH_USER')
    password = os.getenv('N8N_AUTH_PASSWORD')

    auth_header = base64.b64encode(f"{username}:{password}".encode()).decode()

    payload = {
        "job_description": job_description,
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict) and 'output' in first_item:
                return first_item['output']

        if isinstance(data, dict):
            if 'best_candidate' in data and 'ranking_list' in data:
                return data
            if 'output' in data:
                output = data['output']
                if isinstance(output, list) and len(output) > 0:
                    first_item = output[0]
                    if isinstance(first_item, dict) and 'output' in first_item:
                        return first_item['output']
                    if isinstance(first_item, dict) and 'best_candidate' in first_item and 'ranking_list' in first_item:
                        return first_item
                if isinstance(output, dict) and 'best_candidate' in output and 'ranking_list' in output:
                    return output
        print("Could not find expected data structure in response")
        return {"error": "Formato de resposta inválido", "received_data": data}
    else:
        return {"error": f"Erro {response.status_code}: {response.text}"}