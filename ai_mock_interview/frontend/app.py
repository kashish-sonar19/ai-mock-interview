import streamlit as st
import requests
import time

st.title("AI Mock Interview Assistant")

role = st.selectbox("Select Role", ["python", "backend", "data_analyst", "frontend", "devops", "full_stack", "java_developer"])

# store question globally
if "question" not in st.session_state:
    st.session_state.question = ""

# GET QUESTION
if st.button("Get Question"):
    # Tumhare requirement ke hisaab se exact text
    with st.spinner("Fetching question... Please wait."):
        
        # Artificial delay taaki spinner kam se kam 1 second ke liye dikhe
        time.sleep(1) 
        
        # DHYAN RAHE: Agar tum bina Docker ke run kar rahe ho, 
        # toh URL 'http://127.0.0.1:8000/question/' hona chahiye
        res = requests.get(f"http://backend:8000/question/{role}")
        
        if res.status_code == 200:
            data = res.json()
            st.session_state.question = data["question"]
            
            # Agar tum chaho toh dekh sakte ho ki question kahan se aaya
            if data.get("source") == "Local Backup":
                st.info("Showing backup question (AI is currently busy).")
                
            st.rerun()
        else:
            try:
                error_data = res.json()
                st.error(f"Backend Error: {error_data.get('detail', 'Unknown error')}")
            except Exception:
                st.error(f"Failed to connect. Status Code: {res.status_code}")

# SHOW QUESTION
if st.session_state.question:
    st.subheader("Question")
    st.write(st.session_state.question)

    answer = st.text_area("Your Answer")

    submit = st.button("Submit Answer")

    if submit:
        if answer.strip() == "":
            st.warning("Please write an answer first!")
        else:
            # NAYA CODE: Ab hum answer actually backend ko bhej rahe hain
            payload = {
                "role": role,
                "question": st.session_state.question,
                "answer": answer
            }
            
            try:
                # POST request (Data bhejna)
                response = requests.post("http://backend:8000/submit", json=payload)
                
                # Agar backend ne '200 OK' bheja, matlab sab sahi hai
                # Agar backend ne '200 OK' bheja, matlab sab sahi hai
                if response.status_code == 200:
                    st.success("Great! Your answer has been submitted successfully.")
                    
                    # Submission details ko clean text format mein dikhana
                    st.markdown("### 📝 Submission Summary")
                    st.write(f"**Role:** {role.replace('_', ' ').title()}")
                    st.write(f"**Question:** {st.session_state.question}")
                    st.info(f"**Your Answer:** {answer}")
                    
                # Agar 422 aaya, matlab Pydantic bouncer ne rok diya (Validation Error)
                elif response.status_code == 422:
                    st.error("Validation Error: Answer is too short! Please write at least 10 characters.")
                    
                else:
                    st.error(f"Something went wrong: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Is your FastAPI server running?")