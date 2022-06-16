/*
SQLyog Trial v13.1.8 (64 bit)
MySQL - 8.0.29 : Database - crypto_trans
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`crypto_trans` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `crypto_trans`;

/*Table structure for table `payment_list` */

DROP TABLE IF EXISTS `payment_list`;

CREATE TABLE `payment_list` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `TxAddr` varchar(255) DEFAULT NULL,
  `Amount` float DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `payment_list` */

insert  into `payment_list`(`ID`,`Name`,`TxAddr`,`Amount`) values 
(1,'Receiver','0x138EB2CED1E7d03dff233Aa527723df7876Bee52',0.005),
(2,'Account3','0x4cbff41f012534E67bb0D6111476e299224E9B8f',0.002),
(3,'Account4','0x38056037697CE79ABB21F2217F552D614Db7a06b',0.004),
(4,'Wrong','0x38056037697CE79ABB21F2217F552D614Db7a067',0.04);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
