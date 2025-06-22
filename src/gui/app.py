import streamlit as st
import base64
from newsletter_gen.crew import NewsletterGenCrew


class NewsletterGenUI:
    def load_html_template(self):
        with open("src/newsletter_gen/config/newsletter_template.html", "r") as file:
            html_template = file.read()
        return html_template

    def generate_newsletter(self, topic, personal_message):
        inputs = {
            "topic": topic,
            "personal_message": personal_message,
            "html_template": self.load_html_template(),
        }
        return NewsletterGenCrew().crew().kickoff(inputs=inputs)

    def set_custom_css(self):
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1E3A8A;
                margin-bottom: 1rem;
                text-align: center;
            }
            .sub-header {
                font-size: 1.5rem;
                color: #3B82F6;
                margin-bottom: 1rem;
            }
            .card {
                background-color: #F9FAFB;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .success-message {
                background-color: #D1FAE5;
                color: #065F46;
                padding: 15px;
                border-radius: 5px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .info-box {
                background-color: #E0F2FE;
                border-left: 4px solid #0EA5E9;
                padding: 15px;
                margin-bottom: 20px;
            }
            .download-button {
                background-color: #2563EB;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-align: center;
                margin-top: 10px;
                cursor: pointer;
            }
            .preview-container {
                border: 1px solid #E5E7EB;
                border-radius: 5px;
                padding: 10px;
                max-height: 400px;
                overflow-y: auto;
                margin-top: 20px;
                background-color: white;
            }
            .stButton>button {
                background-color: #1E40AF;
                color: white;
                font-weight: bold;
                width: 100%;
            }
            .stTextInput>div>div>input, .stTextArea>div>div>textarea {
                border-radius: 5px;
                border: 1px solid #D1D5DB;
            }
            [data-testid="stSidebar"] {
                background-color: #F3F4F6;
            }
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
                font-size: 1rem;
                line-height: 1.5;
            }
            [data-testid="stSidebar"] h1 {
                color: #1E3A8A;
            }
        </style>
        """, unsafe_allow_html=True)

    def newsletter_generation(self):
        if st.session_state.generating:
            with st.spinner("🔍 AI agents are working on your newsletter..."):
                st.session_state.newsletter = self.generate_newsletter(
                    st.session_state.topic, st.session_state.personal_message
                )

        if st.session_state.newsletter and st.session_state.newsletter != "":
            st.markdown('<div class="success-message">✅ Newsletter generated successfully!</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.download_button(
                    label="📥 Download Newsletter HTML",
                    data=st.session_state.newsletter,
                    file_name="newsletter.html",
                    mime="text/html",
                    use_container_width=True,
                )
            
            with col2:
                if st.button("🔄 Create New Newsletter", use_container_width=True):
                    st.session_state.newsletter = ""
                    st.session_state.generating = False
                    st.rerun()
            
            st.markdown('<div class="sub-header">Newsletter Preview</div>', unsafe_allow_html=True)
            
            # Display newsletter preview
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.components.v1.html(st.session_state.newsletter, height=500, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.session_state.generating = False

    def display_main_content(self):
        st.markdown('<div class="main-header">✨ AI Newsletter Generator</div>', unsafe_allow_html=True)
        
        if not st.session_state.newsletter:
            st.markdown("""
            <div class="info-box">
                <p><strong>👋 Welcome to the AI Newsletter Generator!</strong></p>
                <p>Create professional newsletters in seconds with the help of AI. Simply enter your topic and personal message in the sidebar to get started.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('#### How It Works')
                st.markdown("""
                1. **Enter a topic** in the sidebar
                2. **Add a personal message** for your readers
                3. **Click Generate** and let our AI team work
                4. **Preview and download** your newsletter
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('#### Features')
                st.markdown("""
                - **Professionally designed** newsletter templates
                - **Up-to-date content** from AI research
                - **Customizable format** for your audience
                - **Ready to share** HTML format
                """)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Example topics for inspiration
            st.markdown('<div class="sub-header">Need inspiration?</div>', unsafe_allow_html=True)
            topic_cols = st.columns(3)
            
            topics = [
                "Tech Industry Trends", 
                "Financial Markets Update", 
                "Health and Wellness Tips",
                "Environmental News", 
                "Business Leadership", 
                "Marketing Strategies"
            ]
            
            for i, topic in enumerate(topics):
                with topic_cols[i % 3]:
                    if st.button(f"📌 {topic}", key=f"topic_{i}", use_container_width=True):
                        st.session_state.topic = topic
                        st.rerun()

    def sidebar(self):
        with st.sidebar:
            st.title("📝 Newsletter Creator")
            
            st.markdown("""
            <div style="margin-bottom: 20px;">
            Create professional newsletters with the power of AI. Fill out the form below to get started.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 1. Choose Your Topic")
            st.text_input(
                "What would you like your newsletter to be about?",
                key="topic", 
                placeholder="E.g., Technology Trends, Stock Market, Health Tips",
                help="Be specific for better results"
            )
            
            st.markdown("### 2. Add Your Personal Touch")
            st.text_area(
                "Your personal message to readers",
                key="personal_message",
                placeholder="Dear subscribers, excited to share this week's insights...",
                help="This will appear at the top of your newsletter",
                height=150
            )
            
            st.markdown("---")
            
            generate_button = st.button(
                "🚀 Generate My Newsletter",
                disabled=not (st.session_state.topic and st.session_state.personal_message),
                use_container_width=True
            )
            
            if generate_button:
                st.session_state.generating = True
            
            if not (st.session_state.topic and st.session_state.personal_message):
                st.info("Please fill out both fields to generate your newsletter")

    def render(self):
        st.set_page_config(
            page_title="AI Newsletter Generator",
            page_icon="📧",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        self.set_custom_css()

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "newsletter" not in st.session_state:
            st.session_state.newsletter = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()
        self.display_main_content()
        self.newsletter_generation()


if __name__ == "__main__":
    NewsletterGenUI().render()
