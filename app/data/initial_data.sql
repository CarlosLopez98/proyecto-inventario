/* USUARIOS */
INSERT INTO usuarios VALUES(null, 'Carlos', 'Lopez', 'carlos@mail.com', 'pbkdf2:sha256:150000$eOGMHTUt$17064874d66c02a25c36491680cc5f58c9cc5695f24caf4ed8b731dd67366ed7', 'admin', '2020-07-31 19:01:58.428697');
INSERT INTO usuarios VALUES(null, 'Brayan', 'Lopez', 'brayan@mail.com', 'pbkdf2:sha256:150000$uEhRjPNn$a5500c924b4beb10199372811e7afc68817cc8a93d4d2050f055f97f82b717fd', 'admin', '2020-07-31 19:11:53.736178');
INSERT INTO usuarios VALUES(null, 'Oscar', 'Carrillo', 'oscar@mail.com', 'pbkdf2:sha256:150000$fwLd0kjX$f7d37c6141b25c7e51954c3cb54489b5ab27607856f5e4ac3a4971c231350019', 'admin', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Pepe', 'Perez', 'pepe@mail.com', 'pbkdf2:sha256:150000$urr77P9f$6fa234dd90a2b3e4a9bd519895203c3f737a453e2e8e5b940a0ae868094c8df6', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Antonio', 'Garcia', 'antonio@mail.com', 'pbkdf2:sha256:150000$QKnq0oyA$426a441ee7c0cb5b0b33893f06e37a68d02a9f79de2d6dcb189bfa4bb90005b3', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Maria', 'Martinez', 'maria@mail.com', 'pbkdf2:sha256:150000$RVJK9LyG$e290bd16ab1cc68637e374a0fcb085c9353790335b96ccf6038ea130f793cddd', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Isabel', 'Sanchez', 'isabel@mail.com', 'pbkdf2:sha256:150000$u9xyMdrZ$46a281edb7761a9c6b01a14eeff54e18dae60818db4ee9eebf78053f907e4de3', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Juan', 'Gonzalez', 'juan@mail.com', 'pbkdf2:sha256:150000$rzsCzt3A$0e782563d7deeb100d5eb8938c5ec81b7f01812a7a849bcbd5083430c71cf60c', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Laura', 'Jimenez', 'laura@mail.com', 'pbkdf2:sha256:150000$LWkXKwB2$9f57e131f6da8ff55cab85186f1079f1bdc94cd902609a34fc311b755ce028b2', 'user', '2020-08-04 19:32:13.024842');
INSERT INTO usuarios VALUES(null, 'Camila', 'Navarro', 'camilla@mail.com', 'pbkdf2:sha256:150000$df1Yk09Z$baf1ee619ed0356232082b381c2fbded3fde096c0df403840b08df09b086ad38', 'user', '2020-08-04 19:32:13.024842');

/* CATEGORIAS */
INSERT INTO categorias VALUES(null, 'Estufas');
INSERT INTO categorias VALUES(null, 'Hornos');
INSERT INTO categorias VALUES(null, 'Lavadoras');
INSERT INTO categorias VALUES(null, 'Refigeración');
INSERT INTO categorias VALUES(null, 'Televisores');
INSERT INTO categorias VALUES(null, 'Video');
INSERT INTO categorias VALUES(null, 'Audio');
INSERT INTO categorias VALUES(null, 'Celulares');
INSERT INTO categorias VALUES(null, 'VideoJuegos');
INSERT INTO categorias VALUES(null, 'Computadores');

/* ESTADOS */
INSERT INTO estados VALUES(null, 'Activo');
INSERT INTO estados VALUES(null, 'Inactivo');

/* PROVEEDORES */
INSERT INTO proveedores VALUES(null, 'LG Electronics', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Samsung', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Whirlpool', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Electrolux', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Mabe', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Airlux', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Haceb', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'Abba', 'Carrera 00 #000 - 00', '0 000 000', 'activo');
INSERT INTO proveedores VALUES(null, 'ASUS', 'Carrera 00 #000 - 00', '0 000 000', 'activo');

/* PRDUCTOS */
INSERT INTO productos VALUES(null, 'Nevera 331 Lts Brutos', 'Nevera de color gris con capacidad de 331 litros brutos.', 1600000, 0, 1, '2020-07-31 19:01:58.428697', 4, 1, 2);
INSERT INTO productos VALUES(null, 'Nevera 374 L', 'Nevera de color gris con capacidad de 374 litros.', 2000000, 0, 1, '2020-07-31 19:01:58.428697', 4, 1, 1);
INSERT INTO productos VALUES(null, 'Nevera 230 L', 'Nevera de color gris con capacidad de 230 litros.', 1000000, 0, 1, '2020-07-31 19:01:58.428697', 4, 1, 7);
INSERT INTO productos VALUES(null, 'Lavadora 18kg', 'Lavadora de color gris oscuro con carga superior de 18 kg.', 1300000, 0, 1, '2020-07-31 19:01:58.428697', 3, 1, 3);
INSERT INTO productos VALUES(null, 'Lavadora 19kg', 'Lavadora de color negro con carga superior de 19 kg.', 1700000, 0, 1, '2020-07-31 19:01:58.428697', 3, 1, 2);
INSERT INTO productos VALUES(null, 'Lavadora 18kg', 'Lavadora de color negro con carga superior de 18 kg.', 1300000, 0, 1, '2020-07-31 19:01:58.428697', 3, 1, 7);
INSERT INTO productos VALUES(null, 'Estufa de piso 4 puestos', 'Estufa de piso 4 puestos a gas natural color negro', 350000, 0, 1, '2020-07-31 19:01:58.428697', 1, 1, 8);
INSERT INTO productos VALUES(null, 'Estufa cubierta 60cms 4 puestos', 'Estufa para cubierta de 60cms con 4 puestos a gas natural', 250000, 0, 1, '2020-07-31 19:01:58.428697', 1, 1, 7);
INSERT INTO productos VALUES(null, 'Televisor 43"', 'Televisor LED de 43 pulagadas', 1200000, 0, 1, '2020-07-31 19:01:58.428697', 5, 1, 2);
INSERT INTO productos VALUES(null, 'Televisor 55"', 'Televisor LED de 55 pulagadas', 1800000, 0, 1, '2020-07-31 19:01:58.428697', 5, 1, 1);
INSERT INTO productos VALUES(null, 'ASUS ExpertBook B9', 'Portatil i7 10th, 16gb de ram y 1tb de disco duro', 2200000, 0, 1, '2020-07-31 19:01:58.428697', 10, 1, 9);

/* TIPOS MOVIMIENTO */
INSERT INTO tipos VALUES(null, 'Entrada');
INSERT INTO tipos VALUES(null, 'Salida');

/* MOVIMIENTOS */