"""Create a test PDF for demonstrating the Smart Document Assistant."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# Create PDF
pdf_path = "test_document.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Title
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor='darkblue',
    spaceAfter=30,
    alignment=TA_CENTER
)
title = Paragraph("The Future of AI Assistants", title_style)
story.append(title)
story.append(Spacer(1, 0.5*inch))

# Introduction
intro_style = styles['BodyText']
intro_style.alignment = TA_JUSTIFY
intro = Paragraph(
    """
    Artificial Intelligence assistants have revolutionized how we interact with technology.
    These intelligent systems can understand natural language, process complex queries, and
    provide accurate information from vast knowledge bases. The integration of RAG
    (Retrieval Augmented Generation) technology has enabled AI assistants to provide
    citations and references for their responses, making them more trustworthy and transparent.
    """,
    intro_style
)
story.append(intro)
story.append(Spacer(1, 0.3*inch))

# Section 1
section1_title = Paragraph("1. Document Processing Capabilities", styles['Heading2'])
story.append(section1_title)
story.append(Spacer(1, 0.2*inch))

section1_text = Paragraph(
    """
    Modern AI assistants can process various document formats including PDF, Word documents,
    and plain text files. The PDF processing pipeline typically involves extracting text
    with position tracking, which allows the system to maintain metadata about where each
    piece of text appears in the original document. This metadata includes page numbers,
    character positions, and bounding box coordinates. Such detailed tracking enables
    precise citation and reference capabilities.
    """,
    intro_style
)
story.append(section1_text)
story.append(Spacer(1, 0.3*inch))

# Section 2
section2_title = Paragraph("2. Vector Embeddings and Semantic Search", styles['Heading2'])
story.append(section2_title)
story.append(Spacer(1, 0.2*inch))

section2_text = Paragraph(
    """
    Vector embeddings transform text into numerical representations that capture semantic
    meaning. These embeddings enable semantic search, where queries are matched based on
    meaning rather than exact keyword matches. State-of-the-art embedding models like
    OpenAI's text-embedding-3-small can generate 1536-dimensional vectors that effectively
    represent the semantic content of text. The similarity between vectors is typically
    measured using cosine similarity, with scores ranging from 0 to 1.
    """,
    intro_style
)
story.append(section2_text)
story.append(Spacer(1, 0.3*inch))

# Page break
story.append(PageBreak())

# Section 3
section3_title = Paragraph("3. Citation Tracking and Transparency", styles['Heading2'])
story.append(section3_title)
story.append(Spacer(1, 0.2*inch))

section3_text = Paragraph(
    """
    The 2026 innovation in AI document assistants is precise citation tracking. When an AI
    generates an answer, it not only provides the information but also shows exactly which
    paragraphs from which pages were used to generate that answer. Each citation includes
    the page number, character start and end positions, the actual text excerpt, and a
    relevance score indicating how closely the source matches the query. This level of
    transparency builds trust and allows users to verify information directly in the source
    documents.
    """,
    intro_style
)
story.append(section3_text)
story.append(Spacer(1, 0.3*inch))

# Section 4
section4_title = Paragraph("4. Chunking and Context Preservation", styles['Heading2'])
story.append(section4_title)
story.append(Spacer(1, 0.2*inch))

section4_text = Paragraph(
    """
    Document chunking is a critical process where long documents are split into smaller,
    manageable pieces. The typical chunk size is around 1000 characters with a 200-character
    overlap between consecutive chunks. This overlap ensures that context is not lost at
    chunk boundaries. Intelligent chunking algorithms respect natural text boundaries such
    as paragraph breaks, sentence endings, and section divisions. Each chunk maintains
    metadata linking it back to its original location in the source document.
    """,
    intro_style
)
story.append(section4_text)
story.append(Spacer(1, 0.3*inch))

# Conclusion
conclusion_title = Paragraph("Conclusion", styles['Heading2'])
story.append(conclusion_title)
story.append(Spacer(1, 0.2*inch))

conclusion_text = Paragraph(
    """
    The combination of advanced NLP, vector embeddings, and precise citation tracking
    represents a significant leap forward in AI assistant technology. These systems not
    only answer questions but do so with full transparency and verifiability. As these
    technologies continue to evolve, we can expect even more sophisticated document
    understanding and knowledge retrieval capabilities in the future.
    """,
    intro_style
)
story.append(conclusion_text)

# Build PDF
doc.build(story)
print(f"Test PDF created successfully: {pdf_path}")
