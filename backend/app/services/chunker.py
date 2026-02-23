"""Intelligent text chunking with metadata preservation."""
import logging
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.pdf_processor import TextSegment
from app.config import settings
import uuid

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """A chunk of text with preserved metadata for citations."""
    chunk_id: str
    text: str
    page_number: int
    char_start: int
    char_end: int
    document_id: str
    chunk_index: int  # Order within the document
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return asdict(self)


class IntelligentChunker:
    """Chunk documents while preserving citation metadata."""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """
        Initialize the chunker.

        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        # Use LangChain's recursive splitter for intelligent chunking
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",  # Paragraph breaks
                "\n",    # Line breaks
                ". ",    # Sentences
                " ",     # Words
                ""       # Characters
            ]
        )

    def chunk_segments(
        self,
        segments: List[TextSegment],
        document_id: str,
        filename: str
    ) -> List[DocumentChunk]:
        """
        Chunk text segments while preserving position metadata.

        Args:
            segments: List of text segments from PDF processor
            document_id: Unique identifier for the document
            filename: Original filename

        Returns:
            List of DocumentChunks with preserved metadata
        """
        chunks = []
        chunk_index = 0

        for segment in segments:
            # Split the segment text into chunks
            segment_chunks = self.splitter.split_text(segment.text)

            # Track position within the segment
            segment_char_offset = 0

            for chunk_text in segment_chunks:
                # Calculate absolute position
                absolute_char_start = segment.char_start + segment_char_offset
                absolute_char_end = absolute_char_start + len(chunk_text)

                # Create chunk with full metadata
                chunk = DocumentChunk(
                    chunk_id=f"{document_id}_chunk_{chunk_index}",
                    text=chunk_text,
                    page_number=segment.page_number,
                    char_start=absolute_char_start,
                    char_end=absolute_char_end,
                    document_id=document_id,
                    chunk_index=chunk_index,
                    metadata={
                        "filename": filename,
                        "document_id": document_id,
                        "page": segment.page_number,
                        "char_start": absolute_char_start,
                        "char_end": absolute_char_end,
                        "chunk_id": f"{document_id}_chunk_{chunk_index}"
                    }
                )

                chunks.append(chunk)
                chunk_index += 1

                # Update offset for next chunk in this segment
                # Find where this chunk appears in the original segment text
                chunk_position = segment.text[segment_char_offset:].find(chunk_text)
                if chunk_position != -1:
                    segment_char_offset += chunk_position + len(chunk_text)
                else:
                    # Fallback if exact match not found (shouldn't happen)
                    segment_char_offset += len(chunk_text)

        logger.info(f"Created {len(chunks)} chunks from {len(segments)} segments")
        return chunks

    def merge_overlapping_chunks(self, chunks: List[DocumentChunk]) -> List[DocumentChunk]:
        """
        Merge chunks that have significant overlap (for deduplication).

        Args:
            chunks: List of chunks to potentially merge

        Returns:
            List of merged chunks
        """
        if not chunks:
            return []

        # Sort by page and position
        sorted_chunks = sorted(chunks, key=lambda c: (c.page_number, c.char_start))

        merged = [sorted_chunks[0]]

        for current_chunk in sorted_chunks[1:]:
            last_merged = merged[-1]

            # Check if chunks overlap significantly (>50% overlap)
            if (current_chunk.page_number == last_merged.page_number and
                current_chunk.char_start < last_merged.char_end):

                overlap_start = current_chunk.char_start
                overlap_end = min(current_chunk.char_end, last_merged.char_end)
                overlap_size = overlap_end - overlap_start

                # If overlap is significant, merge
                if overlap_size > len(current_chunk.text) * 0.5:
                    # Extend the last merged chunk
                    last_merged.text = last_merged.text + current_chunk.text[overlap_size:]
                    last_merged.char_end = current_chunk.char_end
                    continue

            merged.append(current_chunk)

        logger.info(f"Merged {len(chunks)} chunks into {len(merged)} chunks")
        return merged
