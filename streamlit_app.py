#!/usr/bin/env python3
import streamlit as st
import os
import tempfile
from pathlib import Path
from file_agent import FileSystemAgent

def main():
    st.set_page_config(
        page_title="File System Analysis Agent",
        page_icon="📁",
        layout="wide"
    )
    
    st.title("📁 File System Analysis Agent")
    st.markdown("Analyze your file system using AI-powered insights")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. You can also set it as OPENAI_API_KEY environment variable."
        )
        
        # Use environment variable if not provided
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        st.markdown("---")
        st.markdown("### How to use:")
        st.markdown("1. Enter your OpenAI API key")
        st.markdown("2. Select a folder to analyze")
        st.markdown("3. Ask a question about the file system")
        st.markdown("4. View the results!")
    
    # Main content area
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
        st.info("💡 You can also set the OPENAI_API_KEY environment variable.")
        return
    
    # Folder selection
    st.header("📂 Select Folder to Analyze")
    
    folder_option = st.radio(
        "Choose how to specify the folder:",
        ["Enter path manually", "Browse files (select a file in the target folder)"],
        help="You can either type the folder path directly or browse to select a file within the target folder."
    )
    
    if folder_option == "Enter path manually":
        folder_path = st.text_input(
            "Folder Path",
            placeholder="/path/to/your/folder",
            help="Enter the full path to the folder you want to analyze"
        )
    else:
        uploaded_file = st.file_uploader(
            "Select any file in the target folder",
            type=None,
            help="Select any file within the folder you want to analyze. The folder containing this file will be analyzed."
        )
        
        if uploaded_file:
            # Get the folder path from the uploaded file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            
            # Note: This is a workaround since Streamlit doesn't provide direct folder access
            # In a real deployment, you might want to use a different approach
            st.info("ℹ️ For security reasons, Streamlit doesn't allow direct folder access. Please use the manual path option for full folder analysis.")
            folder_path = None
        else:
            folder_path = None
    
    # Question input
    st.header("❓ Ask a Question")
    
    question = st.text_area(
        "What would you like to know about the file system?",
        placeholder="e.g., What is the total size of all files? How many Python files are there? What are the largest files?",
        height=100,
        help="Ask any question about the file system structure, file types, sizes, etc."
    )
    
    # Verbose option
    verbose = st.checkbox(
        "Show detailed file system summary",
        help="Display comprehensive file system information including file types, directory structure, and largest files"
    )
    
    # Analyze button
    if st.button("🔍 Analyze File System", type="primary", disabled=not (folder_path and question)):
        if not folder_path:
            st.error("Please specify a folder path.")
            return
        
        if not question.strip():
            st.error("Please enter a question.")
            return
        
        try:
            # Initialize agent
            with st.spinner("Initializing agent..."):
                agent = FileSystemAgent(api_key)
            
            # Scan directory
            with st.spinner(f"Scanning directory: {folder_path}"):
                file_info = agent.scan_directory(folder_path)
            
            # Display results
            st.success("✅ Analysis complete!")
            
            # Show verbose summary if requested
            if verbose:
                st.header("📊 Detailed File System Summary")
                summary = agent.create_summary(file_info, folder_path)
                st.text(summary)
                st.markdown("---")
            
            # Answer the question
            st.header("🤖 AI Response")
            st.markdown(f"**Question:** {question}")
            
            with st.spinner("Generating answer..."):
                answer = agent.answer_question(question, file_info, folder_path)
            
            st.markdown("**Answer:**")
            st.write(answer)
            
            # Display some quick stats
            st.header("📈 Quick Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Files", file_info["total_files"])
            
            with col2:
                st.metric("Total Directories", file_info["total_directories"])
            
            with col3:
                total_size = sum(file_info["file_sizes"].values())
                st.metric("Total Size", agent.format_size(total_size))
            
            with col4:
                unique_types = len(file_info["file_types"])
                st.metric("File Types", unique_types)
            
            # Show file type breakdown
            if file_info["file_types"]:
                st.header("📋 File Types")
                file_types_df = {
                    "Extension": list(file_info["file_types"].keys()),
                    "Count": list(file_info["file_types"].values())
                }
                st.dataframe(file_types_df, use_container_width=True)
            
            # Show largest files
            if file_info["largest_files"]:
                st.header("📦 Largest Files")
                largest_files_df = {
                    "File": [item[0] for item in file_info["largest_files"][:10]],
                    "Size": [agent.format_size(item[1]) for item in file_info["largest_files"][:10]]
                }
                st.dataframe(largest_files_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Tips:** Try asking questions like:\n"
        "- 'What is the total size of all files?'\n"
        "- 'How many Python files are there?'\n"
        "- 'What are the 5 largest files?'\n"
        "- 'What file types are most common?'\n"
        "- 'How many directories are there?'"
    )

if __name__ == "__main__":
    main() 