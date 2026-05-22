# Advisory 000003 | FEATURE-X | 2026-05-22 00:00 | Use Cases: Virtual Space for Citizens and Public Agents

tags: civic-tech, participatory-democracy, use-cases, ux, data-privacy, architecture, open-data, citizen-profiling

## User Brief

Research on use cases for a system as a virtual space for citizens and public agents to discuss problems and solution ideas. Three use cases provided:

1. "Como Cidadao quero espaco virtual para discutir problemas e ideias a respeito do meu territorio para???" (incomplete)
2. "Como investidor, gestor publico, quero conhecer os problemas de um territorio para tomar decisoes embasadas nas necessidades do cidadao"
3. "Como GaveaLab quero uma ferramenta que ajude a coletar e sintetizar pesquisas com cidadaos democratizar acesso a info e consolidar perfis e necessidades"

## Agent Interpretation

Research and grounding of three civic technology use cases for a participatory territorial platform. The system combines a citizen participation layer (UC1), a decision-support layer for managers and investors (UC2), and an AI-assisted research synthesis layer for GaveaLab (UC3). The goal is to complete UC1 (whose motivation clause is missing) and strengthen all three use cases with patterns from comparable platforms (Decidim, Pol.is, Talk to the City, CitizenLab) and with DATA/SEC risk identification under Brazilian law (LGPD).

## Files Referenced

- `knowledge/casos-de-uso.md` -- original use case drafts
- `_references/project/product-design-as-intended.md` -- project design intent
- `_references/project/product-design-as-coded.md` -- implementation state

## Q&A Log

### Q1 -- Research on use cases for a participatory territorial platform

**Question:**

What use cases should a virtual space for citizens, public managers, investors, and GaveaLab support? How should Use Case 1 be completed? What architectural, UX, data, and security considerations apply?

**Answer:**

#### Perspective Evaluation

| Perspective | Status | Summary |
|-------------|--------|---------|
| UX | Deferred | UC1 is structurally incomplete -- missing motivational clause. All three use cases lack explicit success conditions. Four citizen motivation archetypes (voice-seeking, problem-solving, information access, community-building) are unaddressed. |
| ARCH | Deferred | No architecture for the civic platform component is documented. The RAG + clustering synthesis pattern (Talk to the City pipeline) is directly buildable on the existing kb-qa stack but is absent from the design intent. |
| DATA | Deferred | Citizen territorial testimony is PII-adjacent. No consent model, no data-minimization policy, no LGPD compliance mapping (lawful basis, right to deletion, prohibition on sensitive data). |
| SEC | Deferred | No trust model exists. Astroturfing, coordinated inauthentic behavior, identity-linked retaliation, and synthesis-layer capture are the dominant real-world attack vectors for platforms of this type. |

#### Key Findings

**Finding 1 [UX] -- UC1 is missing its motivational anchor**

The user story format requires "As X, I want Y so that Z" -- the "for..." clause is the "so that Z" which aligns every design decision. Based on comparable platforms (Decidim, Consul, Pol.is, vTaiwan), four validated citizen motivation archetypes exist for territorial participation:

- **Voice-seeking:** "so that my lived experience is heard and influences local decisions"
- **Problem-solving:** "so that collective problems I face can be identified and acted on"
- **Information access:** "so that I understand what is planned for my territory"
- **Community building:** "so that I can connect with neighbors who share my concerns"

For GaveaLab's research context, voice-seeking + problem-solving is the most applicable combination.

**Finding 2 [UX] -- UC2 bundles two irreconcilable personas**

Public managers and investors have fundamentally different information needs, trust thresholds, and decision horizons. Merging them into a single use case produces a system that serves neither well. CitizenLab and urban digital twin platforms explicitly separate these personas.

**Finding 3 [ARCH] -- The synthesis pipeline pattern is proven and directly buildable on the team's stack**

The canonical architecture (Talk to the City, Pol.is, vTaiwan):
1. Ingestion layer: multi-modal citizen inputs -> normalize to text + geolocation + metadata
2. Synthesis layer: chunk -> embed (sentence-transformers) -> cluster (UMAP + HDBSCAN) -> label clusters (LLM) -> produce theme trees
3. Presentation layer: structured theme maps to managers/investors; full corpus + provenance to GaveaLab

The team's existing ChromaDB + sentence-transformers + Anthropic SDK stack covers steps 1 and 3. The missing component is the clustering step in stage 2.

**Finding 4 [DATA] -- Citizen territorial testimony is PII-adjacent; LGPD obligations are unaddressed**

Street-level location + complaint type + time + cultural markers can re-identify individuals even without names. GaveaLab's UC3 "profile consolidation" is explicitly a profiling activity under LGPD Art. 5, XII. Key unaddressed LGPD obligations:
- Art. 7: lawful basis for processing (consent must be granular, revocable, not bundled)
- Art. 6, III: data minimization
- Art. 18: right to deletion
- Art. 11: heightened restrictions for sensitive data (racial, health, political characteristics)

**Finding 5 [SEC] -- Three dominant attack vectors for civic platforms**

- **Astroturfing:** AI-generated synthetic testimonies that flood and skew the synthesis layer. This is the primary risk for UC3's research validity.
- **Identity-linked retaliation:** Citizens reporting issues about local actors (landlords, officials) face retaliation if identities are linkable to testimonies.
- **Synthesis-layer capture:** Powerful actors (managers, investors) attempt to influence synthesis outputs to produce narratives favorable to their interests.

**Finding 6 [UX] -- UC3 bundles three distinct workflows that each need separate UX treatment**

Collection, synthesis, and profile consolidation have separate UX challenges, acceptance criteria, and privacy risk profiles. Bundling them risks the communicability failure where a researcher discovers mid-workflow that needed affordances are absent.

#### Trade-offs

**SEC (anti-astroturfing) vs. UX (low-friction participation):**
CPF/ID verification blocks fake inputs but creates barriers for marginalized communities who distrust government systems. Recommended resolution: tiered trust scoring -- pseudonymous contributions are weighted lower in synthesis; verified contributions carry higher weight (Pol.is model). This preserves participation breadth while managing manipulation risk.

**DATA (anonymization at ingestion) vs. ARCH (provenance for longitudinal tracking):**
Stripping identifiers breaks the provenance chain UC3c (longitudinal profile consolidation) needs. Recommended resolution: pseudonymous tokens in a separate identity ledger, purgeable independently of the vector store.

**UX (synthesized outputs for managers) vs. SEC (synthesis layer capture):**
Privileged manager access to aggregated territory profiles creates intelligence asymmetry and capture risk. Recommended resolution: make synthesized outputs public by default (Decidim's radical transparency model) -- this eliminates the asymmetry that creates capture incentives.

---

## Recommendations Summary

### HIGH Priority

**R1 -- Complete Use Case 1 immediately**

Proposed text:
> "As a citizen, I want a virtual space to discuss problems and ideas about my territory so that my local knowledge is heard, synthesized with other residents' voices, and becomes actionable evidence that influences decisions by public managers and researchers about my community."

This phrasing closes the loop across all three use cases and names the specific value proposition: the citizen's contribution becomes evidence, not noise.

**R2 -- Split Use Case 2 into two separate personas**

- UC2a (Public Manager): "As a public manager, I want to see territory problems clustered by theme, location, and urgency so that I can allocate resources and design interventions grounded in citizen-reported evidence."
- UC2b (Investor): "As a social-impact investor, I want to see a territory's consolidated needs profile with trend data so that I can identify gaps where investment can create measurable community benefit."

**R3 -- Define a consent and anonymization layer before any implementation begins**

Specify lawful basis under LGPD for each data element collected, whether location is stored at street level or aggregated, and how withdrawal requests are processed. Default to pseudonymization at ingestion.

**R4 -- Define a threat model for coordinated inauthentic behavior (astroturfing)**

Implement tiered trust scoring (pseudonymous vs. verified contributions), rate-limiting, and consider Pol.is's consensus-detection algorithm which is structurally resistant to outlier injection.

### MEDIUM Priority

**R5 -- Decompose Use Case 3 into three sub-use cases**

- UC3a (Collection): "As GaveaLab, I want to collect citizen testimonies with explicit, granular consent so that I have an authenticated corpus compliant with LGPD."
- UC3b (Synthesis): "As GaveaLab, I want AI-assisted theme extraction over citizen testimonies so that I can identify dominant territorial problems without reading every individual submission."
- UC3c (Profile Consolidation): "As GaveaLab, I want to consolidate and update territory need profiles over time so that I can track changes and measure the impact of interventions."

**R6 -- Adopt the Talk to the City pipeline as the reference architecture for UC3b**

Processing sequence: structured citizen input -> normalize text -> embed (sentence-transformers) -> cluster (UMAP + HDBSCAN) -> label clusters (Anthropic SDK) -> export theme tree + representative quotes. This is directly buildable on the existing kb-qa stack; the only addition is a clustering module.

**R7 -- Define a three-tier access control model**

Citizens contribute but cannot read other citizens' raw testimonies. Managers/investors read synthesized outputs only. GaveaLab reads the full corpus under data-access governance rules. This simultaneously addresses the DATA and SEC concerns.

### LOW Priority

**R8 -- Name A11Y and I18N as constraints in all three use cases**

Territorial communities (especially in Amazonia/Gavea context) include individuals with varying literacy, limited bandwidth, and device access. Voice input, simplified language, SMS-fallback modes are medium-term constraints that should be named now.

---

## Revised Use Case Texts

| ID | Actor | Revised Text |
|----|-------|-------------|
| UC1 | Citizen | As a citizen, I want a virtual space to discuss problems and ideas about my territory so that my local knowledge is heard, synthesized with other residents' voices, and becomes actionable evidence that influences decisions by public managers and researchers about my community. |
| UC2a | Public Manager | As a public manager, I want to see territory problems clustered by theme, location, and urgency so that I can allocate resources and design interventions grounded in citizen-reported evidence. |
| UC2b | Investor | As a social-impact investor, I want to see a territory's consolidated needs profile with trend data so that I can identify gaps where investment can create measurable community benefit. |
| UC3a | GaveaLab | As GaveaLab, I want to collect citizen testimonies with explicit, granular consent so that I have an authenticated corpus compliant with LGPD. |
| UC3b | GaveaLab | As GaveaLab, I want AI-assisted theme extraction over citizen testimonies so that I can identify dominant territorial problems without reading every individual submission. |
| UC3c | GaveaLab | As GaveaLab, I want to consolidate and update territory need profiles over time so that I can track changes, publish research findings, and measure the impact of interventions. |

---

## Reference Platforms and Academic Sources

| Source | Relevance |
|--------|-----------|
| Decidim | Open-source participatory democracy; participatory budgeting + citizen proposals + assemblies modules |
| Pol.is | Consensus-detection algorithm; structurally resistant to astroturfing; used in vTaiwan |
| Talk to the City (AI Objectives Institute) | Canonical AI-assisted synthesis pipeline; embedding + clustering + LLM labeling |
| CitizenLab / Go Vocal | Commercial civic engagement SaaS; separate analytics dashboard for decision-makers |
| Consul Democracy | Participatory budgeting model; collaborative legislation annotation |
| vTaiwan | Governance process model; institutional handoff from synthesis to policy |
| Urban Digital Twins | Spatial anchoring of testimony; equity-first participation design |
| LGPD (Brazil, Lei 13.709/2018) | Data protection law applicable to citizen testimony collection |
| Carnegie Endowment (2026) -- Realizing Gains of AI-Enabled Deliberative Democracy | AI augmentation patterns for deliberative processes |
| Chan 2024 -- Online astroturfing: A problem beyond disinformation | Astroturfing as existential risk for civic platforms |
| arXiv 2405.03452 -- LLMs as Agents for Augmented Democracy | LLM agent patterns for democratic participation at scale |
| arXiv 2604.16348 -- Spatial Anchoring and LLM Agents for Participatory Urban Planning | Spatially-anchored LLM agents for UC2 decision-support |

---

## Platform Synthesis (Deep Research)

*Added 2026-05-22 in response to follow-up. Full research by advisory-reviewer agent with web search.*

### 1. Decidim

**What it is:** Open-source participatory democracy framework (Ruby on Rails), used by 450+ organizations including Barcelona, built around Participatory Spaces (Processes, Assemblies, Initiatives) and Participatory Components (Proposals, Comments, Votes, Budgeting, Accountability).

**Core mechanism:** Citizens submit proposals within a Process space; proposals flow through comment/amendment/vote/accountability stages. All activity is public (radical transparency). A GraphQL API exposes participatory data for external integrations.

**Technical architecture:** Gem-based modularity -- each feature is an independent Rails engine, configurable per deployment. PostgreSQL + Elasticsearch. Space/Component composition decouples "where we discuss" from "how we discuss."

**AI integration:** None native. The GraphQL API is the integration point for an external AI synthesis layer -- export proposals and comments periodically to a T3C-style pipeline.

**Limitations:** Reproduces participation inequalities (requires digital literacy, sustained attention). No native geospatial layer. Upgrade friction from gem modularity. Radical transparency can deter participation on sensitive topics.

**Relevance to GaveaLab:** The Space/Component model maps directly to GaveaLab's structure (territory as Space; testimony collection, deliberation, synthesis reporting as Components). The Accountability component pattern (linking decisions back to citizen proposals) closes the UC3c feedback loop. Radical transparency resolves synthesis-layer capture risk. GraphQL provides the UC3b integration point.

---

### 2. Pol.is

**What it is:** Open-source real-time opinion-collection and consensus-detection system. Participants vote agree/disagree/pass on short statements; PCA + k-means clustering identifies opinion groups and cross-group consensus points.

**Core mechanism:** Sparse vote matrix (participants x statements). PCA finds variance-explaining dimensions; k-means clusters participants by opinion similarity. The algorithm is **structurally resistant to astroturfing**: organized blocs appear as visible outlier clusters rather than distorting consensus. Consensus statements emerge only when they receive high agreement across multiple distinct clusters.

**Key use case:** Identifying where genuine consensus exists before deliberation begins. Not suited for complex multi-stage deliberation or idea generation.

**Technical architecture:** Node.js API + React frontend + R-based math worker. PostgreSQL. Open-source at github.com/compdemocracy/polis. Computationally lightweight (vote matrix, not embeddings).

**AI integration:** arXiv:2306.11932 documents three LLM augmentation patterns: (1) LLM-generated narrative summaries of cluster distinguishing statements; (2) LLM-seeded statements from policy documents to accelerate convergence; (3) LLM deduplication of near-identical statements. vTaiwan now integrates generative AI for post-session summaries.

**Limitations:** Topic-framing depends entirely on who seeds initial statements. Captures sentiment but not reasons. Under-represents minority viewpoints (auditing paper arXiv:2511.04588). Requires 100+ active voters for reliable clusters.

**Relevance to GaveaLab:** Primary use is for UC1 anti-manipulation layer and UC2a manager dashboard. Opinion landscape visualization is more methodologically defensible than raw LLM summaries for public reporting. Tiered trust scoring from advisory-000003 mirrors Pol.is implicit architecture. Statements can be geographically tagged for per-neighborhood opinion maps.

---

### 3. Talk to the City (T3C)

**What it is:** Open-source AI pipeline (Python DAG) by the AI Objectives Institute that transforms large volumes of unstructured citizen text into hierarchical theme trees, with every synthesized claim grounded in a direct participant quote.

**Core mechanism:** Configurable graph pipeline: extract claims (LLM) -> embed (sentence-transformers or OpenAI) -> cluster (UMAP + HDBSCAN) -> label clusters (LLM) -> deduplicate -> generate quote-grounded report. The quote-verification step (confirming every synthesized claim traces to a verbatim source quote) is the anti-hallucination mechanism. Batch mode, not real-time.

**Used in:** Tokyo gubernatorial election pre-consultation (1,000 respondents), Chatham House/vTaiwan AI governance process (1,000 participants), multiple civic deliberation contexts.

**Technical architecture:** Python class DAG configured via JSON/YAML. Steps are composable and replaceable (swap LLM provider, clustering algorithm, embedding model). Output is a structured JSON report (theme tree + quotes + metadata). Open-source at github.com/AIObjectives/talk-to-the-city-reports.

**AI integration:** Entirely AI-native. LLMs used for extraction and labeling (where source grounding is enforceable), not for summarization (where hallucination is hard to detect). Each LLM call must produce a claim + supporting quote; post-processing verifies the quote exists verbatim.

**Limitations:** Context window limits for very large corpora (mitigated by chunking, but cross-chunk claims can be missed). Produces a theme tree, not a deliberative outcome (no agreement signal -- Pol.is addresses this). Asynchronous batch only -- no real-time participation feedback. API costs proportional to corpus size. Cluster quality depends on embedding model and parameter tuning.

**Relevance to GaveaLab:** This is the **direct reference architecture for UC3b**. The pipeline's three stages (embed -> cluster -> label with quote grounding) are buildable on the existing stack: sentence-transformers (already in use), UMAP + HDBSCAN clustering module (add), Anthropic SDK (already in use). The open-source repository provides working Python code to adapt. Quote-grounded output format is specifically well-suited to academic/policy audiences requiring evidence chains. T3C can be understood as the synthesis layer sitting above the retrieval layer the team already built.

---

### 4. Go Vocal (formerly CitizenLab)

**What it is:** Commercial civic engagement SaaS (closed-source, subscription-based). Multi-modal citizen input (ideas, surveys, participatory budgeting, polls) plus built-in NLP sensemaking dashboard for government administrators. 500+ cities globally.

**Core mechanism:** Projects with phases (information, ideation, voting, implementation) and multiple input types. Proprietary NLP pipeline applies topic modeling to cluster submitted ideas, generating a keyword co-occurrence map for administrators. Human-in-the-loop: AI generates draft cluster labels that administrators validate before publishing findings.

**AI integration:** Built-in sensemaking tool (NLP topic clustering, keyword map). Premium "Sensemaking" feature uses AI to assist in writing consultation reports. Cambridge City Council reported 50% reduction in manual processing time.

**Limitations:** Vendor lock-in -- all citizen data on Go Vocal's servers; NLP models are not auditable; pricing is unsuitable for resource-constrained contexts. Portuguese-language NLP quality unknown. No native geospatial layer. Black-box clustering prevents methodological defense in research contexts.

**Relevance to GaveaLab:** Primary extractable pattern is the **two-audience separation**: citizen-facing interface (simple, action-oriented) vs. administrator sensemaking dashboard (analytical, research-oriented). This maps to UC1/UC2/UC3 separation. The human-in-the-loop cluster validation pattern -- AI generates draft labels, researcher confirms before publishing -- is the right model for UC3b methodological defensibility. GaveaLab should build an open-source equivalent using T3C rather than subscribing, given LGPD data residency requirements.

---

### 5. Consul Democracy

**What it is:** Open-source citizen participation platform (Ruby on Rails), built by Madrid City Council (2015), used by 90+ governments. Strongest use case: participatory budgeting. Also supports citizen proposals (with signature thresholds), debates, and collaborative legislation annotation.

**Core mechanism:** Madrid-specific democratic processes: citizen proposals trigger official review at defined signature thresholds; participatory budgeting allocates a defined municipal budget via proposals and vote; citizens annotate draft regulations sentence by sentence in the collaborative legislation module. Identity verification via municipal census check (high-trust, low-accessibility).

**Technical architecture:** Monolithic, non-modular Rails app with PostgreSQL and Elasticsearch. Cannot run multiple participatory portals on a single installation. Extending Consul for non-Madrid processes requires forking the codebase. No plug-in system.

**AI integration:** None.

**Limitations:** Non-modular architecture makes adaptation expensive. Identity verification model is Spain-specific (not directly portable to Brazil without CPF/Cadastro integration). No multi-tenancy (multiple territories require separate instances). No AI synthesis. No geographic filtering or qualitative text analysis.

**Relevance to GaveaLab:** Most useful if the platform eventually adds participatory budget processes -- Consul's data model and UX are the most mature reference implementation. The collaborative legislation annotation feature (citizens commenting on draft regulation paragraph by paragraph) is applicable if GaveaLab's territorial context includes existing urban plans or environmental regulations to annotate. For the core synthesis and research use cases, Decidim + T3C is a stronger architecture choice.

---

### 6. vTaiwan -- The Governance Process

**What it is:** A governance process (not a platform) that combines digital tools (Pol.is for opinion mapping, collaborative notes, GitHub for document versioning) with structured in-person meetings to produce consensus recommendations on contested technology-policy questions.

**How the process works:**
1. **Objective stage**: crowdsource facts and evidence
2. **Reflective stage**: deploy Pol.is to map public opinion before deliberation -- discover existing consensus
3. **Deliberative stage**: live-streamed stakeholder meetings using Pol.is results as a shared factual baseline
4. **Legislative stage**: transmit documented consensus to government ministry

Key insight: Pol.is runs **before** human deliberation, not after. Human meetings begin from a mapped consensus baseline rather than an adversarial blank slate. Early processes achieved 80% implementation rate (government action followed consensus outputs).

**Current status (2025-2026):** Fully volunteer-driven. No formal mandate requiring government to act on outputs. December 2024 AI governance event produced recommendations reflected in Taiwan's National Human Rights Commission guidance on the draft AI Basic Act.

**Relevance to GaveaLab:** Provides the **governance wrapper** the technology platforms alone cannot supply. The critical lesson: a territorial platform will only produce sustained impact if there is a defined institutional receiver for synthesis outputs. The four-stage sequencing (objective -> reflective -> deliberative -> legislative) is transferable as: territory documentation -> Pol.is-style opinion mapping -> GaveaLab synthesis -> handoff to municipal government or publication. GaveaLab's academic legitimacy (framing outputs as peer-reviewed research with methodology and citation) is the mechanism for institutional reception that volunteer-driven processes lack.

---

### 7. Urban Digital Twins for Participatory Planning

**What it is:** Computational models that mirror a physical territory's infrastructure and dynamics, combined with participatory interfaces allowing citizens to see their territory in simulation, propose interventions, and observe modeled consequences.

**Participation patterns:** Interactive immersive visualization (3D web viewers, VR/AR) significantly increases citizen engagement quality -- participants provide more spatially specific, actionable feedback when interacting with a 3D model vs. text descriptions. However, VR/AR creates significant equity barriers.

**Limitations:** Academic critique (Dawkins/Kitchin 2025): UDTs remain "shallow explanations of urban processes" because cities aggregate socio-political complexity that resists parametric modeling. Citizens were explicitly listed as co-developers in only 16.7% of UDT projects. Commercial platforms have faced viability challenges (Cityzenith ceased trading 2023).

**Relevance to GaveaLab:** Two specific applicable patterns:
1. **Spatial anchoring of citizen testimony**: allowing citizens to attach problem reports to a geographic point on a map dramatically increases precision and actionability of synthesis. This is the missing geospatial layer in Decidim and Consul. A simplified version (territorial map with geotagged testimonies, without simulation) captures most of the participation benefit at a fraction of engineering cost.
2. **Equity-first design imperative**: UDT research finding that immersive interfaces create accessibility barriers is directly applicable to Amazonian/Gavea territorial contexts. Text-first, mobile-first, SMS-fallback interfaces are mandatory, not optional features for later versions.

---

### Architecture that emerges from all seven patterns

**Layer 1 -- Citizen participation layer** (Decidim, Pol.is, UDT equity research):
Territory-scoped spaces, multi-modal input (text, geotagged pin, voice), Pol.is-style agree/disagree voting on surfaced themes, mobile-first with SMS fallback.

**Layer 2 -- AI synthesis layer** (Talk to the City, Go Vocal):
Batch pipeline (embed -> cluster -> label with LLM -> quote-ground) producing a theme tree that researchers validate before publishing. Built on existing sentence-transformers + Anthropic SDK stack with a clustering module (UMAP + HDBSCAN) added.

**Layer 3 -- Decision-support layer** (Go Vocal, vTaiwan, UDTs):
Two separate dashboards -- public managers (clustered territorial problems by theme, location, urgency) and GaveaLab researchers (full corpus, audit trail, longitudinal profile) -- plus a defined institutional handoff routing synthesized outputs to municipal government or academic publication.

**The critical gap across all platforms:** Every platform generates synthesis outputs; every platform struggles to ensure those outputs are acted on. GaveaLab's academic legitimacy is a structural asset that commercial platforms and volunteer processes lack -- framing synthesis outputs as peer-reviewed research findings (with methodology, reproducibility, and citation) is the institutional reception mechanism that vTaiwan's volunteer model cannot guarantee.

---

## Q2 -- Open Datasets for Citizen Profiling and Territorial Needs Analysis

*Follow-up question: are there open datasets for this civic tech? We will work on synthesizing these datasets to extract insights and develop citizen common profiles and needs.*

### Brazilian Open Datasets

#### 1. IBGE -- Censo Demografico 2022

The primary sociodemographic source. Portal: censo2022.ibge.gov.br and downloads.ibge.gov.br. REST API: `https://servicodados.ibge.gov.br/api/v3/agregados/{pesquisa}/periodos/{periodo}/variaveis/{variavel}?localidades=N6[all]`. Geographic granularity from Brazil down to census tracts (setor censitario) and weighting areas. Variables: age pyramid, income per capita, literacy, race/ethnicity, water/sanitation/electricity access, employment status, housing conditions, indigenous/quilombola self-declaration. Practical access: Base dos Dados (BigQuery, harmonized codes) and the `censobr` R package.

#### 2. Base dos Dados -- basedosdados.org

The single most practical entry point. A nonprofit data lake hosted on Google BigQuery (~1 TB/month free tier). Aggregates and cleans 100+ Brazilian official datasets (Censo 2022, DATASUS, INEP, RAIS, SNIS, CadUnico aggregates) with harmonized IBGE municipality codes as the universal join key. Access via BigQuery SQL, Python (`pip install basedosdados`), or R package. Eliminates 80% of data engineering work.

#### 3. DATASUS -- Health System Data

Portal: dadosabertos.saude.gov.br (67 data collections). Key systems: SIM (mortality causes by municipality), SINASC (births, maternal conditions), SINAN (notifiable diseases -- dengue, malaria, TB, critical for Amazonian contexts), CNES (health facility locations and capacity), SIA/SIH (outpatient and hospital information). Access tools: `microdatasus` R package, TabNet web queries. Health access gaps and disease burden are direct indicators of territorial neglect.

#### 4. INEP -- Education Data

Portal: gov.br/inep/dados-abertos and community API at api.dadosabertosinep.org. Key datasets: Censo Escolar (enrollment, school infrastructure: water, electricity, internet, toilets -- school and municipal level), IDEB (learning quality index by school and municipality), ENEM microdata (individual exam results with municipality of residence and sociodemographics). `educabR` R package for tidy access.

#### 5. RAIS / CAGED -- Labor Market

Portal: gov.br/trabalho-e-emprego/microdados-rais-e-caged. RAIS: annual formal employment stock by municipality/sector/occupation/gender/age/race/salary band, back to 1985. CAGED: monthly formal job creation/destruction flows (New CAGED, e-Social based, since 2020). Important: full identified microdata requires a Data Use Agreement (months to process). The `clean_RAIS` GitHub repo provides processing scripts. Covers formal employment only -- in many Amazonian municipalities 60-80% of economic activity is informal and invisible in this dataset.

#### 6. CadUnico -- Cadastro Unico

Portal: CECAD 2.0 (cecad.cidadania.gov.br) and Observatorio do CadUnico. Coverage: ~100 million registered low-income individuals in ~40 million families. Variables: household address, composition, housing conditions, income, education level, disabilities, water/sanitation access, employment status, social program enrollment. Open data: municipal aggregates via CECAD. Individual microdata requires formal research partnership with MDS/DATAPREV. The richest available proxy for poverty geography and multi-dimensional vulnerability in Brazil.

#### 7. SNIS / SINISA -- Water and Sanitation

Portal: gov.br/cidades/saneamento/snis (replaced in 2024 by SINISA). Available cleaned at Base dos Dados. Annual municipal data: water access rates, sewerage coverage, treatment rates, per-capita investment. Sanitation deficits are a direct indicator of unmet territorial needs, especially in peri-urban and Amazonian communities.

#### 8. Fala.BR -- Federal Ombudsman Complaints

Portal: falabr.cgu.gov.br. Coverage: 6+ million manifestations (denunciations, complaints, compliments, suggestions, requests). REST API documented at wiki.cgu.gov.br/Fala.BR_API_Faq. Bulk download available. Granularity: individual manifestation with topic categorization, agency, and geographic origin. The closest available real-time citizen need signal from the federal sphere. Complement: SP 156 (sp156.prefeitura.sp.gov.br) for Sao Paulo municipal complaints.

#### 9. datazoom.amazonia -- PUC-Rio DataZoom

Portal: datazoom.com.br/datazoom.amazonia. GitHub: datazoompuc/datazoom.amazonia. An R package (CRAN) that wraps and pre-processes multiple official datasets specifically for Legal Amazon municipalities: PRODES (deforestation), DETER (deforestation alerts), IBGE municipality mapping, agricultural production (PAM), mining (ANM), SINAN health, CNES, conservation units, indigenous lands, land use. This is a direct PUC-Rio output and the most useful aggregation tool for Amazonian territorial analysis.

#### 10. TerraBrasilis / INPE -- Environmental Monitoring

Portal: terrabrasilis.dpi.inpe.br. Datasets: PRODES (annual deforestation since 1988), DETER (daily deforestation alerts), fire hotspots, land use change. Formats: Shapefile, GeoJSON, WMS/WFS web services. Polygon-level granularity aggregable to municipality or indigenous territory. Essential for Amazonian territorial analysis.

#### 11. geobr -- Spatial Boundaries (IPEA)

Portal: ipeagit.github.io/geobr. R/Python package providing 27 spatial datasets: municipalities, states, census tracts, urbanized areas, indigenous lands, conservation units, weighting areas, macro/meso/microregions. Harmonized projections and fixed topology. The recommended tool for all spatial operations -- eliminates common spatial join errors.

#### 12. Brazil Data Commons

Portal: brazildatacommons.com.br. Emerging semantic platform (2024 arXiv:2511.11755) that unifies Brazilian public datasets under shared ontologies and interoperable data standards. Provides a SPARQL endpoint. Addresses the absence of shared schemas that hinder cross-domain integration across existing portals.

---

### International Civic Participation Datasets

| Dataset | Portal | Format | Relevance |
|---------|--------|--------|-----------|
| Open311 / GeoReport v2 | open311.org | REST JSON | Standard for civic service requests (311 equivalent); benchmark for complaint-to-need classification |
| Decidim exports (per city) | decidim.org / per-city admin | CSV, JSON, GraphQL | Proposals, votes, comments, participatory budgeting results per city instance |
| Pol.is exports | compdemocracy/polis GitHub | CSV (vote matrix) | Comment-vote matrix, opinion clusters for deliberative polling studies |
| Participedia | participedia.net | Web / JSON | 3,000+ participatory process case descriptions globally, including Brazilian cases |
| MapAgora (US) | nature.com/s41597-025-05353-6 | CSV (ZIP codes) | Civic opportunity/need profile per territory; direct international precedent |

---

### Entity Model for Citizen Profiles and Territorial Needs

The universal join key across all Brazilian datasets is the **Codigo IBGE de Municipio** (7-digit). Every join happens through this code or through the 15-digit setor censitario code.

```
TERRITORY (municipio / setor censitario / terra indigena)
+-- Sociodemographic Profile
|   +-- IBGE Censo 2022: age, race, income, household, literacy
|   +-- CadUnico (aggregated): poverty concentration, social vulnerability
|   +-- RAIS: formal employment rate by sector
+-- Health Needs
|   +-- SINAN: disease burden (malaria, dengue, TB -- Amazonian)
|   +-- CNES: health facility coverage, distance to nearest facility
|   +-- SIM: premature mortality rate
+-- Education Needs
|   +-- Censo Escolar: school infrastructure, enrollment, dropout rate
|   +-- IDEB: learning quality outcomes
+-- Infrastructure Needs
|   +-- SNIS/SINISA: water access, sewerage coverage
|   +-- IBGE Censo: electricity, internet, housing precarity
+-- Environmental Dimension (Amazonia)
|   +-- PRODES: accumulated deforestation
|   +-- DETER: active deforestation pressure
|   +-- datazoom.amazonia: integrated Legal Amazon variables
+-- Citizen Voice Dimension
    +-- Fala.BR: complaint type frequency by municipality/theme
    +-- Platform-native: participatory platform proposals and votes
```

**Standard methodology for "common citizen profiles":**
1. Sociodemographic segmentation from Census microdata (age, income, race, household type)
2. Multi-dimensional need scoring: normalize deficit indicators across all dimensions above
3. Spatial clustering: k-means or HDBSCAN on census tracts using indicators as features
4. Profile labeling: LLM-generated labels for each cluster backed by indicator values

---

### Key Gaps -- What is NOT in Open Datasets

These are the dimensions that GaveaLab's participatory platform must collect as primary data:

| Gap | Why it matters |
|-----|---------------|
| Intra-municipal granularity (neighborhood, street, community level) | Open datasets stop at municipality or census tract; informal settlements (*favelas*, *comunidades*) and dispersed riverbank communities (*ribeirinhos*) are invisible |
| Expressed vs. derived needs | Datasets measure observed conditions; citizens' own priority ordering only comes from surveys or participatory processes |
| Indigenous and traditional community data | FUNAI TI registry exists but individual socioeconomic data is fragmentary; RAIS undercounts informal Amazonian economies |
| Qualitative/cultural dimensions | No variables for territorial belonging, cultural heritage, community governance, traditional ecological knowledge |
| Real-time needs from acute events | Most datasets are annual or decennial; floods, fires, and economic shocks are invisible until the next cycle |
| Service quality vs. availability | CNES says a health post exists; does not capture wait times, medication stock, or whether staff is present |
| Informal economy | RAIS/CAGED cover formal employment only; 60-80% of economic activity in many Amazonian municipalities is invisible |
| Digital exclusion bias | Fala.BR, Decidim, 156 systems -- only digitally literate, connected citizens participate; rural Amazonian communities are structurally absent |

The last gap is the most critical for GaveaLab's research design: any "citizen voice" dataset from digital platforms requires explicit bias correction when used to characterize territorial needs.

---

### Practical Integration Path for GaveaLab

1. **Start with Base dos Dados** as the technical access layer (BigQuery, harmonized codes, Python/R SDK).
2. **Use datazoom.amazonia** for Legal Amazon municipality profiling -- it is a direct PUC-Rio output.
3. **Layer Fala.BR API data** for the citizen voice dimension -- parse complaint themes and map to municipalities to detect service failure concentrations.
4. **Use geobr** for all spatial operations -- harmonized projections, indigenous land boundaries, conservation units.
5. **Plan primary data collection** for intra-municipal need mapping, expressed preference ordering, and service quality experience. No open dataset covers these, and they represent GaveaLab's distinctive research contribution.

---

### Academic Precedents for Multi-Source Civic Data Synthesis

| Source | Contribution |
|--------|-------------|
| Brazil Data Commons (arXiv 2511.11755, 2024) | Unified semantic layer for Brazilian datasets; SPARQL endpoint; direct precedent for data integration challenge |
| "A Citizen-Centric Approach for Territorial Services Management" (MDPI IJGI, doi:10.3390/ijgi9040223) | Framework combining open government data with citizen-generated service feedback to build territorial service profiles |
| "Effective City Planning: Data-Driven Analysis of Infrastructure and Citizen Feedback in Bangalore" (arXiv 2211.03126) | Infrastructure open data + complaint data -> territorial planning insights pipeline |
| MapAgora (Scientific Data, 2025) | Multi-source civic dataset building territorial civic opportunity/need profiles per ZIP code |
| "Voice to Vision" (arXiv 2505.14853, 2025) | Co-designed civic data infrastructure for participatory decision support -- most recent directly relevant paper |
