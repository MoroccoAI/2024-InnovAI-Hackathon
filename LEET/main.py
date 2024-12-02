import subprocess

if __name__ == "__main__":
    model_name = "llama3.2:1b"
    container_name = "innovai_backend"
    
    
    try:
        subprocess.run(["docker-compose", "build"], check=True)
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True, check=True)
        if container_name not in result.stdout:
            subprocess.run(["docker-compose", "up", "-d"])
            subprocess.run(["docker", "exec", "-it", "ollama", "ollama", "pull", model_name], check=True)
    except Exception as e:
        print(f"An error occurred: {e}")

    subprocess.run(['docker', 'exec', '-it', container_name, 'python3', 'app.py'])
