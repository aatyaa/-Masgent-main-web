# Masgent Web Application - Quick Start Guide

## 🚀 Quick Start

### 1. Installation
All dependencies are already installed! If you need to reinstall:
```bash
python install_deps.py
```

### 2. Run the Application
```bash
streamlit run web_app/app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 User Guide

### **Two Modes of Operation:**

#### 🛠️ **Manual Tools Mode**
- Select from 6 categories of tools
- 20+ simulation tools available
- Dynamic forms auto-generated from tool parameters
- File upload or use session files
- 3D visualization of crystal structures

#### 🤖 **AI Agent Mode**
- Chat with AI to describe what you want
- AI proposes a plan (Phase I)
- You confirm and execute (Phase II)
- Requires OpenAI API key

---

## 🔑 API Keys Setup

### OpenAI API Key (for AI Agent)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an account or sign in
3. Navigate to API Keys
4. Create new secret key
5. Paste in sidebar

### Materials Project API Key (for structure generation)
1. Go to [materialsproject.org](https://next-gen.materialsproject.org/api)
2. Sign up or log in
3. Generate API key
4. Paste in sidebar

---

## 📂 Tool Categories

### 🧪 Structure Preparation
- Generate POSCAR from formula
- Convert formats (CIF, POSCAR, XYZ)
- Create supercells
- Generate surface slabs
- Generate interfaces
- Generate SQS structures

### 🔧 Defect Generation
- Vacancy defects
- Substitution defects
- Interstitial defects

### 📁 VASP Input Preparation
- Full VASP inputs (INCAR, KPOINTS, POTCAR)
- Customize KPOINTS
- HPC Slurm scripts

### 📊 VASP Workflows
- Convergence tests (ENCUT, KPOINTS)
- Equation of State (EOS)
- Elastic constants
- AIMD simulations
- NEB calculations

### ⚡ ML Potentials
- Fast simulations using:
  - CHGNet
  - SevenNet
  - Orb-v3
  - MatSim
- Tasks: Single point, EOS, Elastic, MD

### 🤖 Machine Learning
- Feature analysis
- Dimensionality reduction (PCA)
- Data augmentation (VAE)
- Model design (Optuna)
- Model training & evaluation

---

## 💡 Example Workflows

### Example 1: Generate and Visualize NaCl
1. Select **🧪 Structure Preparation** → **Generate POSCAR**
2. Enter formula: `NaCl`
3. Click **🚀 Execute Tool**
4. View 3D structure automatically

### Example 2: Run ML Simulation
1. Upload or generate a POSCAR file
2. Select **⚡ ML Potentials** → **Run ML Simulation**
3. Choose MLP type (e.g., CHGNet)
4. Choose task (e.g., EOS)
5. Execute and view results

### Example 3: AI Agent
1. Enter OpenAI API key in sidebar
2. Switch to **🤖 AI Agent** mode
3. Type: "Generate a POSCAR for Silicon and run an EOS calculation"
4. Review the plan
5. Click **✅ Confirm & Execute**

---

## 📁 Session Management

Each session has a unique ID and directory:
- Location: `masgent_sessions/<session_id>/`
- All generated files saved here
- Files persist across tool runs
- Can be reused in subsequent operations

---

## 🔮 3D Visualization

Automatic visualization for:
- POSCAR files
- CIF files
- XYZ files

Features:
- Interactive rotation and zoom
- CPK coloring scheme
- Unit cell display
- Structure information (formula, atoms, volume)

---

## 🐛 Troubleshooting

### App won't start
```bash
# Reinstall dependencies
python install_deps.py
```

### Import errors
Make sure you're in the project root:
```bash
cd /storage/home/sii5085/work/webApp/Masgent-main
streamlit run web_app/app.py
```

### 3D visualization not working
```bash
pip install stmol py3Dmol
```

### AI Agent not responding
- Check OpenAI API key is entered
- Verify internet connection
- Check API key has credits

---

## 📝 Notes

- **Session files**: All files are saved in `masgent_sessions/<session_id>/`
- **File uploads**: Uploaded files are automatically saved to session
- **Validation**: All inputs validated before execution
- **Error handling**: Detailed error messages with traceback

---

## 🎯 Next Steps

1. **Test basic functionality**: Generate a POSCAR for a simple compound
2. **Try ML simulations**: Run a quick CHGNet calculation
3. **Explore AI Agent**: Chat with AI to automate workflows
4. **Customize**: Modify `config.py` to add more tools

---

## 📚 Resources

- **Masgent GitHub**: https://github.com/aguang5241/masgent
- **Streamlit Docs**: https://docs.streamlit.io
- **Materials Project**: https://materialsproject.org
- **OpenAI API**: https://platform.openai.com

---

**Enjoy using Masgent Web! 🚀⚛️**
