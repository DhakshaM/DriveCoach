LLM-powered driving behavior analysis using sensor data.

# DriveCoach AI

### AI-Driven Coaching for Enhanced Road Safety

DriveCoach AI is a real-time intelligent driving behavior monitoring platform designed to enhance road safety through AI-powered coaching insights. The system analyzes driving trip segments, classifies behavioral severity levels, and generates actionable recommendations using a Large Language Model (LLM).

The platform supports role-based access for Drivers and Coaches, enabling structured performance monitoring, real-time corrective feedback, and long-term behavioral improvement.







## 1. Overview

DriveCoach AI integrates:

* Real-time trip data streaming
* Segment-level behavioral analysis
* Automated severity classification
* AI-generated coaching recommendations
* Thread-safe background processing
* Role-based dashboards

**Objective:**
To proactively reduce unsafe driving behavior by delivering real-time corrective feedback to drivers while equipping coaches with structured performance insights.






## 2. Key Features

### Authentication and Role Management

* Secure login workflow
* Role-based dashboard routing (Driver / Coach)
* Centralized session state management

### Driver Dashboard

* Start and stop trip streaming
* Real-time segment progression
* Automatic severity detection
* AI-generated coaching feedback per segment
* Audio and visual alerts for high-risk behavior
* Background LLM pre-fetching for seamless transitions

### Coach Dashboard

* Review trip segments
* Analyze severity trends
* Monitor driver performance history
* Access structured AI-generated insights

### AI Feedback Engine

* Segment-wise summary generation
* Context-aware coaching recommendations
* Severity-adaptive response tuning
* Non-blocking threaded execution
* Lock-based concurrency control




## 3. Technical Design Considerations

### Concurrency Handling

* Non-blocking lock mechanism ensures controlled LLM access
* try/finally pattern guarantees lock release
* Daemon threads prevent UI freezing

### State Management

* UI-level state handled via global_State
* Critical results stored in module-level dictionaries to prevent state duplication
* Global session state maintained for authenticated users

### Alert System

High and critical severity levels trigger:

* Programmatic audio alerts using Web Audio API
* Temporary floating visual notifications
* Automatic dismissal for non-intrusive user experience

### Performance Optimization

* LLM initialized once at application startup
* Segment lookahead pre-fetching
* Background processing for improved responsiveness




## File Structure:
```
driving-coach-app/
│
├── README.md
├── .env.example
├── .gitignore
│
└── app/
    │
    ├── main.py                         
    ├── requirements.txt
    │
    ├── backend/
    │   │
    │   ├── auth/
    │   │   ├── auth_service.py         # Prompting + inference wrapper
    │   │   ├── seed_users.py           # Create users
    │   │   └── user_registry.py        # Empty file
    │   │
    │   ├── llm/
    │   │   ├── llm_engine.py          # Prompting + inference wrapper
    │   │   ├── load_llm.py            # Loads GGUF model once
    │   │   └── driving-coach-f16.gguf # (optional, large file – gitignored)
    │   │
    |   ├── processing/
    |   |   ├── merger.py              # CSV Merger merging and segment extraction
    │   │   └── severity.py            # Severity labels for Sensor Summary
    |   |
    │   ├── registry/
    │   │   └── trip_registry.py       # Trip + segment processing logic
    │   │
    │   ├── services/
    │   │   ├── driver_services.py     # Driver-facing operations
    │   │   └── coach_services.py      # Coach/fleet-facing operations
    │   │   
    │   └── state/
    │       └── global_state.py        # Logged-in users & online status
    │  
    │
    ├── ui/
    │   │
    │   ├── gradio_app.py              # App layout + routing
    │   ├── login_view.py              # Login UI
    │   ├── driver_view.py             # Driver dashboard UI
    │   └── coach_view.py              # Coach dashboard UI
    │   
    │
    └── data/
        │
        ├── users.csv                  # Seed users (auth)
        │
        └── trips/
            │
            ├── driver_01/
            │   ├── trip_001/
            │   |   ├── location_data.csv
            │   |   ├── accelerometer_data.csv
            │   |   └── gyroscope_data.csv
            |   |
            │   └── trip_002/
            │       ├── location_data.csv
            │       ├── accelerometer_data.csv
            │       └── gyroscope_data.csv   
            │
            ├── driver_02/
            │   └── trip_001/
            │       └── ...
            │
            └── ...
```

## Requirements:
Python 3.10+

pip (pip install -r requirements.txt)

8GB+ RAM recommended

Local GGUF model (not included) - https://www.kaggle.com/datasets/amudhans07/finetuning-toolkit
