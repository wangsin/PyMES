create table Customer
(
    id      int      not null,
    name    char(64) not null,
    tel     char(32) not null,
    company char(64) not null,
    constraint Customer_id_uindex
        unique (id),
    constraint Customer_tel_uindex
        unique (tel)
);

alter table Customer
    add primary key (id);

create table Material
(
    id   int      not null,
    name char(32) not null,
    rest int      not null,
    constraint Material_id_uindex
        unique (id),
    constraint Material_name_uindex
        unique (name)
);

alter table Material
    add primary key (id);

create table `Order`
(
    order_id         int                  not null,
    start_date       date                 not null,
    end_date         date                 null,
    custom_id        int                  null,
    is_available     tinyint(1) default 0 not null,
    is_finished      tinyint(1) default 0 not null,
    is_urgent        tinyint(1) default 0 not null,
    need_material    int        default 0 not null,
    need_stock       int        default 6 not null,
    need_material_id int                  null,
    constraint Order_order_id_uindex
        unique (order_id),
    constraint Order_Customer_id_fk
        foreign key (custom_id) references Customer (id)
            on update cascade on delete cascade,
    constraint Order_Material_id_fk
        foreign key (need_material_id) references Material (id)
            on update cascade on delete cascade
);

alter table `Order`
    add primary key (order_id);

create table Job
(
    id              int  not null,
    order_id        int  null,
    input_path      text not null,
    best_time       int  not null,
    best_aps        text not null,
    best_solution   text not null,
    result_img_path text not null,
    constraint Job_id_uindex
        unique (id),
    constraint Job_Order_order_id_fk
        foreign key (order_id) references `Order` (order_id)
            on update cascade on delete cascade
);

alter table Job
    add primary key (id);

create table Stock
(
    room_id    int not null,
    rest_num   int not null,
    full_num   int not null,
    last_order int null,
    constraint Stock_room_id_uindex
        unique (room_id),
    constraint Stock_Order_order_id_fk
        foreign key (last_order) references `Order` (order_id)
            on update cascade on delete cascade
);

alter table Stock
    add primary key (room_id);

create table User
(
    name             char(64)             not null,
    id               int                  not null,
    password         char(128)            not null,
    email            char(64)             not null,
    simulate_num     int                  null,
    last_login       datetime             null,
    confirmed        tinyint(1) default 0 not null,
    is_administrator tinyint(1) default 0 not null,
    constraint User_Email_uindex
        unique (email),
    constraint User_Id_uindex
        unique (id),
    constraint User_Name_uindex
        unique (name)
);

alter table User
    add primary key (id);


