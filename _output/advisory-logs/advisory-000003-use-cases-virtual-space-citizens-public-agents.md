# Advisory 000003 | FEATURE-X | 2026-05-22 00:00 | Use Cases: Virtual Space for Citizens and Public Agents

tags: civic-tech, participatory-democracy, use-cases, ux, data-privacy, architecture

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
| CitizenLab | Commercial civic engagement SaaS; separate analytics dashboard for decision-makers |
| UrbanSim / Urban Digital Twins | Territory risk/opportunity profiling for investors and planners |
| LGPD (Brazil, Lei 13.709/2018) | Data protection law applicable to citizen testimony collection |
| Carnegie Endowment (2026) -- Realizing Gains of AI-Enabled Deliberative Democracy | AI augmentation patterns for deliberative processes |
| Chan 2024 -- Online astroturfing: A problem beyond disinformation | Astroturfing as existential risk for civic platforms |
| arXiv 2405.03452 -- LLMs as Agents for Augmented Democracy | LLM agent patterns for democratic participation at scale |
| arXiv 2604.16348 -- Spatial Anchoring and LLM Agents for Participatory Urban Planning | Spatially-anchored LLM agents for UC2 decision-support |
