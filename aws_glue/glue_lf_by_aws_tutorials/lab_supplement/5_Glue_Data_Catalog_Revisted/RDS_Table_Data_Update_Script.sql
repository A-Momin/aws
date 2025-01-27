ALTER TABLE employees
ADD createdon date; 

update employees set createdon = CURRENT_DATE ;