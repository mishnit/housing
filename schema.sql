--
-- Table structure for table `houses`
--

DROP TABLE IF EXISTS `houses`;
CREATE TABLE `houses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` varchar(512) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `style` varchar(100) DEFAULT NULL,
  `bedrooms` int(11) DEFAULT NULL,
  `bathrooms` int(11) DEFAULT NULL,
  `sold` int(11) DEFAULT NULL,
  `list` int(11) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `subarea` varchar(100) DEFAULT NULL,
  `near` varchar(100) DEFAULT NULL,
  `age` varchar(100) DEFAULT NULL,
  `basement` varchar(100) DEFAULT NULL,
  `mbr` varchar(100) DEFAULT NULL,
  `listdate` date DEFAULT NULL,
  `solddate` date DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=145 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `features`;
CREATE TABLE `features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `feature` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=145 DEFAULT CHARSET=latin1;

