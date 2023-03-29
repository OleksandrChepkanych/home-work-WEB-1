-- Знайти середній бал на потоці (по всій таблиці оцінок)
SELECT g2.name as Groups, ROUND(AVG(g.grade), 2) as AVG_grade
from grades g 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN [groups] g2 on g2.id = s.groups_id 
GROUP BY g2.id