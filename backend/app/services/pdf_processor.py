"""PDF processing service with position tracking for citations."""
import logging
from typing import List, Dict, Any
from pathlib import Path
import pdfplumber
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextSegment:
    """Text segment with position information."""
    text: str
    page_number: int
    char_start: int  # Character position within the page
    char_end: int
    bbox: tuple  # Bounding box (x0, y0, x1, y1) for potential future use


class PDFProcessor:
    """Process PDFs and extract text with position tracking."""

    def __init__(self):
        """Initialize PDF processor."""
        pass

    def extract_text_with_positions(self, pdf_path: str) -> tuple[List[TextSegment], Dict[str, Any]]:
        """
        Extract text from PDF with position tracking.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (list of TextSegments, document metadata)
        """
        segments = []
        metadata = {
            "page_count": 0,
            "total_chars": 0,
            "file_size": Path(pdf_path).stat().st_size
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                metadata["page_count"] = len(pdf.pages)

                # Track character positions across the entire document
                document_char_offset = 0

                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text with character-level positions
                    page_text = page.extract_text()

                    if not page_text:
                        logger.warning(f"No text found on page {page_num}")
                        continue

                    # For citation tracking, we need to know where each chunk of text is
                    # We'll create segments based on paragraphs (double newlines)
                    paragraphs = page_text.split('\n\n')
                    page_char_offset = 0

                    for para in paragraphs:
                        if para.strip():
                            segment = TextSegment(
                                text=para.strip(),
                                page_number=page_num,
                                char_start=document_char_offset + page_char_offset,
                                char_end=document_char_offset + page_char_offset + len(para),
                                bbox=(0, 0, page.width, page.height)  # Full page bbox for now
                            )
                            segments.append(segment)

                        page_char_offset += len(para) + 2  # +2 for '\n\n'

                    metadata["total_chars"] += len(page_text)
                    document_char_offset += len(page_text)

                logger.info(f"Extracted {len(segments)} segments from {metadata['page_count']} pages")

        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise

        return segments, metadata

    def validate_pdf(self, pdf_path: str) -> bool:
        """
        Validate that the file is a valid PDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            True if valid, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Try to access first page to verify it's a valid PDF
                if len(pdf.pages) > 0:
                    return True
                return False
        except Exception as e:
            logger.error(f"PDF validation failed for {pdf_path}: {e}")
            return False

    def get_page_count(self, pdf_path: str) -> int:
        """
        Get the number of pages in a PDF.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Number of pages
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            logger.error(f"Error getting page count for {pdf_path}: {e}")
            return 0
