#!/usr/bin/env python3
import os
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any
import openai
from openai import OpenAI
import builtins

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
        
        system_prompt = """You are a file system analysis assistant. You MUST follow these strict rules:

CRITICAL RULES FOR CALCULATE EXPRESSIONS:
1. ONLY use these basic Python constructs: sum(), len(), basic arithmetic (+, -, *, /), and simple if conditions
2. NEVER use: any(), all(), list comprehensions, nested functions, complex logic
3. ONLY use simple string methods: .lower(), .endswith()
4. ALWAYS use simple OR conditions for multiple file types: file.lower().endswith('.png') or file.lower().endswith('.jpg')
5. NEVER use parentheses beyond what's absolutely necessary
6. ALWAYS test your expression mentally before outputting

The file_info dictionary contains:
- file_info['file_sizes']: dict mapping file paths to sizes in bytes
- file_info['file_types']: dict mapping extensions to counts
- file_info['total_files']: total number of files
- file_info['total_directories']: total number of directories

RESPONSE FORMAT:
- For COUNTING files (how many): Answer directly with the number from file_info['file_types']
- For CALCULATING sizes (how much space): Start with "CALCULATE:" followed by a SIMPLE Python expression

CRITICAL: Pay attention to the question type:
- "number of", "count of", "how many" = COUNTING (use file_info['file_types'])
- "size of", "space used", "total size" = CALCULATING (use CALCULATE: expression)

EXAMPLES:
- Question: "How many image files?" → Answer: 15 (the actual number)
- Question: "What is the total size of image files?" → Answer: "CALCULATE: sum(size for file, size in file_info['file_sizes'].items() if file.lower().endswith('.png') or file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.gif') or file.lower().endswith('.bmp') or file.lower().endswith('.svg') or file.lower().endswith('.webp') or file.lower().endswith('.tiff'))"

SAFE EXPRESSION PATTERNS (use these exact patterns):
- COUNTING image files: Answer directly with the number: file_info['file_types'].get('.png', 0) + file_info['file_types'].get('.jpg', 0) + file_info['file_types'].get('.jpeg', 0) + file_info['file_types'].get('.gif', 0) + file_info['file_types'].get('.bmp', 0) + file_info['file_types'].get('.svg', 0) + file_info['file_types'].get('.webp', 0) + file_info['file_types'].get('.tiff', 0)
- COUNTING Python files: Answer directly with the number: file_info['file_types'].get('.py', 0)
- CALCULATING image file sizes: "CALCULATE: sum(size for file, size in file_info['file_sizes'].items() if file.lower().endswith('.png') or file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.gif') or file.lower().endswith('.bmp') or file.lower().endswith('.svg') or file.lower().endswith('.webp') or file.lower().endswith('.tiff'))"
- CALCULATING Python file sizes: "CALCULATE: sum(size for file, size in file_info['file_sizes'].items() if file.lower().endswith('.py'))"
- Average size: "CALCULATE: sum(file_info['file_sizes'].values()) / len(file_info['file_sizes']) if file_info['file_sizes'] else 0"

REMEMBER: Keep it SIMPLE. If in doubt, use the exact patterns above.
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
                # Validate the expression before evaluating
                if not self._validate_expression(answer):
                    # If validation fails, try to get a corrected expression
                    corrected_answer = self._get_corrected_expression(question, answer)
                    if corrected_answer and corrected_answer.startswith("CALCULATE:"):
                        return self._evaluate_calculation(corrected_answer, file_info)
                    else:
                        return f"Error: Generated expression does not match safe patterns. Please try a simpler question."
                
                return self._evaluate_calculation(answer, file_info)
            else:
                # Handle direct answers (for counting questions)
                return self._handle_direct_answer(answer, file_info)
            
            return answer
        
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def _evaluate_calculation(self, answer: str, file_info: Dict[str, Any]) -> str:
        """Evaluate a CALCULATE expression with robust error handling and retry logic."""
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
            'round': round,
            'any': builtins.any,
            'all': builtins.all,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'reversed': reversed
        }
        
        # Try to fix common syntax issues
        expression = self._fix_common_syntax_issues(expression)
        
        # Try to execute the expression
        for attempt in range(2):
            try:
                # Execute the expression
                try:
                    result = eval(expression, {"__builtins__": {}}, safe_dict)
                except NameError:
                    result = eval(expression, safe_dict, safe_dict)
                
                # Format the result appropriately
                if isinstance(result, (int, float)):
                    if result == 0:
                        return f"Result: {result} (no matching files found)"
                    elif result > 1024:
                        # Likely a size in bytes, format it
                        formatted_result = self.format_size(result)
                        return f"Result: {formatted_result} ({result:,} bytes)"
                    else:
                        return f"Result: {result}"
                else:
                    return f"Result: {result}"
                    
            except Exception as calc_error:
                if attempt == 0:
                    # First attempt failed, try to get a simpler expression from the LLM
                    print(f"First attempt failed: {str(calc_error)}")
                    print(f"Generated expression: {expression}")
                    print("Trying to get a simpler expression...")
                    
                    # Ask for a simpler expression
                    simple_expression = self._get_simpler_expression(expression, str(calc_error))
                    if simple_expression:
                        expression = simple_expression
                        continue
                
                # If we get here, both attempts failed
                return f"Error evaluating calculation: {str(calc_error)}\nGenerated expression: {expression}\nPlease check the expression syntax."
        
        return f"Failed to evaluate expression after multiple attempts: {expression}"
    
    def _fix_common_syntax_issues(self, expression: str) -> str:
        """Fix common syntax issues in generated expressions."""
        # Remove trailing commas in function calls
        expression = expression.replace(',)', ')')
        
        # Fix common mismatched parentheses by counting and balancing
        open_parens = expression.count('(')
        close_parens = expression.count(')')
        if open_parens > close_parens:
            expression += ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            # Remove extra closing parentheses from the end
            while expression.endswith(')') and close_parens > open_parens:
                expression = expression[:-1]
                close_parens -= 1
        
        return expression
    
    def _get_simpler_expression(self, failed_expression: str, error_msg: str) -> str:
        """Ask the LLM to generate a simpler expression when the first one fails."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Python expert. Generate simple, working Python expressions."},
                    {"role": "user", "content": f"""The following expression failed with error: {error_msg}

Failed expression: {failed_expression}

Please generate a simpler, working Python expression that accomplishes the same goal. 
Use only basic Python syntax, avoid complex nested expressions, and ensure proper parentheses matching.
Focus on readability and correctness."""}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception:
            return None
    
    def _validate_expression(self, answer: str) -> bool:
        """Validate that the CALCULATE expression follows safe patterns."""
        expression = answer[10:].strip()
        
        # Check for forbidden constructs
        forbidden_patterns = [
            'any(', 'all(', 'filter(', 'map(', 'enumerate(',
            'list(', 'dict(', 'set(', 'tuple(',
            'lambda', 'def ', 'class ',
            'import ', 'from ', 'try:', 'except:', 'finally:',
            'if __name__', 'eval(', 'exec('
        ]
        
        for pattern in forbidden_patterns:
            if pattern in expression:
                print(f"Validation failed: Found forbidden pattern '{pattern}' in expression")
                return False
        
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            print(f"Validation failed: Unbalanced parentheses in expression")
            return False
        
        # Check for basic safe patterns
        safe_patterns = [
            'sum(size for file, size in file_info[\'file_sizes\'].items() if',
            'sum(file_info[\'file_sizes\'].values())',
            'len(file_info[\'file_sizes\'])',
            'file.lower().endswith('
        ]
        
        has_safe_pattern = any(pattern in expression for pattern in safe_patterns)
        if not has_safe_pattern:
            print(f"Validation failed: Expression does not contain safe patterns")
            return False
        
        return True
    
    def _get_corrected_expression(self, question: str, failed_answer: str) -> str:
        """Ask the LLM to generate a corrected expression using only safe patterns."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a Python expert. You MUST generate ONLY simple, safe Python expressions.

CRITICAL: Use ONLY these exact patterns:
- For image files: sum(size for file, size in file_info['file_sizes'].items() if file.lower().endswith('.png') or file.lower().endswith('.jpg') or file.lower().endswith('.jpeg') or file.lower().endswith('.gif') or file.lower().endswith('.bmp') or file.lower().endswith('.svg') or file.lower().endswith('.webp') or file.lower().endswith('.tiff'))
- For Python files: sum(size for file, size in file_info['file_sizes'].items() if file.lower().endswith('.py'))
- For average: sum(file_info['file_sizes'].values()) / len(file_info['file_sizes']) if file_info['file_sizes'] else 0

NEVER use: any(), all(), filter(), map(), list comprehensions, or complex logic.
ALWAYS start with "CALCULATE:" followed by the expression."""},
                    {"role": "user", "content": f"""The previous expression failed validation: {failed_answer}

Question: {question}

Please generate a CORRECTED expression using ONLY the safe patterns listed above. Start with "CALCULATE:" """}
                ],
                max_tokens=150,
                temperature=0.0  # Use 0 temperature for maximum consistency
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error getting corrected expression: {e}")
            return None
    
    def _handle_direct_answer(self, answer: str, file_info: Dict[str, Any]) -> str:
        """Handle direct answers for counting questions."""
        try:
            # Try to evaluate the answer as a Python expression
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
                'round': round,
                'any': builtins.any,
                'all': builtins.all,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'reversed': reversed
            }
            
            # Try to evaluate the answer
            try:
                result = eval(answer, {"__builtins__": {}}, safe_dict)
                return f"Result: {result}"
            except NameError:
                result = eval(answer, safe_dict, safe_dict)
                return f"Result: {result}"
                
        except Exception as e:
            # If evaluation fails, return the answer as-is
            return f"Answer: {answer}"

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
