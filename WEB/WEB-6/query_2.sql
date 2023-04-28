-- Знайти студента із найвищим середнім балом з певного предмета
SELECT d.name as Discipline_name, s.full_name as Fullname, ROUND(avg(g.grade),2) as AVG_Grade
FROM grades g
LEFT JOIN students s on s.id = g.students_id
LEFT JOIN discipline d ON d.id = g.discipline_id
WHERE d.id = 1
GROUP BY s.id, d.id 
ORDER BY avg(g.grade) DESC 
LIMIT 1;
