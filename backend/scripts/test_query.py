#!/usr/bin/env python3
"""Test the RAG chatbot query endpoint."""
import httpx
import json

url = "http://127.0.0.1:8004/query"
payload = {
    "question": "What is ROS 2 and how is it used in humanoid robotics?",
    "mode": "full_book"
}

print(f"Sending query: {payload['question']}")
print("-" * 50)

response = httpx.post(url, json=payload, timeout=60.0)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\nAnswer:\n{data.get('answer', 'No answer')}")
    print(f"\nCitations:")
    for citation in data.get('citations', []):
        print(f"  - Chapter {citation.get('chapter_number')}: {citation.get('chapter_title')}")
        print(f"    Section: {citation.get('section_title')}")
else:
    print(f"Error: {response.text}")
