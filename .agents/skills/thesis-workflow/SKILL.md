# Thesis Workflow Skill

**Purpose:** Automated thesis/project document generation using pipeline workflow  
**Triggers:** Any mention of thesis, project, proposal, presentation, topic work

---

## When to Use

- Starting a new thesis/project
- Continuing existing thesis work
- Adding research papers
- Creating proposal, report, or presentations
- Checking progress
- Finalizing documents

---

## Pipeline Structure

```
docs/proposal/thesis/
├── PIPELINE_WORKFLOW.md       # This workflow guide
├── TOPIC_LOG.md            # Tracks all topics
└── [Topic_Name]/
    ├── index.md           # Topic table of contents
    ├── 01_idea.md       # Initial idea + research notes
    ├── 02_proposal.md   # Proposal document
    ├── 03_project_report.md  # Full project report
    ├── 04_presentations/
    │   ├── mock_1.md   # Mock presentation 1
    │   ├── mock_2.md   # Mock presentation 2
    │   └── mock_3.md   # Mock presentation 3
    ├── 05_references/  # Research papers + summaries
    │   ├── [paper_name].pdf
    │   └── paper-summaries/
    │       └── paper_1_summary.md
    └── 06_notes/      # Working notes, drafts
```

---

## Available Actions

### 1. Start New Thesis
```
"Start new thesis with topic: [YOUR TOPIC IDEA]"
```
**Actions:**
- Create topic folder
- Analyze the idea
- Ask clarifying questions
- Create 01_idea.md

---

### 2. Continue Existing Thesis
```
"Continue thesis: [TOPIC NAME]"
```
**Actions:**
- Load 01_idea.md
- Check progress from index.md
- Ask what to do next

---

### 3. Add Research Paper
```
"Analyze paper: [PAPER PATH/URL]"
"Add research: [PAPER INFO]"
"Add paper: [PAPER]"
```
**Actions:**

#### Step 1: Check for Duplication
- Check if paper already exists in topic folder (by title, DOI, or similar name)
- If duplicate found → Ask user: "Paper already exists. Skip or overwrite?"

#### Step 2: Analyze Relevance
- Read paper abstract and methodology
- Compare with thesis topic (from 01_idea.md)
- If NOT relevant → Warn user: "⚠️ This paper appears unrelated to [TOPIC]. Relevance: [LOW/MEDIUM]. Still add?"
- Wait for user confirmation before proceeding

#### Step 3: Analyze (if confirmed)
- Use PDF skill to extract content
- Extract: methodology, findings, gaps, datasets, tools
- Copy paper to 05_references/
- Create paper summary in 05_references/paper-summaries/
  - Filename: `[paper_name]_summary.md`
  - Include all extracted findings
- Update 01_idea.md with research notes
- Update index.md (add to Research Papers table)

#### Step 4: Show Summary to User
After adding, display:
```
✅ Paper Added Successfully!

## Summary
| Field | Value |
|-------|-------|
| Title | [Paper Title] |
| Authors | [Author(s)] |
| Year | [Year] |
| Source | [Journal/Conference] |

## Key Findings
- [Finding 1]
- [Finding 2]

## Relevance to Thesis
[How this paper helps]

## Files Created
- 05_references/[filename].pdf
- 05_references/paper-summaries/[filename]_summary.md
```

**If duplicate found:**
```
⚠️ Duplicate Paper Detected

A paper with similar title already exists:
- Existing: [Existing paper name]
- New: [New paper name]

Options:
[1] Skip - Don't add the new paper
[2] Add anyway - Overwrite/Create new entry
```

**If irrelevant:**
```
⚠️ Relevance Warning

This paper appears UNRELATED to your thesis:
- Thesis Topic: [Topic]
- Paper Focus: [What paper is about]
- Relevance Score: LOW

Relevance reasons:
- [Reason 1]
- [Reason 2]

Options:
[1] Don't add - Find more relevant paper
[2] Add anyway - Proceed with addition
```

**Paper Summary Structure:**
```markdown
# [Paper Title]

## Metadata
| Field | Value |
|-------|-------|
| Authors | [Author(s)] |
| Year | [Year] |
| Source | [Journal/Conference] |
| DOI | [Link] |

## Abstract
[Summary of the paper]

## Methodology
[Methods used]

## Key Findings
- Finding 1
- Finding 2

## Gaps/Limitations
[What's missing or could be improved]

## Relevance to Study
[How this paper helps your research]
```

---

### 4. Create Proposal
```
"Create proposal"
"Generate proposal document"
```
**Actions:**
- Use Proposal_Format_Guide.md
- Create 02_proposal.md
- Update index.md

---

### 5. Create Project Report
```
"Create project report"
"Generate report chapter [X]"
```
**Actions:**
- Use Project_Report_Format_Guide.md
- Create/Update 03_project_report.md
- Update index.md

---

### 6. Create Presentation
```
"Create mock presentation"
"Generate presentation slide [X]"
```
**Actions:**
- Use Presentation_Format_Guide.md
- Create next available mock_X.md
- Update index.md

---

### 7. Check Progress
```
"Show progress"
"Show progress: [TOPIC NAME]"
```
**Actions:**
- Read index.md
- Display progress table
- Show pending items

---

### 8. Finalize Documents
```
"Finalize the docs"
"Finalize: [TOPIC NAME]"
```
**Actions:**
- Review all documents
- Check against format guides
- Polish formatting
- Commit to git

---

## Skills Integration

This skill automatically uses:

| Task | Skill | When |
|------|-------|------|
| Read PDF | pdf | Adding research papers |
| Edit Word | docx | Creating proposals, reports |
| Create Slides | pptx | Creating presentations |
| Research Web | web-search/tavily-research | Finding references |
| Analyze Data | analyze | Processing research data |

---

## Format Standards (WUB CSE)

### Page Margins
| Side | Measurement |
|------|-------------|
| Top | 1 inch |
| Bottom | 1 inch |
| Left | 1.2 inches |
| Right | 0.80 inches |

### Fonts
| Element | Font | Size | Style |
|---------|------|------|-------|
| Title | Cambria | 14pt | Bold |
| Chapter | Times New Roman | 14pt | Bold |
| Header | Times New Roman | 12pt | Bold |
| Body | Times New Roman | 12pt | Justified |
| Line Spacing | 1.5 | | |

---

## Index.md Structure

Each topic folder has an index.md:

```markdown
# [Topic Name]

## Overview
[Summary of the thesis]

## Progress

| Deliverable | Status | Updated |
|------------|--------|---------|
| 01_idea.md | ✅ | 2026-04-17 |
| 02_proposal.md | 🔄 | - |
| 03_project_report.md | 🔄 | - |
| mock_1.md | 🔄 | - |
| mock_2.md | 🔄 | - |
| mock_3.md | 🔄 | - |

## Research Papers
| # | Paper | Summary | Status |
|---|-------|---------|--------|
| 1 | [Name] | [paper_name]_summary.md | ✅ Analyzed |

## Quick Links
- [01_idea.md](01_idea.md)
- [02_proposal.md](02_proposal.md)
- [05_references/paper-summaries/](paper summaries folder)
- [04_presentations/mock_1.md](04_presentations/mock_1.md)
```

---

## Commands Summary

| Command | Action |
|---------|--------|
| `Start new thesis with topic:` | Create new topic |
| `Continue thesis:` | Load existing topic |
| `Analyze paper:` | Add research |
| `Create proposal` | Generate proposal |
| `Create project report` | Generate report |
| `Create mock presentation` | Generate slides |
| `Show progress` | Display status |
| `Finalize the docs` | Final polish |

---

## Quality Checklist

Before finalization:
- [ ] All phases complete
- [ ] Proposal matches Proposal_Format_Guide.md
- [ ] Report has all 6 chapters
- [ ] 3 mock presentations done
- [ ] All papers in 05_references/
- [ ] Margins correct (1/1/1.2/0.80)
- [ ] Font: Times New Roman 12pt
- [ ] Line spacing: 1.5
- [ ] No spelling errors