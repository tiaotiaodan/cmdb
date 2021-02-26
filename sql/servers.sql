/*
Navicat MySQL Data Transfer

Source Server         : 施超-测试数据库
Source Server Version : 50732
Source Host           : 127.0.0.1:3306
Source Database       : cmdb

Target Server Type    : MYSQL
Target Server Version : 50732
File Encoding         : 65001

Date: 2021-02-20 11:44:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for servers
-- ----------------------------
DROP TABLE IF EXISTS `servers`;
CREATE TABLE `servers` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `server_name` varchar(100) NOT NULL,
  `server_ip` varchar(50) NOT NULL,
  `server_port` int(11) NOT NULL,
  `server_user` varchar(50) NOT NULL,
  `server_passwd` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=468 DEFAULT CHARSET=utf8;
