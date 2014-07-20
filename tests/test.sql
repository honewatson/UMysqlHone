CREATE DATABASE iF NOT EXISTS `umysqlhone_test`;
CREATE TABLE iF NOT EXISTS `umysqlhone_test`.`posts` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_name` char(255) DEFAULT NULL,
  `post_title` char(255) DEFAULT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
