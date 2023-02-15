import os
import subprocess
import pygame
import time
import json
from PIL import Image, ImageSequence

def run_bandit(file_path):
    try:
        result = subprocess.run(["bandit", "-r", file_path], capture_output=True)
        output = result.stdout.decode()

        return {
            "status": "success",
            "output": output
        }

    except subprocess.CalledProcessError:
        return {
            "status": "error",
            "output": "Erro ao executar o Bandit."
        }

file_path = input("Digite o caminho do arquivo Python: ")

if os.path.isfile(file_path) and file_path.endswith(".py"):
    log_data = run_bandit(file_path)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file_name = f"log-{timestamp}.json"
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    log_path = os.path.join(log_directory, log_file_name)
    with open(log_path, "w") as f:
        json.dump(log_data, f)

    pygame.init()
    pygame.mixer.music.load("undertale.mp3")
    pygame.mixer.music.play()

    gif = Image.open("undertale.gif")
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frames.append(frame.convert("RGBA"))

    screen = pygame.display.set_mode((gif.size[0], gif.size[1]))
    clock = pygame.time.Clock()
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                break

        screen.fill((255, 255, 255))
        frame = frames[i % len(frames)]
        surface = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(500)
        i += 1

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    log_data = run_bandit(file_path)
    with open("bandit2.log", "w") as f:
        json.dump(log_data, f)

else:
    print("Arquivo não encontrado ou não é um arquivo Python.")

