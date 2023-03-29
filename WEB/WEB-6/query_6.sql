-- Знайти список студентів у певній групі
SELECT s.full_name as Students, g.name as [Group]
FROM students s 
LEFT JOIN groups g on g.id = s.groups_id
WHERE s.groups_id = 2