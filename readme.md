Open Command Line in base directory of this project

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

python -m venv evolving-creatures-env

.\evolving-creatures-env\Scripts\Activate.ps1

pip install pygame tensorflow numpy matplotlib pandas scipy seaborn tqdm networkx
