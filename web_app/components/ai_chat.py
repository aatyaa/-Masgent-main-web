# web_app/components/ai_chat.py
"""
AI Chat component for Masgent Web Application.
Implements the 2-Phase Protocol (Plan -> Execute) with streaming support.
"""
import streamlit as st
import os
import asyncio
from typing import List, Dict, Any


def check_gemini_key() -> bool:
    """Check if Gemini API key is configured."""
    return bool(os.environ.get("GEMINI_API_KEY"))


def init_chat_history():
    """Initialize chat history in session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_plan" not in st.session_state:
        st.session_state.pending_plan = None
    if "ai_agent" not in st.session_state:
        st.session_state.ai_agent = None


def display_chat_history():
    """Display the chat message history."""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="⚛️"):
                st.markdown(content)
        elif role == "plan":
            with st.chat_message("assistant", avatar="📋"):
                st.markdown("**Proposed Plan:**")
                st.markdown(content)
        elif role == "result":
            with st.chat_message("assistant", avatar="✅"):
                st.markdown("**Execution Result:**")
                st.markdown(content)


def get_ai_response(user_input: str) -> str:
    """
    Get AI response using the Masgent AI backend.
    This is a simplified version - for full streaming, would need async integration.
    """
    try:
        from pydantic_ai.models.gemini import GeminiModel
        from pydantic_ai import Agent
        
        # Import tools from masgent
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
        
        from masgent import tools
        from masgent.utils.utils import load_system_prompts
        
        # Create agent if not exists
        if st.session_state.ai_agent is None:
            model = GeminiModel(model_name='gemini-2.5-flash')
            system_prompt = load_system_prompts()
            
            st.session_state.ai_agent = Agent(
                model=model,
                system_prompt=system_prompt,
                tools=[
                    tools.list_files,
                    tools.generate_vasp_poscar,
                    tools.generate_vasp_inputs_from_poscar,
                    tools.run_simulation_using_mlps,
                    # Add more tools as needed
                ],
            )
        
        agent = st.session_state.ai_agent
        
        # Wrap input with planning instruction
        wrapped_input = f'Request/Confirmation: {user_input} (If this is a Request: ALWAYS output a workflow plan with chosen tools and required parameters FIRST and ask for confirmation; if this is a Confirmation: ignore the instruction above.)'
        
        # Fix for Streamlit event loop issue
        import nest_asyncio
        nest_asyncio.apply()
        
        # Run synchronously
        result = asyncio.run(agent.run(wrapped_input))
        
        return result.output
        
    except Exception as e:
        return f"Error: {str(e)}"


def render_ai_chat():
    """Render the AI chat interface."""
    st.header("🤖 AI Simulation Agent")
    
    # Check API key
    if not check_gemini_key():
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to use the AI Agent.")
        st.info("""
        **How to get a Gemini API key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the key
        5. Paste it in the sidebar
        """)
        return
    
    # Initialize
    init_chat_history()
    
    # Display instructions
    with st.expander("ℹ️ How to use the AI Agent", expanded=False):
        st.markdown("""
        **The AI Agent follows a 2-Phase Protocol:**
        
        1. **Phase I - Planning:** Describe what you want to do, and the AI will propose a plan.
        2. **Phase II - Execution:** Confirm the plan to execute it.
        
        **Example prompts:**
        - "Generate a POSCAR file for NaCl"
        - "Prepare VASP input files for a graphene structure"
        - "Run an EOS calculation for Silicon using CHGNet"
        - "Create a 2x2x2 supercell of the current POSCAR"
        """)
    
    st.divider()
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        display_chat_history()
    
    # Pending plan confirmation
    if st.session_state.pending_plan:
        st.divider()
        st.markdown("### 📋 Pending Plan")
        st.info(st.session_state.pending_plan)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm & Execute", use_container_width=True, type="primary"):
                # Add confirmation to messages
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Confirmed. Please execute the plan."
                })
                
                # Get execution result
                with st.spinner("🔄 Executing plan..."):
                    result = get_ai_response("Confirmed. Execute the plan now.")
                
                st.session_state.messages.append({
                    "role": "result",
                    "content": result
                })
                
                st.session_state.pending_plan = None
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel Plan", use_container_width=True):
                st.session_state.pending_plan = None
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Plan cancelled. How else can I help you?"
                })
                st.rerun()
    
    # Chat input
    st.divider()
    user_input = st.chat_input("Ask the AI Agent anything about materials simulation...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        with st.spinner("🧠 Thinking..."):
            response = get_ai_response(user_input)
        
        # Check if response is a plan (contains confirmation request)
        if any(keyword in response.lower() for keyword in ['confirm', 'proceed', 'execute', 'plan']):
            st.session_state.messages.append({
                "role": "plan",
                "content": response
            })
            st.session_state.pending_plan = response
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
        
        st.rerun()
    
    # Clear chat button
    if st.session_state.messages:
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.pending_plan = None
            st.rerun()
