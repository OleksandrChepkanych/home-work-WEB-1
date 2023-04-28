-- Середній бал, який певний викладач ставить певному студентові
SELECT ROUND(AVG(g.grade), 2) as AVG_Grades, s.full_name as Students, t.full_name as Teacher 
FROM grades g 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN teacher t on t.id = d.teacher_id 
LEFT JOIN students s on s.id = g.students_id 
WHERE s.id = 1 and t.id = 6