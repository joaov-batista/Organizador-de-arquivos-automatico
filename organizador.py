import os
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit

# Definindo as categorias de arquivos e suas extensões associadas
EXTENSOES = {
    'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.odt', '.rtf', '.csv', '.epub', '.md', '.tex', '.log', '.json'],
    'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.psd', '.ai', '.eps', '.raw', '.indd'],
    'Vídeos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.m4v'],
    'Áudio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.alac', '.wma', '.opus', '.aiff', '.pcm'],
    'Código': ['.py', '.java', '.cpp', '.js', '.html', '.css', '.php', '.go', '.swift', '.ts', '.rb', '.vb', '.json', '.xml', '.yml', '.sh'],
    'Arquivos Compactados': ['.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tar.bz2', '.gz', '.xz', '.iso'],
    'Fontes': ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.sfnt'],
    'Outros': []  # Categoria para arquivos não classificados
}

# Função que organiza os arquivos no diretório especificado
def organizar_arquivos(diretorio):
    # Verifica se o diretório existe
    if not os.path.exists(diretorio):
        QMessageBox.critical(None, "Erro", f"O diretório '{diretorio}' não existe.")
        return
    
    # Itera sobre todos os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        
        # Verifica se é um arquivo (não uma pasta)
        if os.path.isfile(caminho_arquivo):
            _, ext = os.path.splitext(arquivo)  # Obtém a extensão do arquivo
            ext = ext.lower()  # Converte a extensão para minúsculas
            movido = False  # Flag para indicar se o arquivo foi movido

            # Verifica a categoria do arquivo com base na sua extensão
            for categoria, extensoes in EXTENSOES.items():
                if ext in extensoes:
                    pasta_categoria = os.path.join(diretorio, categoria)
                    
                    # Cria a pasta da categoria, se não existir
                    if not os.path.exists(pasta_categoria):
                        os.makedirs(pasta_categoria)
                    
                    # Move o arquivo para a pasta correspondente
                    shutil.move(caminho_arquivo, os.path.join(pasta_categoria, arquivo))
                    movido = True
                    break

            # Se o arquivo não pertence a nenhuma das categorias, coloca-o na pasta 'Outros'
            if not movido:
                pasta_outros = os.path.join(diretorio, 'Outros')
                if not os.path.exists(pasta_outros):
                    os.makedirs(pasta_outros)
                shutil.move(caminho_arquivo, os.path.join(pasta_outros, arquivo))
    
    # Exibe uma mensagem de sucesso após a organização
    QMessageBox.information(None, "Sucesso", "Arquivos organizados com sucesso!")

# Classe da interface gráfica para o organizador de arquivos
class OrganizadorArquivos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organizador de Arquivos")  # Define o título da janela
        self.setGeometry(100, 100, 500, 200)  # Define o tamanho e a posição da janela

        # Layout vertical para os widgets
        layout = QVBoxLayout()

        # Label explicativa
        self.label = QLabel("Selecione o diretório para organizar:")
        layout.addWidget(self.label)

        # Campo de entrada para o diretório
        self.entrada_diretorio = QLineEdit()
        layout.addWidget(self.entrada_diretorio)

        # Botão para selecionar o diretório
        self.botao_selecionar = QPushButton("Escolher Pasta")
        self.botao_selecionar.clicked.connect(self.selecionar_pasta)
        layout.addWidget(self.botao_selecionar)

        # Botão para iniciar a organização dos arquivos
        self.botao_organizar = QPushButton("Organizar")
        self.botao_organizar.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.botao_organizar.clicked.connect(self.iniciar_organizacao)
        layout.addWidget(self.botao_organizar)

        # Define o layout da janela
        self.setLayout(layout)

    # Função para abrir o dialogo de seleção de pasta
    def selecionar_pasta(self):
        pasta_selecionada = QFileDialog.getExistingDirectory(self, "Selecionar Diretório")
        if pasta_selecionada:
            self.entrada_diretorio.setText(pasta_selecionada)  # Exibe o diretório selecionado

    # Função que inicia a organização dos arquivos
    def iniciar_organizacao(self):
        diretorio = self.entrada_diretorio.text()  # Obtém o diretório da entrada de texto
        organizar_arquivos(diretorio)  # Chama a função para organizar os arquivos no diretório

# Inicializa a aplicação e exibe a interface gráfica
if __name__ == "__main__":
    app = QApplication([])  # Cria a aplicação Qt
    janela = OrganizadorArquivos()  # Cria a janela principal
    janela.show()  # Exibe a janela
    app.exec()  # Executa a aplicação