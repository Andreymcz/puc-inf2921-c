# QA Log | Advisory 000003 | 2026-05-22 12:18 UTC | Use Cases: Virtual Space for Citizens and Public Agents

**Brief:** Research on use cases for a civic technology platform serving citizens, public managers, investors, and GaveaLab -- a virtual space for discussing territorial problems and solution ideas.

---

## Q1

**User:**
Research on use cases for a system as a virtual space for citizens and public agents to discuss problems and solution ideas. Three use cases provided:

1. "Como Cidadao quero espaco virtual para discutir problemas e ideias a respeito do meu territorio para???" (incomplete)
2. "Como investidor, gestor publico, quero conhecer os problemas de um territorio para tomar decisoes embasadas nas necessidades do cidadao"
3. "Como GaveaLab quero uma ferramenta que ajude a coletar e sintetizar pesquisas com cidadaos democratizar acesso a info e consolidar perfis e necessidades"

## A1

Advisory 000003 was generated. Research was conducted via an advisory-reviewer agent that evaluated the three use cases from UX, ARCH, DATA, and SEC perspectives, with web research on comparable platforms (Decidim, Pol.is, Talk to the City, CitizenLab, UrbanSim).

**Key findings:**

- UC1 is structurally incomplete -- missing the motivational "so that" clause. Four validated citizen motivation archetypes from civic tech literature: voice-seeking, problem-solving, information access, community-building.
- UC2 bundles two irreconcilable personas (public manager vs. investor) with different information needs and decision horizons.
- UC3 bundles three distinct workflows (collection, synthesis, profile consolidation) that each need separate UX treatment and privacy risk profiles.
- All three use cases lack LGPD (Brazilian data protection law) compliance considerations for citizen testimony data.
- Civic platforms face dominant socio-technical attack vectors: astroturfing, identity-linked retaliation, and synthesis-layer capture.
- The synthesis pipeline (Talk to the City pattern: embed -> cluster -> label) is directly buildable on the team's existing ChromaDB + sentence-transformers + Anthropic SDK stack.

**Recommendations issued:**

| Priority | Recommendation |
|----------|---------------|
| HIGH | Complete UC1 with voice-seeking + problem-solving motivation |
| HIGH | Split UC2 into UC2a (Public Manager) and UC2b (Investor) |
| HIGH | Define consent and anonymization layer before implementation (LGPD) |
| HIGH | Define threat model for astroturfing / coordinated inauthentic behavior |
| MEDIUM | Decompose UC3 into UC3a (Collection), UC3b (Synthesis), UC3c (Profile Consolidation) |
| MEDIUM | Adopt Talk to the City pipeline as reference architecture for UC3b |
| MEDIUM | Define three-tier access control model (citizens / managers-investors / GaveaLab) |
| LOW | Name A11Y and I18N constraints in all three use cases |

**Revised use case texts produced:**

- UC1 (Citizen): "As a citizen, I want a virtual space to discuss problems and ideas about my territory so that my local knowledge is heard, synthesized with other residents' voices, and becomes actionable evidence that influences decisions by public managers and researchers about my community."
- UC2a (Public Manager): "As a public manager, I want to see territory problems clustered by theme, location, and urgency so that I can allocate resources and design interventions grounded in citizen-reported evidence."
- UC2b (Investor): "As a social-impact investor, I want to see a territory's consolidated needs profile with trend data so that I can identify gaps where investment can create measurable community benefit."
- UC3a (Collection): "As GaveaLab, I want to collect citizen testimonies with explicit, granular consent so that I have an authenticated corpus compliant with LGPD."
- UC3b (Synthesis): "As GaveaLab, I want AI-assisted theme extraction over citizen testimonies so that I can identify dominant territorial problems without reading every individual submission."
- UC3c (Profile Consolidation): "As GaveaLab, I want to consolidate and update territory need profiles over time so that I can track changes, publish research findings, and measure the impact of interventions."

**Trade-offs documented:**
- SEC (anti-astroturfing verification) vs. UX (low-friction participation) -- resolved via tiered trust scoring (Pol.is model)
- DATA (anonymization at ingestion) vs. ARCH (provenance for longitudinal tracking) -- resolved via pseudonymous tokens in a separate purgeable identity ledger
- UX (synthesized outputs for managers) vs. SEC (synthesis layer capture) -- resolved via public-by-default synthesized outputs (Decidim transparency model)
