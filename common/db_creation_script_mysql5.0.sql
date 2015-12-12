/* ============================================================== */
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     12.12.2015 15:37:42                          */
/* ==============================================================*/



drop table if exists Answer;

drop table if exists Answer_type;

drop table if exists Building;

drop table if exists Contact;

drop table if exists Contact_type;

drop table if exists Family;

drop table if exists Meeting;

drop table if exists Owner;

drop table if exists Owner_type;

drop table if exists Premise;

drop table if exists Property_rights;

drop table if exists Property_type;

drop table if exists Question;

drop table if exists User;

/*==============================================================*/
/* Table: Answer                                                */
/*==============================================================*/
create table Answer
(
   id_question          int not null,
   id_owner             int not null,
   id_answer_type       int,
   answer_num           float,
   answer_str           varchar(256),
   primary key (id_question, id_owner)
);

alter table Answer comment 'Ответ на вопрос на собрании собственников одного из собствен';

/*==============================================================*/
/* Table: Answer_type                                           */
/*==============================================================*/
create table Answer_type
(
   id_answer_type       int not null,
   type                 varchar(64),
   primary key (id_answer_type)
);

alter table Answer_type comment 'Тип ответа на вопрос голосования

За, против, во';

/*==============================================================*/
/* Table: Building                                              */
/*==============================================================*/
create table Building
(
   id_building          int not null,
   address              varchar(256),
   street               varchar(64),
   street_number        int,
   block                int,
   block_type           varchar(32),
   primary key (id_building)
);

alter table Building comment 'Здание

Общая информация о здании (адрес, количе';

/*==============================================================*/
/* Table: Contact                                               */
/*==============================================================*/
create table Contact
(
   id_contact           int not null,
   id_owner             int not null,
   id_contact_type      int not null,
   contact              varchar(256) not null,
   comment              varchar(1024),
   primary key (id_contact)
);

alter table Contact comment 'Контактная информация

Контакты вледельца помеще';

/*==============================================================*/
/* Table: Contact_type                                          */
/*==============================================================*/
create table Contact_type
(
   id_contact_type      int not null,
   type                 varchar(128),
   primary key (id_contact_type)
);

alter table Contact_type comment 'Тип контактной информации

Мобильный телефон, до';

/*==============================================================*/
/* Table: Family                                                */
/*==============================================================*/
create table Family
(
   id_family            int not null,
   id_premise           int,
   id_property_type     int,
   rooms                int,
   living_space         float,
   residents            int,
   primary key (id_family)
);

alter table Family comment 'Семья

Данные по семьям, проживающим (зарегестри';

/*==============================================================*/
/* Table: Meeting                                               */
/*==============================================================*/
create table Meeting
(
   id_meeting           int not null,
   id_building          int not null,
   date_start           datetime not null,
   date_end             datetime,
   absent_voting        bool not null,
   primary key (id_meeting)
);

alter table Meeting comment 'Общее собрание собственников

id_meeting - идент';

/*==============================================================*/
/* Table: Owner                                                 */
/*==============================================================*/
create table Owner
(
   id_owner             int not null,
   id_owner_type        int,
   name                 varchar(64),
   patronymic           varchar(64),
   surname              varchar(64),
   SNILS                varchar(32) not null,
   primary key (id_owner)
);

alter table Owner comment 'Собственник

ФИО (для физ лица), название для юр';

/*==============================================================*/
/* Table: Owner_type                                            */
/*==============================================================*/
create table Owner_type
(
   id_owner_type        int not null,
   type                 varchar(64),
   primary key (id_owner_type)
);

alter table Owner_type comment 'Тип собственника

Физическое лицо, юридическое л';

/*==============================================================*/
/* Table: Premise                                               */
/*==============================================================*/
create table Premise
(
   id_premise           int not null,
   id_building          int,
   number               int,
   number_add           varchar(16),
   floor                int,
   porch                int,
   cadastral_number     varchar(256),
   rooms                int,
   area                 float,
   area_rosreestr       float,
   living_space         float,
   kitchen_space        float,
   public_facilities_space float,
   families             int,
   primary key (id_premise)
);

alter table Premise comment 'Помещение

Описание помещения в здании (квартиры';

/*==============================================================*/
/* Table: Property_rights                                       */
/*==============================================================*/
create table Property_rights
(
   id_rights            int not null,
   id_premise           int not null,
   id_family            int,
   id_owner             int not null,
   id_property_type     int,
   share_numerator      int,
   share_denominator    int,
   regnumber            varchar(128),
   regdate              date,
   primary key (id_rights)
);

alter table Property_rights comment 'Права собственности

Информация о правах собстве';

/*==============================================================*/
/* Table: Property_type                                         */
/*==============================================================*/
create table Property_type
(
   id_property_type     int not null,
   type                 varchar(64),
   rosreestr_type_id    varchar(32),
   primary key (id_property_type)
);

alter table Property_type comment 'Тип собственности

Частная, долевая, государстве';

/*==============================================================*/
/* Table: Question                                              */
/*==============================================================*/
create table Question
(
   id_question          int not null,
   id_meeting           int not null,
   question             varchar(512) not null,
   primary key (id_question)
);

alter table Question comment 'Вопрос на собрании собственников

id_question - ';

/*==============================================================*/
/* Table: User                                                  */
/*==============================================================*/
create table User
(
   id_user              int not null,
   id_owner             int,
   id_premise           int,
   login                varchar(32) not null,
   password             varchar(32) not null,
   admin                int not null,
   status               int not null,
   name                 varchar(64) not null,
   surname              varchar(64) not null,
   patronymic           varchar(64),
   phone                varchar(32) not null,
   email                varchar(32) not null,
   primary key (id_user)
);

alter table User comment 'Information about a web user';

alter table Answer add constraint FK_many_answers_by_one_owner foreign key (id_owner)
      references Owner (id_owner);

alter table Answer add constraint FK_many_answers_to_a_question foreign key (id_question)
      references Question (id_question);

alter table Answer add constraint FK_many_answers_with_one_answer_type foreign key (id_answer_type)
      references Answer_type (id_answer_type);

alter table Contact add constraint FK_many_contacts_to_an_owner foreign key (id_owner)
      references Owner (id_owner);

alter table Contact add constraint FK_many_contacts_to_contact_type foreign key (id_contact_type)
      references Contact_type (id_contact_type);

alter table Family add constraint FK_many_families_an_a_premise foreign key (id_premise)
      references Premise (id_premise);

alter table Family add constraint FK_many_families_to_a_property_type foreign key (id_property_type)
      references Property_type (id_property_type);

alter table Meeting add constraint FK_many_meetins_in_a_building foreign key (id_building)
      references Building (id_building);

alter table Owner add constraint FK_many_owners_in_owner_type foreign key (id_owner_type)
      references Owner_type (id_owner_type);

alter table Premise add constraint FK_many_premises_in_a_building foreign key (id_building)
      references Building (id_building);

alter table Property_rights add constraint FK_many_property_rights_to_a_family foreign key (id_family)
      references Family (id_family);

alter table Property_rights add constraint FK_many_property_rights_to_a_premise foreign key (id_premise)
      references Premise (id_premise);

alter table Property_rights add constraint FK_many_property_rights_to_a_property_type foreign key (id_property_type)
      references Property_type (id_property_type);

alter table Property_rights add constraint FK_many_property_rights_to_owner foreign key (id_owner)
      references Owner (id_owner);

alter table Question add constraint FK_many_questions_on_a_meeting foreign key (id_meeting)
      references Meeting (id_meeting);

alter table User add constraint FK_user_to_owner foreign key (id_owner)
      references Owner (id_owner);

alter table User add constraint FK_user_to_premise foreign key (id_premise)
      references Premise (id_premise);

