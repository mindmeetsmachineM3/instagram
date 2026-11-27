"""Original Marathi scripts. **word** = highlighted in cyan. vis = scene graphic key (see scenes.py)."""
BRAND = "Insta Automation AI"

VIDEOS = [
 {"id": "v1_profile_makeover", "title": "प्रोफाइल मेकओव्हर", "tag": "PROFILE MAKEOVER", "scenes": [
   {"say": "तुमचं Instagram प्रोफाइल लोकांना **खरेदी** करायला लावतं, की फक्त बघून **निघून** जायला?", "vis": "hook", "big": ["PROFILE", "MAKEOVER"]},
   {"say": "बहुतेक बिझनेसचं प्रोफाइल म्हणजे **रँडम** फोटो, अर्धवट बायो आणि कुठलीच दिशा नाही.", "vis": "phone", "style": "random", "label": "BEFORE"},
   {"say": "आधी **नाव, फोटो आणि बायो** नीट करा. तुम्ही काय करता आणि कुणासाठी, हे एका नजरेत कळायला हवं.", "vis": "phone", "style": "clean", "label": "STEP 1 · BIO", "reveal": [0.2, 1.2, 99, 99, 99]},
   {"say": "**हायलाइट्स** मध्ये ऑफर, रिव्ह्यू, सेवा आणि लोकेशन ठेवा, म्हणजे ग्राहकाला प्रश्न विचारावेच लागत नाहीत.", "vis": "phone", "style": "clean", "label": "STEP 2 · HIGHLIGHTS", "reveal": [-9, -9, 0.4, 99, 99]},
   {"say": "पोस्टचा **ग्रिड** एका थीममध्ये ठेवा. रंग, फॉन्ट आणि विषय सारखे असले की प्रोफाइल प्रोफेशनल दिसतं.", "vis": "phone", "style": "clean", "label": "STEP 3 · GRID", "reveal": [-9, -9, -9, 0.4, 1.6]},
   {"say": "असं प्रोफाइल **विश्वास** निर्माण करतं, आणि विश्वासातूनच मेसेज आणि ऑर्डर येतात.", "vis": "cards", "items": [["eye", "Notice", "first look"], ["heart", "Trust", "clear & neat"], ["chat", "Message", "enquiry"]]},
   {"say": "असं सेटअप तुमच्यासाठी बनवून हवं असेल तर **Insta Automation AI** ला मेसेज करा.", "vis": "brand"}],
  "caption": "तुमचं Instagram प्रोफाइल लोकांना खरेदी करायला लावतं का?\n\n✅ नाव, फोटो आणि बायो स्पष्ट\n✅ हायलाइट्समध्ये ऑफर, रिव्ह्यू, लोकेशन\n✅ एका थीमचा ग्रिड\n\nअसं सेटअप हवं असेल तर Insta Automation AI ला मेसेज करा.",
  "tags": "#instagrammarketing #instagramtips #marathi #smallbusiness #socialmediamarketing #profileoptimization #instaautomationai"},

 {"id": "v2_random_vs_clean", "title": "रँडम की क्लीन प्रोफाइल", "tag": "RANDOM vs CLEAN", "scenes": [
   {"say": "हे दोन प्रोफाइल बघा. तुम्ही कुठे **क्लिक** कराल, आणि कुणाकडून **खरेदी** कराल?", "vis": "compare"},
   {"say": "डावीकडचं **रँडम** आहे. आज ऑफर, उद्या मीम, परवा काहीच नाही.", "vis": "phone", "style": "random", "label": "RANDOM", "full": True},
   {"say": "उजवीकडचं **क्लीन** आहे. ठरलेले रंग, ठरलेले विषय आणि स्पष्ट ऑफर.", "vis": "phone", "style": "clean", "label": "CLEAN", "full": True},
   {"say": "ग्राहक तीन गोष्टी बघतात: ऑफर स्पष्ट आहे का, सगळं एकसारखं दिसतं का, आणि **संपर्क** करणं सोपं आहे का.", "vis": "checks", "items": [["star", "Clear offer"], ["eye", "Same look"], ["chat", "Easy contact"]]},
   {"say": "रँडम पोस्टिंगमुळे ग्राहक आणि अल्गोरिदम दोघेही **गोंधळतात**, पण ठरलेल्या पद्धतीमुळे नजर टिकते.", "vis": "bars", "labels": ["Random", "Planned"], "vals": [0.3, 0.78], "note": "ILLUSTRATIVE"},
   {"say": "तुमचं प्रोफाइल **क्लीन** करायचं असेल तर **Insta Automation AI** ला मेसेज करा.", "vis": "brand"}],
  "caption": "रँडम प्रोफाइल की क्लीन प्रोफाइल?\n\nठरलेले रंग, ठरलेले विषय आणि स्पष्ट ऑफर असलेलं प्रोफाइल ग्राहकाचा विश्वास जिंकतं.\n\nप्रोफाइल सुधारायचं असेल तर Insta Automation AI ला मेसेज करा.",
  "tags": "#instagramgrowth #contentstrategy #marathi #smallbusinessindia #branding #instagramtips #instaautomationai"},

 {"id": "v3_one_video_clients", "title": "एक व्हिडिओ, नवे ग्राहक", "tag": "1 VIDEO TO CLIENTS", "scenes": [
   {"say": "एकच **व्हिडिओ** आणि त्यातून नवे **ग्राहक**. शक्य आहे, पण योग्य पद्धतीने केला तर.", "vis": "hook", "big": ["1 VIDEO", "= CLIENTS"]},
   {"say": "व्हिडिओमध्ये तुमच्या ग्राहकाची **समस्या**, तिचं सोपं उत्तर आणि तुमचा **पुरावा** असावा.", "vis": "cards", "items": [["target", "Problem", "customer's pain"], ["bolt", "Answer", "simple fix"], ["star", "Proof", "your work"]]},
   {"say": "शेवटी एकच स्पष्ट **कृती** सांगा: मेसेज करा, कॉल करा किंवा बुक करा.", "vis": "cta_phone"},
   {"say": "तोच व्हिडिओ **रील, स्टोरी आणि पोस्ट** म्हणून पुन्हा वापरा, म्हणजे एकाच कष्टात जास्त लोकांपर्यंत पोहोचता.", "vis": "cards", "items": [["play", "Reel", "main"], ["user", "Story", "reminder"], ["bars", "Post", "carousel"]]},
   {"say": "रिच, मेसेज आणि ग्राहक असा प्रवास असतो. हा फक्त **उदाहरण** आहे, निकाल बिझनेसनुसार वेगळे असतात.", "vis": "bars", "labels": ["Views", "Messages", "Clients"], "vals": [1.0, 0.42, 0.14], "note": "ILLUSTRATIVE EXAMPLE"},
   {"say": "तुमच्यासाठी असे व्हिडिओ बनवून हवेत? **Insta Automation AI** ला मेसेज करा.", "vis": "brand"}],
  "caption": "एकच व्हिडिओ आणि नवे ग्राहक!\n\n1️⃣ समस्या  2️⃣ उत्तर  3️⃣ पुरावा  4️⃣ एकच स्पष्ट कृती\n\nतोच व्हिडिओ रील, स्टोरी आणि पोस्ट म्हणून वापरा.\n(आकडे फक्त उदाहरण आहेत; निकाल बिझनेसनुसार बदलतात.)\n\nInsta Automation AI ला मेसेज करा.",
  "tags": "#reelsmarketing #videomarketing #instagramreels #marathi #leadgeneration #smallbusiness #instaautomationai"},

 {"id": "v4_smart_system", "title": "स्मार्ट ऑटोमॅटिक सिस्टीम", "tag": "SMART SYSTEM", "scenes": [
   {"say": "रोज पोस्ट करायला **वेळ** नाही? मग हे काम **सिस्टीम** ला द्या.", "vis": "toggle"},
   {"say": "प्लॅन, तयार करणे आणि अ‍ॅनालिसिस. हे **चक्र** आपोआप फिरत राहतं.", "vis": "loop"},
   {"say": "कंटेंट कॅलेंडर, कॅप्शन आणि हॅशटॅग, तसंच वेळेवर **पोस्टिंग**. सगळं ठरल्याप्रमाणे होतं.", "vis": "checks", "items": [["cal", "Content calendar"], ["chat", "Captions & hashtags"], ["bolt", "Timely posting"]]},
   {"say": "तुम्ही फक्त **मंजुरी** द्या, बाकी काम सिस्टीम सांभाळते.", "vis": "ring", "label": "APPROVE"},
   {"say": "काय चाललंय हे **रिपोर्ट** मधून दिसतं, म्हणजे पुढचा निर्णय आकड्यांवर घेता येतो.", "vis": "bars", "labels": ["W1", "W2", "W3", "W4"], "vals": [0.35, 0.5, 0.62, 0.8], "note": "SAMPLE REPORT"},
   {"say": "अशी स्मार्ट सिस्टीम हवी असेल तर **Insta Automation AI** ला मेसेज करा.", "vis": "brand"}],
  "caption": "रोज पोस्ट करायला वेळ नाही?\n\nप्लॅन → तयार → अ‍ॅनालिसिस, हे चक्र सिस्टीम सांभाळते. तुम्ही फक्त मंजुरी द्या.\n\nInsta Automation AI ला मेसेज करा.",
  "tags": "#instagramautomation #automation #socialmediamanagement #marathi #aitools #smallbusiness #instaautomationai"},
]
