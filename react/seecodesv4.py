import os

def gather_code_snippets(root_dir='.', output_file='react_code_summary.txt', ignore_dirs=None, ignore_files=None):
    """
    Reúne trechos de código de arquivos .py, .jsx e .json em um diretório e os salva em um arquivo.

    Args:
        root_dir (str, optional): O diretório raiz para pesquisar os arquivos de código.
                                  O padrão é o diretório atual.
        output_file (str, optional): O nome do arquivo de saída.
                                      O padrão é 'react_code_summary.txt'.
        ignore_dirs (list, optional): Lista de diretórios para ignorar.
                                      Exemplo: ['node_modules', 'dist']
        ignore_files (list, optional): Lista de arquivos para ignorar.
                                      Exemplo: ['dict.py', 'test.json']
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    with open(output_file, 'w', encoding='utf-8') as output:
        for root, dirs, files in os.walk(root_dir):
            # Remove directories from the traversal list
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file in files:
                if file.endswith(('.py', '.json','.jsx','.js')) and file not in ignore_files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as code_file:
                            output.write(f'File: {file_path}\n')
                            output.write(code_file.read())
                            output.write('\n\n' + '#' * 80 + '\n\n')
                    except UnicodeDecodeError:
                        print(f"Não foi possível ler {file_path} devido a problemas de codificação.")
    
    print(f"Trechos de código salvos em {output_file}")


def list_files(startpath='.', output_file='react_reboot_folder_structure.txt', ignore_dirs=None, ignore_files=None):
    """
    Lista todos os arquivos .py, .jsx e .json e diretórios a partir de um determinado caminho 
    e salva a estrutura em um arquivo.

    Args:
        startpath (str, optional): O caminho inicial para começar a listar arquivos e diretórios.
                                   O padrão é o diretório atual.
        output_file (str, optional): O nome do arquivo de saída.
                                      O padrão é 'react_reboot_folder_structure.txt'.
        ignore_dirs (list, optional): Lista de diretórios para ignorar.
                                      Exemplo: ['node_modules', 'dist']
        ignore_files (list, optional): Lista de arquivos para ignorar.
                                      Exemplo: ['dict.py', 'test.json']
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_files is None:
        ignore_files = []

    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            # Remove directories from the traversal list
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            # Write the directories without filtering
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))

            # Filter files by extension and ignore specific files
            files = [file for file in files if file.endswith(('.jsx', '.py', '.json','.js')) and file not in ignore_files]

            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write('{}{}\n'.format(subindent, file))


def generate_report(root_dir='.', ignore_dirs=None, ignore_files=None, project_description="You are a Flask expert tasked with assisting in the development and improvement of a React project. You will be provided with the complete project structure, including all files and their contents. Your role is to analyze this information and provide guidance, corrections, and assistance in building new features and directories. Be specific to show the directory path when suggesting a code alteration."):
    """
    Gera um relatório com a descrição do projeto, estrutura de diretórios e trechos de código.

    Args:
        root_dir (str, optional): O diretório raiz do projeto.
                                  O padrão é o diretório atual.
        ignore_dirs (list, optional): Lista de diretórios para ignorar.
                                      Exemplo: ['node_modules', 'dist']
        ignore_files (list, optional): Lista de arquivos para ignorar.
                                      Exemplo: ['dict.py', 'test.json']
        project_description (str, optional): A descrição do projeto.
    """
    list_files(root_dir, output_file='react_reboot_folder_structure.txt', ignore_dirs=ignore_dirs, ignore_files=ignore_files)
    gather_code_snippets(root_dir, output_file='react_code_summary.txt', ignore_dirs=ignore_dirs, ignore_files=ignore_files)

    with open('react_project_report.txt', 'w', encoding='utf-8') as report_file:
        report_file.write(project_description + "\n\n")

        report_file.write("Project Structure:\n")
        with open('react_reboot_folder_structure.txt', 'r', encoding='utf-8') as structure_file:
            report_file.write(structure_file.read() + "\n\n")

        report_file.write("Codes in my project:\n")
        with open('react_code_summary.txt', 'r', encoding='utf-8') as code_file:
            report_file.write(code_file.read())

    print("Relatório do projeto gerado com sucesso em react_project_report.txt")


# Usage example
generate_report(
    ignore_dirs=[
        'node_modules', 'dist', 'public', '.vscode',
        'components', 'material-kit', 'charts','zboard','volatilidade','survival','screener',
        'rrg','recomendations','fundamental','mock','recommendation','screener','survival','core','dolphindb',
        'staticfiles','components','longshort','.git','temp','export','fernd',
        'models','empyrical','pyfolio','archive','tests','schemas','opcoes','machinelearning','longshort','fundamentos','portfolio',
        '__api__','utils'
    ],
    ignore_files=['dictionary.py', 'manage.py', 'db.sqlite3', 'test.json','seecodesv4.py','cumulative_performace_data.json',
    'fluxo.json','IBOV_stocks.json','rrg_data.json','volatility_analysis_results.json','combined_cointegration_results.json',
    'combined_currency_cointegration_results.json','cointegration_matrix.py','collar.py','collar_inverted.py',
    'cumulative_performace.py','currency_cointegration.py','fetch_nasdaq_recommendations.py',
    'fetch_nyse_recommendations.py', 'fluxo_ddm.py','ibov_stocks.py','quant_port.py','rrg_data.py',
    'screener_yf.py','statements.py','survival_lomax.py','update_screener_data.py',
    'cumulative_performance.py','currency_cointegration_matrix.py','ddm_historical_dy.py','fundamental_data.py',
    '__fetch_surface.py','agenda_dividendos.py','fetch_surface.py','bootstrap.py','test_opt_markovitz.py',
    'opt_markovitz.py','test_bootstrap.py','volatility_analysis.py']
)
