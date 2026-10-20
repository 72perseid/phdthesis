# Problem statement, candidates

Written 2026-10-19. Three framings of the same material. The recommendation is at the end.

A problem statement has four parts: the situation, the gap, the consequence, the question.
A thesis answers the question with evidence. Everything that does not produce evidence for the question is a tool or an appendix.

## The situation, shared by all three

Fieldwork projects in Türkiye record what they find in their own structures and their own words:
paper forms, Excel, Word, the ministry's Ek-21 form. The record stays in the project's archive.
What reaches the public is the distilled report in Kazı Sonuçları Toplantısı.
When the director changes, the season ends, or a specialist leaves, the record is read by someone who was not there.

An international structure for such records exists, CIDOC CRM with CRMarchaeo and CRMsci,
and tools built on it exist, Arches, OpenAtlas, iDAI.field. No project in Türkiye uses them.

## Framing A. Translation: what the published record yields

Not part of the thesis. Stated by the user 2026-10-19: the KST work was a private pilot to explore the ontology, the tools and the measures. It is not a chapter and not a baseline. Kept here only to record what was learned from it.

Gap: nobody has measured how much of a Turkish fieldwork report can be turned into comparable, structured data, or where it fails.
Question: how much of what a published Turkish excavation report states can be made comparable across projects under CIDOC CRM, and what is lost?
Evidence: the KST papers, the blind tests. Already in hand: about a third, and the loss is mostly vocabulary.
Weakness: the report is already a distillation. Measuring it says little about the archive, which is where the problem is.
What it taught: the structure can be derived by a written procedure; the loss is mostly vocabulary; a loader with frozen rules gives repeatable outcomes. These lessons carry over. The numbers do not.

## Framing B. Recording: capture at the source

Gap: the standard is not adoptable by a Turkish team as it stands. It needs a data modeller, English, a server, and lists that do not exist.
Nobody has shown what it takes to remove those obstacles, or what share of a team's records the standard then captures.
Question: can a Turkish fieldwork team record directly into a CIDOC CRM conformant structure, without a data modeller,
and what share of what they record becomes comparable data at the point of recording?
Evidence: two surveys. The first observed as it is, the second recorded with the structure and lists. Typed share before and after.
Weakness: depends on field access, and the surveys test the survey part only. The excavation part stays on paper.
Role if not chosen: the application chapter.

## Framing C. Reuse: does the record survive handover

Gap: the real failure is not storage but reading. Nobody has tested whether a record made this way can be used by an archaeologist who was not there.
Question: what is lost between the field and the person who later reads the record, and does structured recording reduce that loss?
Evidence: handover test. A second archaeologist answers a fixed set of questions from the records, once from the project's own files, once from the structured ones.
Weakness: hardest to design well, small numbers of people, results are qualitative as much as quantitative.
Role if not chosen: the evaluation chapter.

## Framing D. Sharing: FAIR data and the technical excuse

Added 2026-10-19 after the user rejected C as too narrow. This is the user's framing.

Gap: fieldwork data in Türkiye is not FAIR. It is not findable outside the project, not accessible,
not interoperable, and reusable only by the people who made it. Directors give reasons for not sharing,
and one of the reasons given is technical: there is no tool, no standard they can apply, no time.
Nobody has tested whether that reason is real, that is, whether willingness to share changes
when the technical barrier is lowered to a form with lists on a phone.

Question: if the technical barrier to FAIR-compliant fieldwork recording is lowered to this level,
does the willingness of Turkish fieldwork directors to share data change, and what level of FAIRness does the record then reach?

Two claims, two kinds of evidence:

| Claim | Evidence | Kind |
|---|---|---|
| The record produced this way is FAIR to a measurable degree | FAIR assessment of the output: identifiers, metadata, licence, CRM conformance, vocabulary alignment. ARIADNE's criteria exist for this | technical, in hand |
| Lowering the technical barrier changes willingness to share | before-and-after interviews or questionnaire with directors, with the working demonstrator as the stimulus | social, needs people and ethics approval |

Risk, stated plainly: the literature on data sharing in archaeology says the technical barrier is rarely the main one.
Career incentives, fear of being pre-empted, the permit regime, and the ministry's ownership of the material weigh more.
The hypothesis may be falsified. That is still a thesis result, and a useful one, if the study is designed to tell the barriers apart.
A study that only asks "would you share now?" cannot. One that asks about each barrier separately, before and after the demonstration, can.

Design consequences:

- The demonstrator must be real enough to be shown. A spreadsheet with lists is enough for the first survey; the app is the stimulus for the interviews.
- The interviews need ethics committee approval, which takes months. Start the application now.
- The sample is directors and senior team members, reached through the advisor. Twenty is realistic, two hundred is not. The result is qualitative with counts, not a statistical test.
- Reasons for not sharing must be separated in the instrument: technical, legal and permit, incentive, trust, time.
- FAIR gives the structure chapter its purpose. CRM and the lists are the I and the R. Identifiers, metadata and licence are the F and the A, and they are cheap to add but must be designed in.

## Recommendation, revised

Take D as the problem. B is the intervention and the stimulus. C, the handover test, is one measure of R in FAIR. A is outside the thesis.

The problem: fieldwork data in Türkiye is not FAIR, and the technical excuse for that has never been tested.

The question: when the technical barrier to FAIR-compliant recording is removed, is the data more FAIR, and are the people more willing?

| Sub-question | Evidence | Status |
|---|---|---|
| Can a Turkish team record into a FAIR, CRM-conformant structure without a modeller | the procedure, the lists from the surveys, the demonstrator, typed share before and after | structure on paper, lists not started |
| How FAIR is the result | FAIR assessment of the survey output against published criteria | not started, cheap once the output exists |
| Does the lowered barrier change willingness to share, and which barriers remain | interviews before and after the demonstration, barriers separated | needs ethics approval and the advisor's network |

What this rules out: generative UI and chat entry; backfilling archives; the excavation module as a tested claim until a trench exists; the KST pilot and its numbers as thesis evidence.

## Title candidates, revised

- Lowering the barrier: FAIR fieldwork data for Turkish archaeology and whether the barrier was the problem
- FAIR by default: a CIDOC CRM recording model for Turkish fieldwork and its effect on willingness to share
