"""
Mangifera Shield — Treatment Recommendation Engine
Disease-specific treatment recommendations in Hindi + English.
Sourced from MangoMedix logic + agricultural extension research.
"""

TREATMENTS = {
    "Anthracnose": {
        "severity": "High",
        "en": {
            "name": "Anthracnose",
            "description": "Fungal disease causing dark, sunken lesions on leaves, flowers, and fruits. Common during warm, humid conditions.",
            "symptoms": [
                "Dark brown to black spots on leaves",
                "Sunken lesions on fruits",
                "Blossom blight and fruit drop",
                "Black spots on mature fruits"
            ],
            "treatment": [
                "Spray Carbendazim (0.1%) or Thiophanate Methyl at first sign",
                "Apply Copper Oxychloride (0.3%) as preventive spray before flowering",
                "Remove and destroy infected plant debris",
                "Ensure proper spacing between trees for air circulation",
                "Apply Mancozeb (0.25%) at 15-day intervals during monsoon"
            ],
            "prevention": [
                "Pre-harvest spray of Carbendazim",
                "Hot water treatment of fruits at 52°C for 15 minutes",
                "Proper post-harvest handling and cold storage"
            ]
        },
        "hi": {
            "name": "एन्थ्रेक्नोज",
            "description": "फफूंद जनित रोग जो पत्तियों, फूलों और फलों पर काले, धंसे हुए घाव पैदा करता है। गर्म और नम स्थितियों में आम है।",
            "symptoms": [
                "पत्तियों पर गहरे भूरे से काले धब्बे",
                "फलों पर धंसे हुए घाव",
                "फूल झड़ना और फल गिरना",
                "पके फलों पर काले धब्बे"
            ],
            "treatment": [
                "पहले लक्षण पर कार्बेन्डाजिम (0.1%) या थियोफैनेट मिथाइल का छिड़काव करें",
                "फूल आने से पहले कॉपर ऑक्सीक्लोराइड (0.3%) का रोकथाम छिड़काव करें",
                "संक्रमित पौधों के अवशेषों को हटाकर नष्ट करें",
                "हवा के प्रवाह के लिए पेड़ों के बीच उचित दूरी रखें",
                "बरसात में 15 दिन के अंतराल पर मैन्कोज़ेब (0.25%) लगाएं"
            ],
            "prevention": [
                "तुड़ाई से पहले कार्बेन्डाजिम का छिड़काव",
                "फलों को 52°C पर 15 मिनट गर्म पानी से उपचारित करें",
                "तुड़ाई के बाद उचित रखरखाव और शीत भंडारण"
            ]
        }
    },
    "Bacterial Canker": {
        "severity": "High",
        "en": {
            "name": "Bacterial Canker",
            "description": "Bacterial infection causing raised, crusty lesions on leaves and stems. Spreads rapidly in wet conditions.",
            "symptoms": [
                "Raised, dark brown cankers on stems",
                "Angular leaf spots with yellow halos",
                "Oozing gummy substance from cankers",
                "Fruit cracking and rotting"
            ],
            "treatment": [
                "Spray Streptocycline (100 ppm) + Copper Oxychloride (0.3%)",
                "Prune and burn infected branches",
                "Apply Bordeaux paste on cut surfaces",
                "Spray Copper Hydroxide during dormant season",
                "Use disease-free planting material"
            ],
            "prevention": [
                "Avoid overhead irrigation",
                "Maintain field sanitation",
                "Use resistant varieties when available"
            ]
        },
        "hi": {
            "name": "बैक्टीरियल कैंकर",
            "description": "जीवाणु संक्रमण जो पत्तियों और तनों पर उभरे हुए, पपड़ीदार घाव बनाता है। गीली स्थितियों में तेजी से फैलता है।",
            "symptoms": [
                "तनों पर उभरे हुए, गहरे भूरे घाव",
                "पीले किनारों वाले कोणीय पत्ती के धब्बे",
                "घावों से चिपचिपा पदार्थ निकलना",
                "फल फटना और सड़ना"
            ],
            "treatment": [
                "स्ट्रेप्टोसाइक्लिन (100 ppm) + कॉपर ऑक्सीक्लोराइड (0.3%) का छिड़काव करें",
                "संक्रमित शाखाओं की छंटाई करके जला दें",
                "कटी सतहों पर बोर्डो पेस्ट लगाएं",
                "सुप्त मौसम में कॉपर हाइड्रॉक्साइड का छिड़काव करें",
                "रोग-मुक्त रोपण सामग्री का उपयोग करें"
            ],
            "prevention": [
                "ऊपरी सिंचाई से बचें",
                "खेत की स्वच्छता बनाए रखें",
                "उपलब्ध होने पर प्रतिरोधी किस्मों का उपयोग करें"
            ]
        }
    },
    "Cutting Weevil": {
        "severity": "Medium",
        "en": {
            "name": "Cutting Weevil",
            "description": "Insect pest that cuts young shoots and twigs, causing significant damage to new growth.",
            "symptoms": [
                "Clean cuts on young shoots and twigs",
                "Wilting of cut portions",
                "Reduced canopy growth",
                "Bore holes in tender shoots"
            ],
            "treatment": [
                "Spray Carbaryl (0.15%) or Quinalphos (0.05%)",
                "Collect and destroy fallen cut shoots",
                "Apply Imidacloprid (0.005%) as systemic spray",
                "Use light traps to monitor adult weevil population",
                "Spray Chlorpyrifos (0.05%) at new flush stage"
            ],
            "prevention": [
                "Regular monitoring during new growth season",
                "Clean cultivation and weed removal",
                "Avoid water stagnation near tree base"
            ]
        },
        "hi": {
            "name": "कटिंग वीविल (टहनी काटने वाला कीट)",
            "description": "कीट जो नई शाखाओं और टहनियों को काटता है, नई वृद्धि को काफी नुकसान पहुंचाता है।",
            "symptoms": [
                "नई शाखाओं और टहनियों पर साफ कटाव",
                "कटे हुए भागों का मुरझाना",
                "छतरी की वृद्धि कम होना",
                "कोमल शाखाओं में छेद"
            ],
            "treatment": [
                "कार्बारिल (0.15%) या क्विनालफॉस (0.05%) का छिड़काव करें",
                "गिरी हुई कटी शाखाओं को इकट्ठा करके नष्ट करें",
                "इमिडाक्लोप्रिड (0.005%) का प्रणालीगत छिड़काव करें",
                "वयस्क वीविल की निगरानी के लिए लाइट ट्रैप लगाएं",
                "नई पत्तियों के समय क्लोरपाइरीफॉस (0.05%) का छिड़काव करें"
            ],
            "prevention": [
                "नई वृद्धि के मौसम में नियमित निगरानी",
                "साफ खेती और खरपतवार हटाना",
                "पेड़ के आधार के पास पानी जमा न होने दें"
            ]
        }
    },
    "Die Back": {
        "severity": "High",
        "en": {
            "name": "Die Back",
            "description": "Progressive drying and death of branches from tip downward. Caused by Lasiodiplodia theobromae fungus.",
            "symptoms": [
                "Drying of twigs from tip downward",
                "Brown discoloration of vascular tissue",
                "Gum exudation from affected branches",
                "Complete drying of branches in severe cases"
            ],
            "treatment": [
                "Prune infected branches 15 cm below the infected area",
                "Apply Bordeaux paste on cut ends",
                "Spray Copper Oxychloride (0.3%) + Carbendazim (0.1%)",
                "Apply Thiophanate Methyl paste on pruning cuts",
                "Improve tree vigor with balanced fertilization"
            ],
            "prevention": [
                "Avoid injuries to bark during farm operations",
                "Maintain tree health with proper nutrition",
                "Immediate treatment of any wounds"
            ]
        },
        "hi": {
            "name": "डाई-बैक (शाखा सूखा)",
            "description": "शाखाओं का सिरे से नीचे की ओर क्रमशः सूखना और मरना। लासियोडिप्लोडिया फफूंद के कारण होता है।",
            "symptoms": [
                "टहनियों का सिरे से नीचे की ओर सूखना",
                "संवहनी ऊतक का भूरा रंग",
                "प्रभावित शाखाओं से गोंद का रिसाव",
                "गंभीर मामलों में शाखाओं का पूर्ण सूखना"
            ],
            "treatment": [
                "संक्रमित क्षेत्र से 15 सेमी नीचे संक्रमित शाखाओं की छंटाई करें",
                "कटे हुए सिरों पर बोर्डो पेस्ट लगाएं",
                "कॉपर ऑक्सीक्लोराइड (0.3%) + कार्बेन्डाजिम (0.1%) का छिड़काव करें",
                "छंटाई कटों पर थियोफैनेट मिथाइल पेस्ट लगाएं",
                "संतुलित उर्वरक से पेड़ की शक्ति बढ़ाएं"
            ],
            "prevention": [
                "खेती के कार्यों के दौरान छाल को चोट से बचाएं",
                "उचित पोषण से पेड़ का स्वास्थ्य बनाए रखें",
                "किसी भी घाव का तुरंत उपचार करें"
            ]
        }
    },
    "Gall Midge": {
        "severity": "Medium",
        "en": {
            "name": "Gall Midge",
            "description": "Insect pest causing abnormal gall formations on leaves and flowers, reducing fruit set.",
            "symptoms": [
                "Swollen, warty galls on leaves",
                "Distorted and curled young leaves",
                "Reduced flowering and fruit set",
                "Tiny larvae inside galls"
            ],
            "treatment": [
                "Spray Dimethoate (0.05%) at new leaf emergence",
                "Apply Neem oil (5%) as organic alternative",
                "Remove and destroy galled plant parts",
                "Spray Imidacloprid (0.005%) for severe infestation",
                "Apply soil drenching with Chlorpyrifos around tree base"
            ],
            "prevention": [
                "Monitor trees during new flush period",
                "Encourage natural predators",
                "Timely pruning of affected shoots"
            ]
        },
        "hi": {
            "name": "गॉल मिज (गांठ बनाने वाला कीट)",
            "description": "कीट जो पत्तियों और फूलों पर असामान्य गांठें बनाता है, फल लगने को कम करता है।",
            "symptoms": [
                "पत्तियों पर सूजी हुई, मस्से जैसी गांठें",
                "विकृत और मुड़ी हुई नई पत्तियां",
                "फूल और फल कम लगना",
                "गांठों के अंदर छोटे लार्वा"
            ],
            "treatment": [
                "नई पत्तियां आने पर डाइमेथोएट (0.05%) का छिड़काव करें",
                "जैविक विकल्प के रूप में नीम तेल (5%) लगाएं",
                "गांठ वाले पौधों के हिस्सों को हटाकर नष्ट करें",
                "गंभीर संक्रमण में इमिडाक्लोप्रिड (0.005%) का छिड़काव करें",
                "पेड़ के आधार के चारों ओर क्लोरपाइरीफॉस से मिट्टी उपचार करें"
            ],
            "prevention": [
                "नई पत्तियों के समय पेड़ों की निगरानी करें",
                "प्राकृतिक शिकारियों को प्रोत्साहित करें",
                "प्रभावित शाखाओं की समय पर छंटाई"
            ]
        }
    },
    "Powdery Mildew": {
        "severity": "Critical",
        "en": {
            "name": "Powdery Mildew",
            "description": "Critical fungal disease for Dasheri mangoes in Malihabad. White powdery coating on flowers and young fruits. Thrives in 11°C–31°C with 64%–72% humidity during Feb-March flowering.",
            "symptoms": [
                "White powdery growth on panicles and flowers",
                "Flower drop and poor fruit set",
                "Whitish coating on young fruits",
                "Premature fruit drop",
                "Affects 60-80% flowers in severe cases"
            ],
            "treatment": [
                "Spray Wettable Sulphur (0.2%) at panicle emergence",
                "Apply Hexaconazole (0.05%) or Triadimefon (0.1%)",
                "Spray Karathane (0.05%) at 15-day intervals",
                "Dust flowers with fine Sulphur (300 mesh) in morning",
                "Second spray 15 days after first application"
            ],
            "prevention": [
                "Monitor weather: Risk HIGH when temp 11°C-31°C + humidity 64-72%",
                "Pre-emptive spray before flowering season (early February)",
                "Avoid excessive nitrogen fertilization",
                "Ensure good air circulation through proper pruning"
            ]
        },
        "hi": {
            "name": "पाउडरी मिल्ड्यू (छाछ्या रोग)",
            "description": "मलिहाबाद में दशहरी आम के लिए सबसे खतरनाक फफूंद रोग। फूलों और नए फलों पर सफेद चूर्णी परत। फरवरी-मार्च में 11°C-31°C तापमान और 64%-72% नमी में पनपता है।",
            "symptoms": [
                "बौर और फूलों पर सफेद चूर्णी वृद्धि",
                "फूल झड़ना और फल न लगना",
                "नए फलों पर सफेद परत",
                "फलों का समय से पहले गिरना",
                "गंभीर मामलों में 60-80% फूल प्रभावित"
            ],
            "treatment": [
                "बौर निकलते ही घुलनशील गंधक (0.2%) का छिड़काव करें",
                "हेक्साकोनाज़ोल (0.05%) या ट्राइडिमेफॉन (0.1%) लगाएं",
                "15 दिन के अंतराल पर कैराथेन (0.05%) का छिड़काव",
                "सुबह में बारीक गंधक (300 मेश) का फूलों पर भुरकाव करें",
                "पहले छिड़काव के 15 दिन बाद दूसरा छिड़काव करें"
            ],
            "prevention": [
                "मौसम पर नज़र: तापमान 11°C-31°C + नमी 64-72% पर खतरा ज़्यादा",
                "फूल आने से पहले (फरवरी की शुरुआत में) रोकथाम का छिड़काव",
                "अधिक नाइट्रोजन खाद से बचें",
                "उचित छंटाई से अच्छा हवा का प्रवाह सुनिश्चित करें"
            ]
        }
    },
    "Sooty Mould": {
        "severity": "Medium",
        "en": {
            "name": "Sooty Mould",
            "description": "Black sooty coating on leaf surfaces caused by fungi growing on honeydew secreted by sap-sucking insects.",
            "symptoms": [
                "Black, sooty coating on leaves and fruits",
                "Reduced photosynthesis",
                "Presence of mealy bugs or scale insects",
                "Sticky honeydew on leaves"
            ],
            "treatment": [
                "Control sap-sucking insects first (Mealy bugs, Scale insects)",
                "Spray Monocrotophos (0.05%) or Dimethoate (0.05%)",
                "Wash leaves with Starch solution (5%) to remove mould",
                "Apply Neem oil (2%) + any wetting agent",
                "Spray Kerr Oil as a physical barrier"
            ],
            "prevention": [
                "Regular monitoring for sap-sucking insects",
                "Maintain tree hygiene",
                "Ant management (ants protect sap-suckers)"
            ]
        },
        "hi": {
            "name": "सूटी मोल्ड (कालिख)",
            "description": "पत्तियों की सतह पर काली कालिख जैसी परत, जो रस चूसने वाले कीड़ों के मधुरस (हनीड्यू) पर फफूंद बढ़ने से होती है।",
            "symptoms": [
                "पत्तियों और फलों पर काली, कालिख जैसी परत",
                "प्रकाश संश्लेषण में कमी",
                "मिलीबग या शल्ककीट की उपस्थिति",
                "पत्तियों पर चिपचिपा मधुरस"
            ],
            "treatment": [
                "पहले रस चूसने वाले कीड़ों (मिलीबग, शल्ककीट) को नियंत्रित करें",
                "मोनोक्रोटोफॉस (0.05%) या डाइमेथोएट (0.05%) का छिड़काव करें",
                "फफूंद हटाने के लिए स्टार्च घोल (5%) से पत्तियां धोएं",
                "नीम तेल (2%) + किसी भी गीला करने वाले एजेंट का प्रयोग",
                "भौतिक अवरोध के रूप में कैर ऑयल का छिड़काव"
            ],
            "prevention": [
                "रस चूसने वाले कीड़ों की नियमित निगरानी",
                "पेड़ की स्वच्छता बनाए रखें",
                "चींटी प्रबंधन (चींटियां रस चूसने वालों की रक्षा करती हैं)"
            ]
        }
    },
    "Healthy": {
        "severity": "None",
        "en": {
            "name": "Healthy",
            "description": "The mango leaf appears healthy with no visible signs of disease or pest damage.",
            "symptoms": [],
            "treatment": [
                "No treatment required — your Dasheri mango is healthy!",
                "Continue regular care: watering, fertilization, and pruning",
                "Monitor regularly for early disease detection"
            ],
            "prevention": [
                "Regular monitoring every 2 weeks",
                "Balanced NPK fertilization",
                "Proper irrigation management",
                "Annual pruning after harvest"
            ]
        },
        "hi": {
            "name": "स्वस्थ",
            "description": "आम की पत्ती स्वस्थ दिखाई देती है, रोग या कीट क्षति का कोई लक्षण नहीं।",
            "symptoms": [],
            "treatment": [
                "कोई उपचार आवश्यक नहीं — आपका दशहरी आम स्वस्थ है!",
                "नियमित देखभाल जारी रखें: सिंचाई, खाद, और छंटाई",
                "शुरुआती रोग पहचान के लिए नियमित निगरानी करें"
            ],
            "prevention": [
                "हर 2 सप्ताह में नियमित निगरानी",
                "संतुलित NPK उर्वरक",
                "उचित सिंचाई प्रबंधन",
                "फसल कटाई के बाद वार्षिक छंटाई"
            ]
        }
    }
}


def get_treatment(disease_name: str, language: str = "en") -> dict:
    """Get treatment info for a disease in the specified language."""
    disease_data = TREATMENTS.get(disease_name, TREATMENTS["Healthy"])
    lang_data = disease_data.get(language, disease_data.get("en"))
    return {
        "disease": lang_data["name"],
        "severity": disease_data["severity"],
        "description": lang_data["description"],
        "symptoms": lang_data.get("symptoms", []),
        "treatment": lang_data["treatment"],
        "prevention": lang_data.get("prevention", [])
    }


def get_all_diseases() -> list:
    """Return list of all disease classes."""
    return list(TREATMENTS.keys())
