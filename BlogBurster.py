#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import random
from threading import Thread, Lock
from queue import Queue
from tqdm import tqdm
from colorama import Fore, Style, init
import time
import os

init(autoreset=True)

def print_ascii_art():
    art = f"""{Fore.RED}
▀█████████▄   ▄█        ▄██████▄     ▄██████▄  ▀█████████▄  ███    █▄     ▄████████    ▄████████     ███        ▄████████    ▄████████ 
  ███    ███ ███       ███    ███   ███    ███   ███    ███ ███    ███   ███    ███   ███    ███ ▀█████████▄   ███    ███   ███    ███ 
  ███    ███ ███       ███    ███   ███    █▀    ███    ███ ███    ███   ███    ███   ███    █▀     ▀███▀▀██   ███    █▀    ███    ███ 
 ▄███▄▄▄██▀  ███       ███    ███  ▄███         ▄███▄▄▄██▀  ███    ███  ▄███▄▄▄▄██▀   ███            ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀██▄  ███       ███    ███ ▀▀███ ████▄  ▀▀███▀▀▀██▄  ███    ███ ▀▀███▀▀▀▀▀   ▀███████████     ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███    ██▄ ███       ███    ███   ███    ███   ███    ██▄ ███    ███ ▀███████████          ███     ███       ███    █▄  ▀███████████ 
  ███    ███ ███▌    ▄ ███    ███   ███    ███   ███    ███ ███    ███   ███    ███    ▄█    ███     ███       ███    ███   ███    ███ 
▄█████████▀  █████▄▄██  ▀██████▀    ████████▀  ▄█████████▀  ████████▀    ███    ███  ▄████████▀     ▄████▀     ██████████   ███    ███ 
             ▀                                                           ███    ███                                         ███    ███ 
- Blog View Booster Bot    
    {Style.RESET_ALL}
    """
    print(art)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(message, duration=3):
    with tqdm(total=duration, desc=message, bar_format="{desc}: {bar} {elapsed}s") as pbar:
        for _ in range(duration):
            time.sleep(1)
            pbar.update(1)
            
def main():
    clear_console()
    print_ascii_art()

    print(f"{Fore.YELLOW}\n[Menu]{Style.RESET_ALL}")
    url = input(f"{Fore.BLUE}Enter the blogpost link: {Style.RESET_ALL}").strip()
    print("")  # Blank line for spacing
    while True:
        try:
            num_requests = int(input(f"{Fore.BLUE}How many views do you want?: {Style.RESET_ALL}").strip())
            if num_requests <= 0:
                raise ValueError("Number of requests must be positive.")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input: {e}{Style.RESET_ALL}")

    print("")  

    while True:
        try:
            num_threads = int(input(f"{Fore.BLUE}How many threads do you want to use?: {Style.RESET_ALL}").strip())
            if num_threads <= 0 or num_threads > 500:
                raise ValueError("Threads must be between 1 and 500.")
            break
        except ValueError as e:
            print(f"{Fore.RED}Invalid input: {e}{Style.RESET_ALL}")

    print("")

    try:
        with open("user-agents.txt", "r") as f:
            user_agents = [ua.strip() for ua in f.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: 'user-agents.txt' file not found. Please provide a valid file.{Style.RESET_ALL}")
        return

    counter = 0
    success_counter = 0
    counter_lock = Lock()

    request_queue = Queue()

    for i in range(1, num_requests + 1):
        request_queue.put(i)

    def send_request():
        nonlocal counter, success_counter
        while not request_queue.empty():
            bot_id = request_queue.get()
            user_agent = random.choice(user_agents)
            headers = {"User-Agent": user_agent}
            try:
                response = requests.get(url, headers=headers)
                with counter_lock:
                    counter += 1
                    if response.status_code == 200:
                        success_counter += 1
                        print(f"{Fore.GREEN}Bot #{bot_id}: Status code {response.status_code}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Bot #{bot_id}: Status code {response.status_code}{Style.RESET_ALL}")
            except requests.exceptions.RequestException as e:
                with counter_lock:
                    counter += 1
                print(f"{Fore.RED}Bot #{bot_id}: Error - {e}{Style.RESET_ALL}")
            request_queue.task_done()

    print(f"{Fore.YELLOW}\n[Starting the bots...]\n{Style.RESET_ALL}")
    threads = []
    for _ in range(min(num_threads, num_requests)):
        thread = Thread(target=send_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"{Fore.CYAN}\n" + "=" * 50 + f"{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Completed {counter} total requests, with {success_counter} successful views.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}" + "=" * 50 + f"{Style.RESET_ALL}")

if __name__ == "__main__":
    loading_animation("Initializing", duration=3)
    main()
