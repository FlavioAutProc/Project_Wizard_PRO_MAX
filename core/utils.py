import os
import json
import shutil
from datetime import datetime
import zipfile

def setup_data_files():
    """Cria os arquivos e diretórios necessários se não existirem"""
    os.makedirs('data', exist_ok=True)
    os.makedirs('assets/templates', exist_ok=True)
    
    # Cria config.json se não existir
    if not os.path.exists('data/config.json'):
        with open('data/config.json', 'w') as f:
            json.dump({
                'theme': 'light',
                'default_dir': os.path.expanduser('~/Documents/Projects'),
                'recent_projects': [],
                'pomodoro_duration': 25
            }, f, indent=4)
    
    # Cria historico.json se não existir
    if not os.path.exists('data/historico.json'):
        with open('data/historico.json', 'w') as f:
            json.dump([], f)

def create_project_structure(project_name, project_type, base_dir):
    """
    Cria a estrutura de diretórios para um novo projeto
    Retorna o caminho completo do projeto criado
    """
    project_path = os.path.join(base_dir, project_name)
    
    # Verifica se o projeto já existe e adiciona sufixo se necessário
    if os.path.exists(project_path):
        counter = 1
        while os.path.exists(f"{project_path}_{counter}"):
            counter += 1
        project_path = f"{project_path}_{counter}"
        project_name = f"{project_name}_{counter}"
    
    # Cria os diretórios principais
    dirs = ['dados', 'documentos', 'relatorios', 'planilhas', 'scripts', 'outputs']
    os.makedirs(project_path)
    
    for dir_name in dirs:
        os.makedirs(os.path.join(project_path, dir_name))
    
    # Cria arquivos iniciais
    create_readme(project_path, project_name, project_type)
    create_main_py(project_path)
    
    return project_path

def create_readme(project_path, project_name, project_type):
    """Cria um arquivo README.md com informações do projeto"""
    content = f"""# {project_name}

**Tipo de Projeto**: {project_type}

**Data de Criação**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Descrição

Este projeto foi criado automaticamente pelo Project Wizard PRO MAX.

## Estrutura de Diretórios

- `/dados/`: Armazena arquivos de dados brutos
- `/documentos/`: Documentação do projeto
- `/relatorios/`: Relatórios e análises
- `/planilhas/`: Arquivos Excel e planilhas
- `/scripts/`: Scripts Python, Shell, etc.
- `/outputs/`: Resultados e saídas do projeto

## Como Usar

1. Descreva o propósito do projeto
2. Adicione instruções de configuração
3. Documente os principais scripts e funções
"""
    
    with open(os.path.join(project_path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(content)

def create_main_py(project_path):
    """Cria um arquivo main.py básico"""
    content = """\"\"\"Script principal do projeto\"\"\"

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
"""
    with open(os.path.join(project_path, 'scripts', 'main.py'), 'w', encoding='utf-8') as f:
        f.write(content)

def backup_project(project_path):
    """Cria um backup zip do projeto"""
    backup_dir = os.path.join(project_path, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.zip')
    
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            # Ignora o próprio diretório de backups para evitar recursão
            if os.path.basename(root) == 'backups':
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=project_path)
                zipf.write(file_path, arcname)
    
    return backup_file

def add_to_history(project_name, project_path, project_type):
    """Adiciona o projeto ao histórico"""
    with open('data/historico.json', 'r+') as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []
        
        history.append({
            'name': project_name,
            'path': project_path,
            'type': project_type,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        f.seek(0)
        json.dump(history, f, indent=4)
        f.truncate()

def get_recent_projects(limit=5):
    """Retorna os projetos mais recentes"""
    try:
        with open('data/historico.json', 'r') as f:
            history = json.load(f)
            return history[-limit:][::-1]  # Retorna os mais recentes primeiro
    except (FileNotFoundError, json.JSONDecodeError):
        return []