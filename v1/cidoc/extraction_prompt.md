# Extraction prompt (for the other KST papers)

Both worked records were extracted by close reading. To repeat the step with a
language model, give it the paper text (from `pdftotext -layout`), `schema.md`
and this instruction. The output must pass `build_graph.py` and
`run_queries.py` before it is accepted; a SHACL violation points to a field
that is missing or wrong, a warning to something the paper itself omits.

---

You are extracting a structured record from a Turkish excavation report
published in Kazı Sonuçları Toplantısı. Produce ONE JSON object that follows
`schema.md` (version 3) exactly. Rules:

1. Record only what the text states. Do not infer dates, counts, names or
   functions. If the paper gives no date for an earlier campaign, leave
   `timespan` out. If it gives only an initial ("V. Onar"), keep the initial.
2. Hedged statements ("olduğu düşünülmektedir", "muhtemelen", "olabileceği",
   "değerlendirilmektedir") go into `interpretations`, or carry
   `certainty` on a relation. They never become a plain `type` or `period`.
3. Every item carries the printed page number(s) in `pages`.
4. The reporting campaign is `A9_Archaeological_Excavation` and is named in
   `document.documents`. Earlier campaigns the paper summarises are separate
   A9 activities listed in its `continued`.
5. Each trench or area dug in the reporting year is one
   `A1_Excavation_Processing_Unit` with `part_of` the campaign. Cleaning,
   sieving, survey, analysis, restoration, outreach, funding and permits are
   `E7_Activity` with a `type`.
6. Anything announced for a future season goes into `plans`, never
   `activities`.
7. Named contexts (A701, BX, M1, D1 ...) are `features` or `strata` with the
   code in `identifier`. Deposits and layers (dolgu, tabaka, kül, harç) are
   `strata`; a find said to come from one gets `from_stratum`.
8. Statements that one context cuts, destroys, overlies, fills or abuts
   another go into `relations`, from the later to the earlier unit.
9. Single objects and bulk assemblages are both `finds`; give `count` only
   when a number is printed. Plant and animal remains are
   `E20_Biological_Object` with scientific or vernacular names in `taxa`,
   spelled as printed.
10. When a dating or identification is credited to someone other than the
    authors (kişisel görüşme, a named specialist), add `dating_by` or
    `identified_by` with that person and `via`.
11. A laboratory date is an `analysis` on one or more `samples`; `dates` names
    the context or object it dates. Keep the range exactly as printed; BC
    years are negative.
12. Periods: reuse the paper's labels. Give `begin` / `end` only when the paper
    gives years or centuries (MS 12.-13. yy → 1100 / 1299). Sub-phases use
    `within`.
13. Measurements: `value` for a single figure, `min` / `max` for a range,
    `approx: true` for "yaklaşık". Depths keep their sign.
14. Figures: one entry per caption, with `kind` as printed (Resim, Şekil,
    Plan, Harita) and an `id` built from kind and number.
15. Where the paper contradicts itself or a name is ambiguous, record what is
    printed and say so in `note`. Do not resolve it.
16. A hedged period ("Neolitik?", "olasılıkla Holosen") gets `dating_certainty: "uncertain"`;
    alternatives ("OP-ÜP?") list both periods with `dating_certainty: "one of"`.
17. A printed table of counts becomes one find per filled cell, each `part_of` the total.
    Check the cells against the printed totals. If they disagree, keep the printed numbers and say so in `note`.
18. Plans, drawings and models made on site go into `records`. Cited literature goes into `references`,
    and the item that rests on it gets `sources`.
19. Do not record e-mail addresses.
20. Return only the JSON.
