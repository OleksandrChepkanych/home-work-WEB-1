-- Знайти список курсів, які відвідує студент
SELECT d.name as Discipline, s.full_name as Student
from grades g 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN students s on s.id = g.students_id 
WHERE students_id = 3
GROUP BY d.id