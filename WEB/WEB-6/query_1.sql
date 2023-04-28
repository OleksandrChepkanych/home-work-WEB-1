-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT s.full_name as Fullname, ROUND(avg(g.grade),2) as AVG_Grade
FROM grades g
LEFT JOIN students s on s.id = g.students_id
GROUP BY s.id
ORDER BY avg(g.grade) DESC 
LIMIT 5;