from django.shortcuts import render

from openai import OpenAI
from google import genai
from google.genai import types
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

ai_platforms = {
    "ChatGPT": {
        "base_url": "https://api.openai.com/v1",
        "model": "o3"
    },
    "DeepSeek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-reasoner"
    },
    #  Gemini 采用原生 SDK
    "Gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": "gemini-2.5-pro-preview-06-05"
    },
    "Claude": {
        # Unsupported now
    },
    "Grok": {
        "base_url": "https://api.x.ai/v1",
        "model": "grok-3-think"
    },
    "Doubao": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "" # Unsupported now
    },
    "KIMI": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-32k"
    },
    "Qwen": {
        # Unsupported now
    },
    "Hunyuan": {
        # Unsupported now
    },
}

def convert_messages_for_gemini(messages):
    full_prompt_text = ""
    for msg in messages:
        if "content" in msg:
            full_prompt_text += f"{msg['role']}: {msg['content']}\n\n"
    return full_prompt_text

class AiGrading(APIView):
    def post(self, request):

        platform = request.data.get("platform")
        token = request.data.get("token")
        messages = request.data.get("messages", [])
        
        if not platform or not token or not messages:
            return Response({"error", "Request must contain platform and token"}, status=HTTP_400_BAD_REQUEST)

        config = ai_platforms.get(platform)
        base_url = config["base_url"]
        model = config["model"]

        try:
            if platform == "Gemini":
                
                client = genai.Client(api_key=token)

                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=15000)
                )

                response = client.models.generate_content(model=model, contents=convert_messages_for_gemini(messages), config=config)
                reply = response.text
                
            else:
                client = OpenAI(api_key=token, base_url=base_url)

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.5, # 更理性
                    max_tokens=1024
                )

                reply = response.choices[0].message.content.strip()
                
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"response": reply})