-- Flight Products
INSERT INTO prods_flights(
	id,pid,
	airport_depart,airport_arrive,
	airline,flight_code,
	depart_date,depart_time,
	arrive_date,arrive_time,
	ticket_id
)VALUES(
	4,44,
	"AKL","BNE",
	"NZ","NZ478",
	"15/08/2019",1130,
	"15/08/2019",1700,2
);

INSERT INTO prods_flights(
	id,pid,
	airport_depart,airport_arrive,
	airline,flight_code,
	depart_date,depart_time,
	arrive_date,arrive_time,
	ticket_id
)VALUES(
	5,45,
	"BNE","AKL",
	"QF","QF742",
	"15/08/2019",1730,
	"15/08/2019",2300,2
);

INSERT INTO prods_flights(
	id,pid,
	airport_depart,airport_arrive,
	airline,flight_code,
	depart_date,depart_time,
	arrive_date,arrive_time,
	ticket_id
)VALUES(
	6,46,
	"MEL","HBA",
	"QF","QF278",
	"17/08/2019",0900,
	"17/08/2019",1130,2
);

INSERT INTO prods_flights(
	id,pid,
	airport_depart,airport_arrive,
	airline,flight_code,
	depart_date,depart_time,
	arrive_date,arrive_time,
	ticket_id
)VALUES(
	7,47,
	"MEL","SYD",
	"QF","QF285",
	"19/08/2019",1300,
	"19/08/2019",1600,3
);

INSERT INTO prods_flights(
	id,pid,
	airport_depart,airport_arrive,
	airline,flight_code,
	depart_date,depart_time,
	arrive_date,arrive_time,
	ticket_id
)VALUES(
	8,48,
	"SYD","NRT",
	"JL","JL824",
	"20/08/2019",1930,
	"21/08/2019",1045,2
);

-- All Products Products

INSERT INTO products(
	pid,name
)VALUES(
	44,"AKL to BNE by NZ (NZ478) - 15/08/2019:1130 / 15/08/2019:1700"
);

INSERT INTO products(
	pid,name
)VALUES(
	45,"BNE to AKL by QF (QF742) - 15/08/2019:1730 / 15/08/2019:2300"
);

INSERT INTO products(
	pid,name
)VALUES(
	46,"MEL to HBA by QF (QF278) - 17/08/2019:0900 / 17/08/2019:1130"
);

INSERT INTO products(
	pid,name
)VALUES(
	47,"MEL to SYD by QF (QF285) - 19/08/2019:1300 / 19/08/2019:1600"
);

INSERT INTO products(
	pid,name
)VALUES(
	48,"SYD to NRT by JL (JL824) - 20/08/2019:1930 / 20/08/2019:1045"
);

-- Slight typo up there...

UPDATE products SET name = "SYD to NRT by JL (JL824) - 20/08/2019:1930 / 21/08/2019:1045" WHERE pid = 48
