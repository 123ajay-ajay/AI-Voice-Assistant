A fully functional AI-based Voice Assistant developed in Python that listens, understands, and executes voice commands – just like your own **J.A.R.V.I.S.**. This assistant can open apps, search Google/YouTube, send WhatsApp messages, and much more — all through **hands-free voice control**.

### 🚀 Key Features

#### 📞 Call & Message
- 📱 **Make Phone Calls** – `Phone call to AnyName`
- ✉️ **Send SMS Messages** – `Send message to AnyName`
- 🔊 **WhatsApp Audio/Video Calls** – `Audio call to AnyName on WhatsApp`
- 💬 **Send WhatsApp Messages** – `Send message to AnyName on WhatsApp`

#### 🌐 Smart Search
- 🔍 **Search on Google** – `Search IPL score on Google`
- 🎥 **Search on YouTube** – `Search Python tutorial on YouTube`

#### 📲 App Control
- 🌐 **Open Google App** – `Open Google`
- 📺 **Open YouTube App** – `Open YouTube`
- 🟢 **Open WhatsApp** – `Open WhatsApp`

#### ⚙️ Phone Controls
- 🔔 **Open Notification Panel** – `Open notification panel`
- 🔄 **Open Recent Apps** – `Open recent apps`

---

### ✅ Extra Highlights
- 🎤 Fully voice-controlled system
- 🤖 Hands-free Android automation
- 🗣️ Accurate speech recognition
- 🔄 Returns to idle (blob UI) automatically after command execution

  Technologies Used
🟢 Python – core desktop logic and automation
🟢 Flutter – mobile app frontend and voice control
🟢 SpeechRecognition (Python) – for desktop voice input
🟢 speech_to_text (Flutter) – for mobile voice input
🟢 pyttsx3 / gTTS – for desktop text-to-speech
🟢 flutter_tts – for mobile text-to-speech
🟢 re (Regex) – to parse and match voice commands
🟢 Provider (Flutter) – state management for speech and UI
🟢 url_launcher – to open apps like YouTube/Google/WhatsApp on mobile
🟢 android_intent_plus – to trigger native Android actions like calling, opening apps
🟢 SiriWaveform + TextAnimator (Flutter) – for waveform and UI animations
🟢 HTML, CSS, JavaScript, jQuery, Textillate.js – desktop Jarvis UI animations
🟢 Lottie Animations – animated visuals in both mobile and desktop
🟢 multiprocessing (Python) – to run Jarvis and hotword detection together
🟢 ADB (Android Debug Bridge) – for controlling phone from desktop
🟢 sqflite (Flutter) – for local SQLite database (contacts, etc.)
🟢 webbrowser / os (Python) – for launching websites and apps on desktop
