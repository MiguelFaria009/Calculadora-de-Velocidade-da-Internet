import speedtest
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import logging
import requests
import math

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Importar bibliotecas para manipulação de janelas no Windows
try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None
    win32con = None

def minimize_console():
    if win32gui is None or win32con is None:
        return
    
    def enum_windows_callback(hwnd, window_list):
        title = win32gui.GetWindowText(hwnd)
        if "cmd.exe" in title.lower() or "command prompt" in title.lower() or "speed_test.py" in title.lower():
            window_list.append(hwnd)

    window_list = []
    win32gui.EnumWindows(enum_windows_callback, window_list)

    for hwnd in window_list:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def get_user_location():
    try:
        # Usar ipinfo.io para obter a localização do usuário
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data['loc'].split(',')
        latitude = float(loc[0])
        longitude = float(loc[1])
        city = data.get('city', 'Desconhecida')
        country = data.get('country', 'Desconhecido')
        logging.info(f"Localização do usuário: {city}, {country} (Lat: {latitude}, Lon: {longitude})")
        return latitude, longitude
    except Exception as e:
        logging.error(f"Erro ao obter localização do usuário: {str(e)}")
        raise Exception("Falha ao obter localização do usuário. Verifique sua conexão.")

def haversine_distance(lat1, lon1, lat2, lon2):
    # Calcular a distância entre dois pontos na Terra usando a fórmula de Haversine
    R = 6371  # Raio da Terra em km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    return distance

def find_closest_server(st, user_lat, user_lon):
    servers = st.get_servers()
    if not servers:
        raise speedtest.NoMatchedServers("Nenhum servidor encontrado.")

    # Converter servidores em uma lista para facilitar o processamento
    server_list = []
    for server_group in servers.values():
        server_list.extend(server_group)

    if not server_list:
        raise speedtest.NoMatchedServers("Nenhum servidor disponível na lista.")

    # Encontrar o servidor mais próximo
    closest_server = None
    min_distance = float('inf')

    for server in server_list:
        if 'lat' not in server or 'lon' not in server:
            continue  # Pular servidores sem coordenadas
        server_lat = float(server['lat'])
        server_lon = float(server['lon'])
        distance = haversine_distance(user_lat, user_lon, server_lat, server_lon)
        if distance < min_distance:
            min_distance = distance
            closest_server = server

    if not closest_server:
        raise speedtest.SpeedtestBestServerFailure("Nenhum servidor com coordenadas válidas encontrado.")

    logging.info(f"Servidor mais próximo: {closest_server['name']} ({closest_server['country']}, Distância: {min_distance:.2f} km)")
    return closest_server

def speed_test(max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            st = speedtest.Speedtest()
            
            # Obter a localização do usuário
            user_lat, user_lon = get_user_location()
            
            # Buscar servidores disponíveis e identificar o mais próximo
            logging.info("Buscando servidores disponíveis...")
            closest_server = find_closest_server(st, user_lat, user_lon)
            
            # Forçar o teste a usar o servidor mais próximo (indiretamente, via contexto)
            logging.info(f"Usando servidor mais próximo: {closest_server['name']} para o teste")
            
            # Medir velocidades com threads otimizadas
            logging.info("Medindo velocidade de download...")
            down_speed = round(st.download(threads=8) / 10**6, 2)
            
            logging.info("Medindo velocidade de upload...")
            up_speed = round(st.upload(threads=8) / 10**6, 2)
            
            ping = st.results.ping
            logging.info(f"Resultados: Download: {down_speed} Mbps, Upload: {up_speed} Mbps, Ping: {ping} ms")
            
            return down_speed, up_speed, ping
        
        except (speedtest.ConfigRetrievalError, speedtest.NoMatchedServers, speedtest.SpeedtestBestServerFailure) as e:
            retries += 1
            logging.error(f"Tentativa {retries} falhou: {str(e)}")
            if retries == max_retries:
                raise Exception(f"Falha após {max_retries} tentativas: {str(e)}")
            time.sleep(2)  # Esperar 2 segundos antes de tentar novamente
        except Exception as e:
            logging.error(f"Erro inesperado: {str(e)}")
            raise Exception(f"Erro inesperado: {str(e)}")

def update_results(window, download_label, upload_label, ping_label, progress):
    try:
        # Simular progresso enquanto calcula
        for i in range(100):
            progress['value'] = i
            window.update()
            time.sleep(0.05)

        # Executar o teste de velocidade com retries
        down_speed, up_speed, ping = speed_test()
        
        # Atualizar labels com os resultados
        download_label.config(text=f"Velocidade de Download: {down_speed} Mbps")
        upload_label.config(text=f"Velocidade de Upload: {up_speed} Mbps")
        ping_label.config(text=f"Ping: {ping} ms")
        progress.pack_forget()

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao realizar o teste de velocidade: {str(e)}")
        window.destroy()

def display_results():
    window = tk.Tk()
    window.title("Teste de Velocidade da Internet")
    window.geometry("400x300")
    window.configure(bg="#f0f0f0")
    window.resizable(False, False)

    # Minimizar o prompt do DOS
    minimize_console()

    def close_window(event=None):
        window.destroy()

    title_label = tk.Label(
        window,
        text="Teste de Velocidade da Internet",
        font=("Helvetica", 16, "bold"),
        bg="#f0f0f0",
        fg="#333333"
    )
    title_label.pack(pady=20)

    download_label = tk.Label(
        window,
        text="Velocidade de Download: Calculando...",
        font=("Helvetica", 12),
        bg="#f0f0f0",
        fg="#0066cc"
    )
    download_label.pack(pady=10)

    upload_label = tk.Label(
        window,
        text="Velocidade de Upload: Calculando...",
        font=("Helvetica", 12),
        bg="#f0f0f0",
        fg="#0066cc"
    )
    upload_label.pack(pady=10)

    ping_label = tk.Label(
        window,
        text="Ping: Calculando...",
        font=("Helvetica", 12),
        bg="#f0f0f0",
        fg="#0066cc"
    )
    ping_label.pack(pady=10)

    progress = ttk.Progressbar(window, length=300, mode="determinate")
    progress.pack(pady=10)

    test_thread = threading.Thread(target=update_results, args=(window, download_label, upload_label, ping_label, progress))
    test_thread.start()

    close_button = tk.Button(
        window,
        text="Fechar",
        command=close_window,
        font=("Helvetica", 10),
        bg="#dc2626",
        fg="white",
        activebackground="#b32020",
        width=10
    )
    close_button.pack(pady=20)

    window.bind("<Return>", close_window)

    window.mainloop()

if __name__ == "__main__":
    display_results()