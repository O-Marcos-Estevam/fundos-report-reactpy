"""
Utilitários para Servidor
Funções auxiliares para gerenciamento do servidor
"""

import socket
from typing import Optional


def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> Optional[int]:
    """
    Encontra uma porta disponível a partir de start_port

    Args:
        start_port: Porta inicial para tentar
        max_attempts: Número máximo de tentativas

    Returns:
        Porta disponível ou None se não encontrar
    """
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    return None


def is_port_available(port: int, host: str = '0.0.0.0') -> bool:
    """
    Verifica se uma porta está disponível

    Args:
        port: Porta para verificar
        host: Host para verificar

    Returns:
        True se a porta está disponível
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.bind((host, port))
            return True
    except (OSError, socket.error):
        return False


def kill_process_on_port(port: int) -> bool:
    """
    Tenta matar o processo que está usando uma porta (Windows)

    Args:
        port: Porta para liberar

    Returns:
        True se conseguiu liberar a porta
    """
    import subprocess
    import sys

    if sys.platform != 'win32':
        print(f"[WARNING] kill_process_on_port não suportado em {sys.platform}")
        return False

    try:
        # Encontrar PID usando netstat
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            timeout=5
        )

        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                pid = parts[-1]

                # Matar processo
                subprocess.run(['taskkill', '/PID', pid, '/F'], timeout=5)
                print(f"[INFO] Processo {pid} na porta {port} foi encerrado")
                return True

        return False

    except Exception as e:
        print(f"[ERROR] Erro ao tentar liberar porta {port}: {e}")
        return False


def get_server_info(host: str, port: int) -> dict:
    """
    Retorna informações sobre o servidor

    Args:
        host: Host do servidor
        port: Porta do servidor

    Returns:
        Dict com informações do servidor
    """
    import socket

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return {
        'host': host,
        'port': port,
        'hostname': hostname,
        'local_ip': local_ip,
        'urls': {
            'local': f'http://localhost:{port}',
            'network': f'http://{local_ip}:{port}' if host == '0.0.0.0' else f'http://{host}:{port}'
        }
    }
