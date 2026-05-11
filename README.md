# How to Build Optimal AI Agents That Actually Work — A Handbook for Devs

<p align="center">
  <img src="https://github.com/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook/raw/main/How_to_Build_Optimal_AI_Agents_Handbook_book_cover.png" alt="How to Build Optimal AI Agents Handbook Cover" width="400"/>
</p>

<p align="center">
  <strong>A practical, research-backed handbook for deciding when (and how) to build AI agent teams that actually ship</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/edition-1.0-blue" alt="Edition"/>
  <img src="https://img.shields.io/github/stars/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook" alt="Forks"/>
  <img src="https://img.shields.io/github/license/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook" alt="License"/>
  <img src="https://img.shields.io/github/last-commit/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook" alt="Last Commit"/>
</p>

---

[Read on FreeCodeCamp](https://www.freecodecamp.org/news/author/tiagomonteiro)

## Table of Contents
- [What is this?](#what-is-this)
- [Getting Started](#getting-started)
- [Code Examples](#code-examples)
- [Contributing](#contributing)
- [Related Resources](#related-resources)
- [Built With](#built-with)
- [Contact](#contact)
- [License](#license)

---

## What is this?

*Most companies in 2026 are shipping AI agents almost by guessing.*

This handbook is different.

Written from an engineering perspective (think in terms of building blocks), it answers the question almost every team building agents is asking:

**What is the best organizational structure for a team of AI agents?**

Instead of opinions or vendor hype, the answers here are grounded in a recent paper from Google Research, Google DeepMind, and MIT — *Towards a Science of Scaling Agent Systems: When and Why Agent Systems Work* — distilled into a simple decision algorithm anyone can apply.

Whether you are a student, self-taught dev, or practitioner shipping agents into production, you'll find clear explanations of *when* to add more agents, *how* to organize them, and *why* most multi-agent systems fail.

For example, why a single agent often beats a team, why most multi-agent failures are coordination problems (not model problems), and why your evals matter more than your model choice.

**What's included:**
- **A Decision Algorithm**: A 7-step framework for choosing between a single agent and an agent team, grounded in 150+ controlled experiments from the Google paper
- **Topology Selection**: When to use a centralized (manager + workers) team vs. a decentralized (peer-to-peer) team, and the empirical error-amplification numbers behind the choice
- **Team Sizing Rules**: Why agent performance degrades after 3–4 agents, and why each agent should have at most 1–3 tools
- **Three Working Code Examples**: A sequential single-agent pipeline, a hierarchical centralized team, and a decentralized peer-review team
- **The Evals Mindset**: Why the organizations that win with agents are the ones with the best evaluation pipelines, not the most agents

## Getting Started

### Prerequisites
- Basic Python knowledge
- A general understanding of what an LLM is
- [Ollama](https://ollama.com/) installed locally or use it inside Google Colab (recommended if hardware is limited)
- A Jupyter Notebook setup (Google Colab works out of the box for all the examples in this repo)

## Code Examples

The code for all three cases lives in a single Jupyter notebook designed to run end-to-end in **Google Colab** with a free GPU. You can also run it locally if you have Ollama installed.

### Quick start (recommended)

This repo ships with a `pyproject.toml` and lock file, so installing all dependencies is one command:

```bash
# Clone the repository
git clone https://github.com/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook.git
cd How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook

# Install uv (fast Python package installer)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install all dependencies from pyproject.toml / uv.lock
uv sync

# (Optional, for local runs) Install Ollama and pull the model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral-small3.2

# Launch the notebook
uv run jupyter notebook
```

That's it — `uv sync` creates the virtual environment and installs the exact pinned versions automatically. Use `uv run <command>` to execute anything inside that environment without manually activating it.

### Manual install (alternative)

If you'd rather install packages explicitly instead of relying on the lock file:

```bash
git clone https://github.com/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook.git
cd How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook

# Install uv (see Quick start above), then:
uv venv
source .venv/bin/activate            # macOS/Linux
# .venv\Scripts\activate             # Windows

uv pip install langchain-ollama ollama crewai duckduckgo-search langchain-community ddgs faker notebook

# (Optional, for local runs)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral-small3.2
```

If you'd rather skip local setup entirely, open the notebook directly in Google Colab — it installs Ollama, `uv`, all Python deps, and pulls the model for you in the first two cells.

## Contributing

- This handbook is actively being improved based on reader feedback! **I am open to any suggestions!**
- **Found an error, have a suggestion, or want to discuss a topic?** Reach out at monteiro.t@northeastern.edu
- **Enjoyed the handbook?** Star the repository!

## Related Resources

- [The Math Behind Artificial Intelligence](https://github.com/tiagomonteiro0715/The-Math-Behind-Artificial-Intelligence-A-Guide-to-AI-Foundations) — Companion book on the mathematical foundations of AI
- [My FreeCodeCamp Articles](https://www.freecodecamp.org/news/author/tiagomonteiro) — Tutorials and deep dives on AI and programming
- [Article Source Code](https://github.com/tiagomonteiro0715/freecodecamp-my-articles-source-code/tree/main) — Code from my FreeCodeCamp articles
- [Signal Processing Guide](https://github.com/tiagomonteiro0715/Signal-Processing-and-Systems-in-Programming-Guide-for-Beginners) — Companion resource on signal processing
- *Towards a Science of Scaling Agent Systems* — Google Research / Google DeepMind / MIT (primary reference paper for this handbook)
- *Principles of Building AI Agents* by Sam Bhagwat — Recommended companion read

## Built With

- Python — Code examples and reference implementations
- [Ollama](https://ollama.com/) — Running LLMs locally for free
- [CrewAI](https://www.crewai.com/) — Multi-agent orchestration
- [LangChain](https://www.langchain.com/) — Model bindings and community tools
- [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search) — Privacy-respecting web search tool
- [Faker](https://faker.readthedocs.io/) — Synthetic data for safe testing
- [UV](https://github.com/astral-sh/uv) — Fast Python package installer
- [Google Colab](https://colab.research.google.com/) — Free notebook environment with GPU
- [Ray.so](https://ray.so/) — For beautiful code snippets and visualizations

## Contact

**Tiago Capelo Monteiro**
- Email: monteiro.t@northeastern.edu
- GitHub: [@tiagomonteiro0715](https://github.com/tiagomonteiro0715)
- FreeCodeCamp: [Author Profile](https://www.freecodecamp.org/news/author/tiagomonteiro)
- Silicon Valley Fellow W25 | Master's in AI @ Northeastern (Silicon Valley)

## License

This project is licensed under the [MIT License](https://github.com/tiagomonteiro0715/How-to-Build-Optimal-AI-Agents-That-Actually-Work-Handbook/blob/main/LICENSE) - see the LICENSE file for details.

---

<p align="center">
  If you find this handbook helpful, please consider starring the repository!<br>
  Your support helps others discover this resource.
</p>

<p align="center">
  <strong>Current Edition: 1.0</strong> | <strong>Status: Actively Maintained</strong>
</p>
