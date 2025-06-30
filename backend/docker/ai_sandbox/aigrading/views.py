
from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from openai import OpenAI
from google import genai
from google.genai import types
from volceginesdkarkruntime import Ark

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
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.5-pro-preview-06-05"
    },
    #  Claude 暂时采用OpenAI SDK
    #  Anthropic 原生SDK 待开发
    "Claude": {
        "base_url": "https://api.anthropic.com/v1",
        "model": "claude-opus-4-20250514"
    },
    "Grok": {
        "base_url": "https://api.x.ai/v1",
        "model": "grok-3-latest"
    },
    #  Doubao 采用原生 SDK
    "Doubao": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-seed-1.6-thinking"
    },
    "KIMI": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-128k"
    },
    "Qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-max-latest"
    },
    "Hunyuan": {
        "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
        "model": "hunyuan-turbo"
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
        api_key = request.data.get("api_key")
        messages = request.data.get("messages", [])
        
        if not platform or not api_key or not messages:
            return Response({"error", "Request must contain platform and api_key"}, status=HTTP_400_BAD_REQUEST)

        config = ai_platforms.get(platform)
        base_url = config["base_url"]
        model = config["model"]

        try:
            if platform == "Gemini":
                client = genai.Client(api_key=api_key)

                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=15000)
                )

                response = client.models.generate_content(model=model, contents=convert_messages_for_gemini(messages), config=config)
                reply = response.text

            else:
                if platform == "Doubao":
                    client = Ark(api_key=api_key)
                else:
                    client = OpenAI(api_key=api_key, base_url=base_url) 

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.4, # 更理性
                    max_tokens=15000
                )

                reply = response.choices[0].message.content
                
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"response": reply})