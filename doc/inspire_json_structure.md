# INSPIRE-HEP JSON Structure

This document provides an explanation of the structure and contents of the INSPIRE-HEP API response JSON file (`inspirehep_result.json`).

## Top-level Structure

The INSPIRE-HEP JSON response has two main top-level components:

```json
{
  "hits": { ... },
  "links": { ... }
}
```

- **hits**: Contains the search results and total count
- **links**: Contains pagination and format links for the API

## The `hits` Object

The `hits` object contains:

```json
"hits": {
  "hits": [ ... ],  // Array of literature records
  "total": 55       // Total number of records matching the search query
}
```

- **hits**: An array of literature records (papers) matching the search query
- **total**: The total count of matching records (55 in this case)

## Literature Record Structure

Each literature record in the `hits.hits` array has the following structure:

```json
{
  "created": "YYYY-MM-DDTHH:MM:SS+00:00",    // Creation date in the database
  "id": "233030",                            // Unique identifier
  "updated": "YYYY-MM-DDTHH:MM:SS+00:00",    // Last update timestamp
  "metadata": { ... },                       // Main content of the record
  "links": { ... }                           // Links to different formats
}
```

## The `metadata` Object

The `metadata` object contains the most important information about the publication:

```json
"metadata": {
  "citation_count": 32,                     // Number of citations
  "citation_count_without_self_citations": 25,
  "authors": [ ... ],                       // Array of author objects
  "publication_info": [ ... ],              // Journal publication details
  "citeable": true,
  "$schema": "https://inspirehep.net/schemas/records/hep.json",
  "keywords": [ ... ],                      // Subject keywords
  "references": [ ... ],                    // Cited references
  "number_of_pages": 4,
  "referenced_authors_bais": [ ... ],       // Referenced authors
  "legacy_version": "20160616173051.0",
  "inspire_categories": [ ... ],            // Subject categories
  "legacy_creation_date": "1986-09-21",
  "preprint_date": "1986",
  "author_count": 1,
  "first_author": { ... },                  // First author details
  "control_number": 233030,
  "dois": [ ... ],                          // Digital Object Identifiers
  "earliest_date": "1986",
  "document_type": ["article"],
  "texkeys": ["Affleck:1986sc"],
  "abstracts": [ ... ],                     // Article abstracts
  "refereed": true,                         // Peer-reviewed status
  "titles": [ ... ],                        // Article titles
  "external_system_identifiers": [ ... ],   // IDs in other systems
  "facet_author_name": [ ... ],
  "core": true,
  "curated": true,
  "journal_title_variants": [ ... ]         // Variants of journal title
}
```

### Author Object Structure

Each author in the `authors` array includes:

```json
{
  "full_name_unicode_normalized": "affleck, i.",
  "full_name": "Affleck, I.",
  "record": {
    "$ref": "https://inspirehep.net/api/authors/1018910"
  },
  "ids": [ ... ],                           // Author identifiers
  "affiliations": [ ... ],                  // Author affiliations
  "last_name": "Affleck",
  "signature_block": "AFLACi",
  "first_name": "I.",
  "uuid": "a3e67525-d5c3-4251-8252-3d6dbda4955f",
  "recid": 1018910
}
```

### Publication Info Structure

The `publication_info` array contains journal publication details:

```json
{
  "journal_volume": "56",
  "page_end": "2766",
  "year": 1986,
  "journal_record": {
    "$ref": "https://inspirehep.net/api/journals/1214495"
  },
  "page_start": "2763",
  "journal_title": "Phys.Rev.Lett."
}
```

### References Structure

Each reference in the `references` array contains:

```json
{
  "reference": {
    "publication_info": { ... }
  },
  "curated_relation": false,
  "record": {
    "$ref": "https://inspirehep.net/api/literature/17876"
  }
}
```

### Abstracts Structure

The `abstracts` array contains the paper's abstract(s):

```json
{
  "source": "APS",
  "value": "The exact T=0 susceptibility times spin-wave velocity of an isotropic spin-s antiferromagnetic chain is calculated...",
  "abstract_source_suggest": {
    "input": "APS"
  }
}
```

### Titles Structure

The `titles` array contains the paper's title(s):

```json
{
  "title": "Realization of a Witten Critical Theory in (Ch-3)-4 Nmncl-3"
}
```

## The `links` Object for Literature Records

Each record includes links to different formats of the publication:

```json
"links": {
  "bibtex": "https://inspirehep.net/api/literature/233030?format=bibtex",
  "latex-eu": "https://inspirehep.net/api/literature/233030?format=latex-eu",
  "latex-us": "https://inspirehep.net/api/literature/233030?format=latex-us",
  "json": "https://inspirehep.net/api/literature/233030?format=json",
  "cv": "https://inspirehep.net/api/literature/233030?format=cv",
  "citations": "https://inspirehep.net/api/literature/?q=refersto%3Arecid%3A233030"
}
```

## Top-level `links` Object

The top-level `links` object provides navigation links for the API results:

```json
"links": {
  "self": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1",
  "next": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=2",
  "bibtex": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1&format=bibtex",
  "latex-eu": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1&format=latex-eu",
  "latex-us": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1&format=latex-us",
  "json": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1&format=json",
  "cv": "https://inspirehep.net/api/literature/?q=%22a+Witten%22&size=10&page=1&format=cv"
}
```

These links allow for:
- Navigation between pages of results
- Obtaining the results in different formats (BibTeX, LaTeX, JSON, etc.)

## Special Features

### Citations and References

The JSON includes detailed citation information:
- **citation_count**: The number of times this paper has been cited
- **references**: The works cited by this paper
- **referenced_authors_bais**: The authors cited by this paper

### Affiliations

Author affiliations are included with institutional IDs:

```json
"affiliations": [
  {
    "record": {
      "$ref": "https://inspirehep.net/api/institutions/903139"
    },
    "value": "Princeton U."
  }
]
```

### DOIs and External Identifiers

Digital Object Identifiers and other external system IDs:

```json
"dois": [
  {
    "value": "10.1103/PhysRevLett.56.2763"
  }
],
"external_system_identifiers": [
  {
    "schema": "ADS",
    "value": "1986PhRvL..56.2763A"
  },
  {
    "schema": "SPIRES",
    "value": "SPIRES-1576356"
  }
]
```

## Search Context

This particular JSON appears to be the results of a search for papers containing the phrase "a Witten" - likely referring to work related to physicist Edward Witten or Witten-type theories. The response includes 10 papers (out of 55 total matches) on various topics in theoretical physics.