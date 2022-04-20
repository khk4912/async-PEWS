from logging import Formatter
from typing import Literal, get_args

LOGGING_FORMAT = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

NOTICE_DELAY = 0
SPEED = 3
TIME_ZONE = 9
TZ_MSEC = 3600000 * TIME_ZONE

HEADER_LEN = 4
STA_LIST = []
STA_LEN = 0
MAX_EQK_INFO_LEN = 120
MAX_EQK_STR_LEN = 60

DELAY = 1000
TIDE = DELAY
SYNC_PEROID = 10000
B_SYNC = True

BIN_PATH = "http://www.weather.go.kr/pews/data/"


# fmt: off

Region = Literal[
  "서울",
  "부산",
  "대구",
  "인천",
  "광주",
  "대전",
  "울산",
  "세종",
  "경기",
  "강원",
  "충북",
  "충남",
  "전북",
  "전남",
  "경북",
  "경남",
  "제주",
]

RA = get_args(Region)

CA = [
  11110, 11140, 11170, 11200, 11215, 11230, 11260, 11290, 11305, 11320, 11350,
  11380, 11410, 11440, 11470, 11500, 11530, 11545, 11560, 11590, 11620, 11650,
  11680, 11710, 11740, 26110, 26140, 26170, 26200, 26230, 26260, 26290, 26320,
  26350, 26380, 26410, 26440, 26470, 26500, 26530, 26710, 27110, 27140, 27170,
  27200, 27230, 27260, 27290, 27710, 28110, 28140, 28177, 28185, 28200, 28237,
  28245, 28260, 28710, 28720, 29110, 29140, 29155, 29170, 29200, 30110, 30140,
  30170, 30200, 30230, 31110, 31140, 31170, 31200, 31710, 36110, 41111, 41113,
  41115, 41117, 41131, 41133, 41135, 41150, 41171, 41173, 41190, 41210, 41220,
  41250, 41271, 41273, 41281, 41285, 41287, 41290, 41310, 41360, 41370, 41390,
  41410, 41430, 41450, 41461, 41463, 41465, 41480, 41500, 41550, 41570, 41590,
  41610, 41630, 41650, 41670, 41800, 41820, 41830, 42110, 42130, 42150, 42170,
  42190, 42210, 42230, 42720, 42730, 42750, 42760, 42770, 42780, 42790, 42800,
  42810, 42820, 42830, 43111, 43112, 43113, 43114, 43130, 43150, 43720, 43730,
  43740, 43745, 43750, 43760, 43770, 43800, 44131, 44133, 44150, 44180, 44200,
  44210, 44230, 44250, 44270, 44710, 44760, 44770, 44790, 44800, 44810, 44825,
  45111, 45113, 45130, 45140, 45180, 45190, 45210, 45710, 45720, 45730, 45740,
  45750, 45770, 45790, 45800, 46110, 46130, 46150, 46170, 46230, 46710, 46720,
  46730, 46770, 46780, 46790, 46800, 46810, 46820, 46830, 46840, 46860, 46870,
  46880, 46890, 46900, 46910, 47111, 47113, 47130, 47150, 47170, 47190, 47210,
  47230, 47250, 47280, 47290, 47720, 47730, 47750, 47760, 47770, 47820, 47830,
  47840, 47850, 47900, 47920, 47930, 47940, 48121, 48123, 48125, 48127, 48129,
  48170, 48220, 48240, 48250, 48270, 48310, 48330, 48720, 48730, 48740, 48820,
  48840, 48850, 48860, 48870, 48880, 48890, 50110, 50130,
]
DA = [
  "서울,종로구,37.573172,126.97922,3975",
  "서울,중구,37.56376,126.997459,3975",
  "서울,용산구,37.532612,126.990182,4126",
  "서울,성동구,37.563386,127.037047,3976",
  "서울,광진구,37.53821,127.082191,4128",
  "서울,동대문구,37.574428,127.039712,3976",
  "서울,중랑구,37.606736,127.092924,3826",
  "서울,성북구,37.58944,127.016817,3976",
  "서울,강북구,37.639745,127.025547,3825",
  "서울,도봉구,37.668639,127.047364,3674",
  "서울,노원구,37.654375,127.056318,3675",
  "서울,은평구,37.602766,126.928839,3823",
  "서울,서대문구,37.579213,126.936773,3974",
  "서울,마포구,37.566404,126.901763,3974,",
  "서울,양천구,37.517019,126.866538,4124",
  "서울,강서구,37.550968,126.849614,3972",
  "서울,구로구,37.49565,126.887771,4275",
  "서울,금천구,37.456979,126.895656,4275",
  "서울,영등포구,37.52641,126.896252,4124",
  "서울,동작구,37.512462,126.939485,4125",
  "서울,관악구,37.478449,126.951758,4127",
  "서울,서초구,37.48378,127.032733,4278",
  "서울,강남구,37.517336,127.047367,4127",
  "서울,송파구,37.514741,127.106052,4129",
  "서울,강동구,37.53012,127.123858,4129",
  "부산,중구,35.106333,129.032372,11415",
  "부산,서구,35.097689,129.023906,11566",
  "부산,동구,35.129298,129.045302,11415",
  "부산,영도구,35.091224,129.067945,11567",
  "부산,부산진구,35.162943,129.053097,11265",
  "부산,동래구,35.205011,129.083632,11265",
  "부산,남구,35.136318,129.084477,11416",
  "부산,북구,35.197266,128.990201,11263",
  "부산,해운대구,35.163096,129.1635,11267",
  "부산,사하구,35.104503,128.974786,11414",
  "부산,금정구,35.243036,129.092125,11114",
  "부산,강서구,35.212155,128.980552,10961",
  "부산,연제구,35.176273,129.079814,11265",
  "부산,수영구,35.145568,129.113132,11417",
  "부산,사상구,35.152585,128.991196,11263",
  "부산,기장군,35.244476,129.222421,11117",
  "대구,중구,35.869305,128.606199,9142",
  "대구,동구,35.886576,128.635483,9142",
  "대구,서구,35.871814,128.559166,9141",
  "대구,남구,35.845968,128.597675,9292",
  "대구,북구,35.885726,128.582811,9141",
  "대구,수성구,35.85821,128.630739,9142",
  "대구,달서구,35.829905,128.532806,9291",
  "대구,달성군,35.774645,128.431478,9440",
  "인천,중구,37.473715,126.621529,4270",
  "인천,동구,37.473831,126.643266,4270",
  "인천,미추홀구,37.463598,126.650573,4271",
  "인천,연수구,37.410183,126.678313,4422",
  "인천,남동구,37.447358,126.731623,4423",
  "인천,부평구,37.506989,126.721668,4121",
  "인천,계양구,37.537102,126.737663,4121",
  "인천,서구,37.545374,126.675987,4120",
  "인천,강화군,37.74745,126.487365,3512",
  "인천,옹진군,37.446609,126.636785,4421",
  "광주,동구,35.146085,126.923103,11373",
  "광주,서구,35.151601,126.890072,12221",
  "광주,남구,35.132829,126.902408,11373",
  "광주,북구,35.174128,126.912084,11222",
  "광주,광산구,35.139557,126.793672,11370",
  "대전,동구,36.311886,127.454818,7760",
  "대전,중구,36.325734,127.421365,7759",
  "대전,서구,36.355413,127.383686,7607",
  "대전,유성구,36.362289,127.356253,7607",
  "대전,대덕구,36.346732,127.415617,7759",
  "울산,중구,35.569376,129.332543,10062",
  "울산,남구,35.543797,129.330113,10213",
  "울산,동구,35.504813,129.416623,10215",
  "울산,북구,35.582601,129.361283,10063",
  "울산,울주군,35.52247,129.242209,10211",
  "세종,세종시,36.592892,127.292362,7001",
  "경기,수원시 장안구,37.303493,127.009678,4731",
  "경기,수원시 권선구,37.25761,126.971702,4881",
  "경기,수원시 팔달구,37.286534,127.035816,4882",
  "경기,수원시 영통구,37.259508,127.046588,4882",
  "경기,성남시 수정구,37.450292,127.145529,4280",
  "경기,성남시 중원구,37.430641,127.137109,4431",
  "경기,성남시 분당구,37.38275,127.118913,4583",
  "경기,의정부시,37.738061,127.033893,3523",
  "경기,안양시 만안구,37.386584,126.93234,4578",
  "경기,안양시 동안구,37.392511,126.951274,4579",
  "경기,부천시,37.503486,126.766046,4122",
  "경기,광명시,37.478545,126.864711,4275",
  "경기,평택시,36.992283,127.112653,5790",
  "경기,동두천시,37.903591,127.060388,2920",
  "경기,안산시 상록구,37.300841,126.846205,4727",
  "경기,안산시 단원구,37.31959,126.812365,4727",
  "경기,고양시 덕양구,37.637468,126.832374,3821",
  "경기,고양시 일산동구,37.65895,126.774759,3669",
  "경기,고양시 일산서구,37.675203,126.750664,3673",
  "경기,과천시,37.429194,126.987607,4428",
  "경기,구리시,37.594326,127.129606,3978",
  "경기,남양주시,37.635977,127.216385,3829",
  "경기,오산시,37.149891,127.077494,5336",
  "경기,시흥시,37.380063,126.802797,4576",
  "경기,군포시,37.361622,126.935121,4578",
  "경기,의왕시,37.344823,126.968291,4730",
  "경기,하남시,37.539257,127.214853,4131",
  "경기,용인시 처인구,37.234494,127.201367,5037",
  "경기,용인시 기흥구,37.280446,127.114683,4884",
  "경기,용인시 수지구,37.322149,127.098082,4732",
  "경기,파주시,37.760141,126.779958,3367",
  "경기,이천시,37.272181,127.434993,4890",
  "경기,안성시,37.008031,127.279768,5640",
  "경기,김포시,37.615271,126.715648,3819",
  "경기,화성시,37.199541,126.831438,5180",
  "경기,광주시,37.429462,127.255175,4434",
  "경기,양주시,37.785227,127.045835,3372",
  "경기,포천시,37.894985,127.200368,3074",
  "경기,여주시,37.298249,127.63721,4894",
  "경기,연천군,38.096677,127.074874,2467",
  "경기,가평군,37.831328,127.509551,3231",
  "경기,양평군,37.491692,127.487591,4287",
  "강원,춘천시,37.881272,127.730144,3084",
  "강원,원주시,37.341707,127.919787,4749",
  "강원,강릉시,37.752109,128.875899,3409",
  "강원,동해시,37.524697,129.114375,4169",
  "강원,태백시,37.164087,128.985759,5223",
  "강원,속초시,38.207089,128.591917,2044",
  "강원,삼척시,37.449935,129.165151,4472",
  "강원,홍천군,37.696825,127.888675,3691",
  "강원,횡성군,37.491874,127.984878,4297",
  "강원,영월군,37.18368,128.461571,5213",
  "강원,평창군,37.370755,128.390208,4607",
  "강원,정선군,37.380645,128.660812,4613",
  "강원,철원군,38.146758,127.313358,2321",
  "강원,화천군,38.106092,127.708213,2329",
  "강원,양구군,38.109959,127.989951,2334",
  "강원,인제군,38.06976,128.170429,2489",
  "강원,고성군,38.380542,128.467781,1589",
  "강원,양양군,38.07539,128.618847,2498",
  "충북,청주시 상당구,36.634684,127.48847,6854",
  "충북,청주시 서원구,36.637684,127.469708,6854",
  "충북,청주시 흥덕구,36.641489,127.431134,6853",
  "충북,청주시 청원구,36.651447,127.486648,6703",
  "충북,충주시,36.99108,127.925919,5806",
  "충북,제천시,37.132628,128.190905,5358",
  "충북,보은군,36.489468,127.729504,7312",
  "충북,옥천군,36.306664,127.571294,7762",
  "충북,영동군,36.175011,127.783425,8219",
  "충북,증평군,36.785403,127.581673,6403",
  "충북,진천군,36.85537,127.435452,6098",
  "충북,괴산군,36.815281,127.786601,6256",
  "충북,음성군,36.940288,127.690467,5952",
  "충북,단양군,36.984664,128.365783,5815",
  "충남,천안시 동남구,36.806985,127.150333,6244",
  "충남,천안시 서북구,36.878428,127.155173,6093",
  "충남,공주시,36.446589,127.119019,7451",
  "충남,보령시,36.333459,126.6128,7743",
  "충남,아산시,36.790076,127.002443,6392",
  "충남,서산시,36.784965,126.450294,6381",
  "충남,논산시,36.187163,127.098742,8205",
  "충남,계룡시,36.274529,127.248676,7906",
  "충남,당진시,36.889545,126.645567,6082",
  "충남,금산군,36.108805,127.487902,8364",
  "충남,부여군,36.275777,126.909812,7900",
  "충남,서천군,36.080231,126.691313,8650",
  "충남,청양군,36.459188,126.802258,7294",
  "충남,홍성군,36.601357,126.660838,6838",
  "충남,예산군,36.682731,126.84878,6690",
  "충남,태안군,36.745739,126.297886,6528",
  "전북,전주시 완산구,35.81218,127.119796,9263",
  "전북,전주시 덕진구,35.829393,127.134326,9263",
  "전북,군산시,35.967613,126.7368,8802",
  "전북,익산시,35.948284,126.95759,8958",
  "전북,정읍시,35.569845,126.856126,10013",
  "전북,남원시,35.416414,127.390423,10476",
  "전북,김제시,35.803591,126.880311,9258",
  "전북,완주군,35.904737,127.161622,8962",
  "전북,진안군,35.79197,127.424684,9420",
  "전북,무주군,36.007103,127.660755,8670",
  "전북,장수군,35.647385,127.521143,9875",
  "전북,임실군,35.618216,127.289172,9870",
  "전북,순창군,35.374285,127.13765,10622",
  "전북,고창군,35.435781,126.701957,10463",
  "전북,부안군,35.731725,126.733384,9557",
  "전남,목포시,34.81191,126.392404,12268",
  "전남,여수시,34.760444,127.662231,12445",
  "전남,순천시,34.950612,127.487359,11837",
  "전남,나주시,35.015837,126.710809,11671",
  "전남,광양시,34.940676,127.695966,11992",
  "전남,담양군,35.32118,126.988104,10770",
  "전남,곡성군,35.282012,127.292012,10927",
  "전남,구례군,35.202566,127.462817,11082",
  "전남,고흥군,34.611232,127.285008,12890",
  "전남,보성군,34.7715,127.080005,12433",
  "전남,화순군,35.064587,126.986489,11525",
  "전남,장흥군,34.681737,126.907008,12732",
  "전남,강진군,34.642083,126.767142,12880",
  "전남,해남군,34.573464,126.599183,13027",
  "전남,영암군,34.800101,126.696823,12274",
  "전남,무안군,34.990455,126.481667,11817",
  "전남,함평군,35.065906,126.516536,11516",
  "전남,영광군,35.277195,126.512012,10912",
  "전남,장성군,35.301822,126.784836,10766",
  "전남,완도군,34.31104,126.754902,13786",
  "전남,진도군,34.486954,126.263558,13323",
  "전남,신안군,34.833436,126.351473,12268",
  "경북,포항시 남구,36.00865,129.35933,8704",
  "경북,포항시 북구,36.041824,129.365649,8704",
  "경북,경주시,35.83754367,129.2144188,9305",
  "경북,김천시,36.139822,128.113657,8377",
  "경북,안동시,36.568409,128.72962,7030",
  "경북,구미시,36.119552,128.344499,8381",
  "경북,영주시,36.805671,128.623988,6273",
  "경북,영천시,35.973241,128.938597,8846",
  "경북,상주시,36.410953,128.159142,7472",
  "경북,문경시,36.586528,128.186769,7019",
  "경북,경산시,35.825078,128.741271,9295",
  "경북,군위군,36.242981,128.572901,8084",
  "경북,의성군,36.352724,128.697164,7633",
  "경북,청송군,36.436256,129.057101,7490",
  "경북,영양군,36.666725,129.112395,6736",
  "경북,영덕군,36.415069,129.366078,7496",
  "경북,청도군,35.647469,128.734127,9899",
  "경북,고령군,35.726098,128.262812,9588",
  "경북,성주군,35.919119,128.282962,8984",
  "경북,칠곡군,35.995518,128.401567,8836",
  "경북,예천군,36.657704,128.45292,6723",
  "경북,봉화군,36.893149,128.732665,6124",
  "경북,울진군,36.993068,129.400533,5836",
  "경북,울릉군,37.484426,130.90586,4356",
  "경남,창원시 의창구,35.254005,128.640122,10954",
  "경남,창원시 성산구,35.198465,128.702644,11258",
  "경남,창원시 마산합포구,35.196928,128.567867,11255",
  "경남,창원시 마산회원구,35.220822,128.579677,11104",
  "경남,창원시 진해구,35.133204,128.710181,11409",
  "경남,진주시,35.180119,128.107529,11246",
  "경남,통영시,34.854366,128.433081,12158",
  "경남,사천시,35.003466,128.064242,11698",
  "경남,김해시,35.228588,128.889428,11110",
  "경남,밀양시,35.503816,128.746619,10201",
  "경남,거제시,34.880459,128.621121,12162",
  "경남,양산시,35.335043,129.037407,10811",
  "경남,의령군,35.32221,128.261686,10796",
  "경남,함안군,35.272494,128.406464,10950",
  "경남,창녕군,35.544566,128.492246,10196",
  "경남,고성군,34.973037,128.32225,11854",
  "경남,남해군,34.837348,127.892289,12298",
  "경남,하동군,35.067313,127.751317,11541",
  "경남,산청군,35.415678,127.873467,10486",
  "경남,함양군,35.520371,127.725153,10181",
  "경남,거창군,35.686719,127.909566,9732",
  "경남,합천군,35.566621,128.165806,10039",
  "제주,제주시,33.499562,126.531164,16348",
  "제주,서귀포시,33.254083,126.56010,16953",
]

STATION = ['안동', '송현', '앙성', '안마도', '안면도', '아산', '백령도', '백운산', '비금도', '백운', '벌곡', '별량', '보개', '보은', '보성', '부산', '부론', '금정', '부석', '부여', '청주', '천안', '청안', '청도', '청일', '청풍', '청운', '창원', '청양', '춘천', '초도', '충주', '전주', '창녕', '춘양', '칠곡', '추자도', '춘장대', '칠서', '추풍령', '청산도', '청송', '철원', '대청도', '경산', '대구', '동두천', '덕적도', '동향', '당진', '동로', '대관령', '덕산', '단북', '단양', '덕유산', '어청도', '음성', '의령', '의성', '개천', '가곡', '가평', '격비', '가덕도', '거진', '강동', '가거도', '강구', '금강송', '광탄', '강화', '김천', '기계', '곡성', '갈천', '결성', '거문도', '김화', '금남', '김포', '고창', '교동', '고산', '강서구', '경주산내', '구좌', '구미', '군위', '사북', '광양', '한림', '삼가', '하일', '함양', '해남', '화원', '화성', '합천', '하의도', '횡성', '홍도', '홍성', '호미곶', '함평', '홍천', '회남', '하태도', '흑산도', '간동', '화도', '화서', '이천', '인제', '기린', '인제북', '임자도', '익산', '임실', '임원', '인천', '익산금강', '재산', '장성', '장흥', '장수', '주천', '진도', '제천', '정자', '완주', '정선', '정읍', '증산', '진주', '제주', '죽장', '지리산', '주문진', '진해', '증평', '전의', '진영', '조도', '주촌', '중랑구', '강릉', '거창', '고흥', '거금도', '금산', '공주', '고성', '거제', '무등산', '무등(초)', '이원', '임계', '마령', '무안', '문경', '밀양', '만재도', '물금', '매물도', '무녀도', '문덕', '모곡', '목포', '밀양산내', '문산', '내초', '남해', '나주', '내면', '남원', '내촌', '난지도', '나로도', '노성', '옥천', '옥계', '외연도', '평은', '포항', '보령', '부안', '면온', '평창', '표선', '산청', '상주', '순천', '서천', '서울', '서산', '서석', '상면', '성남', '서귀포', '서화', '시흥', '시종', '석보', '속초', '설성', '새만금', '심원', '신동', '신기', '신녕', '종로구', '수비', '순창', '수원', '태하', '태인', '태안', '태백', '대전', '동해', '우도', '의정부', '울진', '울릉도', '온정', '웅촌', '울산', '완도', '위천', '원주', '원북', '양동', '야로', '양평', '강현', '양양', '연천', '예천', '영동', '예안', '영광', '여수', '영양', '용암', '양북', '양구', '용정', '영종도', '욕지도', '연도', '영암', '영천', '영덕', '영북', '영주', '영월', '소연평도', '예산', '여서도', '유구']
