import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from pypdf import PdfReader
import matplotlib.pyplot as plt
import re
import json

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenRouter credentials from .env
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not openrouter_api_key:
    st.error("❌ Missing OPENROUTER_API_KEY in .env file. Please check your .env file.")
    st.stop()

# Initialize LLM using CrewAI's LLM wrapper (compatible with LiteLLM)
llm = LLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=openrouter_api_key,
    base_url=openrouter_base_url,
    temperature=0.7
)

# Initialize embeddings via OpenRouter
embeddings = OpenAIEmbeddings(
    openai_api_base=openrouter_base_url,
    openai_api_key=openrouter_api_key,
    model="openai/text-embedding-ada-002"
)


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


# Function to parse skills from AI output
def parse_skills_from_text(text):
    """Extract skills from AI-generated text, handling various formats"""
    skills = []

    # Try to find JSON array format
    json_match = re.search(r'\[([^\]]+)\]', text)
    if json_match:
        try:
            # Try parsing as JSON
            skills_text = '[' + json_match.group(1) + ']'
            skills = json.loads(skills_text.replace("'", '"'))
            return [s.strip() for s in skills if s.strip()]
        except:
            pass

    # Try to find bullet points or numbered lists
    lines = text.split('\n')
    for line in lines:
        # Match patterns like: - Skill, * Skill, 1. Skill, • Skill
        match = re.match(r'^[\s\-\*\d\.\•]+(.+?)(?:,|$)', line.strip())
        if match:
            skill = match.group(1).strip()
            if skill and len(skill) > 2 and len(skill) < 100:
                skills.append(skill)

    # If still no skills found, try splitting by common delimiters
    if not skills:
        for delimiter in [',', ';', '\n']:
            if delimiter in text:
                potential_skills = [s.strip() for s in text.split(delimiter)]
                skills = [s for s in potential_skills if s and 3 < len(s) < 100]
                if skills:
                    break

    return skills[:20]  # Limit to 20 skills


# Streamlit UI Setup
st.set_page_config(page_title="Skill Gap Analyzer", page_icon="📈", layout="wide")
st.title("🚀 Intelligent Skill Gap Analyzer")
st.markdown(
    "Analyze your resume against a job description to identify gaps and get a personalized learning roadmap. Uses Mistral-7B-Instruct (free) via OpenRouter API.")

# Sidebar for Inputs
with st.sidebar:
    st.header("📝 Input Your Details")
    resume_input = st.text_area("Paste your resume text here:", height=150)
    resume_pdf = st.file_uploader("Or upload resume PDF:", type="pdf")
    job_description = st.text_area("Paste the job description here:", height=150)
    analyze_button = st.button("🔍 Analyze Skills", type="primary")
    reset_button = st.button("🔄 Reset")

if reset_button:
    st.rerun()

if analyze_button:
    if not resume_input and not resume_pdf:
        st.error("❌ Please provide a resume (text or PDF).")
        st.stop()
    if not job_description:
        st.error("❌ Please provide a job description.")
        st.stop()

    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.text("Extracting resume text...")

    # Extract resume text
    if resume_pdf:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume_pdf.read())
            resume_text = extract_text_from_pdf(tmp.name)
            os.unlink(tmp.name)
    else:
        resume_text = resume_input

    progress_bar.progress(20)
    status_text.text("Setting up AI agents...")

    # Agent Setup with CrewAI
    resume_analyzer = Agent(
        role="Resume Analyzer",
        goal="Extract and list all skills, technologies, tools, and competencies from resumes.",
        backstory="You are an expert at identifying skills from resumes. You extract technical skills, soft skills, tools, programming languages, frameworks, and methodologies.",
        llm=llm,
        verbose=True
    )

    job_agent = Agent(
        role="Job Requirement Analyst",
        goal="Extract and list all required skills, qualifications, and competencies from job descriptions.",
        backstory="You specialize in analyzing job postings to identify required technical skills, soft skills, tools, and qualifications.",
        llm=llm,
        verbose=True
    )

    skill_gap_agent = Agent(
        role="Career Development Advisor",
        goal="Compare candidate skills with job requirements and create personalized learning plans.",
        backstory="You are a career advisor who helps professionals identify skill gaps and recommends specific learning resources, courses, and certifications.",
        llm=llm,
        verbose=True
    )

    # Tasks with clearer instructions
    task_resume = Task(
        description=f"""Analyze this resume and extract ALL skills mentioned:

Resume:
{resume_text[:3000]}

Instructions:
1. List every technical skill, tool, programming language, framework, and soft skill
2. Return ONLY a comma-separated list of skills
3. Be specific and comprehensive
4. Example format: Python, JavaScript, Machine Learning, Team Leadership, SQL, Docker

Return only the comma-separated list, nothing else.""",
        agent=resume_analyzer,
        expected_output="Comma-separated list of skills"
    )

    task_job = Task(
        description=f"""Analyze this job description and extract ALL required skills:

Job Description:
{job_description[:3000]}

Instructions:
1. List every required technical skill, tool, technology, and qualification mentioned
2. Include both required and preferred skills
3. Return ONLY a comma-separated list of skills
4. Be specific and comprehensive
5. Example format: Machine Learning, AWS, Python, Agile, SQL, Team Leadership

Return only the comma-separated list, nothing else.""",
        agent=job_agent,
        expected_output="Comma-separated list of required skills"
    )

    task_gap = Task(
        description="""Based on the resume skills and job requirements identified:

1. Compare the two skill lists
2. Identify which job skills are missing from the resume
3. Create a detailed learning roadmap with:
   - Specific online courses (Coursera, Udemy, edX)
   - Certifications to pursue
   - Hands-on projects to build
   - Books or resources to study
   - Estimated time to acquire each skill

Format your response as a clear, actionable learning plan.""",
        agent=skill_gap_agent,
        expected_output="Detailed learning roadmap with specific recommendations",
        context=[task_resume, task_job]
    )

    # Crew Setup
    crew = Crew(
        agents=[resume_analyzer, job_agent, skill_gap_agent],
        tasks=[task_resume, task_job, task_gap],
        verbose=True
    )

    progress_bar.progress(50)
    status_text.text("Running AI analysis... (this may take 30-60 seconds)")

    # Execution
    try:
        result = crew.kickoff()

        progress_bar.progress(70)
        status_text.text("Parsing AI results...")

        # Get individual task outputs
        resume_output = str(task_resume.output)
        job_output = str(task_job.output)
        gap_output = str(task_gap.output)

        # Parse skills from outputs
        user_skills = parse_skills_from_text(resume_output)
        job_skills = parse_skills_from_text(job_output)

        # Calculate missing and matched skills
        user_skills_lower = [s.lower() for s in user_skills]
        missing_skills = []
        matched_skills = []

        for job_skill in job_skills:
            # Check if job skill or similar variant exists in user skills
            found = False
            for user_skill in user_skills_lower:
                if job_skill.lower() in user_skill or user_skill in job_skill.lower():
                    found = True
                    matched_skills.append(job_skill)
                    break
            if not found:
                missing_skills.append(job_skill)

        gap_summary = gap_output

        progress_bar.progress(90)
        status_text.text("Generating visualizations...")

        # Compute semantic similarity for better gap detection
        if user_skills and job_skills:
            try:
                splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                user_docs = splitter.create_documents([resume_text])
                job_docs = splitter.create_documents([job_description])

                vectorstore = Chroma.from_documents(user_docs + job_docs, embeddings)

                # Refine missing skills using semantic search
                refined_missing = []
                for skill in job_skills:
                    similar = vectorstore.similarity_search(skill, k=1)
                    # If similarity is low, add to missing
                    if similar and skill.lower() not in resume_text.lower():
                        refined_missing.append(skill)

                if refined_missing:
                    missing_skills = list(set(refined_missing))

                vectorstore.delete_collection()
            except Exception as e:
                st.warning(f"Semantic analysis skipped: {e}")

        progress_bar.progress(100)
        status_text.text("Analysis complete!")

        # Output Display
        st.success("✅ Analysis Complete! Scroll down for results.")

        # Display raw outputs in expanders for debugging
        with st.expander("🔍 Debug: View Raw AI Outputs", expanded=False):
            st.write("**Resume Analysis Output:**")
            st.text(resume_output[:500])
            st.write("**Job Analysis Output:**")
            st.text(job_output[:500])

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📋 Your Extracted Skills", expanded=True):
                if user_skills:
                    for skill in user_skills:
                        st.write(f"- {skill}")
                else:
                    st.warning("No skills extracted. Check debug output above.")

        with col2:
            with st.expander("🎯 Required Job Skills", expanded=True):
                if job_skills:
                    for skill in job_skills:
                        st.write(f"- {skill}")
                else:
                    st.warning("No skills extracted. Check debug output above.")

        st.divider()

        # Matched Skills Section
        with st.expander("✅ Matched Skills (Skills You Already Have)", expanded=True):
            if matched_skills:
                st.success(f"Great! You already have {len(matched_skills)} out of {len(job_skills)} required skills!")
                col1, col2 = st.columns([3, 1])
                with col1:
                    for skill in matched_skills:
                        st.write(f"✓ {skill}")
                with col2:
                    match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
                    st.metric("Match Rate", f"{match_percentage:.0f}%")
            else:
                st.info("No direct skill matches found. This might indicate a significant career transition.")

        st.divider()

        # Missing Skills Section
        with st.expander("⚠️ Skill Gaps (Missing or Weak Skills)", expanded=True):
            if missing_skills:
                st.warning(f"You need to develop {len(missing_skills)} skills to match this job fully.")
                for skill in missing_skills:
                    st.write(f"❌ {skill}")
            else:
                st.success("🎉 No major gaps detected! Your skills match the job requirements well.")

        st.divider()
        st.subheader("🛤️ Personalized Learning Roadmap")

        # Display roadmap in a nice formatted box
        st.markdown("""
        <style>
        .roadmap-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
        }
        </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="roadmap-box">', unsafe_allow_html=True)
            st.markdown(gap_summary)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Roadmap as Text",
                data=gap_summary,
                file_name="learning_roadmap.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Visualization
        st.subheader("📊 Skills Overview")
        col1, col2 = st.columns(2)

        with col1:
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            skills_data = {
                "Your Skills": len(user_skills),
                "Matched": len(matched_skills),
                "Missing": len(missing_skills)
            }
            colors = ["#2196F3", "#4CAF50", "#FF5252"]
            bars = ax1.bar(skills_data.keys(), skills_data.values(), color=colors)
            ax1.set_ylabel("Count")
            ax1.set_title("Skills Breakdown")
            ax1.grid(axis='y', alpha=0.3)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{int(height)}',
                         ha='center', va='bottom')

            st.pyplot(fig1)

        with col2:
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
            gap_percentage = 100 - match_percentage

            colors_pie = ['#4CAF50', '#FF5252']
            explode = (0.05, 0)  # Slightly separate the matched slice

            ax2.pie(
                [match_percentage, gap_percentage],
                labels=[f'Matched\n{match_percentage:.1f}%', f'Gap\n{gap_percentage:.1f}%'],
                colors=colors_pie,
                autopct='%1.1f%%',
                startangle=90,
                explode=explode,
                shadow=True
            )
            ax2.set_title("Job Requirements Match")
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ An error occurred during analysis: {e}")
        st.exception(e)
        progress_bar.empty()
        status_text.empty()

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, LangChain, ChromaDB, and Streamlit. Uses Mistral-7B-Instruct via OpenRouter API.")