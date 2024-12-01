import subprocess
import sys
import os
from pathlib import Path
import logging

def setup_logging(log_file):
    """Setup logging to both file and console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def run_command(command):
    """Run a command and log output"""
    try:
        process = subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=True,
            shell=True
        )
        logging.info(process.stdout)
        if process.stderr:
            logging.error(process.stderr)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running command: {e}")
        if e.output:
            logging.error(e.output)
        if e.stderr:
            logging.error(e.stderr)
        return False

def main():
    # Ensure we're in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Setup logging
    log_file = project_root / "evaluation" / "results" / "evaluation.log"
    setup_logging(log_file)

    logging.info("=== Installing Dependencies ===")
    if not run_command("pip install -r requirements/requirement.txt"):
        return
    if not run_command("pip install pytest"):
        return

    logging.info("\n=== Running Tests ===")
    if not run_command("python -m pytest tests/agent_hub/web_searcher/"):
        return

    logging.info("\n=== Running Evaluation Pipeline ===")
    if not run_command("python -m evaluation.pipelines.web_searcher_pipeline"):
        logging.error("\nEvaluation failed!")
        sys.exit(1)

    logging.info("\nEvaluation completed successfully!")

if __name__ == "__main__":
    main()