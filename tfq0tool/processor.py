"""File processing module with support for parallel processing and progress tracking."""

import os
import logging
import signal
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from threading import Event
import queue
from tqdm import tqdm

from .extractors import get_extractor
from .utils import (
    setup_logging,
    create_output_path,
    get_file_size,
    validate_file_type,
    is_binary_file
)
from .config import config

logger = logging.getLogger(__name__)

class ProcessingError(Exception):
    """Custom exception for processing errors."""
    pass

class FileProcessor:
    """Handles file processing operations."""
    
    def __init__(
        self,
        file_paths: List[str],
        output_dir: Optional[str] = None,
        num_threads: Optional[int] = None,
        force: bool = False,
        preprocessing_options: Optional[Dict[str, Any]] = None,
        output_format: str = 'txt'
    ):
        """Initialize the processor."""
        self.file_paths = [Path(p) for p in file_paths]
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.num_threads = num_threads
        self.force = force
        self.preprocessing_options = preprocessing_options or {}
        self.output_format = output_format.lower()
        self.failed_files = []
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure threading
        self.num_threads = self._configure_threads(num_threads)
        
        # Validate inputs
        self._validate_inputs()
        
        # Setup result tracking
        self.results_queue = queue.Queue()
    
    def _configure_threads(self, num_threads: Optional[int]) -> int:
        """Configure number of threads based on config and system resources."""
        if num_threads is None:
            num_threads = os.cpu_count() or 1
        
        min_threads = config.get("threading", "min_threads")
        max_threads = config.get("threading", "max_threads")
        
        return max(min_threads, min(num_threads, max_threads))
    
    def _validate_inputs(self) -> None:
        """Validate input files and paths."""
        for file_path in self.file_paths:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.is_file():
                raise ValueError(f"Not a file: {file_path}")
            
            if not validate_file_type(file_path):
                raise ValueError(f"Unsupported file type: {file_path}")
            
            file_size = get_file_size(file_path)
            max_size = config.get("processing", "max_file_size")
            if file_size > max_size:
                raise ValueError(
                    f"File too large: {file_path} ({file_size} bytes > {max_size} bytes)"
                )
    
    def _get_output_path(self, input_path: Path) -> Path:
        """Generate output path based on input path and format."""
        # Get the stem (filename without extension)
        stem = input_path.stem
        
        # Determine output extension based on format
        format_extensions = {
            'txt': '.txt',
            'json': '.json',
            'csv': '.csv',
            'md': '.md',
            'docx': '.docx'  # Add support for DOCX output
        }
        
        # Use the specified format's extension, fallback to txt
        ext = format_extensions.get(self.output_format, '.txt')
        
        # Create output path
        return self.output_dir / f"{stem}{ext}"
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file."""
        try:
            # Get output path
            output_path = self._get_output_path(file_path)
            
            # Check if output file exists and handle force flag
            if output_path.exists() and not self.force:
                logger.warning(f"Output file already exists: {output_path}")
                return False
            
            # Process the file based on its type and desired output format
            if self.output_format == 'docx':
                # Handle conversion to DOCX
                self._convert_to_docx(file_path, output_path)
            else:
                # Handle other formats
                self._process_generic(file_path, output_path)
            
            logger.info(f"Successfully processed: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            self.failed_files.append(file_path)
            return False
    
    def _convert_to_docx(self, input_path: Path, output_path: Path) -> None:
        """Convert input file to DOCX format."""
        from docx import Document
        
        # Create a new Word document
        doc = Document()
        
        # Read input file content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add content to document
        doc.add_paragraph(content)
        
        # Save the document
        doc.save(str(output_path))
    
    def _process_generic(self, input_path: Path, output_path: Path) -> None:
        """Process file for non-DOCX output formats."""
        # Add your existing processing logic here
        pass
    
    def _handle_interrupt(self, signum, frame):
        """Handle interrupt signal."""
        logger.info("\nInterrupt received, stopping gracefully...")
        self.stop_event.set()
    
    def process_all(self) -> bool:
        """Process all files."""
        try:
            self._validate_inputs()
            
            total_files = len(self.file_paths)
            processed = 0
            
            for file_path in self.file_paths:
                if self.process_file(file_path):
                    processed += 1
                    logger.info(f"Processed {file_path.name}: {processed}/{total_files}")
            
            # Print summary
            logger.info("\nProcessing Summary:")
            logger.info(f"  Total files: {total_files}")
            logger.info(f"  Successfully processed: {processed}")
            logger.info(f"  Failed: {len(self.failed_files)}")
            
            return len(self.failed_files) == 0
            
        except Exception as e:
            logger.error(f"Error during processing: {str(e)}")
            return False
    
    def _report_statistics(self, results: List[Tuple[Path, Optional[Path], Optional[str]]]):
        """Report processing statistics."""
        total = len(results)
        successful = sum(1 for _, output_path, error in results if output_path and not error)
        failed = len(self.failed_files)
        
        logger.info("\nProcessing Summary:")
        logger.info(f"  Total files: {total}")
        logger.info(f"  Successfully processed: {successful}")
        logger.info(f"  Failed: {failed}")
        
        if failed > 0:
            logger.info("\nFailed files:")
            for file_path in self.failed_files:
                logger.info(f"  - {file_path}") 