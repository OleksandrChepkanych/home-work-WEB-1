-- Оцінки студентів у певній групі з певного предмета на останньому занятті
SELECT g.grade as Grades, s.full_name as Students, d.name as Discipline, g.date_of as Date
FROM grades g 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN groups gr on gr.id = s.groups_id
WHERE gr.id = 2 and d.id = 6 and g.date_of IN (select MAX(g.date_of)
FROM grades g 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN groups gr on gr.id = s.groups_id 
LEFT JOIN discipline d on d.id = g.discipline_id 
WHERE gr.id = 2 and d.id = 6) 