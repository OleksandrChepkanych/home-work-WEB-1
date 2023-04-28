-- Список курсів, які певному студенту читає певний викладач
SELECT d.name  as Discipline, s.full_name as Student, t.full_name as Teacher
FROM grades g 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN teacher t on t.id = d.teacher_id 
WHERE s.id = 1 and t.id = 6
GROUP BY d.id 