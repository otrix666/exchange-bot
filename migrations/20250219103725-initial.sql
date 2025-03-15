-- +migrate Up
create table users
(
    id         bigint primary key,
    username   varchar(32),
    full_name  varchar(64),
    is_banned  bool,
    created_at timestamp

);

create table cards
(
    id         uuid primary key,
    number     varchar(16),
    user_id    bigint,
    is_deleted bool

);

create table cheques
(
    id  serial primary key,
    url varchar(512)
);

create type exchange_status as enum ('created', 'paid', 'canceled', 'completed');

create table sell_exchange_orders
(
    id                 uuid primary key,
    crypto_amount      decimal,
    fiat_amount        decimal,
    ticker             varchar(8),
    status             exchange_status,
    created_at         timestamp,
    completed_at       timestamp,
    note               varchar(512),
    user_requisites    varchar(128),
    service_requisites varchar(128),
    user_id            bigint,
    cheque_id          integer,
    constraint fk_user_id foreign key (user_id) references users (id),
    constraint fk_cheque_id foreign key (cheque_id) references cheques (id)


);

create table buy_exchange_orders
(
    id              uuid primary key,
    crypto_amount   decimal,
    fiat_amount     decimal,
    ticker          varchar(8),
    status          exchange_status,
    created_at      timestamp,
    completed_at    timestamp,
    note            varchar(512),
    user_requisites varchar(128),
    card_id         uuid,
    user_id         bigint,
    cheque_id       integer,
    constraint fk_card_id foreign key (card_id) references cards (id),
    constraint fk_user_id foreign key (user_id) references users (id),
    constraint fk_cheque_id foreign key (cheque_id) references cheques (id)
);

create table contacts
(
    id    serial primary key,
    title varchar(64),
    url   varchar(256)
);

create table wallets
(
    id              serial primary key,
    private_key_hex varchar(512),
    is_deleted      bool
);





-- +migrate Down
