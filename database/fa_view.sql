-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3325
-- Generation Time: Jun 27, 2024 at 08:13 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `automata`
--

-- --------------------------------------------------------

--
-- Structure for view `fa_view`
--

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `fa_view`  AS SELECT `f`.`id` AS `FA`, `f`.`type` AS `Type`, `f`.`description` AS `Description`, `ss`.`name` AS `Start State`, `fs`.`name` AS `Final State`, `s`.`name` AS `State`, `sl`.`name` AS `Symbol`, `sf`.`name` AS `State From`, `st`.`name` AS `State To` FROM (((((((((`fa` `f` join `start_state` `ss` on(`ss`.`id` = `f`.`start_state_id`)) join `final_state` `fs` on(`fs`.`id` = `f`.`final_state_id`)) join `state_list` `stl` on(`stl`.`fa_id` = `f`.`id`)) join `state` `s` on(`s`.`id` = `stl`.`state_id`)) join `transition_list` `tl` on(`tl`.`fa_id` = `f`.`id`)) join `transition` `t` on(`t`.`id` = `tl`.`transition_id`)) join `state_from` `sf` on(`sf`.`id` = `t`.`state_from_id`)) join `state_to` `st` on(`st`.`id` = `t`.`state_to_id`)) join `symbol_list` `sl` on(`sl`.`fa_id` = `f`.`id`)) ;

--
-- VIEW `fa_view`
-- Data: None
--

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
