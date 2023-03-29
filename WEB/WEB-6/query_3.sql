-- Знайти середній бал у групах з певного предмета.
SELECT g2.name, d.name, ROUND(AVG(g.grade), 2) as AVG_grade
from grades g 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN [groups] g2 on g2.id = s.groups_id 
LEFT JOIN discipline d on d.id = g.discipline_id 
WHERE d.id = 1
GROUP BY g2.id 
ORDER BY AVG_grade DESC 