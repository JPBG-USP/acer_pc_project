#!/bin/env python
import socket
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuração inicial dos gráficos
plt.ion()  # Modo interativo do Matplotlib
fig, ax = plt.subplots(3, 1, figsize=(10, 8))

# Criação de um DataFrame inicial para armazenar os dados
df = pd.DataFrame(columns=["time", "cpu_percent", "memory_percent", "disk_usage"])

def monitor_system(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    try:
        while True:
            # Receber os dados do servidor
            data = client_socket.recv(1024).decode()
            if not data:
                break

            try:
                # Converter JSON de volta para um dicionário
                stats = json.loads(data)
                stats["time"] = pd.Timestamp.now()
                global df
                df = df.append(stats, ignore_index=True)
                
                # Limpa os gráficos para redesenhar
                for axis in ax:
                    axis.clear()

                # Plotagem dos dados
                ax[0].plot(df["time"], df["cpu_percent"], label="Uso de CPU (%)", color='r')
                ax[1].plot(df["time"], df["memory_percent"], label="Uso de Memória (%)", color='g')
                ax[2].plot(df["time"], df["disk_usage"], label="Uso de Disco (%)", color='b')

                # Configuração dos rótulos e legendas
                ax[0].set_ylabel("Uso de CPU (%)")
                ax[1].set_ylabel("Uso de Memória (%)")
                ax[2].set_ylabel("Uso de Disco (%)")
                ax[2].set_xlabel("Tempo")

                for axis in ax:
                    axis.legend()
                    axis.grid(True)

                # Atualiza o gráfico
                plt.draw()
                plt.pause(1)  # Pausa para atualizar o gráfico
            except json.JSONDecodeError:
                print("Erro ao decodificar os dados JSON.")
    except KeyboardInterrupt:
        print("Monitoramento interrompido.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    server_ip = '192.168.0.7'  # Substitua pelo IP do servidor
    server_port = 5001
    print(f"Cliente de monitoramento iniciado em {server_ip}:{server_port}")
    monitor_system(server_ip, server_port)
