# Masgent Web App

🚀 **Modern Web Interface for Materials Science Simulations**

A production-grade Streamlit web application that wraps the Masgent CLI tool, providing an intuitive interface for DFT workflows, ML potentials, and materials science calculations.

---

## ✨ Features

- 🤖 **AI Agent** - Chat with Gemini 2.5 Flash for materials science questions
- 🛠️ **24 Tools** across 6 categories for materials simulation
- 🔮 **3D Visualization** - Interactive structure viewer with py3Dmol
- 📊 **Dynamic Forms** - Auto-generated from Pydantic schemas
- 💾 **Session Management** - Persistent file storage
- 🎨 **Clean UI** - Professional light theme design

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/masgent-web.git
cd masgent-web

# Install dependencies
pip install -r requirements_web.txt
python install_deps.py
```

### Run the App

```bash
streamlit run web_app/app.py
```

Open your browser at: **http://localhost:8501**

---

## 🔑 API Keys

### Gemini API Key (Required for AI Agent)
Get your free key at: https://aistudio.google.com/app/apikey

### Materials Project API Key (Optional)
Get your key at: https://next-gen.materialsproject.org/api

---

## 📖 Usage

### AI Agent Mode (Recommended)
1. Enter your Gemini API key in the sidebar
2. Switch to "🤖 AI Agent" mode
3. Ask questions like:
   - "What is NaCl?"
   - "Explain crystal structures"
   - "Generate POSCAR for Silicon"

### Manual Tools Mode
1. Select a tool category (e.g., Structure Preparation)
2. Choose a specific tool
3. Fill in the form
4. Execute and view results

---

## 🎯 Tool Categories

- 🧪 **Structure Preparation** (7 tools)
- 🔧 **Defect Generation** (3 tools)
- 📁 **VASP Input Preparation** (3 tools)
- 📊 **VASP Workflows** (5 tools)
- ⚡ **ML Potentials** (1 tool)
- 🤖 **Machine Learning** (5 tools)

---

## 📁 Project Structure

```
masgent-web/
├── web_app/
│   ├── app.py              # Main application
│   ├── config.py           # Tool registry
│   ├── ui_utils.py         # UI utilities
│   └── components/
│       ├── sidebar.py      # Navigation
│       ├── tool_forms.py   # Tool execution
│       ├── ai_chat.py      # AI integration
│       └── visualizer.py   # 3D viewer
├── src/masgent/            # Core Masgent library
├── requirements_web.txt    # Dependencies
└── README.md              # This file
```

---

## 🛠️ Technologies

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash (via Pydantic AI)
- **3D Viz**: py3Dmol, stmol
- **Materials**: ASE, Pymatgen
- **API**: Materials Project

---

## 📝 Documentation

- **Quick Start Guide**: `QUICK_START.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **User Guide**: `WEB_APP_GUIDE.md`

---

## 🎨 Screenshots

### AI Agent Mode
Chat with AI for materials science questions and get instant answers.

### Manual Tools Mode
Access 24+ tools for structure generation, DFT workflows, and ML simulations.

### 3D Visualization
Interactive visualization of crystal structures with detailed information.

---

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Deploy!

### Local Network
```bash
streamlit run web_app/app.py --server.address 0.0.0.0
```

### Ngrok (Quick Share)
```bash
streamlit run web_app/app.py
ngrok http 8501
```

---

## 📊 Status

- ✅ All core features implemented
- ✅ 100% test pass rate (6/6 tests)
- ✅ Clean, professional UI
- ✅ Production ready

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Original Masgent CLI by Guangchen Liu
- Built with Streamlit
- Powered by Google Gemini AI
- Materials data from Materials Project

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for the Materials Science Community**
