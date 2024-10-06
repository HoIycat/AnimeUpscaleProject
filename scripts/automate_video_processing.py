import os
import subprocess

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Команда для извлечения кадров из видео
    command = f"ffmpeg -i {video_path} {output_folder}/frame_%04d.png"
    subprocess.run(command, shell=True)

def extract_audio(video_path, output_audio_path):
    # Извлечение аудио дорожки
    command = f"ffmpeg -i {video_path} -q:a 0 -map a {output_audio_path}"
    subprocess.run(command, shell=True)

def upscale_frames(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Команда для запуска Real-ESRGAN на каждом кадре
    command = f"python Real-ESRGAN-master/inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i {input_folder} -o {output_folder} --outscale 4 --fp32"
    subprocess.run(command, shell=True)

def combine_frames_and_audio(output_frames_folder, audio_path, output_video_path):
    # Команда для объединения кадров и аудио в видео
    command = f"ffmpeg -framerate 24 -i {output_frames_folder}/frame_%04d.png -i {audio_path} -c:v libx264 -pix_fmt yuv420p {output_video_path}"
    subprocess.run(command, shell=True)

def main():
    video_path = "inputs/input_video.mp4"  # Путь к видео
    frames_folder = "results"
    audio_path = "output_audio/audio.mp3"
    output_video_path = "output_video/output_video.mp4"
    
    print("Извлечение кадров...")
    extract_frames(video_path, frames_folder)
    
    print("Извлечение аудио...")
    extract_audio(video_path, audio_path)
    
    print("Улучшение кадров...")
    upscale_frames(frames_folder, frames_folder)
    
    print("Сборка видео...")
    combine_frames_and_audio(frames_folder, audio_path, output_video_path)
    
    print(f"Обработка видео '{os.path.basename(video_path)}' завершена. Результат сохранён в '{output_video_path}'.")

if __name__ == "__main__":
    main()
