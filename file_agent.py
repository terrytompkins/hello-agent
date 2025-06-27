#!/usr/bin/env python3
import os
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
import openai
from openai import OpenAI

class FileSystemAgent:
    def __init__(self, api_key: str):
        """Initialize the agent with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
    
    def scan_directory(self, root_path: str) -> Dict[str, Any]:
        """Scan directory hierarchy and collect file information."""
        root = Path(root_path)
        if not root.exists():
            raise ValueError(f"Directory '{root_path}' does not exist")
        
        file_info = {
            "total_files": 0,
            "total_directories": 0,
            "file_types": {},
            "file_sizes": {},
            "directory_structure": [],
            "largest_files": [],
            "file_list": []
        }
        
        try:
            for item in root.rglob("*"):
                if item.is_file():
                    file_info["total_files"] += 1
                    
                    # Get file extension
                    extension = item.suffix.lower() or "no_extension"
                    file_info["file_types"][extension] = file_info["file_types"].get(extension, 0) + 1
                    
                    # Get file size
                    try:
                        size = item.stat().st_size
                        file_info["file_sizes"][str(item.relative_to(root))] = size
                        file_info["largest_files"].append((str(item.relative_to(root)), size))
                    except (OSError, PermissionError):
                        pass
                    
                    # Add to file list
                    file_info["file_list"].append(str(item.relative_to(root)))
                
                elif item.is_dir():
                    file_info["total_directories"] += 1
                    file_info["directory_structure"].append(str(item.relative_to(root)))
        
        except PermissionError as e:
            print(f"Warning: Permission denied accessing some files: {e}")
        
        # Sort largest files by size (descending)
        file_info["largest_files"].sort(key=lambda x: x[1], reverse=True)
        file_info["largest_files"] = file_info["largest_files"][:10]  # Keep top 10
        
        return file_info
    
    def create_summary(self, file_info: Dict[str, Any], root_path: str) -> str:
        """Create a text summary of the file system information."""
        summary = f"File System Analysis for: {root_path}\n"
        summary += "=" * 50 + "\n\n"
        
        summary += f"Total Files: {file_info['total_files']}\n"
        summary += f"Total Directories: {file_info['total_directories']}\n\n"
        
        summary += "File Types:\n"
        for ext, count in sorted(file_info['file_types'].items()):
            summary += f"  {ext}: {count} files\n"
        
        summary += f"\nDirectory Structure (first 20):\n"
        for dir_path in sorted(file_info['directory_structure'])[:20]:
            summary += f"  {dir_path}\n"
        
        if len(file_info['largest_files']) > 0:
            summary += f"\nLargest Files:\n"
            for file_path, size in file_info['largest_files'][:5]:
                summary += f"  {file_path}: {self.format_size(size)}\n"
        
        summary += f"\nSample Files (first 20):\n"
        for file_path in sorted(file_info['file_list'])[:20]:
            summary += f"  {file_path}\n"
        
        return summary
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def answer_question(self, question: str, file_info: Dict[str, Any], root_path: str) -> str:
        """Use OpenAI to answer questions about the file system."""
        summary = self.create_summary(file_info, root_path)
        
        system_prompt = """You are a helpful assistant that analyzes file systems. 
        You have been provided with detailed information about a directory hierarchy.
        
        For questions that require calculations (like total size, average size, etc.), 
        generate a Python expression that can be evaluated with the file_info data.
        
        The file_info dictionary contains:
        - file_info['file_sizes']: dict mapping file paths to sizes in bytes
        - file_info['file_types']: dict mapping extensions to counts
        - file_info['total_files']: total number of files
        - file_info['total_directories']: total number of directories
        
        Return your response in this format:
        - For simple questions: Just answer directly
        - For calculation questions: Start with "CALCULATE:" followed by a Python expression
        
        Example: "CALCULATE: sum(file_info['file_sizes'].values())"
        """
        
        user_prompt = f"""Here is the file system information:

{summary}

Raw data for precise calculations:
- File types: {json.dumps(file_info['file_types'], indent=2)}
- Total files: {file_info['total_files']}
- Total directories: {file_info['total_directories']}

Question: {question}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Check if the answer contains a calculation expression
            if answer.startswith("CALCULATE:"):
                try:
                    # Extract the Python expression
                    expression = answer[10:].strip()
                    
                    # Create a safe execution environment
                    safe_dict = {
                        'file_info': file_info,
                        'sum': sum,
                        'len': len,
                        'min': min,
                        'max': max,
                        'sorted': sorted,
                        'filter': filter,
                        'list': list,
                        'dict': dict,
                        'str': str,
                        'int': int,
                        'float': float,
                        'round': round
                    }
                    
                    # Execute the expression
                    result = eval(expression, {"__builtins__": {}}, safe_dict)
                    
                    # Format the result appropriately
                    if isinstance(result, (int, float)) and result > 1024:
                        # Likely a size in bytes, format it
                        formatted_result = self.format_size(result)
                        return f"Result: {formatted_result} ({result:,} bytes)"
                    else:
                        return f"Result: {result}"
                        
                except Exception as calc_error:
                    return f"Error evaluating calculation: {str(calc_error)}\nGenerated expression: {expression}"
            
            return answer
        
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="File System Analysis Agent using OpenAI")
    parser.add_argument("folder", help="Path to the folder to analyze")
    parser.add_argument("question", help="Question to ask about the folder")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed file system summary")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please provide OpenAI API key via --api-key or OPENAI_API_KEY environment variable")
        return 1
    
    try:
        # Initialize agent
        agent = FileSystemAgent(api_key)
        
        # Scan directory
        print(f"Scanning directory: {args.folder}")
        file_info = agent.scan_directory(args.folder)
        
        if args.verbose:
            print("\n" + agent.create_summary(file_info, args.folder))
            print("\n" + "="*50 + "\n")
        
        # Answer question
        print(f"Question: {args.question}")
        answer = agent.answer_question(args.question, file_info, args.folder)
        print(f"Answer: {answer}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
