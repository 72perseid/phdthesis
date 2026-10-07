-- Where does the laboratory date of a context disagree with the period of the finds from it?
SELECT r.title AS excavation, c.label AS context, a.result_begin AS lab_from, a.result_end AS lab_to,
       f.label AS find, p.label AS period, p.begin_year AS period_from, p.end_year AS period_to
FROM analysis a
JOIN report r ON r.id = a.report
JOIN context c ON c.report = a.report AND c.id = a.dates
JOIN find f ON f.report = a.report AND f.at_feature = c.id
JOIN dating d ON d.report = f.report AND d.id = f.id
JOIN period p ON p.report = d.report AND p.id = d.period
WHERE p.end_year < a.result_begin OR p.begin_year > a.result_end
ORDER BY excavation, context, find;
