# AI Turn Co-Pilot

## Overview

AI Turn Co-Pilot is a web-based driving safety assistant built with Streamlit that simulates real-world driving scenarios to test and demonstrate adaptive AI-generated safety alerts. The application uses OpenAI's GPT-5 model to generate context-aware, personalized alerts that help prevent car accidents, with a particular focus on misjudged turns and driver distraction.

The system adapts its communication style based on user behavior history - if a driver repeatedly triggers the same safety scenario (e.g., drowsy driving), the alerts become progressively firmer and more urgent. This adaptive approach prevents alert fatigue by varying tone and phrasing while maintaining relevance.

## Recent Changes (October 24, 2025)

- **Initial Implementation**: Built complete AI Turn Co-Pilot MVP with all core features
- **Escalation Logic**: Implemented correct adaptive behavior escalation (calm→moderate→firm→critical)
- **Bug Fixes**: Resolved off-by-one errors in urgency level calculation and alert generation timing
- **Testing**: Comprehensive end-to-end testing verified all scenarios work correctly
- **UI Layout**: Optimized Current Alert section placement for better visibility

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **UI Pattern**: Single-page application with scenario-based interaction buttons
- **State Management**: Streamlit session state for maintaining user history and alert logs across interactions
- **Component Structure**: 
  - Scenario selection buttons (Left Turn, Distracted Driver, Rainy Weather, Pedestrian Crossing, Drowsy Driver)
  - Real-time alert display area
  - Scenario history log (last 5 alerts)
  - Audio replay functionality

### Backend Architecture
- **Language**: Python 3.x
- **AI Integration**: OpenAI API (GPT-5 model as of August 2025)
- **Audio Generation**: pyttsx3 library for text-to-speech conversion with threading support for non-blocking audio playback
- **Session Management**: In-memory Python dictionaries for tracking scenario history and alert patterns
- **Adaptive Logic**: 
  - Frequency tracking: Monitors how often each scenario is triggered
  - Progressive escalation: Adjusts alert severity and tone based on repetition with the following mapping:
    - 1st occurrence: Calm tone with green indicator (🟢)
    - 2nd occurrence: Moderate tone with yellow indicator (🟡)
    - 3rd occurrence: Firm tone with orange indicator (🟠)
    - 4th+ occurrences: Critical tone with red indicator (🔴)
  - Context awareness: Generates unique, varied alerts to prevent habituation
  - Implementation: Count is incremented BEFORE alert generation to ensure correct urgency level is used in both UI and AI prompts

### Data Storage Solutions
- **Storage Method**: In-memory session state (no persistent database)
- **Data Structures**:
  - `scenario_history`: Dictionary tracking count and details of each triggered scenario
  - `alert_log`: List storing the most recent alerts (limited to last 5)
  - `current_alert`: Current active alert message
- **Rationale**: Lightweight, fast access for real-time adaptation without database overhead. Suitable for demonstration and testing purposes where persistence across sessions is not required.

### Authentication and Authorization
- **Current Implementation**: None - public access application
- **API Security**: OpenAI API key stored in environment variables (`OPENAI_API_KEY`)

### Design Patterns
- **Stateful Session Pattern**: Uses Streamlit's session state to maintain conversation context and behavior history
- **Prompt Engineering**: Dynamic prompt generation that incorporates historical context to produce adaptive responses
- **Progressive Enhancement**: Alert escalation system that modifies tone and urgency based on repetition frequency
- **Non-blocking I/O**: Threading for audio playback to prevent UI freezing during text-to-speech operations

## External Dependencies

### Third-Party APIs
- **OpenAI API**: 
  - Purpose: Generative AI for creating context-aware, adaptive driving safety alerts
  - Model: GPT-5 (latest as of August 2025)
  - Integration: Python `openai` client library
  - Authentication: API key via environment variable

### Python Libraries
- **streamlit**: Web framework for building interactive data applications
- **openai**: Official OpenAI Python client for GPT API access
- **pyttsx3**: Offline text-to-speech conversion library
- **threading**: Standard library for concurrent audio playback

### Environment Configuration
- **Required Environment Variables**:
  - `OPENAI_API_KEY`: Authentication token for OpenAI API access
- **Deployment**: Configured for Replit environment with Streamlit deployment

### Alternative Considerations
- **Text-to-Speech**: pyttsx3 chosen for offline capability; gTTS was considered but requires internet connectivity for each conversion
- **State Persistence**: In-memory storage chosen for speed and simplicity; JSON file storage or database could be added for cross-session persistence if needed