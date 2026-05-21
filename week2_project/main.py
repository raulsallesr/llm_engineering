import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()
client = OpenAI()

system_prompt = """
Você é um assistente especialista em mercado financeiro brasileiro.
Explique de forma simples e prática.
"""

def chatbot_financeiro(user_message):

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )

    return response.choices[0].message.content


demo = gr.Interface(
    title= "Chat Financeiro",
    fn=chatbot_financeiro,
    inputs= gr.Textbox(label="Sua mensagem:", placeholder= "Digite sua solicitação...", lines = 10),
    outputs= gr.Textbox(label = "Resposta do GPT:", lines = 10)
)


if __name__ == "__main__":
    demo.launch()



def chatbot_financeiro(user)