from groq import Groq
client = Groq(api_key="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")
models = client.models.list()
for model in models.data:
    print(model.id)