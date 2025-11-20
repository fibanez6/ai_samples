#!/usr/bin/env python3
"""Quick test of OpenAI API connectivity."""

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

async def test_openai():
    print("🧪 Testing OpenAI API connection...")
    
    try:
        # Load API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ No OPENAI_API_KEY found in environment")
            return
        
        print(f"🔑 Using API key: {api_key[:10]}...")
        
        # Test with gpt-3.5-turbo model (more reliable)
        llm = ChatOpenAI(
            model="gpt-5-mini",
            temperature=0.7,
            timeout=5  # 5 second timeout
        )
        
        print("📡 Making API call...")
        
        # Use asyncio.wait_for for additional timeout control
        response = await asyncio.wait_for(
            llm.ainvoke([HumanMessage(content="Say hello")]),
            timeout=10.0
        )

        # response = await asyncio.wait_for(
        #     llm.ainvoke([HumanMessage(content="make a short description of this url: www.fibanez.com")]),
        #     timeout=10.0
        # )
        
        print(f"✅ Success! Response: {response.content}")
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openai())