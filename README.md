
# 📖 AI-Agents-Trip-Planner

![](output.png)

## 📌 Overview
This project combines the power of **AI agents** and the **CrewAI** framework to create a personalized travel assistant. The backend utilizes multiple AI agents, including a city selection expert, local guide, travel planner, and budget manager, to generate a comprehensive travel plan. The frontend, powered by **Streamlit**, allows users to input their travel preferences and interact with the AI-powered trip planning system.

## ✨ Features
- **City Selection Expert**: Recommends the best cities based on user interests, travel type, and season.
- **Local Destination Expert**: Provides detailed insights about selected cities, including attractions, cuisine, and hidden gems.
- **Professional Travel Planner**: Creates a well-paced, personalized itinerary for your trip.
- **Travel Budget Manager**: Prepares a realistic and itemized budget breakdown based on user inputs.
- **Interactive User Interface**: Streamlit frontend to enter preferences and view results.

## 🛠️ Tech Stack
- **Backend**: 
  - **Python** 3.11
  - **CrewAI** for AI agents and task management
  - **Google Gemini API** (for AI-powered insights)
  - **python-dotenv** (for environment variable management)
  
- **Frontend**:
  - **Streamlit** (for interactive user interface)


## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/PriyanshuDey23/AI-Agents-Trip-Planner.git
cd <repo-directory>

# Install dependencies
pip install -r requirements.txt

# Set up your .env file with your API key
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 How It Works
1. **Agents** are created through the `TripAgents` class, each initialized with a clear role, goal, and backstory.
2. **Tasks** are defined in the `TripTasks` class, specifying task descriptions, expected outputs, and assigned agents.
3. The `TripCrew` class coordinates the process:
   - Initializes agents and tasks.
   - Runs the `Crew` with its agents and tasks.
   - Collects structured results for each step of the trip planning workflow.

## 📑 Code Structure
```
├── trip_planner.py  # Main code with classes for agents, tasks, and crew coordination
├── app.py           # Frontend part 
├── .env             # Environment variables (API keys, etc.)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## 📊 Example Inputs
```python
inputs = {
    'travel_type': 'Leisure',
    'interests': ['culture', 'food', 'nature'],
    'season': 'Summer',
    'duration': 5,
    'budget': 'mid-range'
}
```

## 📝 Example Output
- Recommended cities with rationale
- Detailed city research report
- Day-by-day itinerary with activities and dining options
- Itemized budget plan



## 📬 Contact
For questions, feel free to reach out via [your email/contact link].

---


