-- Знайти середній бал, який ставить певний викладач зі своїх предметів
SELECT ROUND(avg(g.grade), 2) as AVG_Grade, t.full_name as Teacher, d.name as Discipline
from grades g 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN teacher t on t.id = d.teacher_id 
WHERE t.id = 1
GROUP BY d.id 