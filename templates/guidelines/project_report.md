# Project Report Guidelines

## Overview

Guidelines for writing and preparing the thesis/project report following **official WUB CSE format**.

### WUB Official Formatting Standards

| Element | Specification |
|---------|---------------|
| Font (Body) | Times New Roman, 12pt |
| Font (Chapter Title) | Times New Roman, 14pt Bold |
| Font (Headers) | Times New Roman, 12pt Bold |
| Margins (Top/Bottom) | 1 inch |
| Margins (Left) | 1.2 inches |
| Margins (Right) | 0.8 inches |
| Line Spacing | 1.5 line spacing |
| Alignment | Justified |
| Paragraph Indent | None |
| Paragraph Spacing | 6pt between paragraphs |

### Front Matter Components (Required)

| # | Component | Description |
|---|-----------|-------------|
| 1 | Title Page | Official WUB format with student IDs |
| 2 | Letter of Transmittal | Formal letter to supervisor |
| 3 | Declaration | Student statement of originality |
| 4 | Certificate | Supervisor certification |
| 5 | Acknowledgements | Thank you to contributors |
| 6 | Abstract | 150-250 words summary |
| 7 | Table of Contents | Full TOC with page numbers |

### Key Statistics to Include (with in-text citations)

Include these statistics in the Introduction/Background chapter to establish the problem context:

| Statistic | Data | Source |
|-----------|------|--------|
| Annual CSE graduates | ~20,000 per year | Asian Development Bank (2019) |
| Industry demand | 7,500-8,000 new technical personnel/year | TBS News (2019) |
| Job placement rate | 77.1% (top 9 universities) | ADB Tracer Study (2018) |
| Failed basic tests | >80% fail coding/English tests | ADB (2019) |
| Graduate unemployment | 906,000 highly educated unemployed | BBS Labour Force Survey (2023) |
| Skills gap score | 39.1/100 (QS Future Skills Index) | QS (2025) |

### Example Usage

```markdown
Bangladesh produces approximately 20,000 Computer Science and Engineering
(CSE) graduates annually (Asian Development Bank, 2019), yet the domestic
IT industry can only absorb 7,500-8,000 new technical personnel per year
(TBS News, 2019). This stark mismatch highlights a growing concern regarding
skill alignment between academia and industry.

While CSE graduates from top universities show a job placement rate of 77.1%
(Asian Development Bank, 2018), over 80 percent of jobseekers fail basic
coding and English proficiency tests (Asian Development Bank, 2019),
indicating a significant skills gap in the labor market.

According to the Bangladesh Bureau of Statistics Labour Force Survey (2023),
there are approximately 906,000 highly educated unemployed individuals in
the country, underscoring the severity of graduate unemployment.
```

## Structure

Following official WUB CSE format:

| Chapter | Title (Official) | Content | Pages |
|---------|-----------------|---------|-------|
| 1 | Introduction | Background, Problem Statement, RQs, Objectives, Scope | 8-10 |
| 2 | Literature Review | 44 papers in 3 categories + tables + gap identification | 8-10 |
| 3 | Research Methodology | Framework, Data collection, NLP pipeline, Survey, Comparison | 10-12 |
| 4 | Requirement Analysis, Design & Development | System design, Algorithms, DFD, Implementation, Testing | 15-20 |
| 5 | Project Description / Results | Results, Screenshots, Analysis, Cross-country comparison | 15-20 |
| 6 | Conclusions | Summary, Recommendations, Limitations, Future work | 5-7 |

**Note:** Thesis follows similar structure but emphasizes research findings over system development.

---

### Chapter 1: Introduction

**Purpose:** Establish context and justify the research

**Sections:**
1. **Background** (2-3 pages)
   - Bangladesh CSIT graduate context
   - Industry skill gap problem
   - Importance of skill demand analysis

2. **Problem Statement** (1-2 pages)
   - Current skill gap issues
   - Why this research is needed

3. **Research Questions** (1 page)
   - RQ1-RQ10 from the research design

4. **Research Objectives** (1 page)
   - Numbered list (Objective 1, 2, 3, etc.)
   - Use format: "To [action verb]..."

5. **Scope and Limitations** (1-2 pages)
   - What the study covers
   - What it doesn't cover
   - Why no specific university/institution

6. **Thesis Outline** (1 page)
   - Brief description of each chapter

---

### Chapter 2: Literature Review

**Purpose:** Show what others have done and identify the gap

**Sections:**
1. **Introduction** - Overview of reviewed literature
2. **Job Data Analysis using NLP** (3-4 pages)
   - 8-10 papers on NLP methods for job posting analysis
   - Comparative table
3. **Fresh Graduates' Perceived Skills** (2-3 pages)
   - 5-7 papers on graduate self-assessment
4. **Employed Professionals' Skill Development** (2-3 pages)
   - 5-7 papers on working professionals
5. **Research Gap** - What hasn't been done in Bangladesh
6. **Chapter Summary** - Synthesize and transition to methodology

**Key Requirements:**
- 8-10 pages minimum
- Organize by theme, not just list papers
- Include comparative table with: Study, Method, Findings, Strength, Weakness
- Focus on 2020-2026, older only if highly relevant

---

### Chapter 3: Research Methodology

**Purpose:** Explain how you conducted the research

**Sections:**
1. **Research Design** - Overall approach diagram
2. **Data Collection**
   - Job postings: sources, period (2020-2026), volume
   - Survey: participants, format, questions
3. **NLP Pipeline** (see detailed section below)
4. **Survey Design**
   - Fresh graduates questionnaire
   - Employed professionals questionnaire
5. **Cross-Country Comparison Method**
   - How jobs were matched by role and seniority
   - Which countries: Bangladesh, USA, Canada, Australia
6. **Data Analysis** - Methods for analyzing survey data

---

### Chapter 4: Requirement Analysis, Design & Development

**Purpose:** Present system design and implementation

**Sections:**
1. **Requirement Gathering** - Techniques (interviews, surveys, observation)
2. **Analysis of Requirements** - Technology explanation, specifications
3. **System Design** - Architecture, DFD, Flowchart, ER Diagram
4. **Implementation** - Technology stack, key code
5. **Testing** - Test cases, results

**For Thesis:** Replace with Data Analysis & Results

---

### Chapter 5: Project Description / Results

**Purpose:** Present results or system modules

**Option A - For Project Reports (with system):**
1. **Screenshots of Different Modules** - Each module with description and features

**Option B - For Thesis (research focus):**
1. **Job Posting Analysis Results** - Skills extracted by seniority
2. **Survey Results** - Fresh graduates + employed professionals
3. **Cross-Country Comparison** - Bangladesh vs USA/Canada/Australia
4. **Trend Analysis** - 2020-2026 changes

---

### Chapter 6: Conclusions

**Purpose:** Wrap up and provide actionable outputs

**Sections:**
1. **Summary of Findings** (1-2 pages)
   - Answer each research question briefly
2. **Contributions** - What this study adds
3. **Recommendations** (2-3 pages)
   - For curriculum updates
   - For graduate preparation
   - For future research
4. **Limitations** - What constraints existed
5. **Future Work** - What can be done next

### Research Justification - Cross-Country Comparison

The research includes a unique cross-country comparative analysis comparing Bangladesh with developed nations (USA, Canada, Australia). This comparison is justified in the Introduction/Background chapter.

#### Primary Novelty (Claim This)

**Cross-Country Comparison of Skill Requirements for Similar Jobs at Same Seniority Levels**

This research is the first comprehensive analysis that compares skill requirements in Bangladesh CSIT job market with developed nations (USA, Canada, Australia) for similar job roles at matched seniority levels.

#### Supporting Contributions

| Contribution | Description |
|--------------|-------------|
| First in Bangladesh | No prior comprehensive CSIT job market analysis exists |
| Dual Survey | Surveys both fresh graduates AND employed professionals |
| NLP Analysis | Hybrid NLP (TF-IDF + BERT + WSD) for extracting skills from job postings |

#### Why Compare with Developed Nations?

| Reason | Description |
|--------|-------------|
| Global Benchmarking | See how Bangladesh compares with mature job markets |
| Skill Gap Visibility | Identify what skills Bangladesh jobs don't require yet |
| Curriculum Guidance | Help universities align with international standards |
| Graduate Preparation | Show graduates what skills matter for international opportunities |

#### What to Compare

For **similar job roles**, compare:
- Technical skills demanded (programming languages, frameworks, tools)
- Soft skills requirements
- Experience level expectations
- Certification requirements
- Remote/hybrid work policies

#### How to Present in Report

```markdown
## Research Justification

While several studies have analyzed skill demands in developed nations such as
the USA, Canada, and Australia (Smith, 2023; Jones, 2024), limited research
exists on how these skill requirements compare with developing economies like
Bangladesh. This cross-country comparison provides valuable insights into:

1. The skill gap between Bangladesh and global standards
2. Skills that graduates need for international competitiveness
3. Recommendations for curriculum alignment with global benchmarks
```

#### Example Comparison Table (for Results Chapter)

| Skill Category | Bangladesh | USA | Canada | Australia |
|----------------|------------|-----|--------|----------|
| Programming | Python, Java, PHP | Python, Java, AWS | Python, Java, Cloud | Python, JavaScript |
| Frameworks | Laravel, Django | React, Node.js, AWS | React, Django | React, .NET |
| Soft Skills | Communication, Teamwork | Leadership, Problem-solving | Communication, Adaptability | Teamwork, Communication |
| Certifications | Limited demand | AWS, Azure, PMP | AWS, Azure | AWS, CISSP |

### Research Objectives

Format: **numbered list** (Objective 1, Objective 2, etc.)

#### Important Clarifications from Supervisor

1. **Objective 3**: Questionnaire-based survey with **both** fresh graduates AND employed professionals (not just validation)
2. **Job Classification**: Classify jobs by seniority level:
   - Junior/Entry-level
   - Mid-level
   - Senior-level
3. **NLP Methods**: Use **hybrid NLP** approach (TF-IDF + BERT combined)
4. **Trend Analysis**: Analyze last 5 years (2020-2026) - identify increasing/decreasing demands (NOT prediction)

#### Example Format
```markdown
## Research Objectives

The objectives of this research are:

1. To analyze job postings from Bangladesh CSIT job market using text mining
   techniques to identify and categorize demanded skills.

2. To develop and apply hybrid NLP models (TF-IDF + BERT) for automated skill
   extraction and classification of job requirements.

3. To conduct a questionnaire-based survey with both fresh CSIT graduates and
   employed professionals to understand perceived skills vs industry requirements.

4. To compare skill demands between Bangladesh and developed nations (USA, Canada,
   Australia) for similar job roles and seniority levels.

5. To analyze trends in skill demand over the past five years and provide
   recommendations for curriculum alignment.
```

## Literature Review Guidelines

The Literature Review chapter must be **8-10 pages minimum**.

### Paper Distribution (20-25 papers total)

| Category | Number of Papers | Focus |
|----------|-----------------|-------|
| Job Data Analysis using NLP | 8-10 papers | Methods and models for job posting analysis |
| Fresh Graduates' Perceived Skill Knowledge | 5-7 papers | Graduates' self-assessment and readiness |
| Employed Professionals' Skill Development | 5-7 papers | Skill upgrades and gaps among working professionals |

### Literature Review Structure

1. **Organize by theme** (not just listing papers)
2. **Comparative table** summarizing: models used, methodologies, key findings
3. **Strengths and weaknesses** of each study
4. **Identify research gaps** that your study addresses

### Example Table Format

| Study | Method | Key Findings | Strength | Weakness |
|-------|--------|--------------|----------|----------|
| Smith et al. (2023) | TF-IDF + BERT | 85% accuracy on skill extraction | High accuracy | Limited to English |
| Jones (2022) | Keyword matching | Identified top 10 skills | Simple approach | Misses context |

### Time Range

- Focus on **recent studies (2020-2026)**
- Older studies (before 2020) only if highly relevant

## Conceptual Framework

Include this framework diagram in the Methodology chapter:

```
+---------------------------+
|    RESEARCH OBJECTIVE     |
|   Perception-Requirement  |
|        Gap Analysis       |
+---------------------------+
            |
            v
+------------------+------------------+
|                  |                  |
v                  v                  v
+------------+ +-----------+ +----------------+
|   JOB      | | FRESH     | |   EMPLOYED     |
| POSTINGS   | | GRADUATES | | PROFESSIONALS |
| (NLP)      | | (Survey)  | |   (Survey)    |
+------------+ +-----------+ +----------------+
     |              |                |
     v              v                v
+-----------+ +----------+ +-------------+
| Industry  | | Perceived| | Perceived   |
| Required  | | Skills   | | Skills      |
| Skills    | | (Grad)   | | (Employed)  |
+-----------+ +----------+ +-------------+
     |              \        /
     v               v      v
+--------+     +-------------------+
|   GAP  |<--->|  COMPARISON &    |
|ANALYSIS|     |  VALIDATION      |
+--------+     +-------------------+
     |
     v
+---------------------------+
|  FINDINGS &              |
|  CURRICULUM               |
|  RECOMMENDATIONS          |
+---------------------------+
```

### Framework Description

| Component | Description |
|-----------|-------------|
| Job Postings (NLP) | Extract industry-required skills using hybrid NLP |
| Fresh Graduates (Survey) | Assess perceived skills and self-assessment |
| Employed Professionals (Survey) | Industry perspective on required skills |
| Gap Analysis | Compare NLP findings with survey perceptions |
| Cross-Country Comparison | Compare Bangladesh with USA, Canada, Australia |
| Recommendations | Curriculum alignment suggestions |

## Writing Style
- Academic writing tone
- Voice and persona

## Length Guidelines
- Word count per chapter
- Section lengths

## Referencing
- Bibliography format
- Citation style

## In-Text Citations

Harvard referencing style uses the **author-date system**.

### Citation Types

| Type | Format | Example |
|------|--------|---------|
| **Parenthetical** | `(Author, Year)` | `(Smith, 2023)` |
| **Narrative** | `Author (Year)` | `Smith (2023) argues...` |

### When to Cite

- **Every time you use someone's idea, data, or argument** - cite it
- **Direct quotes** - add page number: `(Smith, 2023, p. 48)`
- **Multiple pages**: `(Smith, 2023, pp. 48-52)`

### Author Variations

| Authors | Format |
|---------|--------|
| 1 author | `(Smith, 2023)` |
| 2 authors | `(Smith and Jones, 2023)` |
| 3+ authors | `(Smith et al., 2023)` |
| No date | `(Smith, n.d.)` |
| Same author, same year | `(Smith, 2025a)`, `(Smith, 2025b)` |

### Reference List

- Alphabetical by author surname (not numbered)
- Format: `Author (Year). Title. Publisher.`

### Reference Examples

**Book**:
```
Smith, J. (2023). Machine learning: A practical approach. Academic Press.
```

**Journal Article**:
```
Jones, A. and Khan, R. (2022). "Deep learning methods for NLP", Journal of Artificial Intelligence, 15(3), pp. 45-67.
```

**Conference Paper**:
```
Rahman, M. (2021). "Skill extraction from job postings", Proceedings of ICCSE 2021, Dhaka, pp. 112-118.
```

**Website**:
```
LinkedIn (2024). LinkedIn workforce report. Available at: https://example.com/workforce-report (Accessed: 15 Jan. 2025).
```

**Thesis**:
```
Ali, S. (2020). NLP techniques for skill extraction. M.Sc. Thesis, World University of Bangladesh.
```

## Formatting
- LaTeX templates
- Style guidelines