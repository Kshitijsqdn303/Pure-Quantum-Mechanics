# BEC Solitons Research Notebook

This folder records derivations, computations, reproducible benchmarks, and research questions from Matthias Söhn's *Solitons in Bose–Einstein Condensates* and Balakrishnan–Satija's *Solitons in Bose–Einstein condensates*.

The separate [learning notebook](../BEC-Solitons-Notes/) contains the A–E lessons. Learning progress and research results have different checkpoints. Plots marked *preliminary* reproduce model predictions and are not original findings.

- `main.tex`: short opening roadmap, compiled with `pdflatex main.tex` from this folder.
- `workflow.tex`: one-question learning cards, grouped into small research results. Start at card 0.1.
- `working/`: longer derivations in progress. R1 currently collects the scattering-length coupling, many-boson Hamiltonian, and quasi-1D reduction; read it in pieces as cards 1.1–1.6 are understood.
- `previews/`: preliminary reproductions. P0 checks moving GPE propagation; P1 compares the two source-specific branches. These are separate from the opening roadmap.
- `results/`: verified result entries R1–R13 will be added here as the derivations and checks are completed.
- `benchmarks/gpe_soliton_benchmarks.py`: reproducible Python script using NumPy and Matplotlib. Run from this folder with `python benchmarks/gpe_soliton_benchmarks.py`; it writes both SVG and PNG figures next to the script and prints numerical diagnostics.
- `meetings/`: standalone preparation documents for the 5 October meeting.

Current status: the next card is 0.1 (the meaning and units of the 1D condensate field). The GPE propagation and source-comparison figures are preliminary reproductions. Derivation checkpoints with Kshitij and grid/time-step convergence remain open. Accepted lessons continue to be saved only in the learning notebook.
