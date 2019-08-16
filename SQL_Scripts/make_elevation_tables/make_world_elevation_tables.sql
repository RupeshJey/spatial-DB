-- Rupesh Jeyaram 
-- Created August 5th, 2019

-- DROP TABLE statements

DROP TABLE IF EXISTS elevation_rasters;
DROP TABLE IF EXISTS elevation_points;

-- CREATE TABLE statements

-- elevation_rasters holds all elevation data in raster format

CREATE TABLE elevation_rasters (

    -- Unique raster id
    rid       SERIAL    NOT NULL,

    -- Raster itself
    rast      RASTER    NOT NULL, 

    -- File that the raster belongs to
    filename  TEXT      NOT NULL,
    
    PRIMARY KEY (rid)
);

-- elevation_points holds all elevation data in point-wise format

CREATE TABLE elevation_points (

    -- Unique point ID
    point_id    SERIAL      NOT NULL,

    -- Raster from which point came from
    rid         INTEGER     NOT NULL,

    -- The point 
    center_pt   GEOMETRY    NOT NULL,

    -- Elevation at that point
    elevation   INTEGER,

    -- Slope (rate of steepest descent) at that point (in degrees)
    slope       NUMERIC(5,2),

    -- Aspect (direction of steepest descent) at that point (in degrees)
    aspect      NUMERIC(5,2),
    
    PRIMARY KEY (point_id, rid)

) PARTITION BY LIST(rid); -- Split this table into partitions by raster

-- Create all partitions

CREATE TABLE elevation_points_1 PARTITION OF elevation_points 
    FOR VALUES IN (1);
CREATE TABLE elevation_points_2 PARTITION OF elevation_points 
    FOR VALUES IN (2);
CREATE TABLE elevation_points_3 PARTITION OF elevation_points 
    FOR VALUES IN (3);
CREATE TABLE elevation_points_4 PARTITION OF elevation_points 
    FOR VALUES IN (4);
CREATE TABLE elevation_points_5 PARTITION OF elevation_points 
    FOR VALUES IN (5);
CREATE TABLE elevation_points_6 PARTITION OF elevation_points 
    FOR VALUES IN (6);
CREATE TABLE elevation_points_7 PARTITION OF elevation_points 
    FOR VALUES IN (7);
CREATE TABLE elevation_points_8 PARTITION OF elevation_points 
    FOR VALUES IN (8);
CREATE TABLE elevation_points_9 PARTITION OF elevation_points 
    FOR VALUES IN (9);
CREATE TABLE elevation_points_10 PARTITION OF elevation_points 
    FOR VALUES IN (10);
CREATE TABLE elevation_points_11 PARTITION OF elevation_points 
    FOR VALUES IN (11);
CREATE TABLE elevation_points_12 PARTITION OF elevation_points 
    FOR VALUES IN (12);
CREATE TABLE elevation_points_13 PARTITION OF elevation_points 
    FOR VALUES IN (13);
CREATE TABLE elevation_points_14 PARTITION OF elevation_points 
    FOR VALUES IN (14);
CREATE TABLE elevation_points_15 PARTITION OF elevation_points 
    FOR VALUES IN (15);
CREATE TABLE elevation_points_16 PARTITION OF elevation_points 
    FOR VALUES IN (16);
CREATE TABLE elevation_points_17 PARTITION OF elevation_points 
    FOR VALUES IN (17);
CREATE TABLE elevation_points_18 PARTITION OF elevation_points 
    FOR VALUES IN (18);
CREATE TABLE elevation_points_19 PARTITION OF elevation_points 
    FOR VALUES IN (19);
CREATE TABLE elevation_points_20 PARTITION OF elevation_points 
    FOR VALUES IN (20);
CREATE TABLE elevation_points_21 PARTITION OF elevation_points 
    FOR VALUES IN (21);
CREATE TABLE elevation_points_22 PARTITION OF elevation_points 
    FOR VALUES IN (22);
CREATE TABLE elevation_points_23 PARTITION OF elevation_points 
    FOR VALUES IN (23);
CREATE TABLE elevation_points_24 PARTITION OF elevation_points 
    FOR VALUES IN (24);
CREATE TABLE elevation_points_25 PARTITION OF elevation_points 
    FOR VALUES IN (25);
CREATE TABLE elevation_points_26 PARTITION OF elevation_points 
    FOR VALUES IN (26);
CREATE TABLE elevation_points_27 PARTITION OF elevation_points 
    FOR VALUES IN (27);
CREATE TABLE elevation_points_28 PARTITION OF elevation_points 
    FOR VALUES IN (28);
CREATE TABLE elevation_points_29 PARTITION OF elevation_points 
    FOR VALUES IN (29);
CREATE TABLE elevation_points_30 PARTITION OF elevation_points 
    FOR VALUES IN (30);
CREATE TABLE elevation_points_31 PARTITION OF elevation_points 
    FOR VALUES IN (31);
CREATE TABLE elevation_points_32 PARTITION OF elevation_points 
    FOR VALUES IN (32);
CREATE TABLE elevation_points_33 PARTITION OF elevation_points 
    FOR VALUES IN (33);
CREATE TABLE elevation_points_34 PARTITION OF elevation_points 
    FOR VALUES IN (34);
CREATE TABLE elevation_points_35 PARTITION OF elevation_points 
    FOR VALUES IN (35);
CREATE TABLE elevation_points_36 PARTITION OF elevation_points 
    FOR VALUES IN (36);
CREATE TABLE elevation_points_37 PARTITION OF elevation_points 
    FOR VALUES IN (37);
CREATE TABLE elevation_points_38 PARTITION OF elevation_points 
    FOR VALUES IN (38);
CREATE TABLE elevation_points_39 PARTITION OF elevation_points 
    FOR VALUES IN (39);
CREATE TABLE elevation_points_40 PARTITION OF elevation_points 
    FOR VALUES IN (40);
CREATE TABLE elevation_points_41 PARTITION OF elevation_points 
    FOR VALUES IN (41);
CREATE TABLE elevation_points_42 PARTITION OF elevation_points 
    FOR VALUES IN (42);
CREATE TABLE elevation_points_43 PARTITION OF elevation_points 
    FOR VALUES IN (43);
CREATE TABLE elevation_points_44 PARTITION OF elevation_points 
    FOR VALUES IN (44);
CREATE TABLE elevation_points_45 PARTITION OF elevation_points 
    FOR VALUES IN (45);
CREATE TABLE elevation_points_46 PARTITION OF elevation_points 
    FOR VALUES IN (46);
CREATE TABLE elevation_points_47 PARTITION OF elevation_points 
    FOR VALUES IN (47);
CREATE TABLE elevation_points_48 PARTITION OF elevation_points 
    FOR VALUES IN (48);
CREATE TABLE elevation_points_49 PARTITION OF elevation_points 
    FOR VALUES IN (49);
CREATE TABLE elevation_points_50 PARTITION OF elevation_points 
    FOR VALUES IN (50);
CREATE TABLE elevation_points_51 PARTITION OF elevation_points 
    FOR VALUES IN (51);
CREATE TABLE elevation_points_52 PARTITION OF elevation_points 
    FOR VALUES IN (52);
CREATE TABLE elevation_points_53 PARTITION OF elevation_points 
    FOR VALUES IN (53);
CREATE TABLE elevation_points_54 PARTITION OF elevation_points 
    FOR VALUES IN (54);
CREATE TABLE elevation_points_55 PARTITION OF elevation_points 
    FOR VALUES IN (55);
CREATE TABLE elevation_points_56 PARTITION OF elevation_points 
    FOR VALUES IN (56);
CREATE TABLE elevation_points_57 PARTITION OF elevation_points 
    FOR VALUES IN (57);
CREATE TABLE elevation_points_58 PARTITION OF elevation_points 
    FOR VALUES IN (58);
CREATE TABLE elevation_points_59 PARTITION OF elevation_points 
    FOR VALUES IN (59);
CREATE TABLE elevation_points_60 PARTITION OF elevation_points 
    FOR VALUES IN (60);
CREATE TABLE elevation_points_61 PARTITION OF elevation_points 
    FOR VALUES IN (61);
CREATE TABLE elevation_points_62 PARTITION OF elevation_points 
    FOR VALUES IN (62);
CREATE TABLE elevation_points_63 PARTITION OF elevation_points 
    FOR VALUES IN (63);
CREATE TABLE elevation_points_64 PARTITION OF elevation_points 
    FOR VALUES IN (64);
CREATE TABLE elevation_points_65 PARTITION OF elevation_points 
    FOR VALUES IN (65);
CREATE TABLE elevation_points_66 PARTITION OF elevation_points 
    FOR VALUES IN (66);
CREATE TABLE elevation_points_67 PARTITION OF elevation_points 
    FOR VALUES IN (67);
CREATE TABLE elevation_points_68 PARTITION OF elevation_points 
    FOR VALUES IN (68);
CREATE TABLE elevation_points_69 PARTITION OF elevation_points 
    FOR VALUES IN (69);
CREATE TABLE elevation_points_70 PARTITION OF elevation_points 
    FOR VALUES IN (70);
CREATE TABLE elevation_points_71 PARTITION OF elevation_points 
    FOR VALUES IN (71);
CREATE TABLE elevation_points_72 PARTITION OF elevation_points 
    FOR VALUES IN (72);
CREATE TABLE elevation_points_73 PARTITION OF elevation_points 
    FOR VALUES IN (73);
CREATE TABLE elevation_points_74 PARTITION OF elevation_points 
    FOR VALUES IN (74);
CREATE TABLE elevation_points_75 PARTITION OF elevation_points 
    FOR VALUES IN (75);
CREATE TABLE elevation_points_76 PARTITION OF elevation_points 
    FOR VALUES IN (76);
CREATE TABLE elevation_points_77 PARTITION OF elevation_points 
    FOR VALUES IN (77);
CREATE TABLE elevation_points_78 PARTITION OF elevation_points 
    FOR VALUES IN (78);
CREATE TABLE elevation_points_79 PARTITION OF elevation_points 
    FOR VALUES IN (79);
CREATE TABLE elevation_points_80 PARTITION OF elevation_points 
    FOR VALUES IN (80);
CREATE TABLE elevation_points_81 PARTITION OF elevation_points 
    FOR VALUES IN (81);
CREATE TABLE elevation_points_82 PARTITION OF elevation_points 
    FOR VALUES IN (82);
CREATE TABLE elevation_points_83 PARTITION OF elevation_points 
    FOR VALUES IN (83);
CREATE TABLE elevation_points_84 PARTITION OF elevation_points 
    FOR VALUES IN (84);
CREATE TABLE elevation_points_85 PARTITION OF elevation_points 
    FOR VALUES IN (85);
CREATE TABLE elevation_points_86 PARTITION OF elevation_points 
    FOR VALUES IN (86);
CREATE TABLE elevation_points_87 PARTITION OF elevation_points 
    FOR VALUES IN (87);
CREATE TABLE elevation_points_88 PARTITION OF elevation_points 
    FOR VALUES IN (88);
CREATE TABLE elevation_points_89 PARTITION OF elevation_points 
    FOR VALUES IN (89);
CREATE TABLE elevation_points_90 PARTITION OF elevation_points 
    FOR VALUES IN (90);
CREATE TABLE elevation_points_91 PARTITION OF elevation_points 
    FOR VALUES IN (91);
CREATE TABLE elevation_points_92 PARTITION OF elevation_points 
    FOR VALUES IN (92);
CREATE TABLE elevation_points_93 PARTITION OF elevation_points 
    FOR VALUES IN (93);
CREATE TABLE elevation_points_94 PARTITION OF elevation_points 
    FOR VALUES IN (94);
CREATE TABLE elevation_points_95 PARTITION OF elevation_points 
    FOR VALUES IN (95);
CREATE TABLE elevation_points_96 PARTITION OF elevation_points 
    FOR VALUES IN (96);
CREATE TABLE elevation_points_97 PARTITION OF elevation_points 
    FOR VALUES IN (97);
CREATE TABLE elevation_points_98 PARTITION OF elevation_points 
    FOR VALUES IN (98);
CREATE TABLE elevation_points_99 PARTITION OF elevation_points 
    FOR VALUES IN (99);
CREATE TABLE elevation_points_100 PARTITION OF elevation_points 
    FOR VALUES IN (100);
CREATE TABLE elevation_points_101 PARTITION OF elevation_points 
    FOR VALUES IN (101);
CREATE TABLE elevation_points_102 PARTITION OF elevation_points 
    FOR VALUES IN (102);
CREATE TABLE elevation_points_103 PARTITION OF elevation_points 
    FOR VALUES IN (103);
CREATE TABLE elevation_points_104 PARTITION OF elevation_points 
    FOR VALUES IN (104);
CREATE TABLE elevation_points_105 PARTITION OF elevation_points 
    FOR VALUES IN (105);
CREATE TABLE elevation_points_106 PARTITION OF elevation_points 
    FOR VALUES IN (106);
CREATE TABLE elevation_points_107 PARTITION OF elevation_points 
    FOR VALUES IN (107);
CREATE TABLE elevation_points_108 PARTITION OF elevation_points 
    FOR VALUES IN (108);
CREATE TABLE elevation_points_109 PARTITION OF elevation_points 
    FOR VALUES IN (109);
CREATE TABLE elevation_points_110 PARTITION OF elevation_points 
    FOR VALUES IN (110);
CREATE TABLE elevation_points_111 PARTITION OF elevation_points 
    FOR VALUES IN (111);
CREATE TABLE elevation_points_112 PARTITION OF elevation_points 
    FOR VALUES IN (112);
CREATE TABLE elevation_points_113 PARTITION OF elevation_points 
    FOR VALUES IN (113);
CREATE TABLE elevation_points_114 PARTITION OF elevation_points 
    FOR VALUES IN (114);
CREATE TABLE elevation_points_115 PARTITION OF elevation_points 
    FOR VALUES IN (115);
CREATE TABLE elevation_points_116 PARTITION OF elevation_points 
    FOR VALUES IN (116);
CREATE TABLE elevation_points_117 PARTITION OF elevation_points 
    FOR VALUES IN (117);
CREATE TABLE elevation_points_118 PARTITION OF elevation_points 
    FOR VALUES IN (118);
CREATE TABLE elevation_points_119 PARTITION OF elevation_points 
    FOR VALUES IN (119);
CREATE TABLE elevation_points_120 PARTITION OF elevation_points 
    FOR VALUES IN (120);
CREATE TABLE elevation_points_121 PARTITION OF elevation_points 
    FOR VALUES IN (121);
CREATE TABLE elevation_points_122 PARTITION OF elevation_points 
    FOR VALUES IN (122);
CREATE TABLE elevation_points_123 PARTITION OF elevation_points 
    FOR VALUES IN (123);
CREATE TABLE elevation_points_124 PARTITION OF elevation_points 
    FOR VALUES IN (124);
CREATE TABLE elevation_points_125 PARTITION OF elevation_points 
    FOR VALUES IN (125);
CREATE TABLE elevation_points_126 PARTITION OF elevation_points 
    FOR VALUES IN (126);
CREATE TABLE elevation_points_127 PARTITION OF elevation_points 
    FOR VALUES IN (127);
CREATE TABLE elevation_points_128 PARTITION OF elevation_points 
    FOR VALUES IN (128);
CREATE TABLE elevation_points_129 PARTITION OF elevation_points 
    FOR VALUES IN (129);
CREATE TABLE elevation_points_130 PARTITION OF elevation_points 
    FOR VALUES IN (130);
CREATE TABLE elevation_points_131 PARTITION OF elevation_points 
    FOR VALUES IN (131);
CREATE TABLE elevation_points_132 PARTITION OF elevation_points 
    FOR VALUES IN (132);
CREATE TABLE elevation_points_133 PARTITION OF elevation_points 
    FOR VALUES IN (133);
CREATE TABLE elevation_points_134 PARTITION OF elevation_points 
    FOR VALUES IN (134);
CREATE TABLE elevation_points_135 PARTITION OF elevation_points 
    FOR VALUES IN (135);
CREATE TABLE elevation_points_136 PARTITION OF elevation_points 
    FOR VALUES IN (136);
CREATE TABLE elevation_points_137 PARTITION OF elevation_points 
    FOR VALUES IN (137);
CREATE TABLE elevation_points_138 PARTITION OF elevation_points 
    FOR VALUES IN (138);
CREATE TABLE elevation_points_139 PARTITION OF elevation_points 
    FOR VALUES IN (139);
CREATE TABLE elevation_points_140 PARTITION OF elevation_points 
    FOR VALUES IN (140);
CREATE TABLE elevation_points_141 PARTITION OF elevation_points 
    FOR VALUES IN (141);
CREATE TABLE elevation_points_142 PARTITION OF elevation_points 
    FOR VALUES IN (142);
CREATE TABLE elevation_points_143 PARTITION OF elevation_points 
    FOR VALUES IN (143);
CREATE TABLE elevation_points_144 PARTITION OF elevation_points 
    FOR VALUES IN (144);
CREATE TABLE elevation_points_145 PARTITION OF elevation_points 
    FOR VALUES IN (145);
CREATE TABLE elevation_points_146 PARTITION OF elevation_points 
    FOR VALUES IN (146);
CREATE TABLE elevation_points_147 PARTITION OF elevation_points 
    FOR VALUES IN (147);
CREATE TABLE elevation_points_148 PARTITION OF elevation_points 
    FOR VALUES IN (148);
CREATE TABLE elevation_points_149 PARTITION OF elevation_points 
    FOR VALUES IN (149);
CREATE TABLE elevation_points_150 PARTITION OF elevation_points 
    FOR VALUES IN (150);
CREATE TABLE elevation_points_151 PARTITION OF elevation_points 
    FOR VALUES IN (151);
CREATE TABLE elevation_points_152 PARTITION OF elevation_points 
    FOR VALUES IN (152);
CREATE TABLE elevation_points_153 PARTITION OF elevation_points 
    FOR VALUES IN (153);
CREATE TABLE elevation_points_154 PARTITION OF elevation_points 
    FOR VALUES IN (154);
CREATE TABLE elevation_points_155 PARTITION OF elevation_points 
    FOR VALUES IN (155);
CREATE TABLE elevation_points_156 PARTITION OF elevation_points 
    FOR VALUES IN (156);
CREATE TABLE elevation_points_157 PARTITION OF elevation_points 
    FOR VALUES IN (157);
CREATE TABLE elevation_points_158 PARTITION OF elevation_points 
    FOR VALUES IN (158);
CREATE TABLE elevation_points_159 PARTITION OF elevation_points 
    FOR VALUES IN (159);
CREATE TABLE elevation_points_160 PARTITION OF elevation_points 
    FOR VALUES IN (160);
CREATE TABLE elevation_points_161 PARTITION OF elevation_points 
    FOR VALUES IN (161);
CREATE TABLE elevation_points_162 PARTITION OF elevation_points 
    FOR VALUES IN (162);
CREATE TABLE elevation_points_163 PARTITION OF elevation_points 
    FOR VALUES IN (163);
CREATE TABLE elevation_points_164 PARTITION OF elevation_points 
    FOR VALUES IN (164);
CREATE TABLE elevation_points_165 PARTITION OF elevation_points 
    FOR VALUES IN (165);
CREATE TABLE elevation_points_166 PARTITION OF elevation_points 
    FOR VALUES IN (166);
CREATE TABLE elevation_points_167 PARTITION OF elevation_points 
    FOR VALUES IN (167);
CREATE TABLE elevation_points_168 PARTITION OF elevation_points 
    FOR VALUES IN (168);
CREATE TABLE elevation_points_169 PARTITION OF elevation_points 
    FOR VALUES IN (169);
CREATE TABLE elevation_points_170 PARTITION OF elevation_points 
    FOR VALUES IN (170);
CREATE TABLE elevation_points_171 PARTITION OF elevation_points 
    FOR VALUES IN (171);
CREATE TABLE elevation_points_172 PARTITION OF elevation_points 
    FOR VALUES IN (172);
CREATE TABLE elevation_points_173 PARTITION OF elevation_points 
    FOR VALUES IN (173);
CREATE TABLE elevation_points_174 PARTITION OF elevation_points 
    FOR VALUES IN (174);
CREATE TABLE elevation_points_175 PARTITION OF elevation_points 
    FOR VALUES IN (175);
CREATE TABLE elevation_points_176 PARTITION OF elevation_points 
    FOR VALUES IN (176);
CREATE TABLE elevation_points_177 PARTITION OF elevation_points 
    FOR VALUES IN (177);
CREATE TABLE elevation_points_178 PARTITION OF elevation_points 
    FOR VALUES IN (178);
CREATE TABLE elevation_points_179 PARTITION OF elevation_points 
    FOR VALUES IN (179);
CREATE TABLE elevation_points_180 PARTITION OF elevation_points 
    FOR VALUES IN (180);
CREATE TABLE elevation_points_181 PARTITION OF elevation_points 
    FOR VALUES IN (181);
CREATE TABLE elevation_points_182 PARTITION OF elevation_points 
    FOR VALUES IN (182);
CREATE TABLE elevation_points_183 PARTITION OF elevation_points 
    FOR VALUES IN (183);
CREATE TABLE elevation_points_184 PARTITION OF elevation_points 
    FOR VALUES IN (184);
CREATE TABLE elevation_points_185 PARTITION OF elevation_points 
    FOR VALUES IN (185);
CREATE TABLE elevation_points_186 PARTITION OF elevation_points 
    FOR VALUES IN (186);
CREATE TABLE elevation_points_187 PARTITION OF elevation_points 
    FOR VALUES IN (187);
CREATE TABLE elevation_points_188 PARTITION OF elevation_points 
    FOR VALUES IN (188);
CREATE TABLE elevation_points_189 PARTITION OF elevation_points 
    FOR VALUES IN (189);
CREATE TABLE elevation_points_190 PARTITION OF elevation_points 
    FOR VALUES IN (190);
CREATE TABLE elevation_points_191 PARTITION OF elevation_points 
    FOR VALUES IN (191);
CREATE TABLE elevation_points_192 PARTITION OF elevation_points 
    FOR VALUES IN (192);
CREATE TABLE elevation_points_193 PARTITION OF elevation_points 
    FOR VALUES IN (193);
CREATE TABLE elevation_points_194 PARTITION OF elevation_points 
    FOR VALUES IN (194);
CREATE TABLE elevation_points_195 PARTITION OF elevation_points 
    FOR VALUES IN (195);
CREATE TABLE elevation_points_196 PARTITION OF elevation_points 
    FOR VALUES IN (196);
CREATE TABLE elevation_points_197 PARTITION OF elevation_points 
    FOR VALUES IN (197);
CREATE TABLE elevation_points_198 PARTITION OF elevation_points 
    FOR VALUES IN (198);
CREATE TABLE elevation_points_199 PARTITION OF elevation_points 
    FOR VALUES IN (199);
CREATE TABLE elevation_points_200 PARTITION OF elevation_points 
    FOR VALUES IN (200);
CREATE TABLE elevation_points_201 PARTITION OF elevation_points 
    FOR VALUES IN (201);
CREATE TABLE elevation_points_202 PARTITION OF elevation_points 
    FOR VALUES IN (202);
CREATE TABLE elevation_points_203 PARTITION OF elevation_points 
    FOR VALUES IN (203);
CREATE TABLE elevation_points_204 PARTITION OF elevation_points 
    FOR VALUES IN (204);
CREATE TABLE elevation_points_205 PARTITION OF elevation_points 
    FOR VALUES IN (205);
CREATE TABLE elevation_points_206 PARTITION OF elevation_points 
    FOR VALUES IN (206);
CREATE TABLE elevation_points_207 PARTITION OF elevation_points 
    FOR VALUES IN (207);
CREATE TABLE elevation_points_208 PARTITION OF elevation_points 
    FOR VALUES IN (208);
CREATE TABLE elevation_points_209 PARTITION OF elevation_points 
    FOR VALUES IN (209);
CREATE TABLE elevation_points_210 PARTITION OF elevation_points 
    FOR VALUES IN (210);
CREATE TABLE elevation_points_211 PARTITION OF elevation_points 
    FOR VALUES IN (211);
CREATE TABLE elevation_points_212 PARTITION OF elevation_points 
    FOR VALUES IN (212);
CREATE TABLE elevation_points_213 PARTITION OF elevation_points 
    FOR VALUES IN (213);
CREATE TABLE elevation_points_214 PARTITION OF elevation_points 
    FOR VALUES IN (214);
CREATE TABLE elevation_points_215 PARTITION OF elevation_points 
    FOR VALUES IN (215);
CREATE TABLE elevation_points_216 PARTITION OF elevation_points 
    FOR VALUES IN (216);
CREATE TABLE elevation_points_217 PARTITION OF elevation_points 
    FOR VALUES IN (217);
CREATE TABLE elevation_points_218 PARTITION OF elevation_points 
    FOR VALUES IN (218);
CREATE TABLE elevation_points_219 PARTITION OF elevation_points 
    FOR VALUES IN (219);
CREATE TABLE elevation_points_220 PARTITION OF elevation_points 
    FOR VALUES IN (220);
CREATE TABLE elevation_points_221 PARTITION OF elevation_points 
    FOR VALUES IN (221);
CREATE TABLE elevation_points_222 PARTITION OF elevation_points 
    FOR VALUES IN (222);
CREATE TABLE elevation_points_223 PARTITION OF elevation_points 
    FOR VALUES IN (223);
CREATE TABLE elevation_points_224 PARTITION OF elevation_points 
    FOR VALUES IN (224);
CREATE TABLE elevation_points_225 PARTITION OF elevation_points 
    FOR VALUES IN (225);
CREATE TABLE elevation_points_226 PARTITION OF elevation_points 
    FOR VALUES IN (226);
CREATE TABLE elevation_points_227 PARTITION OF elevation_points 
    FOR VALUES IN (227);
CREATE TABLE elevation_points_228 PARTITION OF elevation_points 
    FOR VALUES IN (228);
CREATE TABLE elevation_points_229 PARTITION OF elevation_points 
    FOR VALUES IN (229);
CREATE TABLE elevation_points_230 PARTITION OF elevation_points 
    FOR VALUES IN (230);
CREATE TABLE elevation_points_231 PARTITION OF elevation_points 
    FOR VALUES IN (231);
CREATE TABLE elevation_points_232 PARTITION OF elevation_points 
    FOR VALUES IN (232);
CREATE TABLE elevation_points_233 PARTITION OF elevation_points 
    FOR VALUES IN (233);
CREATE TABLE elevation_points_234 PARTITION OF elevation_points 
    FOR VALUES IN (234);
CREATE TABLE elevation_points_235 PARTITION OF elevation_points 
    FOR VALUES IN (235);
CREATE TABLE elevation_points_236 PARTITION OF elevation_points 
    FOR VALUES IN (236);
CREATE TABLE elevation_points_237 PARTITION OF elevation_points 
    FOR VALUES IN (237);
CREATE TABLE elevation_points_238 PARTITION OF elevation_points 
    FOR VALUES IN (238);
CREATE TABLE elevation_points_239 PARTITION OF elevation_points 
    FOR VALUES IN (239);
CREATE TABLE elevation_points_240 PARTITION OF elevation_points 
    FOR VALUES IN (240);
CREATE TABLE elevation_points_241 PARTITION OF elevation_points 
    FOR VALUES IN (241);
CREATE TABLE elevation_points_242 PARTITION OF elevation_points 
    FOR VALUES IN (242);
CREATE TABLE elevation_points_243 PARTITION OF elevation_points 
    FOR VALUES IN (243);
CREATE TABLE elevation_points_244 PARTITION OF elevation_points 
    FOR VALUES IN (244);
CREATE TABLE elevation_points_245 PARTITION OF elevation_points 
    FOR VALUES IN (245);
CREATE TABLE elevation_points_246 PARTITION OF elevation_points 
    FOR VALUES IN (246);
CREATE TABLE elevation_points_247 PARTITION OF elevation_points 
    FOR VALUES IN (247);
CREATE TABLE elevation_points_248 PARTITION OF elevation_points 
    FOR VALUES IN (248);
CREATE TABLE elevation_points_249 PARTITION OF elevation_points 
    FOR VALUES IN (249);
CREATE TABLE elevation_points_250 PARTITION OF elevation_points 
    FOR VALUES IN (250);
CREATE TABLE elevation_points_251 PARTITION OF elevation_points 
    FOR VALUES IN (251);
CREATE TABLE elevation_points_252 PARTITION OF elevation_points 
    FOR VALUES IN (252);
CREATE TABLE elevation_points_253 PARTITION OF elevation_points 
    FOR VALUES IN (253);
CREATE TABLE elevation_points_254 PARTITION OF elevation_points 
    FOR VALUES IN (254);
CREATE TABLE elevation_points_255 PARTITION OF elevation_points 
    FOR VALUES IN (255);
CREATE TABLE elevation_points_256 PARTITION OF elevation_points 
    FOR VALUES IN (256);
CREATE TABLE elevation_points_257 PARTITION OF elevation_points 
    FOR VALUES IN (257);
CREATE TABLE elevation_points_258 PARTITION OF elevation_points 
    FOR VALUES IN (258);
CREATE TABLE elevation_points_259 PARTITION OF elevation_points 
    FOR VALUES IN (259);
CREATE TABLE elevation_points_260 PARTITION OF elevation_points 
    FOR VALUES IN (260);
CREATE TABLE elevation_points_261 PARTITION OF elevation_points 
    FOR VALUES IN (261);
CREATE TABLE elevation_points_262 PARTITION OF elevation_points 
    FOR VALUES IN (262);
CREATE TABLE elevation_points_263 PARTITION OF elevation_points 
    FOR VALUES IN (263);
CREATE TABLE elevation_points_264 PARTITION OF elevation_points 
    FOR VALUES IN (264);
CREATE TABLE elevation_points_265 PARTITION OF elevation_points 
    FOR VALUES IN (265);
CREATE TABLE elevation_points_266 PARTITION OF elevation_points 
    FOR VALUES IN (266);
CREATE TABLE elevation_points_267 PARTITION OF elevation_points 
    FOR VALUES IN (267);
CREATE TABLE elevation_points_268 PARTITION OF elevation_points 
    FOR VALUES IN (268);
CREATE TABLE elevation_points_269 PARTITION OF elevation_points 
    FOR VALUES IN (269);
CREATE TABLE elevation_points_270 PARTITION OF elevation_points 
    FOR VALUES IN (270);
CREATE TABLE elevation_points_271 PARTITION OF elevation_points 
    FOR VALUES IN (271);
CREATE TABLE elevation_points_272 PARTITION OF elevation_points 
    FOR VALUES IN (272);
CREATE TABLE elevation_points_273 PARTITION OF elevation_points 
    FOR VALUES IN (273);
CREATE TABLE elevation_points_274 PARTITION OF elevation_points 
    FOR VALUES IN (274);
CREATE TABLE elevation_points_275 PARTITION OF elevation_points 
    FOR VALUES IN (275);
CREATE TABLE elevation_points_276 PARTITION OF elevation_points 
    FOR VALUES IN (276);
CREATE TABLE elevation_points_277 PARTITION OF elevation_points 
    FOR VALUES IN (277);
CREATE TABLE elevation_points_278 PARTITION OF elevation_points 
    FOR VALUES IN (278);
CREATE TABLE elevation_points_279 PARTITION OF elevation_points 
    FOR VALUES IN (279);
CREATE TABLE elevation_points_280 PARTITION OF elevation_points 
    FOR VALUES IN (280);
CREATE TABLE elevation_points_281 PARTITION OF elevation_points 
    FOR VALUES IN (281);
CREATE TABLE elevation_points_282 PARTITION OF elevation_points 
    FOR VALUES IN (282);
CREATE TABLE elevation_points_283 PARTITION OF elevation_points 
    FOR VALUES IN (283);
CREATE TABLE elevation_points_284 PARTITION OF elevation_points 
    FOR VALUES IN (284);
CREATE TABLE elevation_points_285 PARTITION OF elevation_points 
    FOR VALUES IN (285);
CREATE TABLE elevation_points_286 PARTITION OF elevation_points 
    FOR VALUES IN (286);
CREATE TABLE elevation_points_287 PARTITION OF elevation_points 
    FOR VALUES IN (287);
CREATE TABLE elevation_points_288 PARTITION OF elevation_points 
    FOR VALUES IN (288);
CREATE TABLE elevation_points_289 PARTITION OF elevation_points 
    FOR VALUES IN (289);
CREATE TABLE elevation_points_290 PARTITION OF elevation_points 
    FOR VALUES IN (290);
CREATE TABLE elevation_points_291 PARTITION OF elevation_points 
    FOR VALUES IN (291);
CREATE TABLE elevation_points_292 PARTITION OF elevation_points 
    FOR VALUES IN (292);
CREATE TABLE elevation_points_293 PARTITION OF elevation_points 
    FOR VALUES IN (293);
CREATE TABLE elevation_points_294 PARTITION OF elevation_points 
    FOR VALUES IN (294);
CREATE TABLE elevation_points_295 PARTITION OF elevation_points 
    FOR VALUES IN (295);
CREATE TABLE elevation_points_296 PARTITION OF elevation_points 
    FOR VALUES IN (296);
CREATE TABLE elevation_points_297 PARTITION OF elevation_points 
    FOR VALUES IN (297);
CREATE TABLE elevation_points_298 PARTITION OF elevation_points 
    FOR VALUES IN (298);
CREATE TABLE elevation_points_299 PARTITION OF elevation_points 
    FOR VALUES IN (299);
CREATE TABLE elevation_points_300 PARTITION OF elevation_points 
    FOR VALUES IN (300);
CREATE TABLE elevation_points_301 PARTITION OF elevation_points 
    FOR VALUES IN (301);
CREATE TABLE elevation_points_302 PARTITION OF elevation_points 
    FOR VALUES IN (302);
CREATE TABLE elevation_points_303 PARTITION OF elevation_points 
    FOR VALUES IN (303);
CREATE TABLE elevation_points_304 PARTITION OF elevation_points 
    FOR VALUES IN (304);
CREATE TABLE elevation_points_305 PARTITION OF elevation_points 
    FOR VALUES IN (305);
CREATE TABLE elevation_points_306 PARTITION OF elevation_points 
    FOR VALUES IN (306);
CREATE TABLE elevation_points_307 PARTITION OF elevation_points 
    FOR VALUES IN (307);
CREATE TABLE elevation_points_308 PARTITION OF elevation_points 
    FOR VALUES IN (308);
CREATE TABLE elevation_points_309 PARTITION OF elevation_points 
    FOR VALUES IN (309);
CREATE TABLE elevation_points_310 PARTITION OF elevation_points 
    FOR VALUES IN (310);
CREATE TABLE elevation_points_311 PARTITION OF elevation_points 
    FOR VALUES IN (311);
CREATE TABLE elevation_points_312 PARTITION OF elevation_points 
    FOR VALUES IN (312);
CREATE TABLE elevation_points_313 PARTITION OF elevation_points 
    FOR VALUES IN (313);
CREATE TABLE elevation_points_314 PARTITION OF elevation_points 
    FOR VALUES IN (314);
CREATE TABLE elevation_points_315 PARTITION OF elevation_points 
    FOR VALUES IN (315);
CREATE TABLE elevation_points_316 PARTITION OF elevation_points 
    FOR VALUES IN (316);
CREATE TABLE elevation_points_317 PARTITION OF elevation_points 
    FOR VALUES IN (317);
CREATE TABLE elevation_points_318 PARTITION OF elevation_points 
    FOR VALUES IN (318);
CREATE TABLE elevation_points_319 PARTITION OF elevation_points 
    FOR VALUES IN (319);
CREATE TABLE elevation_points_320 PARTITION OF elevation_points 
    FOR VALUES IN (320);
CREATE TABLE elevation_points_321 PARTITION OF elevation_points 
    FOR VALUES IN (321);
CREATE TABLE elevation_points_322 PARTITION OF elevation_points 
    FOR VALUES IN (322);
CREATE TABLE elevation_points_323 PARTITION OF elevation_points 
    FOR VALUES IN (323);
CREATE TABLE elevation_points_324 PARTITION OF elevation_points 
    FOR VALUES IN (324);
CREATE TABLE elevation_points_325 PARTITION OF elevation_points 
    FOR VALUES IN (325);
CREATE TABLE elevation_points_326 PARTITION OF elevation_points 
    FOR VALUES IN (326);
CREATE TABLE elevation_points_327 PARTITION OF elevation_points 
    FOR VALUES IN (327);
CREATE TABLE elevation_points_328 PARTITION OF elevation_points 
    FOR VALUES IN (328);
CREATE TABLE elevation_points_329 PARTITION OF elevation_points 
    FOR VALUES IN (329);
CREATE TABLE elevation_points_330 PARTITION OF elevation_points 
    FOR VALUES IN (330);
CREATE TABLE elevation_points_331 PARTITION OF elevation_points 
    FOR VALUES IN (331);
CREATE TABLE elevation_points_332 PARTITION OF elevation_points 
    FOR VALUES IN (332);
CREATE TABLE elevation_points_333 PARTITION OF elevation_points 
    FOR VALUES IN (333);
CREATE TABLE elevation_points_334 PARTITION OF elevation_points 
    FOR VALUES IN (334);
CREATE TABLE elevation_points_335 PARTITION OF elevation_points 
    FOR VALUES IN (335);
CREATE TABLE elevation_points_336 PARTITION OF elevation_points 
    FOR VALUES IN (336);
CREATE TABLE elevation_points_337 PARTITION OF elevation_points 
    FOR VALUES IN (337);
CREATE TABLE elevation_points_338 PARTITION OF elevation_points 
    FOR VALUES IN (338);
CREATE TABLE elevation_points_339 PARTITION OF elevation_points 
    FOR VALUES IN (339);
CREATE TABLE elevation_points_340 PARTITION OF elevation_points 
    FOR VALUES IN (340);
CREATE TABLE elevation_points_341 PARTITION OF elevation_points 
    FOR VALUES IN (341);
CREATE TABLE elevation_points_342 PARTITION OF elevation_points 
    FOR VALUES IN (342);
CREATE TABLE elevation_points_343 PARTITION OF elevation_points 
    FOR VALUES IN (343);
CREATE TABLE elevation_points_344 PARTITION OF elevation_points 
    FOR VALUES IN (344);
CREATE TABLE elevation_points_345 PARTITION OF elevation_points 
    FOR VALUES IN (345);
CREATE TABLE elevation_points_346 PARTITION OF elevation_points 
    FOR VALUES IN (346);
CREATE TABLE elevation_points_347 PARTITION OF elevation_points 
    FOR VALUES IN (347);
CREATE TABLE elevation_points_348 PARTITION OF elevation_points 
    FOR VALUES IN (348);
CREATE TABLE elevation_points_349 PARTITION OF elevation_points 
    FOR VALUES IN (349);
CREATE TABLE elevation_points_350 PARTITION OF elevation_points 
    FOR VALUES IN (350);
CREATE TABLE elevation_points_351 PARTITION OF elevation_points 
    FOR VALUES IN (351);
CREATE TABLE elevation_points_352 PARTITION OF elevation_points 
    FOR VALUES IN (352);
CREATE TABLE elevation_points_353 PARTITION OF elevation_points 
    FOR VALUES IN (353);
CREATE TABLE elevation_points_354 PARTITION OF elevation_points 
    FOR VALUES IN (354);
CREATE TABLE elevation_points_355 PARTITION OF elevation_points 
    FOR VALUES IN (355);
CREATE TABLE elevation_points_356 PARTITION OF elevation_points 
    FOR VALUES IN (356);
CREATE TABLE elevation_points_357 PARTITION OF elevation_points 
    FOR VALUES IN (357);
CREATE TABLE elevation_points_358 PARTITION OF elevation_points 
    FOR VALUES IN (358);
CREATE TABLE elevation_points_359 PARTITION OF elevation_points 
    FOR VALUES IN (359);
CREATE TABLE elevation_points_360 PARTITION OF elevation_points 
    FOR VALUES IN (360);
CREATE TABLE elevation_points_361 PARTITION OF elevation_points 
    FOR VALUES IN (361);
CREATE TABLE elevation_points_362 PARTITION OF elevation_points 
    FOR VALUES IN (362);
CREATE TABLE elevation_points_363 PARTITION OF elevation_points 
    FOR VALUES IN (363);
CREATE TABLE elevation_points_364 PARTITION OF elevation_points 
    FOR VALUES IN (364);
CREATE TABLE elevation_points_365 PARTITION OF elevation_points 
    FOR VALUES IN (365);
CREATE TABLE elevation_points_366 PARTITION OF elevation_points 
    FOR VALUES IN (366);
CREATE TABLE elevation_points_367 PARTITION OF elevation_points 
    FOR VALUES IN (367);
CREATE TABLE elevation_points_368 PARTITION OF elevation_points 
    FOR VALUES IN (368);
CREATE TABLE elevation_points_369 PARTITION OF elevation_points 
    FOR VALUES IN (369);
CREATE TABLE elevation_points_370 PARTITION OF elevation_points 
    FOR VALUES IN (370);
CREATE TABLE elevation_points_371 PARTITION OF elevation_points 
    FOR VALUES IN (371);
CREATE TABLE elevation_points_372 PARTITION OF elevation_points 
    FOR VALUES IN (372);
CREATE TABLE elevation_points_373 PARTITION OF elevation_points 
    FOR VALUES IN (373);
CREATE TABLE elevation_points_374 PARTITION OF elevation_points 
    FOR VALUES IN (374);
CREATE TABLE elevation_points_375 PARTITION OF elevation_points 
    FOR VALUES IN (375);
CREATE TABLE elevation_points_376 PARTITION OF elevation_points 
    FOR VALUES IN (376);
CREATE TABLE elevation_points_377 PARTITION OF elevation_points 
    FOR VALUES IN (377);
CREATE TABLE elevation_points_378 PARTITION OF elevation_points 
    FOR VALUES IN (378);
CREATE TABLE elevation_points_379 PARTITION OF elevation_points 
    FOR VALUES IN (379);
CREATE TABLE elevation_points_380 PARTITION OF elevation_points 
    FOR VALUES IN (380);
CREATE TABLE elevation_points_381 PARTITION OF elevation_points 
    FOR VALUES IN (381);
CREATE TABLE elevation_points_382 PARTITION OF elevation_points 
    FOR VALUES IN (382);
CREATE TABLE elevation_points_383 PARTITION OF elevation_points 
    FOR VALUES IN (383);
CREATE TABLE elevation_points_384 PARTITION OF elevation_points 
    FOR VALUES IN (384);
CREATE TABLE elevation_points_385 PARTITION OF elevation_points 
    FOR VALUES IN (385);
CREATE TABLE elevation_points_386 PARTITION OF elevation_points 
    FOR VALUES IN (386);
CREATE TABLE elevation_points_387 PARTITION OF elevation_points 
    FOR VALUES IN (387);
CREATE TABLE elevation_points_388 PARTITION OF elevation_points 
    FOR VALUES IN (388);
CREATE TABLE elevation_points_389 PARTITION OF elevation_points 
    FOR VALUES IN (389);
CREATE TABLE elevation_points_390 PARTITION OF elevation_points 
    FOR VALUES IN (390);
CREATE TABLE elevation_points_391 PARTITION OF elevation_points 
    FOR VALUES IN (391);
CREATE TABLE elevation_points_392 PARTITION OF elevation_points 
    FOR VALUES IN (392);
CREATE TABLE elevation_points_393 PARTITION OF elevation_points 
    FOR VALUES IN (393);
CREATE TABLE elevation_points_394 PARTITION OF elevation_points 
    FOR VALUES IN (394);
CREATE TABLE elevation_points_395 PARTITION OF elevation_points 
    FOR VALUES IN (395);
CREATE TABLE elevation_points_396 PARTITION OF elevation_points 
    FOR VALUES IN (396);
CREATE TABLE elevation_points_397 PARTITION OF elevation_points 
    FOR VALUES IN (397);
CREATE TABLE elevation_points_398 PARTITION OF elevation_points 
    FOR VALUES IN (398);
CREATE TABLE elevation_points_399 PARTITION OF elevation_points 
    FOR VALUES IN (399);
CREATE TABLE elevation_points_400 PARTITION OF elevation_points 
    FOR VALUES IN (400);
CREATE TABLE elevation_points_401 PARTITION OF elevation_points 
    FOR VALUES IN (401);
CREATE TABLE elevation_points_402 PARTITION OF elevation_points 
    FOR VALUES IN (402);
CREATE TABLE elevation_points_403 PARTITION OF elevation_points 
    FOR VALUES IN (403);
CREATE TABLE elevation_points_404 PARTITION OF elevation_points 
    FOR VALUES IN (404);
CREATE TABLE elevation_points_405 PARTITION OF elevation_points 
    FOR VALUES IN (405);
CREATE TABLE elevation_points_406 PARTITION OF elevation_points 
    FOR VALUES IN (406);
CREATE TABLE elevation_points_407 PARTITION OF elevation_points 
    FOR VALUES IN (407);
CREATE TABLE elevation_points_408 PARTITION OF elevation_points 
    FOR VALUES IN (408);
CREATE TABLE elevation_points_409 PARTITION OF elevation_points 
    FOR VALUES IN (409);
CREATE TABLE elevation_points_410 PARTITION OF elevation_points 
    FOR VALUES IN (410);
CREATE TABLE elevation_points_411 PARTITION OF elevation_points 
    FOR VALUES IN (411);
CREATE TABLE elevation_points_412 PARTITION OF elevation_points 
    FOR VALUES IN (412);
CREATE TABLE elevation_points_413 PARTITION OF elevation_points 
    FOR VALUES IN (413);
CREATE TABLE elevation_points_414 PARTITION OF elevation_points 
    FOR VALUES IN (414);
CREATE TABLE elevation_points_415 PARTITION OF elevation_points 
    FOR VALUES IN (415);
CREATE TABLE elevation_points_416 PARTITION OF elevation_points 
    FOR VALUES IN (416);
CREATE TABLE elevation_points_417 PARTITION OF elevation_points 
    FOR VALUES IN (417);
CREATE TABLE elevation_points_418 PARTITION OF elevation_points 
    FOR VALUES IN (418);
CREATE TABLE elevation_points_419 PARTITION OF elevation_points 
    FOR VALUES IN (419);
CREATE TABLE elevation_points_420 PARTITION OF elevation_points 
    FOR VALUES IN (420);
CREATE TABLE elevation_points_421 PARTITION OF elevation_points 
    FOR VALUES IN (421);
CREATE TABLE elevation_points_422 PARTITION OF elevation_points 
    FOR VALUES IN (422);
CREATE TABLE elevation_points_423 PARTITION OF elevation_points 
    FOR VALUES IN (423);
CREATE TABLE elevation_points_424 PARTITION OF elevation_points 
    FOR VALUES IN (424);
CREATE TABLE elevation_points_425 PARTITION OF elevation_points 
    FOR VALUES IN (425);
CREATE TABLE elevation_points_426 PARTITION OF elevation_points 
    FOR VALUES IN (426);
CREATE TABLE elevation_points_427 PARTITION OF elevation_points 
    FOR VALUES IN (427);
CREATE TABLE elevation_points_428 PARTITION OF elevation_points 
    FOR VALUES IN (428);
CREATE TABLE elevation_points_429 PARTITION OF elevation_points 
    FOR VALUES IN (429);
CREATE TABLE elevation_points_430 PARTITION OF elevation_points 
    FOR VALUES IN (430);
CREATE TABLE elevation_points_431 PARTITION OF elevation_points 
    FOR VALUES IN (431);
CREATE TABLE elevation_points_432 PARTITION OF elevation_points 
    FOR VALUES IN (432);
CREATE TABLE elevation_points_433 PARTITION OF elevation_points 
    FOR VALUES IN (433);
CREATE TABLE elevation_points_434 PARTITION OF elevation_points 
    FOR VALUES IN (434);
CREATE TABLE elevation_points_435 PARTITION OF elevation_points 
    FOR VALUES IN (435);
CREATE TABLE elevation_points_436 PARTITION OF elevation_points 
    FOR VALUES IN (436);
CREATE TABLE elevation_points_437 PARTITION OF elevation_points 
    FOR VALUES IN (437);
CREATE TABLE elevation_points_438 PARTITION OF elevation_points 
    FOR VALUES IN (438);
CREATE TABLE elevation_points_439 PARTITION OF elevation_points 
    FOR VALUES IN (439);
CREATE TABLE elevation_points_440 PARTITION OF elevation_points 
    FOR VALUES IN (440);
CREATE TABLE elevation_points_441 PARTITION OF elevation_points 
    FOR VALUES IN (441);
CREATE TABLE elevation_points_442 PARTITION OF elevation_points 
    FOR VALUES IN (442);
CREATE TABLE elevation_points_443 PARTITION OF elevation_points 
    FOR VALUES IN (443);
CREATE TABLE elevation_points_444 PARTITION OF elevation_points 
    FOR VALUES IN (444);
CREATE TABLE elevation_points_445 PARTITION OF elevation_points 
    FOR VALUES IN (445);
CREATE TABLE elevation_points_446 PARTITION OF elevation_points 
    FOR VALUES IN (446);
CREATE TABLE elevation_points_447 PARTITION OF elevation_points 
    FOR VALUES IN (447);
CREATE TABLE elevation_points_448 PARTITION OF elevation_points 
    FOR VALUES IN (448);
CREATE TABLE elevation_points_449 PARTITION OF elevation_points 
    FOR VALUES IN (449);
CREATE TABLE elevation_points_450 PARTITION OF elevation_points 
    FOR VALUES IN (450);
CREATE TABLE elevation_points_451 PARTITION OF elevation_points 
    FOR VALUES IN (451);
CREATE TABLE elevation_points_452 PARTITION OF elevation_points 
    FOR VALUES IN (452);
CREATE TABLE elevation_points_453 PARTITION OF elevation_points 
    FOR VALUES IN (453);
CREATE TABLE elevation_points_454 PARTITION OF elevation_points 
    FOR VALUES IN (454);
CREATE TABLE elevation_points_455 PARTITION OF elevation_points 
    FOR VALUES IN (455);
CREATE TABLE elevation_points_456 PARTITION OF elevation_points 
    FOR VALUES IN (456);
CREATE TABLE elevation_points_457 PARTITION OF elevation_points 
    FOR VALUES IN (457);
CREATE TABLE elevation_points_458 PARTITION OF elevation_points 
    FOR VALUES IN (458);
CREATE TABLE elevation_points_459 PARTITION OF elevation_points 
    FOR VALUES IN (459);
CREATE TABLE elevation_points_460 PARTITION OF elevation_points 
    FOR VALUES IN (460);
CREATE TABLE elevation_points_461 PARTITION OF elevation_points 
    FOR VALUES IN (461);
CREATE TABLE elevation_points_462 PARTITION OF elevation_points 
    FOR VALUES IN (462);
CREATE TABLE elevation_points_463 PARTITION OF elevation_points 
    FOR VALUES IN (463);
CREATE TABLE elevation_points_464 PARTITION OF elevation_points 
    FOR VALUES IN (464);
CREATE TABLE elevation_points_465 PARTITION OF elevation_points 
    FOR VALUES IN (465);
CREATE TABLE elevation_points_466 PARTITION OF elevation_points 
    FOR VALUES IN (466);
CREATE TABLE elevation_points_467 PARTITION OF elevation_points 
    FOR VALUES IN (467);
CREATE TABLE elevation_points_468 PARTITION OF elevation_points 
    FOR VALUES IN (468);
CREATE TABLE elevation_points_469 PARTITION OF elevation_points 
    FOR VALUES IN (469);
CREATE TABLE elevation_points_470 PARTITION OF elevation_points 
    FOR VALUES IN (470);
CREATE TABLE elevation_points_471 PARTITION OF elevation_points 
    FOR VALUES IN (471);
CREATE TABLE elevation_points_472 PARTITION OF elevation_points 
    FOR VALUES IN (472);
CREATE TABLE elevation_points_473 PARTITION OF elevation_points 
    FOR VALUES IN (473);
CREATE TABLE elevation_points_474 PARTITION OF elevation_points 
    FOR VALUES IN (474);
CREATE TABLE elevation_points_475 PARTITION OF elevation_points 
    FOR VALUES IN (475);
CREATE TABLE elevation_points_476 PARTITION OF elevation_points 
    FOR VALUES IN (476);
CREATE TABLE elevation_points_477 PARTITION OF elevation_points 
    FOR VALUES IN (477);
CREATE TABLE elevation_points_478 PARTITION OF elevation_points 
    FOR VALUES IN (478);
CREATE TABLE elevation_points_479 PARTITION OF elevation_points 
    FOR VALUES IN (479);
CREATE TABLE elevation_points_480 PARTITION OF elevation_points 
    FOR VALUES IN (480);
CREATE TABLE elevation_points_481 PARTITION OF elevation_points 
    FOR VALUES IN (481);
CREATE TABLE elevation_points_482 PARTITION OF elevation_points 
    FOR VALUES IN (482);
CREATE TABLE elevation_points_483 PARTITION OF elevation_points 
    FOR VALUES IN (483);
CREATE TABLE elevation_points_484 PARTITION OF elevation_points 
    FOR VALUES IN (484);
CREATE TABLE elevation_points_485 PARTITION OF elevation_points 
    FOR VALUES IN (485);
CREATE TABLE elevation_points_486 PARTITION OF elevation_points 
    FOR VALUES IN (486);
CREATE TABLE elevation_points_487 PARTITION OF elevation_points 
    FOR VALUES IN (487);
CREATE TABLE elevation_points_488 PARTITION OF elevation_points 
    FOR VALUES IN (488);
CREATE TABLE elevation_points_489 PARTITION OF elevation_points 
    FOR VALUES IN (489);
CREATE TABLE elevation_points_490 PARTITION OF elevation_points 
    FOR VALUES IN (490);
CREATE TABLE elevation_points_491 PARTITION OF elevation_points 
    FOR VALUES IN (491);
CREATE TABLE elevation_points_492 PARTITION OF elevation_points 
    FOR VALUES IN (492);
CREATE TABLE elevation_points_493 PARTITION OF elevation_points 
    FOR VALUES IN (493);
CREATE TABLE elevation_points_494 PARTITION OF elevation_points 
    FOR VALUES IN (494);
CREATE TABLE elevation_points_495 PARTITION OF elevation_points 
    FOR VALUES IN (495);
CREATE TABLE elevation_points_496 PARTITION OF elevation_points 
    FOR VALUES IN (496);
CREATE TABLE elevation_points_497 PARTITION OF elevation_points 
    FOR VALUES IN (497);
CREATE TABLE elevation_points_498 PARTITION OF elevation_points 
    FOR VALUES IN (498);
CREATE TABLE elevation_points_499 PARTITION OF elevation_points 
    FOR VALUES IN (499);
CREATE TABLE elevation_points_500 PARTITION OF elevation_points 
    FOR VALUES IN (500);
CREATE TABLE elevation_points_501 PARTITION OF elevation_points 
    FOR VALUES IN (501);
CREATE TABLE elevation_points_502 PARTITION OF elevation_points 
    FOR VALUES IN (502);
CREATE TABLE elevation_points_503 PARTITION OF elevation_points 
    FOR VALUES IN (503);
CREATE TABLE elevation_points_504 PARTITION OF elevation_points 
    FOR VALUES IN (504);
CREATE TABLE elevation_points_505 PARTITION OF elevation_points 
    FOR VALUES IN (505);
CREATE TABLE elevation_points_506 PARTITION OF elevation_points 
    FOR VALUES IN (506);
CREATE TABLE elevation_points_507 PARTITION OF elevation_points 
    FOR VALUES IN (507);
CREATE TABLE elevation_points_508 PARTITION OF elevation_points 
    FOR VALUES IN (508);
CREATE TABLE elevation_points_509 PARTITION OF elevation_points 
    FOR VALUES IN (509);
CREATE TABLE elevation_points_510 PARTITION OF elevation_points 
    FOR VALUES IN (510);
CREATE TABLE elevation_points_511 PARTITION OF elevation_points 
    FOR VALUES IN (511);
CREATE TABLE elevation_points_512 PARTITION OF elevation_points 
    FOR VALUES IN (512);
CREATE TABLE elevation_points_513 PARTITION OF elevation_points 
    FOR VALUES IN (513);
CREATE TABLE elevation_points_514 PARTITION OF elevation_points 
    FOR VALUES IN (514);
CREATE TABLE elevation_points_515 PARTITION OF elevation_points 
    FOR VALUES IN (515);
CREATE TABLE elevation_points_516 PARTITION OF elevation_points 
    FOR VALUES IN (516);
CREATE TABLE elevation_points_517 PARTITION OF elevation_points 
    FOR VALUES IN (517);
CREATE TABLE elevation_points_518 PARTITION OF elevation_points 
    FOR VALUES IN (518);
CREATE TABLE elevation_points_519 PARTITION OF elevation_points 
    FOR VALUES IN (519);
CREATE TABLE elevation_points_520 PARTITION OF elevation_points 
    FOR VALUES IN (520);
CREATE TABLE elevation_points_521 PARTITION OF elevation_points 
    FOR VALUES IN (521);
CREATE TABLE elevation_points_522 PARTITION OF elevation_points 
    FOR VALUES IN (522);
CREATE TABLE elevation_points_523 PARTITION OF elevation_points 
    FOR VALUES IN (523);
CREATE TABLE elevation_points_524 PARTITION OF elevation_points 
    FOR VALUES IN (524);
CREATE TABLE elevation_points_525 PARTITION OF elevation_points 
    FOR VALUES IN (525);
CREATE TABLE elevation_points_526 PARTITION OF elevation_points 
    FOR VALUES IN (526);
CREATE TABLE elevation_points_527 PARTITION OF elevation_points 
    FOR VALUES IN (527);
CREATE TABLE elevation_points_528 PARTITION OF elevation_points 
    FOR VALUES IN (528);
CREATE TABLE elevation_points_529 PARTITION OF elevation_points 
    FOR VALUES IN (529);
CREATE TABLE elevation_points_530 PARTITION OF elevation_points 
    FOR VALUES IN (530);
CREATE TABLE elevation_points_531 PARTITION OF elevation_points 
    FOR VALUES IN (531);
CREATE TABLE elevation_points_532 PARTITION OF elevation_points 
    FOR VALUES IN (532);
CREATE TABLE elevation_points_533 PARTITION OF elevation_points 
    FOR VALUES IN (533);
CREATE TABLE elevation_points_534 PARTITION OF elevation_points 
    FOR VALUES IN (534);
CREATE TABLE elevation_points_535 PARTITION OF elevation_points 
    FOR VALUES IN (535);
CREATE TABLE elevation_points_536 PARTITION OF elevation_points 
    FOR VALUES IN (536);
CREATE TABLE elevation_points_537 PARTITION OF elevation_points 
    FOR VALUES IN (537);
CREATE TABLE elevation_points_538 PARTITION OF elevation_points 
    FOR VALUES IN (538);
CREATE TABLE elevation_points_539 PARTITION OF elevation_points 
    FOR VALUES IN (539);
CREATE TABLE elevation_points_540 PARTITION OF elevation_points 
    FOR VALUES IN (540);
CREATE TABLE elevation_points_541 PARTITION OF elevation_points 
    FOR VALUES IN (541);
CREATE TABLE elevation_points_542 PARTITION OF elevation_points 
    FOR VALUES IN (542);
CREATE TABLE elevation_points_543 PARTITION OF elevation_points 
    FOR VALUES IN (543);
CREATE TABLE elevation_points_544 PARTITION OF elevation_points 
    FOR VALUES IN (544);
CREATE TABLE elevation_points_545 PARTITION OF elevation_points 
    FOR VALUES IN (545);
CREATE TABLE elevation_points_546 PARTITION OF elevation_points 
    FOR VALUES IN (546);
CREATE TABLE elevation_points_547 PARTITION OF elevation_points 
    FOR VALUES IN (547);
CREATE TABLE elevation_points_548 PARTITION OF elevation_points 
    FOR VALUES IN (548);
CREATE TABLE elevation_points_549 PARTITION OF elevation_points 
    FOR VALUES IN (549);
CREATE TABLE elevation_points_550 PARTITION OF elevation_points 
    FOR VALUES IN (550);
CREATE TABLE elevation_points_551 PARTITION OF elevation_points 
    FOR VALUES IN (551);
CREATE TABLE elevation_points_552 PARTITION OF elevation_points 
    FOR VALUES IN (552);
CREATE TABLE elevation_points_553 PARTITION OF elevation_points 
    FOR VALUES IN (553);
CREATE TABLE elevation_points_554 PARTITION OF elevation_points 
    FOR VALUES IN (554);
CREATE TABLE elevation_points_555 PARTITION OF elevation_points 
    FOR VALUES IN (555);
CREATE TABLE elevation_points_556 PARTITION OF elevation_points 
    FOR VALUES IN (556);
CREATE TABLE elevation_points_557 PARTITION OF elevation_points 
    FOR VALUES IN (557);
CREATE TABLE elevation_points_558 PARTITION OF elevation_points 
    FOR VALUES IN (558);
CREATE TABLE elevation_points_559 PARTITION OF elevation_points 
    FOR VALUES IN (559);
CREATE TABLE elevation_points_560 PARTITION OF elevation_points 
    FOR VALUES IN (560);
CREATE TABLE elevation_points_561 PARTITION OF elevation_points 
    FOR VALUES IN (561);
CREATE TABLE elevation_points_562 PARTITION OF elevation_points 
    FOR VALUES IN (562);
CREATE TABLE elevation_points_563 PARTITION OF elevation_points 
    FOR VALUES IN (563);
CREATE TABLE elevation_points_564 PARTITION OF elevation_points 
    FOR VALUES IN (564);
CREATE TABLE elevation_points_565 PARTITION OF elevation_points 
    FOR VALUES IN (565);
CREATE TABLE elevation_points_566 PARTITION OF elevation_points 
    FOR VALUES IN (566);
CREATE TABLE elevation_points_567 PARTITION OF elevation_points 
    FOR VALUES IN (567);
CREATE TABLE elevation_points_568 PARTITION OF elevation_points 
    FOR VALUES IN (568);
CREATE TABLE elevation_points_569 PARTITION OF elevation_points 
    FOR VALUES IN (569);
CREATE TABLE elevation_points_570 PARTITION OF elevation_points 
    FOR VALUES IN (570);
CREATE TABLE elevation_points_571 PARTITION OF elevation_points 
    FOR VALUES IN (571);
CREATE TABLE elevation_points_572 PARTITION OF elevation_points 
    FOR VALUES IN (572);
CREATE TABLE elevation_points_573 PARTITION OF elevation_points 
    FOR VALUES IN (573);
CREATE TABLE elevation_points_574 PARTITION OF elevation_points 
    FOR VALUES IN (574);
CREATE TABLE elevation_points_575 PARTITION OF elevation_points 
    FOR VALUES IN (575);
CREATE TABLE elevation_points_576 PARTITION OF elevation_points 
    FOR VALUES IN (576);
CREATE TABLE elevation_points_577 PARTITION OF elevation_points 
    FOR VALUES IN (577);
CREATE TABLE elevation_points_578 PARTITION OF elevation_points 
    FOR VALUES IN (578);
CREATE TABLE elevation_points_579 PARTITION OF elevation_points 
    FOR VALUES IN (579);
CREATE TABLE elevation_points_580 PARTITION OF elevation_points 
    FOR VALUES IN (580);
CREATE TABLE elevation_points_581 PARTITION OF elevation_points 
    FOR VALUES IN (581);
CREATE TABLE elevation_points_582 PARTITION OF elevation_points 
    FOR VALUES IN (582);
CREATE TABLE elevation_points_583 PARTITION OF elevation_points 
    FOR VALUES IN (583);
CREATE TABLE elevation_points_584 PARTITION OF elevation_points 
    FOR VALUES IN (584);
CREATE TABLE elevation_points_585 PARTITION OF elevation_points 
    FOR VALUES IN (585);
CREATE TABLE elevation_points_586 PARTITION OF elevation_points 
    FOR VALUES IN (586);
CREATE TABLE elevation_points_587 PARTITION OF elevation_points 
    FOR VALUES IN (587);
CREATE TABLE elevation_points_588 PARTITION OF elevation_points 
    FOR VALUES IN (588);
CREATE TABLE elevation_points_589 PARTITION OF elevation_points 
    FOR VALUES IN (589);
CREATE TABLE elevation_points_590 PARTITION OF elevation_points 
    FOR VALUES IN (590);
CREATE TABLE elevation_points_591 PARTITION OF elevation_points 
    FOR VALUES IN (591);
CREATE TABLE elevation_points_592 PARTITION OF elevation_points 
    FOR VALUES IN (592);
CREATE TABLE elevation_points_593 PARTITION OF elevation_points 
    FOR VALUES IN (593);
CREATE TABLE elevation_points_594 PARTITION OF elevation_points 
    FOR VALUES IN (594);
CREATE TABLE elevation_points_595 PARTITION OF elevation_points 
    FOR VALUES IN (595);
CREATE TABLE elevation_points_596 PARTITION OF elevation_points 
    FOR VALUES IN (596);
CREATE TABLE elevation_points_597 PARTITION OF elevation_points 
    FOR VALUES IN (597);
CREATE TABLE elevation_points_598 PARTITION OF elevation_points 
    FOR VALUES IN (598);
CREATE TABLE elevation_points_599 PARTITION OF elevation_points 
    FOR VALUES IN (599);
CREATE TABLE elevation_points_600 PARTITION OF elevation_points 
    FOR VALUES IN (600);
CREATE TABLE elevation_points_601 PARTITION OF elevation_points 
    FOR VALUES IN (601);
CREATE TABLE elevation_points_602 PARTITION OF elevation_points 
    FOR VALUES IN (602);
CREATE TABLE elevation_points_603 PARTITION OF elevation_points 
    FOR VALUES IN (603);
CREATE TABLE elevation_points_604 PARTITION OF elevation_points 
    FOR VALUES IN (604);
CREATE TABLE elevation_points_605 PARTITION OF elevation_points 
    FOR VALUES IN (605);
CREATE TABLE elevation_points_606 PARTITION OF elevation_points 
    FOR VALUES IN (606);
CREATE TABLE elevation_points_607 PARTITION OF elevation_points 
    FOR VALUES IN (607);
CREATE TABLE elevation_points_608 PARTITION OF elevation_points 
    FOR VALUES IN (608);
CREATE TABLE elevation_points_609 PARTITION OF elevation_points 
    FOR VALUES IN (609);
CREATE TABLE elevation_points_610 PARTITION OF elevation_points 
    FOR VALUES IN (610);
CREATE TABLE elevation_points_611 PARTITION OF elevation_points 
    FOR VALUES IN (611);
CREATE TABLE elevation_points_612 PARTITION OF elevation_points 
    FOR VALUES IN (612);
CREATE TABLE elevation_points_613 PARTITION OF elevation_points 
    FOR VALUES IN (613);
CREATE TABLE elevation_points_614 PARTITION OF elevation_points 
    FOR VALUES IN (614);
CREATE TABLE elevation_points_615 PARTITION OF elevation_points 
    FOR VALUES IN (615);
CREATE TABLE elevation_points_616 PARTITION OF elevation_points 
    FOR VALUES IN (616);
CREATE TABLE elevation_points_617 PARTITION OF elevation_points 
    FOR VALUES IN (617);
CREATE TABLE elevation_points_618 PARTITION OF elevation_points 
    FOR VALUES IN (618);
CREATE TABLE elevation_points_619 PARTITION OF elevation_points 
    FOR VALUES IN (619);
CREATE TABLE elevation_points_620 PARTITION OF elevation_points 
    FOR VALUES IN (620);
CREATE TABLE elevation_points_621 PARTITION OF elevation_points 
    FOR VALUES IN (621);
CREATE TABLE elevation_points_622 PARTITION OF elevation_points 
    FOR VALUES IN (622);
CREATE TABLE elevation_points_623 PARTITION OF elevation_points 
    FOR VALUES IN (623);
CREATE TABLE elevation_points_624 PARTITION OF elevation_points 
    FOR VALUES IN (624);
CREATE TABLE elevation_points_625 PARTITION OF elevation_points 
    FOR VALUES IN (625);
CREATE TABLE elevation_points_626 PARTITION OF elevation_points 
    FOR VALUES IN (626);
CREATE TABLE elevation_points_627 PARTITION OF elevation_points 
    FOR VALUES IN (627);
CREATE TABLE elevation_points_628 PARTITION OF elevation_points 
    FOR VALUES IN (628);
CREATE TABLE elevation_points_629 PARTITION OF elevation_points 
    FOR VALUES IN (629);
CREATE TABLE elevation_points_630 PARTITION OF elevation_points 
    FOR VALUES IN (630);
CREATE TABLE elevation_points_631 PARTITION OF elevation_points 
    FOR VALUES IN (631);
CREATE TABLE elevation_points_632 PARTITION OF elevation_points 
    FOR VALUES IN (632);
CREATE TABLE elevation_points_633 PARTITION OF elevation_points 
    FOR VALUES IN (633);
CREATE TABLE elevation_points_634 PARTITION OF elevation_points 
    FOR VALUES IN (634);
CREATE TABLE elevation_points_635 PARTITION OF elevation_points 
    FOR VALUES IN (635);
CREATE TABLE elevation_points_636 PARTITION OF elevation_points 
    FOR VALUES IN (636);
CREATE TABLE elevation_points_637 PARTITION OF elevation_points 
    FOR VALUES IN (637);
CREATE TABLE elevation_points_638 PARTITION OF elevation_points 
    FOR VALUES IN (638);
CREATE TABLE elevation_points_639 PARTITION OF elevation_points 
    FOR VALUES IN (639);
CREATE TABLE elevation_points_640 PARTITION OF elevation_points 
    FOR VALUES IN (640);
CREATE TABLE elevation_points_641 PARTITION OF elevation_points 
    FOR VALUES IN (641);
CREATE TABLE elevation_points_642 PARTITION OF elevation_points 
    FOR VALUES IN (642);
CREATE TABLE elevation_points_643 PARTITION OF elevation_points 
    FOR VALUES IN (643);
CREATE TABLE elevation_points_644 PARTITION OF elevation_points 
    FOR VALUES IN (644);
CREATE TABLE elevation_points_645 PARTITION OF elevation_points 
    FOR VALUES IN (645);
CREATE TABLE elevation_points_646 PARTITION OF elevation_points 
    FOR VALUES IN (646);
CREATE TABLE elevation_points_647 PARTITION OF elevation_points 
    FOR VALUES IN (647);
CREATE TABLE elevation_points_648 PARTITION OF elevation_points 
    FOR VALUES IN (648);
CREATE TABLE elevation_points_649 PARTITION OF elevation_points 
    FOR VALUES IN (649);
CREATE TABLE elevation_points_650 PARTITION OF elevation_points 
    FOR VALUES IN (650);
CREATE TABLE elevation_points_651 PARTITION OF elevation_points 
    FOR VALUES IN (651);
CREATE TABLE elevation_points_652 PARTITION OF elevation_points 
    FOR VALUES IN (652);
CREATE TABLE elevation_points_653 PARTITION OF elevation_points 
    FOR VALUES IN (653);
CREATE TABLE elevation_points_654 PARTITION OF elevation_points 
    FOR VALUES IN (654);
CREATE TABLE elevation_points_655 PARTITION OF elevation_points 
    FOR VALUES IN (655);
CREATE TABLE elevation_points_656 PARTITION OF elevation_points 
    FOR VALUES IN (656);
CREATE TABLE elevation_points_657 PARTITION OF elevation_points 
    FOR VALUES IN (657);
CREATE TABLE elevation_points_658 PARTITION OF elevation_points 
    FOR VALUES IN (658);
CREATE TABLE elevation_points_659 PARTITION OF elevation_points 
    FOR VALUES IN (659);
CREATE TABLE elevation_points_660 PARTITION OF elevation_points 
    FOR VALUES IN (660);
CREATE TABLE elevation_points_661 PARTITION OF elevation_points 
    FOR VALUES IN (661);
CREATE TABLE elevation_points_662 PARTITION OF elevation_points 
    FOR VALUES IN (662);
CREATE TABLE elevation_points_663 PARTITION OF elevation_points 
    FOR VALUES IN (663);
CREATE TABLE elevation_points_664 PARTITION OF elevation_points 
    FOR VALUES IN (664);
CREATE TABLE elevation_points_665 PARTITION OF elevation_points 
    FOR VALUES IN (665);
CREATE TABLE elevation_points_666 PARTITION OF elevation_points 
    FOR VALUES IN (666);
CREATE TABLE elevation_points_667 PARTITION OF elevation_points 
    FOR VALUES IN (667);
CREATE TABLE elevation_points_668 PARTITION OF elevation_points 
    FOR VALUES IN (668);
CREATE TABLE elevation_points_669 PARTITION OF elevation_points 
    FOR VALUES IN (669);
CREATE TABLE elevation_points_670 PARTITION OF elevation_points 
    FOR VALUES IN (670);
CREATE TABLE elevation_points_671 PARTITION OF elevation_points 
    FOR VALUES IN (671);
CREATE TABLE elevation_points_672 PARTITION OF elevation_points 
    FOR VALUES IN (672);
CREATE TABLE elevation_points_673 PARTITION OF elevation_points 
    FOR VALUES IN (673);
CREATE TABLE elevation_points_674 PARTITION OF elevation_points 
    FOR VALUES IN (674);
CREATE TABLE elevation_points_675 PARTITION OF elevation_points 
    FOR VALUES IN (675);
CREATE TABLE elevation_points_676 PARTITION OF elevation_points 
    FOR VALUES IN (676);
CREATE TABLE elevation_points_677 PARTITION OF elevation_points 
    FOR VALUES IN (677);
CREATE TABLE elevation_points_678 PARTITION OF elevation_points 
    FOR VALUES IN (678);
CREATE TABLE elevation_points_679 PARTITION OF elevation_points 
    FOR VALUES IN (679);
CREATE TABLE elevation_points_680 PARTITION OF elevation_points 
    FOR VALUES IN (680);
CREATE TABLE elevation_points_681 PARTITION OF elevation_points 
    FOR VALUES IN (681);
CREATE TABLE elevation_points_682 PARTITION OF elevation_points 
    FOR VALUES IN (682);
CREATE TABLE elevation_points_683 PARTITION OF elevation_points 
    FOR VALUES IN (683);
CREATE TABLE elevation_points_684 PARTITION OF elevation_points 
    FOR VALUES IN (684);
CREATE TABLE elevation_points_685 PARTITION OF elevation_points 
    FOR VALUES IN (685);
CREATE TABLE elevation_points_686 PARTITION OF elevation_points 
    FOR VALUES IN (686);
CREATE TABLE elevation_points_687 PARTITION OF elevation_points 
    FOR VALUES IN (687);
CREATE TABLE elevation_points_688 PARTITION OF elevation_points 
    FOR VALUES IN (688);
CREATE TABLE elevation_points_689 PARTITION OF elevation_points 
    FOR VALUES IN (689);
CREATE TABLE elevation_points_690 PARTITION OF elevation_points 
    FOR VALUES IN (690);
CREATE TABLE elevation_points_691 PARTITION OF elevation_points 
    FOR VALUES IN (691);
CREATE TABLE elevation_points_692 PARTITION OF elevation_points 
    FOR VALUES IN (692);
CREATE TABLE elevation_points_693 PARTITION OF elevation_points 
    FOR VALUES IN (693);
CREATE TABLE elevation_points_694 PARTITION OF elevation_points 
    FOR VALUES IN (694);
CREATE TABLE elevation_points_695 PARTITION OF elevation_points 
    FOR VALUES IN (695);
CREATE TABLE elevation_points_696 PARTITION OF elevation_points 
    FOR VALUES IN (696);
CREATE TABLE elevation_points_697 PARTITION OF elevation_points 
    FOR VALUES IN (697);
CREATE TABLE elevation_points_698 PARTITION OF elevation_points 
    FOR VALUES IN (698);
CREATE TABLE elevation_points_699 PARTITION OF elevation_points 
    FOR VALUES IN (699);
CREATE TABLE elevation_points_700 PARTITION OF elevation_points 
    FOR VALUES IN (700);
CREATE TABLE elevation_points_701 PARTITION OF elevation_points 
    FOR VALUES IN (701);
CREATE TABLE elevation_points_702 PARTITION OF elevation_points 
    FOR VALUES IN (702);
CREATE TABLE elevation_points_703 PARTITION OF elevation_points 
    FOR VALUES IN (703);
CREATE TABLE elevation_points_704 PARTITION OF elevation_points 
    FOR VALUES IN (704);
CREATE TABLE elevation_points_705 PARTITION OF elevation_points 
    FOR VALUES IN (705);
CREATE TABLE elevation_points_706 PARTITION OF elevation_points 
    FOR VALUES IN (706);
CREATE TABLE elevation_points_707 PARTITION OF elevation_points 
    FOR VALUES IN (707);
CREATE TABLE elevation_points_708 PARTITION OF elevation_points 
    FOR VALUES IN (708);
CREATE TABLE elevation_points_709 PARTITION OF elevation_points 
    FOR VALUES IN (709);
CREATE TABLE elevation_points_710 PARTITION OF elevation_points 
    FOR VALUES IN (710);
CREATE TABLE elevation_points_711 PARTITION OF elevation_points 
    FOR VALUES IN (711);
CREATE TABLE elevation_points_712 PARTITION OF elevation_points 
    FOR VALUES IN (712);
CREATE TABLE elevation_points_713 PARTITION OF elevation_points 
    FOR VALUES IN (713);
CREATE TABLE elevation_points_714 PARTITION OF elevation_points 
    FOR VALUES IN (714);
CREATE TABLE elevation_points_715 PARTITION OF elevation_points 
    FOR VALUES IN (715);
CREATE TABLE elevation_points_716 PARTITION OF elevation_points 
    FOR VALUES IN (716);
CREATE TABLE elevation_points_717 PARTITION OF elevation_points 
    FOR VALUES IN (717);
CREATE TABLE elevation_points_718 PARTITION OF elevation_points 
    FOR VALUES IN (718);
CREATE TABLE elevation_points_719 PARTITION OF elevation_points 
    FOR VALUES IN (719);
CREATE TABLE elevation_points_720 PARTITION OF elevation_points 
    FOR VALUES IN (720);
CREATE TABLE elevation_points_721 PARTITION OF elevation_points 
    FOR VALUES IN (721);
CREATE TABLE elevation_points_722 PARTITION OF elevation_points 
    FOR VALUES IN (722);
CREATE TABLE elevation_points_723 PARTITION OF elevation_points 
    FOR VALUES IN (723);
CREATE TABLE elevation_points_724 PARTITION OF elevation_points 
    FOR VALUES IN (724);
CREATE TABLE elevation_points_725 PARTITION OF elevation_points 
    FOR VALUES IN (725);
CREATE TABLE elevation_points_726 PARTITION OF elevation_points 
    FOR VALUES IN (726);
CREATE TABLE elevation_points_727 PARTITION OF elevation_points 
    FOR VALUES IN (727);
CREATE TABLE elevation_points_728 PARTITION OF elevation_points 
    FOR VALUES IN (728);
CREATE TABLE elevation_points_729 PARTITION OF elevation_points 
    FOR VALUES IN (729);
CREATE TABLE elevation_points_730 PARTITION OF elevation_points 
    FOR VALUES IN (730);
CREATE TABLE elevation_points_731 PARTITION OF elevation_points 
    FOR VALUES IN (731);
CREATE TABLE elevation_points_732 PARTITION OF elevation_points 
    FOR VALUES IN (732);
CREATE TABLE elevation_points_733 PARTITION OF elevation_points 
    FOR VALUES IN (733);
CREATE TABLE elevation_points_734 PARTITION OF elevation_points 
    FOR VALUES IN (734);
CREATE TABLE elevation_points_735 PARTITION OF elevation_points 
    FOR VALUES IN (735);
CREATE TABLE elevation_points_736 PARTITION OF elevation_points 
    FOR VALUES IN (736);
CREATE TABLE elevation_points_737 PARTITION OF elevation_points 
    FOR VALUES IN (737);
CREATE TABLE elevation_points_738 PARTITION OF elevation_points 
    FOR VALUES IN (738);
CREATE TABLE elevation_points_739 PARTITION OF elevation_points 
    FOR VALUES IN (739);
CREATE TABLE elevation_points_740 PARTITION OF elevation_points 
    FOR VALUES IN (740);
CREATE TABLE elevation_points_741 PARTITION OF elevation_points 
    FOR VALUES IN (741);
CREATE TABLE elevation_points_742 PARTITION OF elevation_points 
    FOR VALUES IN (742);
CREATE TABLE elevation_points_743 PARTITION OF elevation_points 
    FOR VALUES IN (743);
CREATE TABLE elevation_points_744 PARTITION OF elevation_points 
    FOR VALUES IN (744);
CREATE TABLE elevation_points_745 PARTITION OF elevation_points 
    FOR VALUES IN (745);
CREATE TABLE elevation_points_746 PARTITION OF elevation_points 
    FOR VALUES IN (746);
CREATE TABLE elevation_points_747 PARTITION OF elevation_points 
    FOR VALUES IN (747);
CREATE TABLE elevation_points_748 PARTITION OF elevation_points 
    FOR VALUES IN (748);
CREATE TABLE elevation_points_749 PARTITION OF elevation_points 
    FOR VALUES IN (749);
CREATE TABLE elevation_points_750 PARTITION OF elevation_points 
    FOR VALUES IN (750);
CREATE TABLE elevation_points_751 PARTITION OF elevation_points 
    FOR VALUES IN (751);
CREATE TABLE elevation_points_752 PARTITION OF elevation_points 
    FOR VALUES IN (752);
CREATE TABLE elevation_points_753 PARTITION OF elevation_points 
    FOR VALUES IN (753);
CREATE TABLE elevation_points_754 PARTITION OF elevation_points 
    FOR VALUES IN (754);
CREATE TABLE elevation_points_755 PARTITION OF elevation_points 
    FOR VALUES IN (755);
CREATE TABLE elevation_points_756 PARTITION OF elevation_points 
    FOR VALUES IN (756);
CREATE TABLE elevation_points_757 PARTITION OF elevation_points 
    FOR VALUES IN (757);
CREATE TABLE elevation_points_758 PARTITION OF elevation_points 
    FOR VALUES IN (758);
CREATE TABLE elevation_points_759 PARTITION OF elevation_points 
    FOR VALUES IN (759);
CREATE TABLE elevation_points_760 PARTITION OF elevation_points 
    FOR VALUES IN (760);
CREATE TABLE elevation_points_761 PARTITION OF elevation_points 
    FOR VALUES IN (761);
CREATE TABLE elevation_points_762 PARTITION OF elevation_points 
    FOR VALUES IN (762);
CREATE TABLE elevation_points_763 PARTITION OF elevation_points 
    FOR VALUES IN (763);
CREATE TABLE elevation_points_764 PARTITION OF elevation_points 
    FOR VALUES IN (764);
CREATE TABLE elevation_points_765 PARTITION OF elevation_points 
    FOR VALUES IN (765);
CREATE TABLE elevation_points_766 PARTITION OF elevation_points 
    FOR VALUES IN (766);
CREATE TABLE elevation_points_767 PARTITION OF elevation_points 
    FOR VALUES IN (767);
CREATE TABLE elevation_points_768 PARTITION OF elevation_points 
    FOR VALUES IN (768);
CREATE TABLE elevation_points_769 PARTITION OF elevation_points 
    FOR VALUES IN (769);
CREATE TABLE elevation_points_770 PARTITION OF elevation_points 
    FOR VALUES IN (770);
CREATE TABLE elevation_points_771 PARTITION OF elevation_points 
    FOR VALUES IN (771);
CREATE TABLE elevation_points_772 PARTITION OF elevation_points 
    FOR VALUES IN (772);
CREATE TABLE elevation_points_773 PARTITION OF elevation_points 
    FOR VALUES IN (773);
CREATE TABLE elevation_points_774 PARTITION OF elevation_points 
    FOR VALUES IN (774);
CREATE TABLE elevation_points_775 PARTITION OF elevation_points 
    FOR VALUES IN (775);
CREATE TABLE elevation_points_def PARTITION OF elevation_points DEFAULT;

-- Index on the center points of the data
CREATE INDEX elevation_center_points_idx
  ON elevation_points
  USING GIST (center_pt);
