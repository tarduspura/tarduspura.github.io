---
name: course-note-transcriber
description: Convert uploaded lecture PDFs, slides, handouts, OCR text, or class transcripts into structured Markdown course notes that match Mayazar's personal notes under note/docs/courses. Use when Codex is asked to transcribe, summarize, reorganize, or turn a PDF into logical Chinese course notes with frontmatter, numbered headings, formulas, figures, tables, algorithms, and Chinese/English technical terminology.
---

# Course Note Transcriber

## Workflow

1. Identify the source PDF or transcript and the intended course/lecture target.
   - If the target path is not specified, infer `note/docs/courses/<course>/<course>_lecN.md` from nearby files and the lecture title.
   - Use today's date only when the user explicitly wants a new note date and the PDF does not provide one.

2. Extract the PDF content.
   - Prefer native text extraction before OCR.
   - Use `scripts/extract_pdf_text.py` when a local PDF path is available:

```bash
python path/to/course-note-transcriber/scripts/extract_pdf_text.py lecture.pdf --out lecture.extracted.md
```

3. Read `references/mayazar-note-style.md` before drafting.

4. Build a logical outline before writing.
   - Preserve the lecture's conceptual order when it is already coherent.
   - Reorder slide fragments only when doing so makes prerequisites, definitions, examples, and conclusions easier to follow.
   - Keep page/slide evidence in mind, but do not produce a slide-by-slide dump.

5. Write the note as a clean Markdown document.
   - Use YAML frontmatter, numbered headings, short bullets, nested bullets, MathJax LaTeX, and MkDocs admonitions.
   - Preserve important English terms and acronyms beside Chinese explanations.
   - Convert dense slide text into concise explanatory notes; avoid copying whole paragraphs unless the source wording is a definition that should be retained.

6. Handle uncertainty honestly.
   - Mark unresolved OCR or unclear symbols as `TODO:` or `(check against source)`.
   - Do not invent theorem statements, parameters, proofs, or diagram details not supported by the source.

7. Finish with a quick quality pass.
   - Check heading numbering, frontmatter, formula delimiters, image paths/placeholders, table alignment, and whether the note reads like the existing notes rather than a generic summary.

## Figure Handling

- If figures are extracted or already available, place them under `note/docs/images/` and link with the same relative style as existing notes, such as `![name](../../images/pc.6.1.jpg)`.
- If image extraction is not requested or not possible, summarize the figure's role in nearby bullets and leave a compact `TODO` only when the diagram is essential.
- Keep alt text short and lowercase or mnemonic: `![process]`, `![eg1]`, `![proof]`, `![cache]`.

## Output Contract

Return either:

- the created/updated Markdown file path, with a short summary of important choices; or
- the full Markdown note when the user asks for inline output.

When editing files, keep the note scoped to the requested lecture and do not rewrite unrelated notes.
