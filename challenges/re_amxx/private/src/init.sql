
CREATE TABLE `hex_data` (
  `name` varchar(64) NOT NULL,
  `func_base` int NOT NULL,
  `data` text NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `hex_data` VALUES ('stage1',2440,'2e00000089000000890000002c0000007cffffff590000000e0000007cffffff7700000084000000890000002c000000fcffffff2700000020000000850000007cffffff290000000c000000270000000c0000007b000000080000002c000000100000001100000078ffffff8900000027000000000000002700000000000000330000001c0a0000890000006e00000074ffffff0300000074ffffff040000001400000040000000c40a0000890000000300000074ffffff04000000100000001b0000002400000009000000240000000d0000007cffffff240000000300000070ffffff6e00000070ffffff79000000200000002b0000001b000000090000002b000000530000002b00000017000000890000000300000078ffffff0400000070ffffff4a000000210000001100000070ffffff33000000100a00002c0000000800000089000000270000000000000033000000fc0a0000890000000300000074ffffff57000000020000001100000074ffffff0300000074ffffff57000000010000002200000003000000140000003e0000003c0c0000890000000300000074ffffff04000000100000001b0000002400000009000000240000000300000010000000240000000300000074ffffff57000000010000002b0000001b000000090000002b000000530000002b00000017000000890000000300000010000000240000000300000074ffffff57000000010000002b0000001b0000002400000009000000240000000300000074ffffff04000000100000001b000000090000002b000000530000002b00000017000000890000000300000074ffffff04000000100000001b0000002400000009000000240000000300000010000000240000000300000074ffffff57000000010000002b0000001b000000090000002b000000530000002b0000001700000033000000e00a00002c000000040000008900000003000000140000002c0000008800000030000000'),('stage2',4016,'2e0000008900000089000000270000000000000089000000270000000000000033000000e40f0000890000006e000000f8ffffff03000000f8ffffff040000001000000040000000ac1000008900000085000000fcffffff2d000000000400002500000003000000f8ffffff040000000c0000001b0000002400000027000000c403000027000000080000007b000000000000002c0000000c0000002a00000024000000280000002c040000270000000c0000007b000000070000002c000000100000002d00000000fcffff8900000003000000f8ffffff040000000c0000001b0000002200000003000000fcffffff1700000033000000d80f00002c000000040000008900000003000000100000002c0000000400000030000000'),('stage3',4696,'2e00000089000000890000002c000000fcffffff27000000d803000027000000040000007b000000090000002c0000000800000011000000fcffffff89000000270000000000000033000000b4120000890000006e000000f8ffffff03000000f8ffffff0400000010000000400000007c1300008900000003000000fcffffff2400000003000000f8ffffff040000000c0000001b0000000900000058000000adde00002b0000004e00000011000000fcffffff8900000003000000fcffffff570000000100000011000000fcffffff890000000b0000000010000004000000fcffffff4a0000002100000011000000fcffffff8900000003000000f8ffffff040000000c0000001b0000002200000003000000fcffffff1700000033000000a81200002c000000040000008900000003000000100000002c0000000400000030000000');

-- CREATE USER 'jctf'@'%' IDENTIFIED BY 'jctf1234';
-- GRANT SELECT ON hex_data TO 'jctf'@'%';
-- FLUSH PRIVILEGES;
