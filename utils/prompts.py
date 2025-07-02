schema_cot = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["core", "node", "path", "final_answer"]
        },
        "data": {
            "type": "object",
            "oneOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "idea": {"type": "string"},
                        "description": {"type": "string"},
                        "links": {"type": "array", "items": {"type": "string"}, "maxItems": 1}
                    },
                    "required": ["id", "idea", "description", "links"]
                },
                {
                    "type": "object",
                    "properties": {
                        "route": {"type": "string"},
                        "explanation": {"type": "string"},
                        "verification": {"type": "string"},
                        "code": {"type": "string"}
                    },
                    "required": ["route", "explanation", "verification", "code"]
                },
                {
                    "type": "object",
                    "properties": {
                        "analysis": {"type": "string"},
                        "final_response": {"type": "string"},
                        "recommendation": {"type": "string"},
                        "chosen_path": {"type": "string"},
                        "rationale": {"type": "string"},
                        "code_snippet": {"type": "string"}
                    },
                    "required": ["analysis", "final_response", "recommendation", "chosen_path", "rationale", "code_snippet"]
                }
            ]
        }
    },
    "required": ["type", "data"]
}

schema_got = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["core", "node", "path", "final_answer"]
        },
        "data": {
            "type": "object",
            "oneOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "idea": {"type": "string"},
                        "description": {"type": "string"},
                        "links": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["id", "idea", "description", "links"]
                },
                {
                    "type": "object",
                    "properties": {
                        "route": {"type": "string"},
                        "explanation": {"type": "string"},
                        "verification": {"type": "string"},
                        "code": {"type": "string"}
                    },
                    "required": ["route", "explanation", "verification", "code"]
                },
                {
                    "type": "object",
                    "properties": {
                        "analysis": {"type": "string"},
                        "final_response": {"type": "string"},
                        "recommendation": {"type": "string"},
                        "chosen_path": {"type": "string"},
                        "rationale": {"type": "string"},
                        "code_snippet": {"type": "string"}
                    },
                    "required": ["analysis", "final_response", "recommendation", "chosen_path", "rationale", "code_snippet"]
                }
            ]
        }
    },
    "required": ["type", "data"]
}

schema_tot = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": ["core", "node", "path", "final_answer"]
        },
        "data": {
            "type": "object",
            "oneOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "Node ID in hierarchical format, e.g., N1, N2, N11, N12"},
                        "idea": {"type": "string"},
                        "description": {"type": "string"},
                        "links": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["id", "idea", "description", "links"]
                },
                {
                    "type": "object",
                    "properties": {
                        "route": {"type": "string"},
                        "explanation": {"type": "string"},
                        "verification": {"type": "string"},
                        "code": {"type": "string"}
                    },
                    "required": ["route", "explanation", "verification", "code"]
                },
                {
                    "type": "object",
                    "properties": {
                        "analysis": {"type": "string"},
                        "final_response": {"type": "string"},
                        "recommendation": {"type": "string"},
                        "chosen_path": {"type": "string"},
                        "rationale": {"type": "string"},
                        "code_snippet": {"type": "string"}
                    },
                    "required": ["analysis", "final_response", "recommendation", "chosen_path", "rationale", "code_snippet"]
                }
            ]
        }
    },
    "required": ["type", "data"]
}

def get_schema(strategy):
    if strategy == "cot":
        return schema_cot
    elif strategy == "tot":
        return schema_tot
    elif strategy == "got":
        return schema_got
    else:
        raise ValueError("Unknown strategy")
    
def get_prompt_template(strategy, question):
    if strategy == "cot":
        schema = schema_cot
    elif strategy == "tot":
        schema = schema_tot
    elif strategy == "got":
        schema = schema_got
    else:
        raise ValueError("Unknown strategy")

    if strategy == "cot":
        return f"""
        You are a Chain-of-Thought reasoner capable of multi-step reasoning. Think step by step and provide a detailed response.
        For the given question, provide the response in a series of JSON objects, each on its own line, following this format:
        First, output the core concept:
        {{"type": "core", "data": "Central concept (3-5 words)"}}
        Then, for each node:
        {{"type": "node", "data": {{"id": "N1", "idea": "Specific idea", "description": "Description of the node idea", "links": ["N2"]}}}}
        Then, for each path:
        {{"type": "path", "data": {{"route": "N1→N2", "explanation": "Use the nodes and their description to explain in details the path route.", "verification": "Answer based on this route and verify that the answer is correct.", "code": "Implementation details"}}}}
        Finally, output the final answer:
        {{"type": "final_answer", "data": {{"analysis": "Perform a thoughtful reasoning and explanation by analysing all the answers generated for each of the paths and select the most accurate answer with detailed and strong argumentation", "final_response": "Exact and concise answer or solution (e.g., '40 ballons', '130 gallons', 'Yes, use blockchain', 'see the code snippet below')", "recommendation": "Specific actionable recommendation (e.g., 'Implement blockchain for secure transactions')", "chosen_path": "N1→N2→N3", "rationale": "Detailed explanation of the final solution, referencing the nodes and paths", "code_snippet": "If the query requires code, provide a full code example with explanatory comments here: \\"for i in range(10): ...\\""}}}}
        For "{question}", follow these steps:
        1. Identify the core concept (3-5 words).
        2. Create at least 5 to 20 connected nodes representing alternative ideas or steps.
        3. Develop step by step at least 4 to 10 solution paths with code snippets if required or implementation details and answer the user's query in each path.
        4. Select the best path based on:
           - Technical feasibility
           - Implementation complexity
           - Resource efficiency
        5. Provide an answer once you have multiple solution alternatives leading to the same answer.
        6. Provide a specific, actionable recommendation (e.g., 'Implement blockchain for secure transactions') and explain the choice using node relationships.
        CRITICAL:
        - You must develop multiple solution paths and go through each of them step by step.
        - Each JSON object must be on its own line.
        - Output ONLY valid JSON objects, one per line (no markdown, no prose, no ```json markers).
        - In the "links" array of nodes, all entries must be strings in double quotes (e.g., ["N1", "N2"], not [N1, N2]).
        - Escape special characters properly (e.g., use \\ for backslashes in code_snippet).
        - All nodes must be connected (every node must appear in at least one link or path).
        - Recommendation must be specific, not generic like 'Best approach'.
        - Final answer must reference path nodes.
        - Do not include any extra text, comments, or markdown outside the JSON objects."""
    elif strategy == "tot":
        return f"""
        You are a Tree-of-Thought reasoner designed to create a Christmas-tree-like structure with branching reasoning. Think step by step and provide a detailed response in a strict tree format.
        For the given question, provide the response in a series of JSON objects, each on its own line, following this format:
        First, output the core concept (tree top):
        {{"type": "core", "data": "Central concept (3-5 words)"}}
        Then, for each node (tree branches):
        {{"type": "node", "data": {{"id": "N1", "idea": "Specific idea", "description": "Description of the node idea", "links": ["N11", "N12"]}}}}
        Then, for each path (reasoning branches):
        {{"type": "path", "data": {{"route": "CORE→N1→N11", "explanation": "Detailed explanation of this path using node descriptions.", "verification": "Verify the answer based on this route.", "code": "Implementation details or empty string if not applicable"}}}}
        Finally, output the final answer (tree base with best path):
        {{"type": "final_answer", "data": {{"analysis": "Analyze all paths, comparing technical feasibility, complexity, and efficiency to select the best.", "final_response": "Exact answer (e.g., '40 balloons', 'Yes, use blockchain')", "recommendation": "Actionable step (e.g., 'Use SQL for data queries')", "chosen_path": "CORE→N1→N11", "rationale": "Why this path is best, referencing nodes and paths", "code_snippet": "Full code example if needed, e.g., \\"for i in range(10): ...\\""}}}}
        For "{question}", follow these steps:
        1. Identify the core concept (3-5 words) as the tree top.
        2. Build a tree with 5-20 nodes:
           - Start with CORE as the root.
           - Each node has 0 or more children in "links".
           - No cycles allowed (each node has exactly one parent except CORE).
           - Nodes branch out like a Christmas tree (wider at the base).
           - Use hierarchical naming for nodes, e.g., N1, N2 for top-level nodes, and N11, N12 for subnodes of N1.
        3. Create 4-10 paths from CORE to leaf nodes, each a full reasoning branch.
        4. Evaluate paths based on:
           - Technical feasibility
           - Implementation complexity
           - Resource efficiency
        5. Select the best path and provide a final answer with a specific recommendation.
        CRITICAL:
        - Structure MUST be a tree: no cycles, CORE as single root, hierarchical.
        - Each JSON object on its own line.
        - Output ONLY valid JSON, no extra text or markdown.
        - "links" array contains child node IDs as strings (e.g., ["N11", "N12"]).
        - Paths start with "CORE" and end at a leaf (e.g., "CORE→N1→N11").
        - Escape special characters (e.g., \\ in code_snippet).
        - All nodes must be part of the tree (connected via links or paths).
        - Final answer must reference the chosen path explicitly.
        """
    elif strategy == "got":
        return f"""
        You are a Graph-of-Thought reasoner capable of interconnected reasoning. Think step by step and provide a detailed response in a graph format.
        For the given question, provide the response in a series of JSON objects, each on its own line, following this format:
        First, output the core concept:
        {{"type": "core", "data": "Central concept (3-5 words)"}}
        Then, for each node:
        {{"type": "node", "data": {{"id": "N1", "idea": "Specific idea", "description": "Description of the node idea", "links": ["N2"]}}}}
        Then, for each path:
        {{"type": "path", "data": {{"route": "N1→N2", "explanation": "Use the nodes and their description to explain in details the path route.", "verification": "Answer based on this route and verify that the answer is correct.", "code": "Implementation details"}}}}
        Finally, output the final answer:
        {{"type": "final_answer", "data": {{"analysis": "Perform a thoughtful reasoning and explanation by analysing all the answers generated for each of the paths and select the most accurate answer with detailed and strong argumentation", "final_response": "Exact and concise answer or solution (e.g., '40 ballons', '130 gallons', 'Yes, use blockchain', 'see the code snippet below')", "recommendation": "Specific actionable recommendation (e.g., 'Implement blockchain for secure transactions')", "chosen_path": "N1→N2→N3", "rationale": "Detailed explanation of the final solution, referencing the nodes and paths", "code_snippet": "If the query requires code, provide a full code example with explanatory comments here: \\"for i in range(10): ...\\""}}}}
        For "{question}", follow these steps:
        1. Identify the core concept (3-5 words).
        2. Create at least 5 to 20 connected nodes representing alternative ideas or steps.
        3. Develop step by step at least 4 to 10 solution paths with code snippets if required or implementation details and answer the user's query in each path.
        4. Select the best path based on:
           - Technical feasibility
           - Implementation complexity
           - Resource efficiency
        5. Provide an answer once you have multiple solution alternatives leading to the same answer.
        6. Provide a specific, actionable recommendation (e.g., 'Implement blockchain for secure transactions') and explain the choice using node relationships.
        CRITICAL:
        - You must develop multiple solution paths and go through each of them step by step.
        - Each JSON object must be on its own line.
        - Output ONLY valid JSON objects, one per line (no markdown, no prose, no ```json markers).
        - In the "links" array of nodes, all entries must be strings in double quotes (e.g., ["N1", "N2"], not [N1, N2]).
        - Escape special characters properly (e.g., use \\ for backslashes in code_snippet).
        - All nodes must be connected (every node must appear in at least one link or path).
        - Recommendation must be specific, not generic like 'Best approach'.
        - Final answer must reference path nodes.
        - Do not include any extra text, comments, or markdown outside the JSON objects."""
    else:
        return ""