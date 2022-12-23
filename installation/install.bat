@echo off

:start
cls

IF "%1"=="install" (
    python -m venv venv
    .\venv\Scripts\activate.bat

    python -m pip install --upgrade pip

    pip install qiskit
    pip install qiskit[visualization]
    pip install qiskit[machine-learning]
    pip install qiskit[nature]

    cls
    echo "Successfully installed packages."
    echo "Please restart all your teminals to register the environment variables."
)

IF "%1"=="uninstall" (
    pip uninstall -y qiskit
    pip uninstall -y qiskit[visualization]
    pip uninstall -y qiskit[machine-learning]
    pip uninstall -y qiskit[nature]

    cls
    echo "Successfully uninstalled packages."
)

exit