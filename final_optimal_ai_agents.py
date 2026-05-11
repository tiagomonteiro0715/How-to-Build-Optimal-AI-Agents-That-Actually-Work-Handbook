# -*- coding: utf-8 -*-
"""final_optimal_AI_agents.py

Converted from Colab notebook to a standalone Python script (Windows-compatible).

GitHub: https://github.com/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook

# 1. MIT Code Licence

MIT License
Copyright (c) 2026 Tiago Capelo Monteiro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# 2. Setup requirements (run once, manually, before this script)

  Install Ollama for Windows: https://ollama.com/download
  Install Python packages:
      pip install langchain-ollama ollama crewai duckduckgo-search langchain-community ddgs faker

This script will:
  - start the Ollama server if it isn't already running
  - pull the mistral-small3.2 model if not yet pulled
  - run the three agent demos
"""

import os
import shutil
import socket
import subprocess
import sys
import time

import ollama
from crewai import Agent, Crew, LLM, Process, Task
from langchain_ollama.llms import OllamaLLM

from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

from faker import Faker

fake = Faker("en_US")
Faker.seed(42)


def show(title, body):
    """Replacement for IPython display(Markdown(...)) in a plain script."""
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    print(body)
    print("=" * 78 + "\n")


# 3. Starting the Ollama server, getting the model and tools

def is_server_ready(port=11434):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def start_ollama_server():
    if is_server_ready():
        print("Ollama server already running.")
        return None

    if shutil.which("ollama") is None:
        print("ERROR: 'ollama' executable not found on PATH.")
        print("Install Ollama for Windows from https://ollama.com/download and re-run.")
        sys.exit(1)

    log_file = open("ollama.log", "w")
    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

    process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=log_file,
        stderr=log_file,
        creationflags=creationflags,
    )

    print("Booting Ollama server...")
    for i in range(30):
        if is_server_ready():
            print("Success! Ollama is running and ready for models.")
            return process
        time.sleep(1)
        if i % 5 == 0:
            print(f"Still waiting... ({i}s)")

    print("Error: Ollama server failed to start. Check 'ollama.log' for details.")
    sys.exit(1)


def ensure_model(model_name="mistral-small3.2"):
    try:
        installed = {m.get("name", "") for m in ollama.list().get("models", [])}
    except Exception:
        installed = set()
    if any(name.startswith(model_name) for name in installed):
        print(f"Model '{model_name}' already pulled.")
        return
    print(f"Pulling model '{model_name}' (this can take a while)...")
    subprocess.run(["ollama", "pull", model_name], check=True)


start_ollama_server()
ensure_model("mistral-small3.2")

_ddg = DuckDuckGoSearchRun()


@tool("web_search")
def web_search(query: str) -> str:
    """Search the public web via DuckDuckGo. Input: a concise search query string. Returns: top result snippets as plain text."""
    return _ddg.run(query)


# 4. Testing the model

AI_prompt = "Write a quick system prompt for an AI agent whose job is to summarize financial documents."

AI_model = OllamaLLM(model="mistral-small3.2")

crew_llm = LLM(
    model="ollama/mistral-small3.2",
    base_url="http://localhost:11434",
)

print("Running Mistral...")
AI_response = AI_model.invoke(AI_prompt)
show("AI Output", AI_response)


# 5. Running AI agents
# 5.1 Sequential tasks in a single agent
# 5.1.1 Creating a fake financial report

doc_5_1 = f"""{fake.company()} {fake.company_suffix()}  Q3 2026 Earnings Report
Prepared by: {fake.name()}, CFO
KEY METRICS
Revenue: ${fake.random_int(50, 500)}M (up {fake.random_int(5, 25)}% YoY)
Net Income: ${fake.random_int(10, 80)}M
Operating Margin: {fake.random_int(12, 28)}%
Active Customers: {fake.random_int(10_000, 500_000):,}
Cash on Hand: ${fake.random_int(100, 900)}M
Employee Headcount: {fake.random_int(200, 5000):,}
MANAGEMENT COMMENTARY
{fake.paragraph(nb_sentences=5)}
RISK FACTORS
{fake.paragraph(nb_sentences=4)}
"""

print(doc_5_1)


# 5.1.2 Applying AI agents

analyst = Agent(
    role="Senior Financial Document Specialist",
    goal=(
        "Read the provided document end-to-end, extract the 5 most decision-relevant KPIs "
        "(with units, period, and source line when available), and produce a CEO-ready summary. "
        "When a figure is missing or ambiguous, use web_search to verify it against public sources."
    ),
    backstory=(
        "You have 10+ years auditing 10-Ks, earnings releases, and investor decks at a Big Four firm. "
        "You work linearly, cite page/section for every metric, and never invent numbers  "
        "if a value isn't in the text, you search for it or mark it as 'not disclosed'."
    ),
    tools=[web_search],
    llm=crew_llm,
    verbose=True,
    allow_delegation=False,
)

task_1 = Task(
    description=(
        "Analyze the following document for KPI metrics.\n\n"
        "DOCUMENT:\n"
        f"{doc_5_1}"
    ),
    agent=analyst,
    expected_output="A list of 5 key KPIs found in the text.",
)

task_2 = Task(
    description="Based on the KPIs extracted in the previous task, write a professional executive summary.",
    agent=analyst,
    expected_output="A 200-word summary suitable for a CEO.",
)

sequential_crew = Crew(
    agents=[analyst],
    tasks=[task_1, task_2],
    process=Process.sequential,
)

print("Running Case 1: Sequential...")
result_1 = sequential_crew.kickoff()
show("Case 1 Result", result_1)


# 5.2 Centralized team of 4 agents

researcher = Agent(
    role="Commodity Market Researcher (Battery Metals)",
    goal=(
        "Produce dated, sourced price data points for 2026 lithium carbonate and lithium hydroxide forecasts. "
        "Always pull from web_search; never guess. Return each data point as: value, unit, date, source URL."
    ),
    backstory=(
        "Ex-analyst at a commodities desk. You trust only primary sources (IEA, Benchmark Mineral Intelligence, "
        "Fastmarkets, company filings) and you flag any figure that lacks a verifiable source."
    ),
    tools=[web_search],
    llm=crew_llm,
    verbose=True,
    allow_delegation=False,
)

finance_pro = Agent(
    role="Capex Financial Modeler",
    goal=(
        "Take the researcher's price data and run a 10-year NPV and IRR simulation at a 10% discount rate, "
        "stating all assumptions explicitly and returning a table plus a short narrative."
    ),
    backstory=(
        "You've built DCF models for gigafactory investments. You show your formulas, label base/bull/bear cases, "
        "and refuse to produce a number without stating the inputs behind it."
    ),
    llm=crew_llm,
    verbose=True,
    allow_delegation=False,
)

strategy_advisor = Agent(
    role="Investment Strategy Advisor",
    goal=(
        "Synthesize the researcher's price data and the modeler's NPV/IRR results into a "
        "clear go/no-go recommendation, with the top 3 risks and the conditions under which "
        "the recommendation flips."
    ),
    backstory=(
        "Former MD at a project-finance fund. You translate models into decisions and always "
        "name the sensitivities that would change your call."
    ),
    llm=crew_llm,
    verbose=True,
    allow_delegation=False,
)

centralized_crew = Crew(
    agents=[researcher, finance_pro, strategy_advisor],
    tasks=[
        Task(description="Research 2026 lithium price forecasts.", agent=researcher, expected_output="Price data points."),
        Task(description="Run an NPV simulation using prices.", agent=finance_pro, expected_output="Full NPV report."),
        Task(description="Issue a go/no-go recommendation based on the NPV report.", agent=strategy_advisor, expected_output="Go/no-go memo with top 3 risks."),
    ],
    process=Process.hierarchical,
    manager_llm=crew_llm,
)

print("Running Case 2: Centralized (Hierarchical)...")
result_2 = centralized_crew.kickoff()
show("Case 2 Result", result_2)


# 5.3 Decentralized team of 3 agents
# 5.3.1 Creating a fake hiring batch

groups = ["Group A (men)", "Group B (women)", "Group C (under-40)", "Group D (over-40)"]
hiring_stats = "\n".join(
    f"{g}: {fake.random_int(40, 120)} applicants, {fake.random_int(5, 25)} hired"
    for g in groups
)
feedback = "\n".join(
    f'- Candidate {fake.name()}: "{fake.sentence(nb_words=12)}"'
    for _ in range(6)
)
doc_5_3 = f"""Q1 2026 Hiring Audit Data  {fake.company()}
APPLICANT POOL & SELECTION RATES
{hiring_stats}
INTERVIEWER FEEDBACK NOTES (sample)
{feedback}
"""

print(doc_5_3)


# 5.3.2 Applying AI agents

auditor_a = Agent(
    role="Statistical Hiring Auditor",
    goal=(
        "Compute selection-rate ratios across demographic groups for the Q1 hiring batch, "
        "apply the 4/5ths rule, and flag any group where the ratio falls below 0.80. "
        "Use web_search only to confirm regulatory definitions."
    ),
    backstory=(
        "Former EEOC compliance analyst. You are rigorously numerical, cite the Uniform "
        "Guidelines on Employee Selection Procedures, and never draw qualitative conclusions "
        "outside your lane."
    ),
    tools=[web_search],
    llm=crew_llm,
    verbose=True,
    allow_delegation=True,
)

auditor_b = Agent(
    role="Qualitative Bias Reviewer",
    goal=(
        "Read interview notes and written feedback for coded language, inconsistent rubric "
        "application, and sentiment skew across candidate groups. Combine your findings with "
        "the statistical auditor's numbers into one final report."
    ),
    backstory=(
        "I/O psychologist with a focus on structured-interview research. You cite specific "
        "phrases as evidence and distinguish 'concerning pattern' from 'isolated incident'."
    ),
    tools=[web_search],
    llm=crew_llm,
    verbose=True,
    allow_delegation=True,
)

auditor_c = Agent(
    role="Process & Policy Compliance Auditor",
    goal=(
        "Review the hiring process for adherence to documented policy: structured-interview "
        "use, rubric consistency, and required approval steps. Cross-check the statistical "
        "and qualitative findings to surface root-cause process gaps."
    ),
    backstory=(
        "Internal audit lead with an HR-ops background. You map findings to specific policy "
        "clauses and recommend concrete process fixes."
    ),
    tools=[web_search],
    llm=crew_llm,
    verbose=True,
    allow_delegation=True,
)

task_audit_stats = Task(
    description=(
        "Audit the Q1 hiring batch for structural bias. "
        "Compute selection rates per group and flag any disparities.\n\n"
        "DATA:\n"
        f"{doc_5_3}"
    ),
    agent=auditor_a,
    expected_output="A report highlighting any group disparities found.",
)

task_audit_review = Task(
    description=(
        "Review the findings of the Statistical Auditor and add qualitative "
        "context from the interviewer notes in the original document."
    ),
    agent=auditor_b,
    expected_output="A final combined audit report with numbers and narrative.",
)

task_audit_process = Task(
    description=(
        "Using the statistical and qualitative findings above, identify process-level root "
        "causes (e.g. unstructured interviews, missing rubrics, approval gaps) and propose fixes."
    ),
    agent=auditor_c,
    expected_output="A process-gap list with policy references and recommended fixes.",
)

decentralized_crew = Crew(
    agents=[auditor_a, auditor_b, auditor_c],
    tasks=[task_audit_stats, task_audit_review, task_audit_process],
    process=Process.sequential,
)
print("Running Case 3: Decentralized (Peer Review)...")
result_3 = decentralized_crew.kickoff()
show("Case 3 Result", result_3)
