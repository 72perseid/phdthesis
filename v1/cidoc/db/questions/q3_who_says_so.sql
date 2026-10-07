-- How much of each report is observation, and how much is a claim someone makes?
SELECT r.title AS excavation,
       (SELECT count(*) FROM context x WHERE x.report = r.id) AS contexts,
       (SELECT count(*) FROM find x WHERE x.report = r.id) AS finds,
       (SELECT count(*) FROM relation x WHERE x.report = r.id) AS stratigraphic_relations,
       (SELECT count(*) FROM analysis x WHERE x.report = r.id) AS lab_results,
       (SELECT count(*) FROM interpretation x WHERE x.report = r.id) AS interpretations,
       (SELECT count(*) FROM attribution x WHERE x.report = r.id AND x.via = 'personal communication') AS by_personal_communication
FROM report r ORDER BY r.id;
