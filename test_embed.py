from openai import OpenAI

# Paste your full API key here (not sk-proj, use sk-xxxxxxxxxxx)
client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

try:
    response = client.embeddings.create(
        input=["hello world"],
        model="text-embedding-3-small"
    )
    print("✅ Response:", response)
except Exception as e:
    print("❌ Error:", e)
