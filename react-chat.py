from datetime import date
from time import sleep
import pydash as _
import re
import guidance
import requests
from tools.calculate import calculate 
from tools.serps_search import serps_search 
from tools.wikipedia import wikipedia_page_content_retrieval, wikipedia_pages_search 
import utils.env as env
from utils.gpt import COMPLETION_MODEL_3_5, COMPLETION_MODEL_4, gpt_completion

# ==========================================================
# ReAct (reason, action)
# https://gartist.medium.com/a-simple-agent-with-guidance-and-local-llm-c0865c97eaa9
# https://til.simonwillison.net/llms/python-react-pattern
# https://github.com/QuangBK/localLLM_guidance/blob/main/demo_ReAct.ipynb
# Recreating this concept just to get familiar with it
# ==========================================================

# ==========================================================
# TOOLS
# ==========================================================

dict_tools = {
    'Calculator': {
        'func': calculate,
        'description': 'Runs a calculation for math computation - uses Python eval function so must use math operations (example input: 4 * 7 / 3)',
    },
    'WebSearch': {
        'func': serps_search,
        'description': 'Search Google (example input: Who is the current CEO of the Robin Hood Foundation?)',
    },
    'WikipediaPagesSearch': {
        'func': wikipedia_pages_search,
        'description': 'Search to see what pages on Wikipedia exist for a topic, person, organization exists before retrieving content. (eample input: Jurrasic Park cast)',
    },
    'WikipediaPageContent': {
        'func': wikipedia_page_content_retrieval,
        'description': 'After performing a pages search, this tool can retrieve content for a given Wikipedia page title (example input: President of the United States)',
    }
}
valid_tools = list(dict_tools.keys())

# ==========================================================
# PROMPT TEMPLATES
# ==========================================================
FINAL_ANSWER = 'Final Answer'

react_prompt_system_tools_text = "\n".join(map(lambda tool_name: f"{tool_name}: {dict_tools[tool_name]['description']}", valid_tools))
react_prompt_system = "{{#system~}}" + f"""
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request, and ends with a final answer. Current date: {date.today()}

### Instruction:
Complete the objective as best you can. You have access to the following tools:

{react_prompt_system_tools_text}

Strictly use the following format:

Thought: you should always think about what to do
Action: the action to take, should be one of [{", ".join(valid_tools)}]
Action Input: the input to the action, should be appropriate for tool input
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: do you know the final answer
Final Answer: the final answer to the original input question
""" + "{{~/system}}"

react_prompt_init_user = """
{{#user~}}
Question: {{query}}
{{~/user}}
"""

react_prompt_progress_assistant = """
{{history}}
{{#assistant~}}
{{gen 'fn' temperature=0.7 max_tokens=300}}
{{~/assistant}}
"""

# ==========================================================
# AGENT
# ==========================================================
class ReActChatGuidance():
    def __init__(self, guidance, tools):
        self.guidance = guidance
        self.llm = guidance.llms.OpenAI("gpt-3.5-turbo", token=env.env_get_open_ai_api_key()) # gpt-4
        self.tools = tools

    def fn_tool(self, tool_name, tool_input):
        print('fn_tool', tool_name, tool_input)
        return self.tools[tool_name]['func'](tool_input)
    
    def query(self, query):
        chat_prompt_init = self.guidance("\n".join([react_prompt_system, react_prompt_init_user]), llm=self.llm)
        chat_start = chat_prompt_init(query=query)
        chat_progressing = chat_start # (gets replaced on each cycle, just initial setting)
        history = chat_progressing.text
        # --- assistant config
        assistant_cycles_num = 0
        # --- RUN
        while assistant_cycles_num < 10:
            print(f'assistant working... cycle #{assistant_cycles_num}...')
            chat_prompt_assistant = self.guidance(react_prompt_progress_assistant, llm=self.llm)
            chat_progressing = chat_prompt_assistant(history=history)
            chat_progressing_recent_assistant_text = chat_progressing.text[chat_progressing.text.rindex('<|im_start|>assistant'):]
            # ... in the most recent assistant cycle, if we have an "Action", execute it with a tool so we can insert the true value
            if 'Action:' in chat_progressing_recent_assistant_text or assistant_cycles_num == 0:
                # TODO: make this more flexible where we can halt any action evaluation, for when we'd want a ToT approach where it'd vote on paths suggested
                assistant_text_arr = chat_progressing_recent_assistant_text.split('\n')
                print(assistant_text_arr)
                val_rexep = re.compile(': (.+)')
                first_action_thought_idx  = _.find_index(assistant_text_arr, lambda txt: 'Thought' in txt)
                first_action_idx  = _.find_index(assistant_text_arr, lambda txt: 'Action' in txt)
                first_action_name  = val_rexep.findall(assistant_text_arr[first_action_idx])[0]
                first_action_input_idx  = _.find_index(assistant_text_arr, lambda txt: 'Action Input' in txt)
                first_action_input  = val_rexep.findall(assistant_text_arr[first_action_input_idx])[0]
                # ... if we have a valid tool
                if dict_tools.get(first_action_name) != None:
                    # ... replace the end of the history with output and CoT can continue w/ updated info
                    first_action_output = self.fn_tool(first_action_name, first_action_input)
                    updated_agent_block = '\n'.join([
                        f'{assistant_text_arr[first_action_thought_idx]}',
                        f'Action: {first_action_name}',
                        f'Action Input: {first_action_input}',
                        f'Action Output: {first_action_output}',
                    ])
                    history = chat_progressing.text[:chat_progressing.text.rindex('<|im_start|>assistant')] + "<|im_start|>assistant\n" + updated_agent_block + "\n<|im_end|>\n"
            # ... if it was just a final answer, and no action, then be done
            elif FINAL_ANSWER in chat_progressing_recent_assistant_text:
                break
            # ... increment and run again!
            assistant_cycles_num += 1

        # FIN
        # print("///////////")
        # print("///////////")
        # print(history)
        # print("///////////")
        # print("///////////")
        fn = chat_progressing.variables()['fn']
        # --- TODO: handle some case where it's not resolving
        # --- return (strip out the leading "Final Answer: ")
        return fn[fn.rindex('Final Answer:'):].replace('Final Answer:', '').strip()        


# ==========================================================
# TEST: CALCULATOR
# ==========================================================
agent = ReActChatGuidance(guidance, tools=dict_tools)
# prompt = "Whats does 24 + 17 + ((2 + 2) / 2) * 100 - 5 * 65.5 equal and is it the number as the age of the President of Zimbabwe?"
prompt_calculation = "Whats does 24 + 17 + ((2 + 2) / 2) * 100 - 2 * 100 equal? What is the age of NYC's Brooklyn Borough President? Return the difference between the two numbers?" # lol, funny how you can contradict a IO statement. but our ReAct setup still works
response_react = agent.query(prompt_calculation)
print(f'========== ReAct Response: Tools - Calculator & Search ==========')
print('Response ReAct: ', response_react)
response_io = gpt_completion(prompt=prompt_calculation, model=COMPLETION_MODEL_4)
print('Response IO: ', response_io)

exit()
