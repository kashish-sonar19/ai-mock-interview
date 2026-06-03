#  AI Mock Interview Project Assistant

An intelligent, AI-driven application designed to simulate real-world technical and HR interviews, providing users with dynamic questions and instant, actionable feedback to enhance their interview readiness.

 **Live Demo:** [Click here to practice your interview live on AWS](http://13.234.59.65:8501)

##  Tech Stack
* **Frontend:** Streamlit
* **Backend:** Python
* **AI Engine:** Generative AI (Google Gemini)
* **DevOps & Cloud:** Docker, Docker Compose, AWS EC2

##  Key Features
* **Role-Specific Simulation:** Generates highly relevant interview questions based on the target job role and experience level.
* **Real-Time AI Feedback:** Evaluates user responses instantly, highlighting strengths and areas for improvement.
* **Interactive UI:** Clean, distraction-free interface built with Streamlit for a seamless practice experience.
* **Cloud Deployed:** Fully containerized with Docker and hosted securely on an AWS EC2 instance.

##  Local Setup
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/kashish-sonar19/ai-mock-interview.
   
2. Add your `.env` file with `GEMINI_API_KEY`.
    GEMINI_API_KEY = your_api_key_here

3. Run `docker compose up --build -d`.
    docker compose up --build -d

4. Access the app locally at http://13.234.59.65:8501.
