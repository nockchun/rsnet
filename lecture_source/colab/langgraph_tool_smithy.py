from unsloth import FastModel
from langchain.embeddings import HuggingFaceEmbeddings
import torch

model, tokenizer = FastModel.from_pretrained(
    model_name = "unsloth/gemma-3-4b-it",
    max_seq_length = 1024*5, # Choose any for long context!
    load_in_4bit = True,  # 4 bit quantization to reduce memory
)

from typing import List, Any, Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any

class GemmaChatModel(BaseChatModel):
    def __init__(self, model, tokenizer, max_tokens: int = 512, do_sample: bool = True, temperature: float = 0.7, top_p: float = 0.9):
        super().__init__()
        object.__setattr__(self, "model", model)
        object.__setattr__(self, "tokenizer", tokenizer)
        object.__setattr__(self, "max_tokens", max_tokens)
        object.__setattr__(self, "do_sample", do_sample)
        object.__setattr__(self, "temperature", temperature)
        object.__setattr__(self, "top_p", top_p)

    @property
    def _llm_type(self) -> str:
        return "gemma-chat"

    def _format_messages(self, messages: List[Any]) -> str:
        prompt = ""
        for message in messages:
            if isinstance(message, SystemMessage):
                prompt += f"<|system|>\n{message.content}</s>\n"
            elif isinstance(message, HumanMessage):
                prompt += f"<|user|>\n{message.content}</s>\n"
            elif isinstance(message, AIMessage):
                prompt += f"<|assistant|>\n{message.content}</s>\n"
        prompt += "<|assistant|>\n"
        return prompt

    def _generate(self, messages: List[Any], **kwargs) -> ChatResult:
        prompt = self._format_messages(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                do_sample=kwargs.get("do_sample", self.do_sample),
                temperature=kwargs.get("temperature", self.temperature),
                top_p=kwargs.get("top_p", self.top_p),
                eos_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = decoded.split("<|assistant|>\n")[-1].strip()

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response))])

llm = GemmaChatModel(model=model, tokenizer=tokenizer, max_tokens=512)

def get_weather(city: str) -> str:
    return f"{city}: 맑음, 25℃ (데모)"

def add(a: float, b: float) -> float:
    return float(a) + float(b)

TOOLS: Dict[str, Dict[str, Any]] = {
    "get_weather": {
        "description": "도시의 현재 날씨를 조회",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
    "add": {
        "description": "두 수를 더한다",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
            "required": ["a", "b"],
        },
    },
}

TOOL_FUNCS = {
    "get_weather": get_weather,
    "add": add,
}

select_instruct = """\
You are a tool router. Read the user's request and decide whether to call a tool.
Return ONLY one JSON object and NOTHING ELSE (no code fences, no commentary).

Strict output JSON (one object):
{{
  "tool": "<one of: {tool_names} | none>",
  "args": <object>
}}

Global rules:
- Use ONLY tools defined in the TOOL SCHEMA below. If nothing matches, set "tool" to "none" and "args" to {{}}.
- Output must be valid JSON with double quotes and no trailing commas.
- Only choose a tool if:
  (a) the request clearly matches the tool’s description/purpose, AND
  (b) you can supply ALL required parameters from the user input.
- Do NOT invent, guess, or hallucinate parameter values. If a required value is missing/unclear, choose "none".
- Conform exactly to the selected tool's parameter schema (names, types, enums). Do not add extra keys not in the schema.
- If multiple tools could work, prefer the most specific one that best matches the user’s intent.
- Keep numbers as numbers, booleans as booleans, arrays as arrays, strings as strings. Do not convert types arbitrarily.
- Preserve user-provided text as-is (do not translate or rewrite); only extract values for "args".
- Think silently; DO NOT include chain-of-thought or explanations in the output.

TOOL SCHEMA (names, descriptions, and JSON parameter schemas):
{tool_schema}

Examples (for style only; do NOT copy literally):
User: What's the weather in Paris?
Output:
{{"tool":"get_weather","args":{{"city":"Paris"}}}}

User: add 7.5 and 2
Output:
{{"tool":"add","args":{{"a":7.5,"b":2}}}}

User: Tell me a joke
Output:
{{"tool":"none","args":{{}}}}
""".strip()

select_prompt = ChatPromptTemplate.from_messages([
    ("system", select_instruct),
    ("human", "Now produce the JSON for this user request:\n{input}")
])

parser = JsonOutputParser()  # {"tool": str, "args": dict}

select_tool_chain = select_prompt | llm | parser

question_instruct = """\
You must answer concisely and accurately in korean.

Tool result:
{observation}

Instructions:
- If the Tool result is NON-EMPTY, produce ONE short paragraph grounded ONLY in that result. Do not contradict it. If it is incomplete or conflicting, state what is missing and answer only with what can be supported.
- If the Tool result is EMPTY, answer directly from your knowledge. If you do not know, say "I don't know." Do NOT invent or guess facts.
- Do NOT include analysis, chain-of-thought, meta commentary, or mentions of tools/pipelines. Output only the final answer.
- Keep it concise (about 1–5 sentences) unless the user explicitly requested another format.
- If the user asked for a specific format (e.g., code or bullet points), follow it; otherwise use plain text.
""".strip()

question_prompt = ChatPromptTemplate.from_messages([
    ("system", question_instruct),
    ("human", "User question:\n{input}")
])

question_chain = question_prompt | llm

class StateToolQA(TypedDict):
    input: str
    tool_schema: Dict[str, Any]
    tool_names: str
    selection: Dict[str, Any]
    observation: Optional[Any]
    answer: Optional[str]

def node_tool_select(state: StateToolQA) -> StateToolQA:
    print(f"[+] node_tool_select\n{state}")
    selection = select_tool_chain.invoke({
        "input": state["input"],
        "tool_schema": state.get("tool_schema", TOOLS),
        "tool_names": state.get("tool_names", ", ".join(TOOLS.keys())),
    })
    print(f"[+] node_tool_select\n{selection}")
    return {**state, "selection": selection}

def node_tool_call(state: StateToolQA) -> StateToolQA:
    print(f"[+] node_tool_call\n{state}")
    selection = state.get("selection", {}) or {}
    tool = selection.get("tool", "none")
    args = selection.get("args") or {}

    if tool not in TOOL_FUNCS:
        return {**state, "observation": None}

    try:
        result = TOOL_FUNCS[tool](**args)
    except Exception as e:
        result = f"TOOL_ERROR: {e}"
    return {**state, "observation": result}

def node_question(state: StateToolQA) -> StateToolQA:
    print(f"[+] node_question\n{state}")
    msg = question_chain.invoke({
        "input": state["input"],
        "observation": state.get("observation")
    })
    content = getattr(msg, "content", str(msg))
    return {**state, "answer": content}


























































