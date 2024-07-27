import streamlit as st
import time
from agents.research_agent import research_agent
from agents.news_curator_agent import news_curator_agent
from agents.post_writer_agent import post_writer_agent
from agents.editor_agent import editor_agent
from state_manager import update_session_state

def generate_post():
    if st.session_state.topic:
        if 'research_results' not in st.session_state:
            st.info("Researching and curating content... This may take a moment.")

            # Research step
            start_time = time.time()
            with st.spinner("Researching topic..."):
                research_results = research_agent({"messages": [{"content": st.session_state.topic}]}, model=st.session_state.model)
            st.session_state.research_time = time.time() - start_time
            st.text(f"Research completed in {st.session_state.research_time:.2f} seconds")

            # News Curation step
            start_time = time.time()
            with st.spinner("Curating and analyzing news..."):
                curated_results = news_curator_agent(research_results, model=st.session_state.model, use_groq=st.session_state.use_groq)
            st.session_state.curation_time = time.time() - start_time
            st.text(f"News curated and analyzed in {st.session_state.curation_time:.2f} seconds")    
            update_session_state('curated_news', curated_results['content'])
            update_session_state('research_results', research_results)
            update_session_state('show_personalization', True)
            st.experimental_rerun()

        if st.session_state.get('show_personalization', False):
            # Personalization inputs are handled in the UI component

            if st.button("Generate Personalized Post", key="generate_personalized_post"):
                # Writing step
                start_time = time.time()
                with st.spinner("Writing post..."):
                    post_result = post_writer_agent(
                        {
                            "messages": [{"content": st.session_state.curated_news}],
                            "tone": st.session_state.tone if st.session_state.tone else st.session_state.tone,
                            "author": st.session_state.author,
                            "audience": st.session_state.audience
                        },
                        model=st.session_state.model,
                        use_groq=st.session_state.use_groq
                    )
                st.session_state.writing_time = time.time() - start_time
                st.text(f"Post written in {st.session_state.writing_time:.2f} seconds")

                # Editing step
                start_time = time.time()
                with st.spinner("Editing and optimizing post for LinkedIn..."):
                    edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
                st.session_state.editing_time = time.time() - start_time
                st.text(f"Post edited and optimized in {st.session_state.editing_time:.2f} seconds")

                # Store the original post content
                update_session_state('original_post', edited_result['content'])
                update_session_state('generated_post', edited_result['content'])
                update_session_state('rewritten_post', None)  # Reset rewritten post
            
                st.success("Post generated successfully!")
                update_session_state('post_generated', True)
                update_session_state('show_personalization', False)  # Hide personalization after generating
                st.experimental_rerun()

    else:
        st.warning("Please enter a topic before generating a post.")

def rewrite_post(feedback=""):
    if st.session_state.curated_news:
        st.info("Rewriting post... This may take a moment.")

        # Update the query with feedback
        updated_query = f"{st.session_state.topic} FEEDBACK: {feedback}" if feedback else st.session_state.topic

        # Writing step
        start_time = time.time()
        with st.spinner("Writing post..."):
            post_result = post_writer_agent(
                {
                    "messages": [{"content": st.session_state.curated_news}, {"content": updated_query}],
                    "tone": st.session_state.tone,
                    "author": st.session_state.author,
                    "audience": st.session_state.audience,
                    "feedback": feedback
                },
                model=st.session_state.model,
                use_groq=st.session_state.use_groq
            )
        st.session_state.writing_time = time.time() - start_time
        st.text(f"Post rewritten in {st.session_state.writing_time:.2f} seconds")

        # Editing step
        start_time = time.time()
        with st.spinner("Editing and optimizing post for LinkedIn..."):
            edited_result = editor_agent({"messages": [{"content": post_result['content']}]}, model=st.session_state.model, use_groq=st.session_state.use_groq)
        st.session_state.editing_time = time.time() - start_time
        st.text(f"Post edited and optimized in {st.session_state.editing_time:.2f} seconds")
       
        # Store the rewritten post content
        update_session_state('rewritten_post', edited_result['content'])
        
        st.success("Post rewritten successfully!")
        update_session_state('post_generated', True)
        st.experimental_rerun()
    else:
        st.error("No curated news available. Please generate a post first.")