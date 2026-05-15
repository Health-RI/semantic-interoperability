# Health-RI SSSOM Mapping Set

<!-- [Download the full SSSOM mapping.](../../mappings/health-ri-mappings.tsv) -->

!!! warning "Use with care"
    The current mapping set contains inconsistencies. We are aware of these issues, but no further release activity is currently planned while the initiative is paused. Until then, please use the mappings with care.

!!! note "Scope"
    This page **visualizes** the mappings that already exist. For the Mapping Set's schema and stable PIDs, see the **[SSSOM Mapping Set](../method/mapping-schema.md)**.

!!! note "Enable the Comment column"
    We recommend enabling the **comment** column so that each entry can be better understood.

!!! tip "Need help mapping your terms to HRIO?"
    Use the **[HRIO Mapping Assistant](https://chatgpt.com/g/g-6990a7e348c4819190ef2de88503ff5e-hrio-mapping-assistant)** to draft candidate mappings (one HRIV predicate + confidence + evidence snippets):

    *Drafting aid only — while the initiative is paused, contributed mappings are not actively reviewed, curated, or scheduled for release.*

This table is automatically generated from the SSSOM TSV:

<input type="text" id="tableSearchInput" placeholder="Search mappings...">

<div id="columnToggles"></div>

{{ read_csv('deliverables/assets/health-ri-mappings.tsv', sep='\t') }}
