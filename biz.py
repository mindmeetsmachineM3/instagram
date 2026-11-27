"""One automation-idea video per business type (original text). Each: n=Marathi name, en=big label, kw=comment keyword,
pain=problem line, a=3 automations (icon, Marathi title, short sub), flow=3 node labels, q=question for comments, tags=business hashtags."""
from scripts import BRAND

B = [
 dict(id="hotel", n="हॉटेल किंवा रेस्टॉरंट", en="HOTEL", kw="HOTEL", pain="फोनवर टेबल बुकिंग, मेन्यूचे प्रश्न आणि रिव्ह्यू, यातच **स्टाफचा** वेळ जातो.",
      a=[("cal", "टेबल बुकिंग", "DM मधूनच बुक"), ("chat", "मेन्यू व वेळ", "आपोआप उत्तर"), ("star", "रिव्ह्यू रिक्वेस्ट", "जेवणानंतर मेसेज")],
      flow=["ग्राहक मेसेज", "ऑटो उत्तर", "बुकिंग तुमच्याकडे"], q="तुमच्या हॉटेलमध्ये सगळ्यात जास्त कोणता प्रश्न विचारला जातो?",
      tags="#hotelmarketing #restaurantmarketing #restaurantowner #foodbusiness #hotelindustry #tablebooking #zomato #restaurantindia"),
 dict(id="clinic", n="क्लिनिक किंवा डॉक्टर", en="CLINIC", kw="CLINIC", pain="अपॉइंटमेंट कॉल, वेळा बदलणं आणि विसरलेले पेशंट, यामुळे **रिसेप्शन** थकतं.",
      a=[("cal", "अपॉइंटमेंट बुकिंग", "वेळ निवडा"), ("bolt", "रिमाइंडर", "आदल्या दिवशी मेसेज"), ("chat", "सामान्य प्रश्न", "वेळ, फी, पत्ता")],
      flow=["पेशंट मेसेज", "वेळ निवड", "रिमाइंडर"], q="तुमच्या क्लिनिकमध्ये सगळ्यात जास्त वेळ कशात जातो?",
      tags="#clinicmarketing #doctorsofinstagram #healthcaremarketing #patientcare #appointment #dentalclinic #clinicindia #doctormarketing"),
 dict(id="salon", n="सलून किंवा ब्युटी पार्लर", en="SALON", kw="SALON", pain="रोज सेवा आणि दर विचारणारे मेसेज येतात, आणि काम करता करता **उत्तर** राहून जातं.",
      a=[("chat", "दरपत्रक उत्तर", "सेवा आणि किंमत"), ("cal", "स्लॉट बुकिंग", "रिकामी वेळ"), ("heart", "रिपीट ऑफर", "महिन्यानंतर मेसेज")],
      flow=["ग्राहक मेसेज", "दर व स्लॉट", "बुकिंग पक्कं"], q="तुमच्या पार्लरची सगळ्यात जास्त चालणारी सेवा कोणती?",
      tags="#salonmarketing #beautyparlour #salonowner #bridalmakeup #hairstylist #beautybusiness #parlourindia #salonbooking"),
 dict(id="gym", n="जिम किंवा फिटनेस सेंटर", en="GYM", kw="GYM", pain="नवे चौकशी करणारे येतात, पण फॉलो-अप नसल्यामुळे **मेंबर** होत नाहीत.",
      a=[("target", "लीड फॉलो-अप", "चौकशीनंतर मेसेज"), ("bolt", "रिन्यूअल रिमाइंडर", "मुदत संपण्यापूर्वी"), ("star", "ट्रान्सफॉर्मेशन पोस्ट", "नियमित कंटेंट")],
      flow=["चौकशी", "फॉलो-अप", "मेंबरशिप"], q="तुमच्या जिममध्ये मेंबर कशामुळे थांबतात?",
      tags="#gymmarketing #fitnessbusiness #gymowner #fitnessindia #personaltrainer #gymmembership #fitnesscoach #gymlife"),
 dict(id="coaching", n="कोचिंग क्लास", en="COACHING", kw="CLASS", pain="बॅच, फी आणि टाइमटेबलचे प्रश्न सतत येतात, आणि **पालकांना** उत्तर द्यायला वेळ पुरत नाही.",
      a=[("chat", "बॅच माहिती", "वेळ, फी, पत्ता"), ("bolt", "फी रिमाइंडर", "ठरलेल्या तारखेला"), ("play", "रिझल्ट कंटेंट", "नियमित पोस्ट")],
      flow=["पालकांचा मेसेज", "माहिती आपोआप", "प्रवेश"], q="तुमच्या क्लासमध्ये प्रवेशाआधी पालक काय विचारतात?",
      tags="#coachingclass #educationmarketing #tutionclass #teachersofinstagram #admissionopen #studentsindia #classesmarketing #onlinecoaching"),
 dict(id="kirana", n="किराणा किंवा सुपरमार्केट", en="KIRANA", kw="SHOP", pain="ऑर्डर फोनवर आणि चिठ्ठीवर येतात, आणि **चुका** होतात.",
      a=[("menu", "ऑर्डर लिस्ट", "मेसेजमधून ऑर्डर"), ("star", "ऑफर ब्रॉडकास्ट", "आठवड्याची ऑफर"), ("pin", "डिलिव्हरी माहिती", "एरिया व वेळ")],
      flow=["ऑर्डर मेसेज", "लिस्ट तयार", "डिलिव्हरी"], q="तुमच्याकडे सगळ्यात जास्त कोणत्या वस्तूंची ऑर्डर येते?",
      tags="#kiranastore #supermarket #localbusiness #grocerystore #homedelivery #retailbusiness #smallshop #kiranaindia"),
 dict(id="clothes", n="कपड्यांचं दुकान", en="BOUTIQUE", kw="STYLE", pain="रोज नवीन स्टॉक येतो, पण त्याचे **फोटो** टाकायला आणि दर सांगायला वेळ मिळत नाही.",
      a=[("play", "नवीन स्टॉक रील", "आठवड्याला ठरलेली"), ("chat", "साइज व दर उत्तर", "DM मध्ये लगेच"), ("heart", "सेल ऑफर", "सणांना आगाऊ")],
      flow=["स्टॉक फोटो", "रील तयार", "ऑर्डर DM"], q="तुमच्याकडे कोणता कपड्यांचा प्रकार सगळ्यात जास्त विकला जातो?",
      tags="#boutique #clothingbusiness #fashionbrand #sareelove #ethnicwear #boutiqueowner #fashionindia #smallbusinessindia"),
 dict(id="realestate", n="रिअल इस्टेट एजंट", en="PROPERTY", kw="PLOT", pain="चौकशी खूप येते, पण **गंभीर** ग्राहक कोण हे ओळखायला वेळ लागतो.",
      a=[("target", "लीड फिल्टर", "बजेट आणि एरिया"), ("play", "प्रॉपर्टी टूर रील", "नियमित पोस्ट"), ("cal", "साइट व्हिजिट बुकिंग", "वेळ निवडा")],
      flow=["चौकशी", "बजेट प्रश्न", "साइट व्हिजिट"], q="तुमचा सगळ्यात जास्त चौकशी येणारा एरिया कोणता?",
      tags="#realestate #propertyindia #realestateagent #plotsforsale #homebuyers #propertymarketing #realtor #kolhapur"),
 dict(id="photographer", n="फोटोग्राफर", en="PHOTO", kw="PHOTO", pain="पॅकेज, तारखा आणि दर विचारणारे मेसेज येतात, आणि **बुकिंग** हातातून जातं.",
      a=[("chat", "पॅकेज माहिती", "दर आणि सेवा"), ("cal", "तारीख तपासणी", "रिकामी तारीख"), ("star", "पोर्टफोलिओ पोस्ट", "नियमित कंटेंट")],
      flow=["चौकशी", "पॅकेज व तारीख", "बुकिंग"], q="तुमचं सगळ्यात आवडतं शूट कोणतं होतं?",
      tags="#photographer #weddingphotography #photographybusiness #preweddingshoot #candidphotography #photographerindia #photoshoot #eventphotography"),
 dict(id="medical", n="मेडिकल स्टोअर", en="PHARMACY", kw="MEDICAL", pain="औषधं आहेत का, हे विचारायला फोन येतात, आणि **गर्दीत** उत्तर देणं अवघड होतं.",
      a=[("chat", "उपलब्धता उत्तर", "आहे किंवा नाही"), ("bolt", "रिफिल रिमाइंडर", "ठरलेल्या औषधांसाठी"), ("pin", "होम डिलिव्हरी", "एरिया व वेळ")],
      flow=["औषधाची चौकशी", "उत्तर", "डिलिव्हरी"], q="तुमच्याकडे सगळ्यात जास्त कोणती चौकशी येते?",
      tags="#medicalstore #pharmacy #pharmacyindia #healthcare #localbusiness #homedelivery #medicalshop #pharmacist"),
 dict(id="bakery", n="बेकरी किंवा केक शॉप", en="BAKERY", kw="CAKE", pain="केकच्या ऑर्डर, फ्लेवर आणि वजन, हे सगळं **DM** मध्ये विखुरलेलं असतं.",
      a=[("menu", "ऑर्डर फॉर्म", "फ्लेवर, वजन, तारीख"), ("chat", "दर उत्तर", "किलोप्रमाणे"), ("play", "केक रील", "रोज नवीन")],
      flow=["ऑर्डर DM", "फॉर्म भरतो", "ऑर्डर पक्की"], q="तुमचा सगळ्यात जास्त मागणीचा केक कोणता?",
      tags="#bakery #cakeshop #homebaker #customcakes #birthdaycake #cakeorder #bakeryindia #cakesofinstagram"),
 dict(id="travel", n="ट्रॅव्हल एजन्सी", en="TRAVEL", kw="TRIP", pain="सहलीचे दर आणि तारखा विचारणाऱ्या चौकशी खूप, पण **फॉलो-अप** राहतो.",
      a=[("chat", "पॅकेज माहिती", "तारीख आणि दर"), ("target", "लीड फॉलो-अप", "दोन दिवसांनी मेसेज"), ("play", "डेस्टिनेशन रील", "नियमित पोस्ट")],
      flow=["चौकशी", "पॅकेज", "बुकिंग"], q="तुमचं सगळ्यात आवडतं डेस्टिनेशन कोणतं?",
      tags="#travelagency #tourpackages #traveltips #tourismindia #holidaypackages #traveldeals #tripplanner #travelagent"),
 dict(id="garage", n="गॅरेज किंवा कार वॉश", en="GARAGE", kw="CAR", pain="सर्व्हिसची वेळ, दर आणि गाडी तयार झाल्याची माहिती देण्यातच **वेळ** जातो.",
      a=[("cal", "सर्व्हिस बुकिंग", "वेळ निवडा"), ("bolt", "गाडी तयार मेसेज", "आपोआप सूचना"), ("star", "पुढच्या सर्व्हिसची आठवण", "ठरल्या कालावधीनंतर")],
      flow=["बुकिंग", "सर्व्हिस", "तयार सूचना"], q="तुमच्याकडे सगळ्यात जास्त कोणती सर्व्हिस होते?",
      tags="#garage #carwash #carservice #autorepair #carcare #detailing #vehicleservice #garageindia"),
 dict(id="jewellery", n="ज्वेलरी शॉप", en="JEWELLERY", kw="GOLD", pain="नवीन डिझाइन दाखवायला आणि चौकशीला उत्तर द्यायला **वेळ** कमी पडतो.",
      a=[("play", "नवीन डिझाइन रील", "आठवड्याला"), ("chat", "चौकशी उत्तर", "डिझाइन आणि दुकानाची वेळ"), ("star", "सणाची ऑफर", "आगाऊ आठवण")],
      flow=["डिझाइन रील", "चौकशी", "दुकानात भेट"], q="तुमचं सगळ्यात जास्त पसंत होणारं डिझाइन कोणतं?",
      tags="#jewellery #jewelleryshop #goldjewellery #jewellerydesign #bridaljewellery #sarafa #jewelleryindia #festivaloffer"),
 dict(id="agri", n="शेतमाल विक्रेता", en="FARM", kw="FARM", pain="ग्राहक थेट शेतातून माल मागतात, पण **दर** आणि उपलब्धता सांगायला वेळ मिळत नाही.",
      a=[("bars", "आजचे दर", "आपोआप अपडेट"), ("chat", "ऑर्डर घेणं", "प्रमाण आणि पत्ता"), ("play", "शेतातला व्हिडिओ", "विश्वास वाढवतो")],
      flow=["ग्राहक चौकशी", "दर व उपलब्धता", "ऑर्डर"], q="तुम्ही कोणता शेतमाल विकता?",
      tags="#farmtotable #organicfarming #farmersofinstagram #freshproduce #maharashtrafarmer #agribusiness #directfromfarm #shetkari"),
 dict(id="event", n="इव्हेंट प्लॅनर", en="EVENTS", kw="EVENT", pain="लग्न आणि कार्यक्रमांच्या चौकशी खूप, पण **बजेट** आणि तारीख समजेपर्यंत वेळ जातो.",
      a=[("target", "बजेट प्रश्न", "आपोआप विचारतो"), ("cal", "तारीख तपासणी", "रिकामी तारीख"), ("play", "इव्हेंट रील", "नियमित पोस्ट")],
      flow=["चौकशी", "बजेट व तारीख", "मीटिंग"], q="तुमचा सगळ्यात आठवणीतला इव्हेंट कोणता होता?",
      tags="#eventplanner #weddingplanner #eventmanagement #decorators #weddingindia #eventplanning #partyplanner #eventindia"),
 dict(id="mobile", n="मोबाइल शॉप", en="MOBILE", kw="MOBILE", pain="मॉडेल, दर आणि ऑफर विचारणारे मेसेज खूप, आणि **ग्राहक** दुसरीकडे जातात.",
      a=[("chat", "मॉडेल व दर उत्तर", "लगेच"), ("star", "ऑफर पोस्ट", "सणांना"), ("bolt", "रिपेअर अपडेट", "तयार असल्याचा मेसेज")],
      flow=["मॉडेलची चौकशी", "दर व ऑफर", "दुकानात भेट"], q="तुमच्याकडे सगळ्यात जास्त कोणता मोबाइल विकला जातो?",
      tags="#mobileshop #mobileaccessories #smartphone #mobilerepair #retailindia #mobilestore #localshop #phonedeals"),
]


def make_video(b):
    a = b["a"]
    say = [
        f"{b['n']} चालवता? मग हे **ऑटोमेशन** तुमच्यासाठी आहे.",
        b["pain"],
        f"तीन गोष्टी ऑटोमॅटिक करा: **{a[0][1]}**, **{a[1][1]}** आणि **{a[2][1]}**.",
        f"ग्राहकाचा मेसेज येतो, सिस्टीम आपोआप **उत्तर** देते, आणि तुम्हाला फक्त खरी **ऑर्डर** दिसते.",
        f"तुमचा बिझनेस कोणता आहे? कमेंटमध्ये **{b['kw']}** लिहा आणि हा व्हिडिओ **सेव्ह** करा.",
        f"असं ऑटोमेशन हवं असेल तर **{BRAND}** ला मेसेज करा.",
    ]
    sc = [
        {"say": say[0], "vis": "hook", "big": [b["en"], "AUTOMATION"]},
        {"say": say[1], "vis": "pain", "label": b["en"], "line": b["pain"].replace("**", "")},
        {"say": say[2], "vis": "cards", "items": [[x[0], x[1], x[2]] for x in a]},
        {"say": say[3], "vis": "flow", "nodes": b["flow"]},
        {"say": say[4], "vis": "engage", "kw": b["kw"]},
        {"say": say[5], "vis": "brand"},
    ]
    cap = (f"{b['n']} साठी ऑटोमेशन आयडिया 👇\n\n" + "\n".join(f"✅ {x[1]}: {x[2]}" for x in a) +
           f"\n\n💬 {b['q']}\nकमेंटमध्ये सांगा, आणि तुमचा बिझनेस {b['kw']} लिहा, पुढचा व्हिडिओ त्यावर बनवू!\n"
           f"🔖 सेव्ह करा  |  📤 मित्राला शेअर करा\n\n{BRAND} ला मेसेज करा.")
    tags = b["tags"] + " #instaautomationai #automation #instagramautomation #marathi"
    return {"id": "biz_" + b["id"], "title": b["n"], "tag": b["en"] + " AUTOMATION", "scenes": sc, "caption": cap, "tags": tags}


BIZ_VIDEOS = [make_video(b) for b in B]
