-- Знайти які курси читає певний викладач
SELECT d.name as Discipline, t.full_name as Teacher
FROM discipline d 
LEFT JOIN teacher t on t.id = d.teacher_id 
WHERE teacher_id = 1