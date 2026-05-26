# QA Log -- communicate 000007

**Brief:** re-write this repo readme in order to comunicate what is being done in last commits ( running talk to the city locally  
**Skill:** communicate  
**ID:** 000007  
**Date:** 2026-05-26 11:06 UTC -- 2026-05-26 11:10 UTC

---

## Q&A

**Q: Who is the primary audience for this README?**  
A: Academics (ACD) -- researchers and peers interested in the Talk to the City + local LLM approach.

**Q: Should I update the README.md file directly, or generate a communication artifact in _output/communication/?**  
A: Update README.md directly.

---

## Context gathered

Recent commits showed the project has evolved beyond the original kb-qa RAG tool to include a full Talk to the City PoC (TRL 3) running locally. Key work:

- `tttc-poc/`: Docker Compose stack with five services (ollama, redis, pyserver, express-server, next-client)
- Every cloud dependency replaced: OpenAI -> Ollama + llama3.2, Firebase Auth -> TypeScript stub patch, GCS -> LocalFileStorage patch
- Test data: `tttc-poc/data/sample-gavealab.csv` (25 qualitative urban responses, Gavea/Rio)
- Original README described only kb-qa and made no mention of the PoC work

---

## Outcome

`README.md` rewritten to cover both artifacts, leading with the Talk to the City PoC and its research motivation (local deployment of a participatory AI platform). kb-qa retained as a secondary section.
