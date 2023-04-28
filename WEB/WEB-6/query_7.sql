-- Знайти оцінки студентів у окремій групі з певного предмета
SELECT g.grade as Grade, d.name as Discipline, s.full_name as Students, gr.name as [Group]
FROM grades g 
LEFT JOIN discipline d on d.id = g.discipline_id 
LEFT JOIN students s on s.id = g.students_id 
LEFT JOIN groups gr on gr.id = s.groups_id 
WHERE gr.id = 1 and d.id = 1