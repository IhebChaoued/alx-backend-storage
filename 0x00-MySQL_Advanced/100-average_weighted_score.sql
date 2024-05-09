-- Create stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    
    SELECT SUM(corrections.score * projects.weight) INTO total_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    SELECT SUM(weight) INTO total_weight FROM projects;

    UPDATE users
    SET average_score = total_weighted_score / total_weight
    WHERE id = user_id;
END//

DELIMITER ;
