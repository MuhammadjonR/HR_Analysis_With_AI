import json
from langchain_ollama import ChatOllama

class RecruitmentAgent:
    def __init__(self, retriever):
        self.llm = ChatOllama(model="llama3", temperature=0.1, format="json")
        self.retriever = retriever

    def analyze(self, job_description):
        relevant_docs = self.retriever.invoke(job_description)
        
        grouped_docs = {}
        for doc in relevant_docs:
            source_file = doc.metadata.get('source', 'Unknown').split('/')[-1]
            if source_file not in grouped_docs:
                grouped_docs[source_file] = []
            grouped_docs[source_file].append(doc.page_content)

        structured_results = []
        
        for source_file, contents in grouped_docs.items():
            full_cv_text = "\n---\n".join(contents)
            prompt = f"""
        You are a Senior Technical Recruiter. Analyze the CV against the Job Description.
        
        # ... (Oldingi Scoring qismlari qolsin) ...

        EMAIL RULES:
        - The 'interview_email' MUST be a complete, ready-to-send professional email.
        - Include: Subject line, Greeting, 2-3 paragraphs about why they were selected, the specific roles/skills that impressed us, and a call to action for an interview.
        - Tone: Professional, encouraging, and specific to the candidate's CV.
        - MUST end with 'Best Regards, HR Team'.

        JD: {job_description}
        CV CONTENT: {full_cv_text}

        JSON STRUCTURE:
        {{
            "candidate_name": "Full Name",
            "overall_score": 0.0,
            "metrics": {{
                "Technical": 0.0,
                "Experience": 0.0,
                "Soft Skills": 0.0,
                "Education": 0.0
            }},
            "matching_skills": ["skill1", "skill2"],
            "missing_skills": ["skill3"],
            "summary": "Deep technical critique.",
            "interview_questions": ["Q1", "Q2", "Q3"],
            "interview_email": "Subject: Invitation to Technical Interview - [Company Name]\\n\\nDear [Name],\\n\\nI am writing to you regarding your impressive background in [Specific Skill from CV]. After reviewing your experience with [Project from CV], we believe you would be a great fit for our team... [Ensure this is a full 150-200 word email]\\n\\nBest Regards,\\nHR Team"
        }}
        """
          
            try:
                response = self.llm.invoke(prompt)
                data = json.loads(response.content)
                data["source_filename"] = source_file 
                structured_results.append(data)
            except Exception as e:
                print(f"Error processing {source_file}: {e}")
                continue
                
        return structured_results