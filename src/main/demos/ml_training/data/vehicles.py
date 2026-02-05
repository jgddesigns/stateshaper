vehicles = [
{"name":"tesla_model_s_plaid","torque":1.0,"acceleration":1.0,"speed":0.95,"durability":0.75,"tread":0.8,"size":0.55,"tank":0.7,"efficiency":0.85},
{"name":"tesla_model_s","torque":0.95,"acceleration":0.9,"speed":0.9,"durability":0.75,"tread":0.8,"size":0.55,"tank":0.7,"efficiency":0.85},
{"name":"tesla_model_3","torque":0.9,"acceleration":0.85,"speed":0.75,"durability":0.7,"tread":0.75,"size":0.45,"tank":0.65,"efficiency":0.9},
{"name":"tesla_model_y","torque":0.9,"acceleration":0.8,"speed":0.75,"durability":0.75,"tread":0.75,"size":0.6,"tank":0.7,"efficiency":0.85},
{"name":"tesla_model_x","torque":0.95,"acceleration":0.9,"speed":0.8,"durability":0.8,"tread":0.8,"size":0.65,"tank":0.75,"efficiency":0.8},

{"name":"toyota_corolla","torque":0.45,"acceleration":0.45,"speed":0.55,"durability":0.85,"tread":0.7,"size":0.45,"tank":0.75,"efficiency":0.85},
{"name":"toyota_camry","torque":0.55,"acceleration":0.5,"speed":0.6,"durability":0.85,"tread":0.7,"size":0.5,"tank":0.75,"efficiency":0.8},
{"name":"toyota_prius","torque":0.45,"acceleration":0.4,"speed":0.55,"durability":0.8,"tread":0.65,"size":0.45,"tank":0.85,"efficiency":0.95},
{"name":"toyota_avalon","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.85,"tread":0.7,"size":0.55,"tank":0.8,"efficiency":0.75},
{"name":"toyota_supra","torque":0.8,"acceleration":0.85,"speed":0.9,"durability":0.7,"tread":0.85,"size":0.45,"tank":0.65,"efficiency":0.6},
{"name":"toyota_tacoma","torque":0.8,"acceleration":0.55,"speed":0.6,"durability":0.9,"tread":0.8,"size":0.75,"tank":0.85,"efficiency":0.55},
{"name":"toyota_tundra","torque":0.9,"acceleration":0.6,"speed":0.65,"durability":0.9,"tread":0.8,"size":0.85,"tank":0.9,"efficiency":0.45},
{"name":"toyota_4runner","torque":0.85,"acceleration":0.5,"speed":0.6,"durability":0.95,"tread":0.85,"size":0.8,"tank":0.9,"efficiency":0.45},
{"name":"toyota_rav4","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.85,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.75},

{"name":"honda_civic","torque":0.5,"acceleration":0.5,"speed":0.6,"durability":0.8,"tread":0.7,"size":0.45,"tank":0.7,"efficiency":0.85},
{"name":"honda_accord","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.5,"tank":0.75,"efficiency":0.8},
{"name":"honda_crv","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.75},
{"name":"honda_pilot","torque":0.75,"acceleration":0.6,"speed":0.65,"durability":0.85,"tread":0.8,"size":0.75,"tank":0.8,"efficiency":0.6},
{"name":"honda_odyssey","torque":0.7,"acceleration":0.55,"speed":0.65,"durability":0.85,"tread":0.75,"size":0.75,"tank":0.8,"efficiency":0.65},

{"name":"ford_f150","torque":0.95,"acceleration":0.6,"speed":0.65,"durability":0.9,"tread":0.8,"size":0.85,"tank":0.9,"efficiency":0.45},
{"name":"ford_ranger","torque":0.8,"acceleration":0.6,"speed":0.65,"durability":0.85,"tread":0.8,"size":0.75,"tank":0.85,"efficiency":0.5},
{"name":"ford_explorer","torque":0.75,"acceleration":0.6,"speed":0.7,"durability":0.85,"tread":0.8,"size":0.7,"tank":0.8,"efficiency":0.6},
{"name":"ford_escape","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.75},
{"name":"ford_mustang_gt","torque":0.85,"acceleration":0.8,"speed":0.85,"durability":0.7,"tread":0.75,"size":0.55,"tank":0.65,"efficiency":0.55},

{"name":"chevy_silverado","torque":0.95,"acceleration":0.6,"speed":0.65,"durability":0.9,"tread":0.8,"size":0.85,"tank":0.9,"efficiency":0.45},
{"name":"chevy_colorado","torque":0.8,"acceleration":0.6,"speed":0.65,"durability":0.85,"tread":0.8,"size":0.75,"tank":0.85,"efficiency":0.5},
{"name":"chevy_malibu","torque":0.55,"acceleration":0.5,"speed":0.6,"durability":0.8,"tread":0.7,"size":0.5,"tank":0.7,"efficiency":0.75},
{"name":"chevy_camaro_ss","torque":0.85,"acceleration":0.8,"speed":0.85,"durability":0.7,"tread":0.75,"size":0.55,"tank":0.65,"efficiency":0.5},
{"name":"chevy_tahoe","torque":0.85,"acceleration":0.55,"speed":0.65,"durability":0.9,"tread":0.8,"size":0.9,"tank":0.9,"efficiency":0.4},
{"name":"chevy_bolt_ev","torque":0.8,"acceleration":0.7,"speed":0.65,"durability":0.75,"tread":0.7,"size":0.45,"tank":0.6,"efficiency":0.9},

{"name":"bmw_3_series","torque":0.7,"acceleration":0.65,"speed":0.75,"durability":0.75,"tread":0.8,"size":0.5,"tank":0.7,"efficiency":0.7},
{"name":"bmw_m3","torque":0.85,"acceleration":0.85,"speed":0.9,"durability":0.7,"tread":0.85,"size":0.5,"tank":0.65,"efficiency":0.6},
{"name":"bmw_x3","torque":0.7,"acceleration":0.6,"speed":0.7,"durability":0.8,"tread":0.8,"size":0.6,"tank":0.75,"efficiency":0.65},
{"name":"bmw_x5","torque":0.8,"acceleration":0.65,"speed":0.75,"durability":0.8,"tread":0.8,"size":0.7,"tank":0.8,"efficiency":0.6},

{"name":"audi_a4","torque":0.65,"acceleration":0.6,"speed":0.7,"durability":0.75,"tread":0.75,"size":0.5,"tank":0.7,"efficiency":0.7},
{"name":"audi_a6","torque":0.7,"acceleration":0.65,"speed":0.75,"durability":0.75,"tread":0.75,"size":0.55,"tank":0.75,"efficiency":0.65},
{"name":"audi_q5","torque":0.7,"acceleration":0.65,"speed":0.7,"durability":0.8,"tread":0.8,"size":0.6,"tank":0.75,"efficiency":0.65},
{"name":"audi_q7","torque":0.8,"acceleration":0.65,"speed":0.7,"durability":0.85,"tread":0.8,"size":0.75,"tank":0.8,"efficiency":0.55},

{"name":"mercedes_c_class","torque":0.65,"acceleration":0.6,"speed":0.7,"durability":0.75,"tread":0.75,"size":0.5,"tank":0.7,"efficiency":0.7},
{"name":"mercedes_e_class","torque":0.7,"acceleration":0.65,"speed":0.75,"durability":0.75,"tread":0.75,"size":0.55,"tank":0.75,"efficiency":0.65},
{"name":"mercedes_glc","torque":0.7,"acceleration":0.6,"speed":0.7,"durability":0.8,"tread":0.8,"size":0.6,"tank":0.75,"efficiency":0.65},
{"name":"mercedes_g_wagon","torque":0.9,"acceleration":0.6,"speed":0.7,"durability":0.95,"tread":0.9,"size":0.85,"tank":0.85,"efficiency":0.35},

{"name":"subaru_impreza","torque":0.55,"acceleration":0.5,"speed":0.6,"durability":0.85,"tread":0.85,"size":0.45,"tank":0.7,"efficiency":0.75},
{"name":"subaru_wrx","torque":0.75,"acceleration":0.7,"speed":0.8,"durability":0.75,"tread":0.85,"size":0.5,"tank":0.65,"efficiency":0.6},
{"name":"subaru_outback","torque":0.65,"acceleration":0.55,"speed":0.65,"durability":0.85,"tread":0.85,"size":0.6,"tank":0.75,"efficiency":0.7},
{"name":"subaru_forester","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.85,"tread":0.85,"size":0.6,"tank":0.75,"efficiency":0.7},

{"name":"nissan_altima","torque":0.55,"acceleration":0.5,"speed":0.6,"durability":0.75,"tread":0.7,"size":0.5,"tank":0.7,"efficiency":0.75},
{"name":"nissan_maxima","torque":0.65,"acceleration":0.6,"speed":0.7,"durability":0.75,"tread":0.75,"size":0.55,"tank":0.75,"efficiency":0.7},
{"name":"nissan_rogue","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.75},
{"name":"nissan_gtr","torque":0.95,"acceleration":0.9,"speed":0.95,"durability":0.8,"tread":0.9,"size":0.55,"tank":0.65,"efficiency":0.45},

{"name":"hyundai_elantra","torque":0.5,"acceleration":0.5,"speed":0.6,"durability":0.75,"tread":0.7,"size":0.45,"tank":0.7,"efficiency":0.8},
{"name":"hyundai_sonata","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.75,"tread":0.7,"size":0.5,"tank":0.75,"efficiency":0.75},
{"name":"hyundai_tucson","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.7},
{"name":"hyundai_palisade","torque":0.75,"acceleration":0.6,"speed":0.65,"durability":0.85,"tread":0.8,"size":0.8,"tank":0.8,"efficiency":0.55},

{"name":"kia_forte","torque":0.5,"acceleration":0.5,"speed":0.6,"durability":0.75,"tread":0.7,"size":0.45,"tank":0.7,"efficiency":0.8},
{"name":"kia_k5","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.75,"tread":0.7,"size":0.5,"tank":0.75,"efficiency":0.75},
{"name":"kia_sportage","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.7},
{"name":"kia_telluride","torque":0.75,"acceleration":0.6,"speed":0.65,"durability":0.85,"tread":0.8,"size":0.8,"tank":0.8,"efficiency":0.55},

{"name":"mazda_3","torque":0.55,"acceleration":0.55,"speed":0.65,"durability":0.75,"tread":0.75,"size":0.45,"tank":0.7,"efficiency":0.8},
{"name":"mazda_6","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.75,"tread":0.75,"size":0.5,"tank":0.75,"efficiency":0.75},
{"name":"mazda_cx5","torque":0.6,"acceleration":0.55,"speed":0.65,"durability":0.8,"tread":0.75,"size":0.6,"tank":0.75,"efficiency":0.7},
{"name":"mazda_miata","torque":0.55,"acceleration":0.65,"speed":0.75,"durability":0.7,"tread":0.85,"size":0.35,"tank":0.55,"efficiency":0.75}
]
