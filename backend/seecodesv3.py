import os

def gather_code_snippets(root_dir='.', output_file='raw_code_summary.txt'):
    """
    Reúne trechos de código de arquivos .py e .html em um diretório e os salva em um arquivo.

    Args:
        root_dir (str, optional): O diretório raiz para pesquisar os arquivos de código. 
                                  O padrão é o diretório atual.
        output_file (str, optional): O nome do arquivo de saída. 
                                      O padrão é 'code_summary.txt'.
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(('.py', '.html')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as code_file:
                            output.write(f'File: {file_path}\n')
                            output.write(code_file.read())
                            output.write('\n\n' + '#' * 80 + '\n\n')
                    except UnicodeDecodeError:
                        print(f"Não foi possível ler {file_path} devido a problemas de codificação.")
    
    print(f"Trechos de código salvos em {output_file}")


def list_files(startpath='.', output_file='raw_reboot_folder_structure.txt'):
    """
    Lista todos os arquivos .py e .html e diretórios a partir de um determinado caminho 
    e salva a estrutura em um arquivo.

    Args:
        startpath (str, optional): O caminho inicial para começar a listar arquivos e diretórios.
                                   O padrão é o diretório atual.
        output_file (str, optional): O nome do arquivo de saída.
                                      O padrão é 'reboot_folder_structure.txt'.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            # Write the directories without filtering
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))

            # Filter out non-.py and non-.html files
            files = [file for file in files if file.endswith(('.py', '.html'))]

            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write('{}{}\n'.format(subindent, file))


def generate_report(root_dir='.', project_description="You are a Django expert tasked with assisting in the development and improvement of a Django project.  You will be provided with the complete project structure, including all files and their contents. Your role is to analyze this information and provide guidance, corrections, and assistance in building new features and directories. Be specific to show the directory path when suggesting a code alteration."):
    """
    Gera um relatório com a descrição do projeto, estrutura de diretórios e trechos de código.

    Args:
        root_dir (str, optional): O diretório raiz do projeto.
                                  O padrão é o diretório atual.
        project_description (str, optional): A descrição do projeto.
    """
    list_files(root_dir)
    gather_code_snippets(root_dir)

    with open('raw_project_report.txt', 'w', encoding='utf-8') as report_file:
        report_file.write(project_description + "\n\n")

        report_file.write("Project Structure:\n")
        with open('raw_reboot_folder_structure.txt', 'r', encoding='utf-8') as structure_file:
            report_file.write(structure_file.read() + "\n\n")

        report_file.write("Codes in my project:\n")
        with open('raw_code_summary.txt', 'r', encoding='utf-8') as code_file:
            report_file.write(code_file.read())

    print("Relatório do projeto gerado com sucesso em raw_project_report.txt")


# Exemplo de uso
generate_report()