"""
Utilitários para processamento de arquivos.
"""
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple, List
import streamlit as st
from PIL import Image
import io


class FileProcessor:
    """Utilitário para processamento de arquivos."""
    
    # Tipos de arquivo suportados
    SUPPORTED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'],
        'pdf': ['.pdf'],
        'document': ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    }
    
    # Tamanho máximo de arquivo (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @classmethod
    def is_supported_file(cls, file_path: str) -> bool:
        """Verifica se o arquivo é suportado."""
        extension = Path(file_path).suffix.lower()
        return extension in cls.SUPPORTED_EXTENSIONS['document']
    
    @classmethod
    def is_image_file(cls, file_path: str) -> bool:
        """Verifica se o arquivo é uma imagem."""
        extension = Path(file_path).suffix.lower()
        return extension in cls.SUPPORTED_EXTENSIONS['image']
    
    @classmethod
    def is_pdf_file(cls, file_path: str) -> bool:
        """Verifica se o arquivo é um PDF."""
        extension = Path(file_path).suffix.lower()
        return extension in cls.SUPPORTED_EXTENSIONS['pdf']
    
    @classmethod
    def validate_file_size(cls, file_path: str) -> bool:
        """Valida o tamanho do arquivo."""
        try:
            file_size = os.path.getsize(file_path)
            return file_size <= cls.MAX_FILE_SIZE
        except OSError:
            return False
    
    @classmethod
    def get_file_info(cls, file_path: str) -> Tuple[str, int, str]:
        """Retorna informações do arquivo."""
        path = Path(file_path)
        file_size = os.path.getsize(file_path)
        file_type = path.suffix.lower()
        
        return str(path.name), file_size, file_type
    
    @classmethod
    def save_uploaded_file(cls, uploaded_file) -> Optional[str]:
        """Salva arquivo enviado via Streamlit."""
        try:
            if uploaded_file is None:
                return None
            
            # Cria diretório temporário
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            
            # Salva o arquivo
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return temp_path
            
        except Exception as e:
            st.error(f"Erro ao salvar arquivo: {str(e)}")
            return None
    
    @classmethod
    def cleanup_temp_file(cls, file_path: str) -> None:
        """Remove arquivo temporário."""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                # Remove diretório pai se estiver vazio
                parent_dir = os.path.dirname(file_path)
                if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                    os.rmdir(parent_dir)
        except Exception as e:
            st.warning(f"Erro ao limpar arquivo temporário: {str(e)}")
    
    @classmethod
    def convert_image_to_bytes(cls, image_path: str) -> Optional[bytes]:
        """Converte imagem para bytes."""
        try:
            with open(image_path, 'rb') as f:
                return f.read()
        except Exception as e:
            st.error(f"Erro ao converter imagem: {str(e)}")
            return None
    
    @classmethod
    def resize_image_if_needed(cls, image_path: str, max_size: Tuple[int, int] = (1920, 1080)) -> str:
        """Redimensiona imagem se necessário."""
        try:
            with Image.open(image_path) as img:
                # Verifica se precisa redimensionar
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Salva imagem redimensionada
                    temp_path = tempfile.mktemp(suffix=Path(image_path).suffix)
                    img.save(temp_path, quality=85, optimize=True)
                    return temp_path
                
                return image_path
                
        except Exception as e:
            st.warning(f"Erro ao redimensionar imagem: {str(e)}")
            return image_path
    
    @classmethod
    def validate_uploaded_file(cls, uploaded_file) -> Tuple[bool, str]:
        """Valida arquivo enviado via Streamlit."""
        if uploaded_file is None:
            return False, "Nenhum arquivo foi enviado."
        
        # Verifica extensão
        file_name = uploaded_file.name
        if not cls.is_supported_file(file_name):
            supported_extensions = ", ".join(cls.SUPPORTED_EXTENSIONS['document'])
            return False, f"Tipo de arquivo não suportado. Suportados: {supported_extensions}"
        
        # Verifica tamanho
        file_size = len(uploaded_file.getbuffer())
        if file_size > cls.MAX_FILE_SIZE:
            max_size_mb = cls.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"Arquivo muito grande. Tamanho máximo: {max_size_mb}MB"
        
        return True, "Arquivo válido."
    
    @classmethod
    def get_document_type_from_filename(cls, filename: str) -> str:
        """Tenta inferir o tipo de documento pelo nome do arquivo."""
        filename_lower = filename.lower()
        
        if any(keyword in filename_lower for keyword in ['cnh', 'habilitacao', 'carteira']):
            return 'cnh'
        elif any(keyword in filename_lower for keyword in ['rg', 'registro', 'identidade']):
            return 'rg'
        else:
            return 'Não reconhecido tipo de documento, exemplo: cnh.pdf, rg.png, etc...'
    
    @classmethod
    def create_temp_file_path(cls, original_filename: str) -> str:
        """Cria caminho para arquivo temporário."""
        temp_dir = tempfile.mkdtemp()
        return os.path.join(temp_dir, original_filename)


class DocumentAnalyzer:
    """Analisador de documentos."""
    
    @staticmethod
    def analyze_document_content(file_path: str) -> dict:
        """Analisa o conteúdo do documento para inferir tipo."""
        try:
            file_info = FileProcessor.get_file_info(file_path)
            filename, file_size, file_type = file_info
            
            analysis = {
                "filename": filename,
                "file_size": file_size,
                "file_type": file_type,
                "inferred_document_type": FileProcessor.get_document_type_from_filename(filename),
                "is_image": FileProcessor.is_image_file(file_path),
                "is_pdf": FileProcessor.is_pdf_file(file_path)
            }
            
            return analysis
            
        except Exception as e:
            st.error(f"Erro ao analisar documento: {str(e)}")
            return {}
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> Optional[str]:
        """Extrai texto de imagem usando OCR básico."""
        try:
            # Aqui você pode integrar com python-doctr ou outra biblioteca OCR
            # Por enquanto, retorna None
            return None
        except Exception as e:
            st.warning(f"Erro ao extrair texto da imagem: {str(e)}")
            return None 