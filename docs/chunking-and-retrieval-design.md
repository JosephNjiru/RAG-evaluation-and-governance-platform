# Chunking and retrieval design

Stage 2 uses section-aware chunking because the corpus is already structured into auditable policy and procedure sections.

Each chunk carries:

- chunk ID
- document ID
- section ID
- title
- version
- date
- owner
- risk domain
- section heading

TF-IDF retrieval is the first baseline. It is transparent, fast and deterministic. This makes failures easier to inspect than with heavier embedding models. Later stages can compare TF-IDF against embedding-based retrieval, but TF-IDF remains the baseline for local checks.

The indexed text includes document title, section heading, risk domain and section body. Returned chunks still preserve the original section text for citation and evaluation, so retrieval can benefit from human-readable headings without changing evidence content.
