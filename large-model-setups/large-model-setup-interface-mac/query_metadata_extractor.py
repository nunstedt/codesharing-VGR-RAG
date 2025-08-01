import os
import json
import difflib
from typing import Iterable, Optional
from llama_index.core import Settings
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterOperator



from IPython import embed  # For debugging purposes

# Remove hardcoded configuration - use config.py instead


_PROMPT_TEMPLATE = """
You are a metadata extraction assistant.
Below is the list of supported documents:
{titles_list}

If the user’s query mentions one or more of these (even if slightly misspelled),
output a JSON array of titles under the key "pdf_titles":
  {{"pdf_titles": ["<title1>", "<title2>", ...]}}

If none is referenced, output {{ "pdf_titles": [] }}.

If the query contains the term "AI" (case‑insensitive), include every title that contains "AI".

# Examples
Query: Summarize obligations in the EU AI Akct and NIS2.
Output:
{{"pdf_titles": ["EU AI Act", "NIS2"]}}

Query: What does MDR say about invasive devices?
Output:
{{"pdf_titles": ["Medical Device Regulation (MDR)"]}}

Query: What does the EU AI Act say about high-risk AI?
Output:
{{"pdf_titles": ["EU AI Act", "Commission Guidelines on AI Prohibitions", "High Level Summary of the AI Act"]}}
"""

def _strip_code_block(raw: str) -> str:
    """
    Remove Markdown code fences and optional 'json' specifier from the LLM output.

    Args:
        raw: The raw response string from the LLM.

    Returns:
        The cleaned JSON string without markdown fences or language tags.
    """
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[len("json"):].strip()
    return raw


def fuzzy_map_title(
    raw_title: str,
    known_titles: Iterable[str],
    cutoff: float = 0.6
) -> Optional[str]:
    """
    Fuzzy-match a raw title against a set of known titles.

    Args:
        raw_title: Title string extracted from the LLM.
        known_titles: Iterable of canonical document titles.
        cutoff: Minimum difflib similarity (0–1) to accept.

    Returns:
        The best-matching canonical title or None if no match meets the cutoff.
    """
    matches = difflib.get_close_matches(raw_title, list(known_titles), n=1, cutoff=cutoff)
    return matches[0] if matches else None


def validate_metadata_filters(
    filters: MetadataFilters,
    known_titles: Iterable[str],
    cutoff: float = 0.6
) -> MetadataFilters:
    """
    Validate and normalize MetadataFilters by fuzzy-matching 'pdf_title' values.

    Args:
        filters: MetadataFilters returned by extract_metadata_filters.
        known_titles: Iterable of allowed document titles.
        cutoff: difflib similarity threshold for fuzzy matching.

    Returns:
        A MetadataFilters containing only filters whose values
        match a known title, normalized to the canonical title.
    """
    valid = []
    for f in filters.filters:
        if f.key != "pdf_title":
            continue
        canon = fuzzy_map_title(f.value, known_titles, cutoff)
        if canon:
            valid.append(
                MetadataFilter(key="pdf_title", value=canon, operator=f.operator)
            )

    # embed()

    return MetadataFilters(filters=valid)


def extract_metadata_filters(
    query: str,
    known_titles: Iterable[str],
) -> MetadataFilters:
    """
    Extract metadata filters from a user query using the LLM, constrained to known_titles.

    Args:
        query: The user's natural-language question.
        known_titles: Iterable of canonical document titles.

    Returns:
        A MetadataFilters object with any extracted 'pdf_title' filters.
    """
    # Build a sorted, numbered list for consistency
    titles_list = "\n".join(f"{i+1}. {t}" for i, t in enumerate(sorted(known_titles)))
    prompt = _PROMPT_TEMPLATE.format(titles_list=titles_list)


    response = Settings.llm.complete(
        prompt=f"{prompt}\nQuery: {query}\nOutput:",
        max_tokens=100,
        temperature=0.0,
    )
    # for debugging
    # print(f"meta data extraction response: {response.text.strip()}")
    
    raw = _strip_code_block(response.text.strip())
    try:
        metadata = json.loads(raw)
        # parse the array instead of a single dict
        titles = metadata.get("pdf_titles", [])
        filters = [
            MetadataFilter(key="pdf_title", value=title, operator=FilterOperator.EQ)
            for title in titles
        ]
        
        # # For debugging purposes, can remove for production
        # embed()
        
        
        return MetadataFilters(filters=filters)
    except json.JSONDecodeError as e:
        print(f"[ERROR] … {e}")
        return MetadataFilters(filters=[])

if __name__ == "__main__":
    KNOWN_TITLES = {
    "Commission Guidelines on AI Prohibitions",
    "Critical Entity Resilience (CER)",
    "EU AI Act",
    "High Level Summary of the AI Act",
    "ISO 27002",
    "Medical Device Regulation (MDR)",
    "NIS2 Directive",
    "Policy för säkerhet och beredskap 2025-2029",
    "Protective Security Act"
    }
    
    query = "What does the EU AI Act say about high risk AI systems?"
    raw_filters = extract_metadata_filters(query, KNOWN_TITLES)
    filters = validate_metadata_filters(raw_filters, KNOWN_TITLES)
    print(filters)
    # Expected: MetadataFilters(filters=[MetadataFilter(key='pdf_title', value='EU AI Act', operator='==')])