# BEC Solitons Research Notebook

This folder records derivations, computations, reproducible benchmarks, and research questions from Matthias Söhn's *Solitons in Bose–Einstein Condensates* and Balakrishnan–Satija's *Solitons in Bose–Einstein condensates*.

The separate [learning notebook](../BEC-Solitons-Notes/) contains the A–E lessons. Learning progress and research results have different checkpoints. Plots marked *preliminary* reproduce model predictions and are not original findings.

- `main.tex`: standalone research notebook, compiled with `pdflatex main.tex` from this folder.
- `workflow.tex`: sequence of research entries R1–R13, with sources, outputs, and verification gates.
- `previews/`: preliminary reproductions. P0 checks moving GPE propagation; P1 compares the two source-specific branches.
- `results/`: verified result entries R1–R13 will be added here as the derivations and checks are completed.
- `benchmarks/gpe_soliton_benchmarks.py`: reproducible Python script using NumPy and Matplotlib. Run from this folder with `python benchmarks/gpe_soliton_benchmarks.py`; it writes both SVG and PNG figures next to the script and prints numerical diagnostics.
- `meetings/`: standalone preparation documents for the 5 October meeting.

Current status: the GPE propagation and source-comparison figures are preliminary reproductions. Derivation checkpoints with Kshitij and grid/time-step convergence remain open. Accepted lessons continue to be saved only in the learning notebook.
