sudo apt-get install python3-dev

sudo pip3 install cairocffi

pip install lxml

pip install


sudo apt-get install python3-dev python3-setuptools

sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev

pip install Pillow

pip install qrcode

pip install jinjia2

/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     12.12.2015 21:48:24                          */
/*==============================================================*/



drop table Answer;


drop table Answer_type;


drop table Building;



drop table Contact;



drop table Contact_type;



drop table Family;



drop table Meeting;


drop table Owner;



drop table Owner_type;



drop table Premise;


drop table Property_rights;



drop table Property_type;



drop table Question;





drop table "User";

/*==============================================================*/
/* Table: Answer                                                */
/*==============================================================*/
create table Answer (
   id_question          INT4                 not null,
   id_owner             INT4                 not null,
   id_answer_type       INT4                 null,
   answer_num           FLOAT8               null,
   answer_str           VARCHAR(256)         null,
   constraint PK_ANSWER primary key (id_question, id_owner)
);

comment on table Answer is
'Îòâåò íà âîïðîñ íà ñîáðàíèè ñîáñòâåííèêîâ îäíîãî èç ñîáñòâåííèêîâ

id_question - ññûëêà íà âîïðîñ, íà êîòîðûé áûë äàí îòâåò
id_owner - ññûëêà íà ñîáñòâåííèêà, êîòîðûé äàë îòâåò íà âîïðîñ
id_answer_type - ññûëêà íà îòâåò íà âîïðîñ (çà, ïðîòèâ, âîçäåðæàëñÿ)
answer_num - îòâåò íà âîïðîñ â âèäå ÷èñëà (åñëè ïðèìåíèìî ê äàííîìó âîïðîñó)
answer_str - îòâåò íà âîïðîñ â âèäå ñòðîêè (åñëè ïðèìåíèìî ê äàííîìó âîïðîñó)';


/*==============================================================*/
/* Table: Answer_type                                           */
/*==============================================================*/
create table Answer_type (
   id_answer_type       INT4                 not null,
   type                 VARCHAR(64)          null,
   constraint PK_ANSWER_TYPE primary key (id_answer_type)
);

comment on table Answer_type is
'Òèï îòâåòà íà âîïðîñ ãîëîñîâàíèÿ

Çà, ïðîòèâ, âîçäåðæàëñÿ';


/*==============================================================*/
/* Table: Building                                              */
/*==============================================================*/
create table Building (
   id_building          INT4                 not null,
   address              VARCHAR(256)         null,
   street               VARCHAR(64)          null,
   street_number        INT4                 null,
   block                INT4                 null,
   block_type           VARCHAR(32)          null,
   constraint PK_BUILDING primary key (id_building)
);

comment on table Building is
'Çäàíèå

Îáùàÿ èíôîðìàöèÿ î çäàíèè (àäðåñ, êîëè÷åñòâî ïîäúåçäîâ, êîëè÷åñòâî êâàðòèð, ýòàæíîñòü, ïëîùàäü, ...)

id_building
address - ïîëíûé àäðåñ
street - íàçâàíèå óëèöû áåç èäåíòèôèêàòîðà "óë.", "ïð.", "ïåð." è ò.ä.
street_number - íîìåð äîìà
block - êîðïóñ
block_type - ëèòåðà äîìà';


/*==============================================================*/
/* Table: Contact                                               */
/*==============================================================*/
create table Contact (
   id_contact           INT4                 not null,
   id_owner             INT4                 not null,
   id_contact_type      INT4                 not null,
   contact              VARCHAR(256)         not null,
   comment              VARCHAR(1024)        null,
   constraint PK_CONTACT primary key (id_contact)
);



/*==============================================================*/
/* Table: Contact_type                                          */
/*==============================================================*/
create table Contact_type (
   id_contact_type      INT4                 not null,
   type                 VARCHAR(128)         null,
   constraint PK_CONTACT_TYPE primary key (id_contact_type)
);

comment on table Contact_type is
'Òèï êîíòàêòíîé èíôîðìàöèè

Ìîáèëüíûé òåëåôîí, äîìàøíèé òåëåôîí, ðàáî÷èé òåëåôîí, ýëåêòðîííûé àäðåñ, ñîöèàëüíûå ñåòè è ò.ä.';



/*==============================================================*/
/* Table: Family                                                */
/*==============================================================*/
create table Family (
   id_family            INT4                 not null,
   id_premise           INT4                 null,
   id_property_type     INT4                 null,
   rooms                INT4                 null,
   living_space         FLOAT8               null,
   residents            INT4                 null,
   constraint PK_FAMILY primary key (id_family)
);

comment on table Family is
'Ñåìüÿ

Äàííûå ïî ñåìüÿì, ïðîæèâàþùèì (çàðåãåñòðèðîâàííûì) â êâàðòèðå

id_family - èäåíòèôèêàòîð ñåìüè
id_premise - ññûëêà íà ïîìåùåíèå (êâàðòèðó), â êîòîðîé æèâåò (ïðîïèñàíà) ñåìüÿ
id_property_type - ññûëêà íà òèï ñîáñòâåííîñòè (÷àñòíàÿ, äîëåâàÿ, ãîñóäàðñòâåííàÿ, ...)
rooms - ÷èñëî êîìíàò, êîòîðûå ïðèíàäëåæàò ñåìüå
living_space - æèëàÿ ïëîùàäü (â êâàäðàòíûõ ìåòðàõ)
residents - êîëè÷åñòâî ïðîïèñàííûõ ÷åëîâåê';


/*==============================================================*/
/* Table: Meeting                                               */
/*==============================================================*/
create table Meeting (
   id_meeting           INT4                 not null,
   id_building          INT4                 not null,
   date_start           DATE                 not null,
   date_end             DATE                 null,
   absent_voting        BOOL                 not null,
   constraint PK_MEETING primary key (id_meeting)
);

comment on table Meeting is
'Îáùåå ñîáðàíèå ñîáñòâåííèêîâ

id_meeting - èäåíòèôèêàòîð îáùåãî ñîáðàíèÿ ñîáñòâåííèêîâ (ÎÑÑ)
id_building - èäåíòèôèêàòîð çäàíèÿ, ñîáñòâåííèêè êîòîðîãî ïðîâîäÿò ÎÑÑ
date_start - äàòà è âðåìÿ íà÷àëà ÎÑÑ
date_end - äàòà è âðåìÿ êîíöà ÎÑÑ (äëÿ çàî÷íîãî ãîëîñîâàíèÿ)
absent_voting - ãîëîñîâàíèå çàî÷íîå? (çíà÷åíèå "TRUE", åñëè ýòî òàê)';


/*==============================================================*/
/* Table: Owner                                                 */
/*==============================================================*/
create table Owner (
   id_owner             INT4                 not null,
   id_owner_type        INT4                 null,
   name                 VARCHAR(64)          null,
   patronymic           VARCHAR(64)          null,
   surname              VARCHAR(64)          null,
   SNILS                VARCHAR(32)          not null,
   constraint PK_OWNER primary key (id_owner)
);

comment on table Owner is
'Ñîáñòâåííèê

ÔÈÎ (äëÿ ôèç ëèöà), íàçâàíèå äëÿ þðëèöà, íàèìåíîâàíèå îðãàíà ãîñ âëàñòè äëÿ ãîññîáñòâåííîñòè

ÑÍÈËÑ äîëæåí óêàçûâàòüñÿ âñåãäà. Åñëè îí íåèçâåñòåí - óêàçûâàåòñÿ ïóñòàÿ ñòðîêà (à íå NULL)';



/*==============================================================*/
/* Table: Owner_type                                            */
/*==============================================================*/
create table Owner_type (
   id_owner_type        INT4                 not null,
   type                 VARCHAR(64)          null,
   constraint PK_OWNER_TYPE primary key (id_owner_type)
);

comment on table Owner_type is
'Òèï ñîáñòâåííèêà

Ôèçè÷åñêîå ëèöî, þðèäè÷åñêîå ëèöî, ãîñóäàðñòâåííàÿ ñîáñòâåííîñòü';



/*==============================================================*/
/* Table: Premise                                               */
/*==============================================================*/
create table Premise (
   id_premise           INT4                 not null,
   id_building          INT4                 null,
   number               INT4                 null,
   number_add           VARCHAR(16)          null,
   floor                INT4                 null,
   porch                INT4                 null,
   cadastral_number     VARCHAR(256)         null,
   rooms                INT4                 null,
   area                 FLOAT8               null,
   area_rosreestr       FLOAT8               null,
   living_space         FLOAT8               null,
   kitchen_space        FLOAT8               null,
   public_facilities_space FLOAT8               null,
   families             INT4                 null,
   constraint PK_PREMISE primary key (id_premise)
);

comment on table Premise is
'Ïîìåùåíèå

Îïèñàíèå ïîìåùåíèÿ â çäàíèè (êâàðòèðû â æèëîì äîìå)

id_premise - èäåíòèôèêàòîð ïîìåùåíèÿ (êâàðòèðû)
id_building - ññûëêà íà çäàíèå, â êîòîðîì ðàñïîëîæåíî ýòî ïîìåùåíèå (êâàðòèðà)
number - íîìåð ïîìåùåíèÿ (êâàðòèðû)
number_add - ñòðîêîâûé èäåíòèôèêàòîð ïîìåùåíèÿ ("À", "Á", è ò.ï.)
floor - íîìåð ýòàæà
porch - íîìåð ïîäúåçäà

rooms - ÷èñëî êîìíàò
area - ïëîùàäü ïîìåùåíèÿ (êâàðòèðû) (â êâàäðàòíûõ ìåòðàõ)
area_rosreestr - ïëîùàäü ïîìåùåíèÿ (êâàðòèðû) ïî äàííûì ÐîñÐååñòðà (â êâàäðàòíûõ ìåòðàõ)
living_space - ïëîùàäü æèëàÿ (â êâàäðàòíûõ ìåòðàõ)
kitchen_space - ïëîùàäü êóõíè (â êâàäðàòíûõ ìåòðàõ)
public_facilities_space - ïëîùàäü ìåñò îáùåñòâåííîãî ïîëüçîâàíèÿ (ÌÎÏ: òóàëåò, âàííàÿ è ò.ä.) (â êâàäðàòíûõ ìåòðàõ)

families - ÷èñëî ñåìåé, ïðîæèâàþùèõ â ïîìåùåíèè (êâàðòèðå)';



/*==============================================================*/
/* Table: Property_rights                                       */
/*==============================================================*/
create table Property_rights (
   id_rights            INT4                 not null,
   id_premise           INT4                 not null,
   id_family            INT4                 null,
   id_owner             INT4                 not null,
   id_property_type     INT4                 null,
   share_numerator      INT4                 null,
   share_denominator    INT4                 null,
   regnumber            VARCHAR(128)         null,
   regdate              DATE                 null,
   constraint PK_PROPERTY_RIGHTS primary key (id_rights)
);

comment on table Property_rights is
'Ïðàâà ñîáñòâåííîñòè

Èíôîðìàöèÿ î ïðàâàõ ñîáñòâåíîñòè íà ïîìåùåíèå (êâàðòèðó)

id_rights - èäåíèôèêàòîð çàïèñè î ïðàâàõ ñîáñòâåííîñòè
id_premise - ññûëêà íà ïîìåùåíèå (êâàðòèðó), êîòîðîé ñîîòâåòñòâóåò äàííàÿ çàïèñü î ïðàâàõ ñîáñòâåííîñòè
id_family - ññûëêà íà ñåìüþ, íà êîòîðóþ çàðåãåñòðèðîâàíû ïðàâà ñîáñòâåííîñòè
id_owner - ññûëêà íà âëàäåëüöà ïðàâ ñîáñòâåííîñòè
id_property_type - ññûëêà íà òèï ñîáñòâåííîñòè (÷àñòíàÿ, äîëåâàÿ, ãîñóäàðñòâåííàÿ, ...)
share_numerator - äîëÿ â ñîáñòâåííîñòè (÷èñëèòåëü)
share_denominator - äîëÿ â ñîáñòâåííîñòè (çíàìåíàòåëü)
regnumber - íîìåð äîêóìåíòà, ïîäòâåðæäàþùåãî ïðàâà ñîáñòâåííîñòè
regdate - äàòà ðåãèñòðàöèè ïðàâ ñîáñòâåííîñòè';
/*==============================================================*/
/* Table: Property_type                                         */
/*==============================================================*/
create table Property_type (
   id_property_type     INT4                 not null,
   type                 VARCHAR(64)          null,
   rosreestr_type_id    VARCHAR(32)          null,
   constraint PK_PROPERTY_TYPE primary key (id_property_type)
);

comment on table Property_type is
'Òèï ñîáñòâåííîñòè

×àñòíàÿ, äîëåâàÿ, ãîñóäàðñòâåííàÿ, ...';


/*==============================================================*/
/* Table: Question                                              */
/*==============================================================*/
create table Question (
   id_question          INT4                 not null,
   id_meeting           INT4                 not null,
   sequence_no          INT2                 not null,
   question             VARCHAR(512)         not null,
   constraint PK_QUESTION primary key (id_question)
);

comment on table Question is
'Âîïðîñ íà ñîáðàíèè ñîáñòâåííèêîâ

id_question - èäåíòèôèêàòîð âîïðîñà
id_meeting - ññûëêà íà îáùåå ñîáðàíèå ñîáñòâåííèêîâ, íà êîòîðîì îáñóæäàåòñÿ âîïðîñ
sequence_no - ïîðÿäêîâûé íîìåð âîïðîñà â áþëëåòåíå
question - âîïðîñ äëÿ ãîëîñîâàíèÿ íà ñîáðàíèè';



/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" (
   id_user              INT4                 not null,
   id_owner             INT4                 null,
   id_premise           INT4                 null,
   login                VARCHAR(32)          not null,
   password             VARCHAR(32)          not null,
   admin                INT4                 not null,
   status               INT4                 not null,
   name                 VARCHAR(64)          not null,
   surname              VARCHAR(64)          not null,
   patronymic           VARCHAR(64)          null,
   phone                VARCHAR(32)          not null,
   email                VARCHAR(32)          not null,
   constraint PK_USER primary key (id_user)
);




