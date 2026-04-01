import asyncio
import os
from dotenv import load_dotenv

# Force load the .env file so the AWS and Grok SDKs find the keys
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.services.execution.orchestrator import ExecutionOrchestrator

async def run_test():
    print("--------------------------------------------------")
    print("🚀 Initializing Execution Engine...")
    print("--------------------------------------------------")
    
    orchestrator = ExecutionOrchestrator()
    
    # Simple prompt for the AI to process
    prompt_text = "In exactly 2 sentences, explain why moving LLMs to AWS Bedrock is a good idea."
    
    source_messages = [{"role": "user", "content": prompt_text}]
    # Amazon Bedrock ConverseAPI requires strings to be wrapped in a text block
    bedrock_messages = [{"role": "user", "content": [{"text": prompt_text}]}]

    print("⚡ Sending concurrent requests to xAI (Grok) and AWS Bedrock (Claude 3)...")
    try:
        results = await orchestrator.run_comparison(
            source_provider="openai",  # the grok client is using the openai standard!
            source_model="grok-beta",  
            source_messages=source_messages,
            bedrock_model="anthropic.claude-3-sonnet-20240229-v1:0",
            bedrock_messages=bedrock_messages
        )
        
        print("\n🏆 --- EXECUTION RESULTS --- 🏆\n")
        
        print("xAI (Grok-Beta) vs AWS Bedrock (Claude 3 Sonnet)\n")
        print(f"[Grok Latency]: {results['source']['latency_ms']}ms")
        print(f"[AWS Latency] : {results['bedrock']['latency_ms']}ms")
        print("-------------------------------")
        
        print("\n=== GROK RAW OUTPUT ===")
        print(results['source']['content'])
        
        print("\n=== CLAUDE RAW OUTPUT ===")
        print(results['bedrock']['content'])
        
        print("\n✅ Test completed successfully. Job saved to DynamoDB and S3!")

    except Exception as e:
        print("\n❌ EXECUTION FAILED:")
        print(str(e))

if __name__ == "__main__":
    asyncio.run(run_test())
