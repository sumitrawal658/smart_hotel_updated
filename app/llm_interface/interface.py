import gradio as gr
from .chatbot import SmartHotelChatbot
import os

def create_chatbot_interface():
    # Initialize chatbot
    chatbot = SmartHotelChatbot(
        base_url="http://localhost:5000",
        openai_key=os.getenv("OPENAI_API_KEY")
    )
    
    def respond(message, history, room_id, state):
        response = chatbot.process_user_input(message, room_id)
        return response

    def process_audio(audio, room_id, state):
        text = chatbot.process_voice_input(audio)
        response = chatbot.process_user_input(text, room_id)
        return response

    # Create Gradio interface
    with gr.Blocks() as interface:
        gr.Markdown("# Smart Hotel Room Assistant")
        
        with gr.Row():
            room_id = gr.Number(label="Room ID", value=101)
            state = gr.State({})
        
        chatbot = gr.ChatInterface(
            respond,
            additional_inputs=[room_id, state],
            title="Chat with your Room Assistant"
        )
        
        with gr.Row():
            audio_input = gr.Audio(source="microphone", type="filepath")
            audio_button = gr.Button("Process Voice Input")
        
        audio_button.click(
            process_audio,
            inputs=[audio_input, room_id, state],
            outputs=[chatbot]
        )
        
    return interface

if __name__ == "__main__":
    interface = create_chatbot_interface()
    interface.launch() 