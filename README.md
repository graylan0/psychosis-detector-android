# psychosis-detector-android

## Engineer Notes:
Quantum Circuit: The quantum_emotion_circuit function uses rotations (RY) to encode the normalized RGB values and the amplitude (related to sentiment) into a quantum state. Conditional entanglement is applied based on the amplitude, which could represent the intensity of the emotion.

AsyncIO: The application uses asyncio and httpx for asynchronous HTTP requests. This is necessary for non-blocking network calls in an async application.

AIOSQLite: The application uses aiosqlite to perform asynchronous database operations, which is suitable for async applications.

OpenAI API: The application uses the OpenAI API to generate color codes from emotions and to perform psychosis detection. The API key is loaded from a configuration file.

Kivy UI: The application uses Kivy for the user interface, with screens for chat and settings.

TextBlob: Sentiment analysis is performed using TextBlob, which provides a simple API for common natural language processing (NLP) tasks.
To set up a Python environment with Kivy for debugging, follow these steps:

1. **Install Python**: Ensure you have Python installed on your system. You can download it from the official Python website. It's recommended to use Python 3.6 or above.

2. **Create a Virtual Environment**:
   - Open your terminal or command prompt.
   - Navigate to your project directory.
   - Run `python -m venv kivy_venv` to create a virtual environment named `kivy_venv`.

3. **Activate the Virtual Environment**:
   - On Windows, run `kivy_venv\Scripts\activate`.
   - On macOS/Linux, run `source kivy_venv/bin/activate`.

4. **Install Kivy**:
   - With the virtual environment activated, install Kivy by running `pip install kivy`.

5. **Install Additional Dependencies**:
   - For any additional libraries (like `httpx`, `aiosqlite`, etc.), install them using
   -
   -   `pip install httpx aiosqlite openai kivymd`

6. **Set Up an IDE for Debugging**:
   - Use an IDE like PyCharm, VS Code, or Atom that supports Python and install the necessary extensions for Python and Kivy (if available).

7. **Configure the Debugger**:
   - Set breakpoints in your code where you want to pause execution.
   - Configure the debugger in your IDE to run the script with the correct Python interpreter from your virtual environment.

8. **Run Your Application**:
   - Execute your Kivy application through your IDE with the debugger attached.

9. **Inspect Variables and Step Through Code**:
   - When the debugger hits a breakpoint, inspect variables, step through code, and watch how the application behaves.

10. **Close the Application**:
    - Ensure your application can be closed properly by handling all exceptions and stopping any asynchronous tasks.

By following these steps, you'll have a Python environment set up with Kivy, ready for debugging your application.


## config.json Tutorial 

To obtain an OpenAI API key and set it in a `config.json` file for your project, follow these steps:

1. **Sign Up for OpenAI**:
   - Visit the OpenAI website and sign up for an account if you don't already have one.
   - Navigate to the API section on the OpenAI website.

2. **API Key Generation**:
   - Once you have access to the API section, there should be an option to create a new API key.
   - Follow the prompts to generate a new key. This key is your private token to access OpenAI's API, so keep it secure.

3. **Copy the API Key**:
   - After the key is generated, make sure to copy it. OpenAI will not show the key again for security reasons.

4. **Create `config.json` File**:
   - In your project directory, create a new file named `config.json`.
   - Open this file in a text editor of your choice.

5. **Insert API Key into `config.json`**:
   - Structure your `config.json` file to store the API key. It should look something like this:

```json
{
    "openai_api_key": "your-api-key-here"
}
```

   - Replace `your-api-key-here` with the API key you copied from the OpenAI website.

6. **Save the `config.json` File**:
   - Save the changes to your `config.json` file.

7. **Use the API Key in Your Application**:
   - In your application, you will typically load the `config.json` file to access your API key. Here's an example in Python:

```python
import json

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

openai_api_key = config["openai_api_key"]
```

   - Now you can use `openai_api_key` in your application to authenticate API requests.

8. **Keep the API Key Secure**:
   - Do not share your `config.json` with others or upload it to public repositories.
   - Consider using environment variables for additional security in a production environment.

By following these steps, you'll have your OpenAI API key securely stored in a `config.json` file and ready to be used in your application.
