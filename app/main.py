import asyncio
import aiosqlite
import openai
import json
import re
import httpx
from textblob import TextBlob
import pennylane as qml
from pennylane import numpy as np
import openai
import asyncio
from kivy.clock import Clock
import json
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label

class ChatLabel(RecycleDataViewBehavior, Label):
    """Basic label class for chat messages in the RecycleView."""
    pass

class ChatScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

openai.api_key = config["openai_api_key"]

qml_device = qml.device('default.qubit', wires=4)

KV = '''
ScreenManager:
    ChatScreen:
    SettingsScreen:

<ChatScreen>:
    name: 'chat'
    BoxLayout:
        orientation: 'vertical'
        ActionBar:
            background_color: 0.3, 0.3, 0.3, 1
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'Chat with Bot'
                    with_previous: False
                    app_icon: ''
                    color: 1, 1, 1, 1
                ActionButton:
                    icon: 'brain'
                    on_release: app.analyze_emotion(message_input.text)
                    color: 0.9, 0.9, 0.9, 1
                ActionButton:
                    text: 'Settings'
                    on_release: app.root.current = 'settings'
                    color: 0.9, 0.9, 0.9, 1
        BoxLayout:
            canvas.before:
                Color:
                    rgba: 0.2, 0.2, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            RecycleView:
                id: chat_list
                viewclass: 'ChatLabel'
                RecycleBoxLayout:
                    default_size: None, dp(56)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
                    spacing: dp(2)
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(4)
            spacing: dp(4)
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            TextInput:
                id: message_input
                hint_text: 'Type a message...'
                background_color: 1, 1, 1, 0.3
                foreground_color: 1, 1, 1, 1
                padding_y: dp(10)
                padding_x: dp(10)
                size_hint_x: 0.8
                multiline: False
                on_text_validate: app.analyze_emotion(self.text)
            Button:
                text: 'Analyze'
                background_normal: ''
                background_color: 0.8, 0.8, 0.8, 1
                color: 0, 0, 0, 1
                on_release: app.analyze_emotion(message_input.text)

<SettingsScreen>:
    name: 'settings'
    BoxLayout:
        orientation: 'vertical'
        ActionBar:
            background_color: 0.3, 0.3, 0.3, 1
            pos_hint: {'top':1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: 'Settings'
                    with_previous: False
                    app_icon: ''
                    color: 1, 1, 1, 1
                ActionButton:
                    text: 'Back'
                    on_release: app.root.current = 'chat'
                    color: 0.9, 0.9, 0.9, 1
        GridLayout:
            cols: 1
            padding: dp(24)
            spacing: dp(15)
            TextInput:
                id: api_key
                hint_text: 'OpenAI API Key'
                multiline: False
                padding_y: dp(10)
                padding_x: dp(10)
                size_hint_x: 0.8
                pos_hint: {'center_x': 0.5}
            Button:
                text: 'Save Settings'
                size_hint_x: 0.8
                pos_hint: {'center_x': 0.5}
                on_release: app.save_settings(api_key.text)
'''
class MainApp(App):
    def build(self):
        self.screen = Builder.load_string(KV)
        return self.screen

    def analyze_emotion(self, emotion):
        self.screen.ids.result_label.text = f'Analyzing "{emotion}"...'
        asyncio.create_task(self.async_analyze_emotion(emotion))

    async def async_analyze_emotion(self, emotion):
        async with httpx.AsyncClient() as client:
            color_code = await self.get_color_code(emotion, client)
            amplitude = self.sentiment_to_amplitude(emotion)
            quantum_state = self.quantum_emotion_circuit(color_code, amplitude)
            detection_state = await self.perform_psychosis_detection(emotion, color_code, client)
            await self.store_emotion_data(emotion, color_code, quantum_state, amplitude, detection_state)
            self.screen.ids.result_label.text = f'Result for "{emotion}": {detection_state}'

    async def get_color_code(self, emotion, client):
        # Define the prompt with more structured instructions
        color_prompt = "Translate the emotion '" + emotion + "' into a corresponding HTML color code. " \
                       "The color should visually represent the feeling conveyed by the emotion."

        # Make the API call using the correct endpoint and improved prompt
        response = await client.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': 'Bearer ' + openai.api_key},
            json={
                "model": "gpt-3.5-turbo",  # Specify the model you want to use
                "prompt": color_prompt,
                "max_tokens": 60,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        data = response.json()
        color_code_match = re.search(r'#[0-9a-fA-F]{6}', data['choices'][0]['text'])
        return color_code_match.group(0) if color_code_match else '#FFFFFF'


    def sentiment_to_amplitude(self, emotion):
        analysis = TextBlob(emotion)
        return (analysis.sentiment.polarity + 1) / 2

    def quantum_emotion_circuit(self, color_code, amplitude):
        @qml.qnode(qml_device)
        def circuit():
            qml.RY(np.pi * amplitude, wires=0)
            qml.templates.ColorCode(color_code, wires=range(1, 4))
            return qml.state()

        return circuit()

    async def perform_psychosis_detection(self, emotion, color_code, quantum_state, amplitude, client):
        # Convert the quantum state to a string representation
        quantum_state_str = json.dumps(quantum_state.tolist())

        # Construct the prompt
        task2_prompt = (
            "Please analyze the user's input as " + quantum_state_str + 
            " this is the " + str(amplitude) + 
            " and the text generating the quantum state: " + emotion + 
            ", and provide insights into psychosis detection by providing the following 1. " +
            "Only reply with Yes or No as the first words, after yes or no, " +
            "then the clustering of emotions and potential if any of mania or depression or psychosis. " +
            "Following is quantum state data that provides a right to left emotional and brain capacitive " +
            "delivery of understanding to AI models. Interpret the data from the text in the example. " +
            "Provide Yes or No."
        )

        # Make the API call
        response = await client.post(
            'https://api.openai.com/v1/completions',
            headers={'Authorization': f'Bearer {openai.api_key}'},
            json={
                "model": "gpt-3.5-turbo",
                "prompt": task2_prompt,
                "max_tokens": 60,
                "temperature": 0  # You can adjust this if you want different creativity levels
            }
        )
        response.raise_for_status()
        data = response.json()
        detection_state_match = re.search(r'\b(Yes|No)\b', data['choices'][0]['text'], re.IGNORECASE)
        return detection_state_match.group(0) if detection_state_match else "Unknown"

    
    async def store_emotion_data(self, emotion, color_code, quantum_state, amplitude, detection_state):
        async with aiosqlite.connect("emotion_data.db") as db:
            await db.execute("INSERT INTO emotion_data (emotion, color_code, quantum_state, amplitude) VALUES (?, ?, ?, ?)",
                             (emotion, color_code, json.dumps(quantum_state), amplitude))
            await db.commit()

if __name__ == '__main__':
    MainApp().run()
