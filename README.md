🛡️ Climate Disaster Forecasting: 
Climate Intelligence PlatformDisasterGuard AI is a real-time, hybrid intelligence system designed to forecast climate disasters across the Indian subcontinent. It bridges the gap between raw meteorological data and actionable civil safety insights by combining deterministic risk logic with generative AI strategies.

🚀 Project OverviewTraditional weather apps provide numbers (e.g., "60mm rain"). DisasterGuard AI provides intelligence (e.g., "High Flood Risk: Evacuate low-lying areas").
The platform performs three critical functions:
1. Situational Awareness: Visualizes live active fires (NASA FIRMS) and global disaster alerts (GDACS) on an interactive map.
2. Hyper-Local Risk Assessment: Allows users to click any coordinate in India to run a real-time risk check based on current and forecasted weather.
3. AI Strategic Briefing: Uses Large Language Models (LLMs) to generate a "News Anchor" style report with specific instructions for civilians and emergency teams.

🏗️ Architecture & Tech StackThe project is built on a modular Python architecture.


⚡ Key Features1.
1. The Hybrid Risk Engine (risk_model.py)
We do not rely solely on AI hallucinations. We use a Deterministic Logic Layer based on official thresholds (IMD/WMO) as a failsafe:
🔴 Cyclone Logic: Triggers if Wind Speed > 89 km/h.
🌊 Flood Logic: Triggers if (Rain > 50mm AND Soil Moisture > 0.4) OR (Future Rain > 100mm).
🔥 Heatwave Logic: Triggers if Temperature > 45°C.2.
2. The "Self-Healing" AI Agent (ai_agent.py)The system connects to Gemini for summarizing the analysis of a particular place.
Note: It automatically cleans "thinking" tags from reasoning models.

📂 Project StructurebashDisasterGuard
├── app.py               # The Main Dashboard (Frontend UI)
├── data_manager.py      # Backend: Fetches Weather, NASA Fire, and GDACS data
├── risk_model.py        # Logic: Mathematical rules for disaster classification
├── ai_agent.py          # AI: LLM connection and prompt engineering
└── requirements.txt     # Dependency list
---

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.8 or higher installed.
*   An API Key from(https://openrouter.ai/) (Free).

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/disaster-guard-ai.git](https://github.com/YOUR_USERNAME/disaster-guard-ai.git)
cd disaster-guard-ai
Step 2: Install DependenciesBashpip install -r requirements.txt
Step 3: Configure API KeyOpen ai_agent.py and paste your GEMINI API Key: ''
Step 4: Run the AppBashstreamlit run app.py
```
🔮 Future Roadmap"Am I Safe?" Radius Check: Calculate distance from user location to the nearest active disaster (GDACS).Live News Ticker: Integrate NewsAPI to show scrolling headlines for "India Floods" or "Cyclone Alert".
