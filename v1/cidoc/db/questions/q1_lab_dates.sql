-- Which excavations report laboratory dates, for which contexts, from which samples?
SELECT r.title AS excavation, c.label AS context, a.result_begin AS from_year, a.result_end AS to_year,
       group_concat(s.label, '; ') AS samples,
       (SELECT group_concat(page) FROM source_page p WHERE p.report = a.report AND p.id = a.id) AS page
FROM analysis a
JOIN report r ON r.id = a.report
JOIN entity e ON e.report = a.report AND e.id = a.dates
LEFT JOIN context c ON c.report = a.report AND c.id = a.dates
JOIN analysis_sample x ON x.report = a.report AND x.analysis = a.id
JOIN sample s ON s.report = x.report AND s.id = x.sample
GROUP BY a.report, a.id ORDER BY a.result_begin;
