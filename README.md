# TCP Congestion Control: BBR vs Reno

This repository contains the implementation, simulation, and analysis of **TCP congestion control algorithms**, focusing on **BBR (Bottleneck Bandwidth and Round-trip propagation time)** and **Reno**.  
The project leverages **NS-2 (Network Simulator 2)** for network experiments, custom **C++ implementations** for BBR, and **Python scripts** for post-simulation data analysis.

---

## 📂 Project Structure
codes and files/

│── C++ code for BBR/
│   └── tcp-bbr.cc # BBR implementation in C++
│
│── otcl code and files/

│   ├── tcp-reno-bbr.tcl # Main OTcl simulation script

│   ├── reno.tcl # Reno simulation script

│   ├── project_BBR.nam # BBR network animation trace

│   ├── project_reno.nam # Reno network animation trace

│   ├── project_trace_BBR.tr # BBR raw trace file

│   └── projectTrace_reno.tr # Reno raw trace file
│
│── python code/

│   └── analyze5.py # Python script for analyzing results

---

## 🚀 Features
- Implementation of **TCP BBR congestion control** in C++.
- Simulation of **BBR vs Reno** using **NS-2**.
- Collection of trace files (`.tr`, `.nam`) for detailed analysis.
- Python-based post-processing for performance evaluation.
- Visualization of results from network experiments.

---

## ⚙️ Requirements
- **NS-2** (Network Simulator 2)
- **GCC / g++** (for compiling the BBR C++ code)
- **Python 3.x** with libraries:
  - `matplotlib`
  - `pandas`
  - `numpy`

---

## 🛠️ Usage

### 1. Compile BBR
```bash
cd "codes and files/C++ code for BBR"
ns make tcp-bbr.cc

2. ** Run Simulations **
bash
Copy code
cd "codes and files/otcl code and files"

# Run Reno simulation
ns reno.tcl

# Run BBR simulation
ns tcp-reno-bbr.tcl
- This will generate trace files (.tr) and animation files (.nam).

3. Analyze Results
bash
Copy code
cd "codes and files/python code"
python3 analyze5.py
📊 Expected Output
- Trace files for each algorithm
- NAM visualizations showing network behavior
- Plots/graphs comparing throughput, delay, and fairness between Reno and BBR


🤝 Contributing
Contributions are welcome!
Please open an issue or submit a pull request if you’d like to extend the analysis or add new congestion control algorithms.
