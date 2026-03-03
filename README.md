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
* Role-based dashboards

**Objective:**
To proactively reduce unsafe driving behavior by delivering real-time corrective feedback to drivers while equipping coaches with structured performance insights.


## 2. Key Features

### Driver Dashboard

* Start and stop trip streaming
* Real-time segment progression
* Automatic severity detection
* AI-generated coaching feedback per segment
* Audio and visual alerts for high-risk behavior

### Coach Dashboard

* Review trip segments
* Analyze severity trends
* Monitor driver performance history
* Access structured AI-generated insights

### AI Feedback Engine

* Segment-wise summary generation
* Context-aware coaching recommendations
* Severity-adaptive response tuning


## 3. How It Works

1. **Sensor Data Processing**  
   - Inputs: location (speed/position), accelerometer (forces), gyroscope (rotations)  
   - Extracts: avg/max speed, harsh brakes/accel counts, sharp corners, bumps, jerk, yaw variance  
   - Processes full trips (daily drives) for natural context

2. **Seed & Scaled Data Creation**  
   - Rule-based grading → 1,770 high-quality seed pairs  
   - Self-instruct generation (larger LLM) → diverse scenarios  
   - Augmentation (paraphrasing + safe perturbation) → ~7,080 robust examples

3. **Fine-Tuning**  
   - Base model: Llama-3.2-1B-Instruct  
   - Low Rank Adaptation (r=64)
   - 4-bit/ 5-bit quantization    

4. **Optimization & Interface**  
   - Merge LoRA → convert to GGUF (F16) with llama.cpp  
   - Gradio UI with driver/fleet logins
   - Auto-query on driver side 




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

