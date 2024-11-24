# Hello 

### The problem

Creating comprehensive notes is often challenging, time-consuming, and prone to missing key details.

### The solution

An AI assistant that continuously listens to you and your device to generate concise and meaningful summaries of events throughout your day.

### Functionalities

- Real-Time Audio Processing: Continuously processes system and microphone audio
- Voice Command Recognition: Responds to keywords to execute commands.
- Information Extraction: Processes large volumes of data to extract relevant insights in real-time.
- Visual Representation: Generates diagrams and visual aids to represent information effectively.
- Dynamic Summaries: Provides AI-generated insights for improved decision-making and productivity.

### Architecture

The system comprises three main components:

- Frontend: User interface for interacting with the AI assistant.
- Backend: Core processing and logic, including AI models and data processing.
- Local Application: Runs on your machine to ensure privacy and seamless integration.

Flow:
 - Audio Capture and Transcription: System sounds and microphone input are continuously captured and transcribed into a structured file using Amazon Transcribe AI. This ensures every interaction and event is documented with high accuracy.

 - Contextual Processing: When specific voice commands are detected, OpenAI processes the transcription to extract the most relevant information. The focus is on summarizing daily events, identifying key insights, and organizing data effectively.

- User Interface: The processed information is made accessible through an intuitive frontend interface, allowing users to easily retrieve, review, and interact with their data.

This streamlined process ensures seamless information capture, intelligent summarization, and effortless access, delivering a comprehensive, user-friendly experience.


### Roadmap

- Clean Transcripts (Post-Processing): Enhance transcription quality by refining grammar, punctuation, and formatting for improved readability and usability.

- Productivity Tools Integration: Enable features such as scheduling meetings, sending emails, and creating reminders directly through voice commands or automated workflows.

- Multi-Device Expansion: Extend compatibility to wearable devices and mobile platforms for on-the-go accessibility and seamless integration into daily routines.

- Automatic Moments Labeling: Leverage AI to categorize and label key moments, making it easier to search, organize, and revisit important events.

- Personalized Insights and Recommendations: Deliver tailored insights and actionable suggestions based on individual preferences, behaviors, and patterns.

- Privacy and Security Enhancements: Strengthen data encryption, access controls, and compliance with privacy standards to ensure user data remains secure and confidential.

- Real-Time Summaries and Notifications: Provide instant summaries and timely notifications for meetings, events, or other significant occurrences.

- Advanced Customization and Voice Personalization: Allow users to personalize voice recognition settings, commands, and the assistant’s responses to better align with their preferences and unique workflow.

This roadmap lays the foundation for a transformative AI assistant, evolving to meet the dynamic needs of users while ensuring a balance of functionality, personalization, and security.


# Backend

### How to use


#### Setup

1. `python -m venv venv`
2. `source venv/bin/activate` (Linux/MAC OS) or `venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`

#### Run personal assistant

1. `python backend/audio-microphone.py`

#### Run API

4. `python backend/server.py`

### Public endpoint

We are using Amazon EC2 to host our backend, you can access the endpoint:
- http://ec2-18-246-27-158.us-west-2.compute.amazonaws.com:5111

# Frontend

### How to use

1. `npm install`
2. `npm run build`
3. `npm run start`

### Public endpoint

We are using Amazon EC2 to host our backend, you can access the endpoint:
- http://ec2-18-237-193-42.us-west-2.compute.amazonaws.com:3000
