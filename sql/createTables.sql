create schema mydb;
use mydb;


CREATE TABLE chedui
(
	chedui_id            INTEGER NOT NULL PRIMARY KEY auto_increment,
	cheduiduizhang       VARCHAR(20) NULL
);



CREATE TABLE luduizhang
(
	luduizhang_id        INTEGER NOT NULL,
    xianlu_mingcheng     VARCHAR(20) NULL
);



ALTER TABLE luduizhang
ADD PRIMARY KEY (luduizhang_id);



CREATE TABLE qiche
(
	chepaihao            VARCHAR(20) NOT NULL,
	zuoshu               INTEGER NULL,
	xianlu_mingcheng     VARCHAR(20) NOT NULL
);



ALTER TABLE qiche
ADD PRIMARY KEY (chepaihao);



CREATE TABLE siji
(
	siji_id              INTEGER NOT NULL PRIMARY KEY auto_increment,
	siji_xingming        VARCHAR(20) NULL,
	siji_xingbie         VARCHAR(20) NULL,
	xianlu_mingcheng     VARCHAR(20) NOT NULL
);





CREATE TABLE weizhang
(
	weizhang_id          INTEGER NOT NULL  PRIMARY KEY auto_increment,
	weizhang_neirong     VARCHAR(20) NULL
);




CREATE TABLE weizhangjilu
(
	siji_id              INTEGER NULL,
	shijian              DATETIME NULL,
	weizhangjilu_id      INTEGER NOT NULL PRIMARY KEY auto_increment,
	chepaihao            VARCHAR(20) NULL,
	weizhang_id          INTEGER NULL,
	zhandian_id          INTEGER NULL
);





CREATE TABLE xianlu
(
	chedui_id            INTEGER NOT NULL,
	xianlu_mingcheng     VARCHAR(20) NOT NULL
);



ALTER TABLE xianlu
ADD PRIMARY KEY (xianlu_mingcheng);



CREATE TABLE zhandian
(
	zhandian_id          INTEGER NOT NULL PRIMARY KEY auto_increment,
	zhandian_mingcheng   VARCHAR(20) NULL
);





CREATE TABLE zhandianxianlu
(
	xianlu_mingcheng     VARCHAR(20) NOT NULL,
	zhandian_id          INTEGER NOT NULL
);



ALTER TABLE zhandianxianlu
ADD PRIMARY KEY (xianlu_mingcheng,zhandian_id);



ALTER TABLE luduizhang
ADD FOREIGN KEY R_61 (luduizhang_id) REFERENCES siji (siji_id);



ALTER TABLE luduizhang
ADD FOREIGN KEY R_612 (xianlu_mingcheng) REFERENCES xianlu (xianlu_mingcheng);



ALTER TABLE qiche
ADD FOREIGN KEY R_36 (xianlu_mingcheng) REFERENCES xianlu (xianlu_mingcheng);



ALTER TABLE siji
ADD FOREIGN KEY R_60 (xianlu_mingcheng) REFERENCES xianlu (xianlu_mingcheng);



ALTER TABLE weizhangjilu
ADD FOREIGN KEY R_29 (siji_id) REFERENCES siji (siji_id);



ALTER TABLE weizhangjilu
ADD FOREIGN KEY R_49 (chepaihao) REFERENCES qiche (chepaihao);



ALTER TABLE weizhangjilu
ADD FOREIGN KEY R_63 (weizhang_id) REFERENCES weizhang (weizhang_id);



ALTER TABLE weizhangjilu
ADD FOREIGN KEY R_64 (zhandian_id) REFERENCES zhandian (zhandian_id);



ALTER TABLE xianlu
ADD FOREIGN KEY R_32 (chedui_id) REFERENCES chedui (chedui_id);



ALTER TABLE zhandianxianlu
ADD FOREIGN KEY R_54 (xianlu_mingcheng) REFERENCES xianlu (xianlu_mingcheng);



ALTER TABLE zhandianxianlu
ADD FOREIGN KEY R_62 (zhandian_id) REFERENCES zhandian (zhandian_id);


create view sjwz as
select siji_id, shijian, zhandian_mingcheng zhandian, weizhang_neirong weizhang 
from weizhang, weizhangjilu, zhandian 
where weizhang.weizhang_id = weizhangjilu.weizhang_id
and zhandian.zhandian_id = weizhangjilu.zhandian_id;

create view cdwz as
select chedui_id, shijian, zhandian_mingcheng zhandian, weizhang_neirong weizhang
from weizhang, weizhangjilu, zhandian, siji, xianlu
where weizhang.weizhang_id = weizhangjilu.weizhang_id
and zhandian.zhandian_id = weizhangjilu.zhandian_id
and weizhangjilu.siji_id = siji.siji_id
and siji.xianlu_mingcheng = xianlu.xianlu_mingcheng;

create view zdxl as
select xianlu_mingcheng, zhandian_mingcheng
from zhandianxianlu, zhandian
where zhandianxianlu.zhandian_id = zhandian.zhandian_id;


set foreign_key_checks = 0;

alter table chedui CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table luduizhang CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table weizhang CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table zhandian CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table xianlu CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table siji CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table weizhangjilu CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table zhandianxianlu CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;
alter table qiche CONVERT TO CHARACTER SET utf8 collate utf8_general_ci;

set foreign_key_checks = 1


DELIMITER $$
USE `mydb`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lrqc`(in chepai varchar(20), in n int(11), in xianlu varchar(20))
BEGIN

insert into
qiche(chepaihao, zuoshu, xianlu_mingcheng)
values(chepai, n, xianlu);

END$$
DELIMITER ;


DELIMITER $$
USE `mydb`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lrsj`(in id int(11),in xingming varchar(20),in xingbie varchar(20), in xianlu varchar(20))
BEGIN

insert into
siji(siji_id, siji_xingming, siji_xingbie, xianlu_mingcheng)
values(id, xingming, xingbie, xianlu);

END$$

DELIMITER ;


DELIMITER $$
USE `mydb`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `lrwz`(in id int(11), in chepai varchar(20), in weizhang_nr varchar(20), in zhandian_mc varchar(20), in shijian datetime)
BEGIN

insert into
weizhangjilu(siji_id, chepaihao, shijian, weizhang_id, zhandian_id)
values(id, chepai, shijian, 
(select weizhang_id
from weizhang
where weizhang_neirong = weizhang_nr),
(select zhandian_id
from zhandian
where zhandian_mingcheng = zhandian_mc));

END$$

DELIMITER ;



