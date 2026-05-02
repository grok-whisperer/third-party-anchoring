"""
Third-Party Anchoring Demo
Simple implementation of the User → Copy → Analyst pattern
for reducing instruction misattribution in agentic workflows.
"""

import os
from openai import OpenAI  # Change to Anthropic SDK if preferred

# Initialize your client (choose one)
client = OpenAI()  # OpenAI / Groq / etc.
# from anthropic import Anthropic
# client = Anthropic()

def third_party_anchoring_demo():
    print("=== Third-Party Anchoring Demo ===\n")
    print("Type your requests. Type 'exit' to quit.\n")
    
    history = []  # Keeps conversation context
    
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Demo ended.")
            break
            
        history.append({"role": "user", "content": user_input})
        
        # === COPY: Generate Proposal ===
        copy_msg = {
            "role": "system",
            "content": "You are 'Copy'. Your ONLY job is to generate one clear, concise proposal or next step. Do not evaluate or decide."
        }
        
        copy_response = client.chat.completions.create(
            model="gpt-4o-mini",          # Change to claude-3-5-sonnet-20240620 or similar
            messages=history + [copy_msg],
            max_tokens=300,
            temperature=0.7
        ).choices[0].message.content
        
        print(f"\nCopy (Proposal): {copy_response}")
        history.append({"role": "assistant", "content": f"[Copy Proposal]: {copy_response}"})
        
        # === ANALYST: Evaluate & Decide ===
        analyst_msg = {
            "role": "system",
            "content": "You are the Analyst. Critically evaluate Copy's proposal. Give reasoning and a clear accept/modify/reject decision."
        }
        
        analyst_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history + [analyst_msg],
            max_tokens=400,
            temperature=0.7
        ).choices[0].message.content
        
        print(f"Analyst: {analyst_response}\n")
        history.append({"role": "assistant", "content": f"[Analyst Decision]: {analyst_response}"})
        
        # Optional: trim history to avoid token limits
        if len(history) > 30:
            history = history[-30:]

if __name__ == "__main__":
    third_party_anchoring_demo()
