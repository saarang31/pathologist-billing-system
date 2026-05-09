import tkinter
import tkinter.ttk
import tkinter.messagebox
import sqlite3
import datetime
import pandas as pd
from tkinter import filedialog
import os
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# Billing Code Dictionary as provided by Dr. Matthew Cesari
code_dict = {
 'AA100': [18, "Brain and/or spinal cord - Neurodegenerative BRAIN ONLY"],
 'AA110': [24, "Brain and/or spinal cord - Neurodegenerative BRAIN and SPINAL CORD"],
 'AA120': [18, "Brain and/or spinal cord - Non-neurodegenerative BRAIN ONLY"],
 'AA130': [24, "Brain and/or spinal cord - Non-neurodegenerative BRAIN and SPINAL CORD"],
 'AA140': [6, "Brain and/or spinal cord - Non-neurodegenerative REMOVAL ONLY"],
 'AA150': [36, "Full non-complex autopsy - ADULT"],
 'AA160': [48, "Complex medico-legal autopsy - ADULT"],
 'AA170': [48, "Complex hospital autopsy - ADULT"],
 'AA180': [12, "External examination only - ADULT"],
 'AA190': [18, "Partial autopsy - ADULT"],
 'AA200': [24, "Limited autopsy - ADULT"],
 'PA150': [36, "Full non-complex autopsy - PEDIATRIC or FETAL"],
 'PA160': [48, "Complex medico-legal autopsy - PEDIATRIC or FETAL"],
 'PA170': [48, "Complex hospital autopsy - PEDIATRIC or FETAL"],
 'PA180': [2, "External examination only - PEDIATRIC or FETAL"],
 'PA190': [18, "Partial autopsy - PEDIATRIC or FETAL"],
 'PA200': [24, "Limited autopsy - PEDIATRIC or FETAL"],
 'BR100': [0.125, "Implant capsules - GROSS ONLY"],
 'BR110': [0.5, "Implant capsules - GROSS and MICRO"],
 'BR120': [0.25, "Mastectomies or lumpectomies alone - BENIGN"],
 'BR130': [0.25, "Mastectomies or lumpectomies alone - (PRE-)MALIGNANT"],
 'BR140': [0.25, "Mastectomy partial/full/lumpectomy + nodal dissection"],
 'BR150A': [1, "Needle core or mammatome biopsy - BENIGN"],
 'BR150B': [0.25, "Needle core or mammatome biopsy - BENIGN"],
 'BR160A': [1, "Needle core or mammatome biopsy - (PRE-)MALIGNANT"],
 'BR160B': [0.25, "Needle core or mammatome biopsy - (PRE-)MALIGNANT"],
 'BR170': [0.25, "Reduction Mammoplasty, Gynecomastia - BENIGN"],
 'BR180': [0.25, "Reduction Mammoplasty, Gynecomastia - (PRE-)MALIGNANT"],
 'CV100': [0.125, "Aneurysm contents, thrombus, hematoma, atheromatous plaque: GROSS ONLY"],
 'CV110': [0.25, "Aneurysm contents, thrombus, hematoma, atheromatous plaque: GROSS & MICRO"],
 'CV120': [1, "Artery - biopsy"],
 'CV130': [10, "Cardiac explant for coronary bypass"],
 'CV140': [5, "Cardiac explant not for coronary bypass"],
 'CV150': [0.25, "Cardiac resection for benign tumours"],
 'CV160': [5, "Cardiac resection for malignant tumours"],
 'CV170': [5, "Cardiac, myocardial biopsy for transplant, includes pediatrics"],
 'CV180': [5, "Cardiac, myocardial biopsy"],
 'CV190': [10, "Heart for conduction system"],
 'CV200': [0.125, "Heart valve: GROSS ONLY"],
 'CV210': [0.5, "Heart valve: GROSS & MICRO"],
 'CV230': [0.125, "Hematoma: GROSS ONLY"],
 'CV240': [0.25, "Hematoma: GROSS & MICRO"],
 'CV250': [1, "Pericardial biopsy"],
 'CV260': [0.25, "Ventricle heart, aneurysm, atrium partial resection"],
 'CV270': [0.125, "Vessels, vein - varicose veins: GROSS ONLY"],
 'CV280': [0.25, "Vessels, vein - varicose veins: GROSS & MICRO"],
 'CS100': [0.5, "Review of case and choosing the appropriate block/material for special studies as an insured clinical service"],
 'EC1': [1, "Send out of difficult case"],
 'QA100': [0.5, "Internal consults as per policy (e.g. mandatory prospective reviews)"],
 'QA110': [1, "Internal consults done at departmental rounds by multiple pathologists"],
 'QA120': [0.5, "Documented 'curbside' consults for a precise question (e.g.: is this extraprostatic extension or not?)"],
 'QA130': [1, "Internal consults for diagnostic difficulty (i.e.: what is the diagnosis?)"],
 'QA150': [1, "Review of previous material relevant to a current case"],
 'QA170': [1, "Preparation for clinical-pathological specialty rounds and tumour board rounds"],
 'QA180': [1, "Clinical-pathological speciality rounds and tumour board rounds"],
 'RDU': [1, "Urgent/Stat cases and critical diagnoses: RDU Cases"],
 'SEND': [0.125, "Routine transfer of cases (for the sending pathologist)"],
 'STAT': [1, "Urgent/Stat cases and critical diagnoses: Non RDU Cases"],
 'CY100': [3, "Bronchoalveolar washing with cell count"],
 'CY110': [3 , "FNA, doing the procedure"],
 'CY120': [3, "FNA, screening for adequacy: INITIAL ASSESSMENT BY CYTOPATHOLOGIST"],
 'CY125': [3, "FNA, screening for adequacy: INITIAL ASSESSMENT BY CYTOTECHNOLOGIST"],
 'CY130': [2, "FNA, screening for adequacy: ADDITIONAL REQUESTS BY CYTOPATHOLOGIST"],
 'CY135': [2, "FNA, screening for adequacy: ADDITIONAL REQUESTS BY CYTOTECHNOLOGIST"],
 'CY140': [2, "FNA, brushes and washes"],
 'CY150': [1, "Pap smears, urine and sputum, fluids"],
 'CY160': [0.125, "Automated molecular HPV testing and similar other tests"],
 'EM100': [5, "EM - also includes selection of the blocks, taking photos, reviewing the pictures and report"],
 'EM110': [2, "EM - selection of the blocks for EM, reviewing of pictures and issuing an integrated report"],
 'EN100': [0.25, "Adrenal resection: BENIGN"],
 'EN110': [0.25, "Adrenal resection: MALIGNANT"],
 'EN120': [1, "Parathyroid – biopsy: BENIGN"],
 'EN130': [0.25, "Parathyroid – biopsy: MALIGNANT"],
 'EN140': [1, "Pituitary biopsy/resection: BENIGN"],
 'EN150': [0.25, "Pituitary biopsy/resection: MALIGNANT"],
 'EN160': [0.25, "Thyroid - lobectomy or total thyroidectomy: BENIGN"],
 'EN170': [0.25, "Thyroid - lobectomy or total thyroidectomy: MALIGNANT"],
 'EN180': [0.25, "Thyroid - thyroidectomy with neck dissection, malignant"],
 'EY100': [0.5, "Conjunctiva - biopsy, benign, includes pterygium"],
 'EY110': [1, "Conjunctiva - biopsy, premalignant or malignant"],
 'EY120': [0.5, "Cornea - benign"],
 'EY130': [1, "Cornea, premalignant or malignant"],
 'EY140': [5, "Eye - enucleation, benign"],
 'EY150': [0.25, "Eye - enucleation, malignant"],
 'EY160': [0.25, "Eye - evisceration"],
 'EY170': [0.25, "Eye - exenteration"],
 'EY180': [1, "Orbit – biopsy: BENIGN"],
 'EY190': [1, "Orbit – biopsy: MALIGNANT"],
 'GI100': [0.25, "Endoscopic resection of lesions"],
 'GI110': [0.5, "Gallbladder, resection, benign"],
 'GI120': [0.25, "Gallbladder, malignant and premalignant"],
 'GI130': [0.5, "Gastrointestinal tract - fissure/fistula in ano"],
 'GI140': [0.5, "Gastrointestinal tract (esophagus to anus) - medical biopsies"],
 'GI150': [0.25, "Gastrointestinal tract (esophagus to anus) - resection with LN dissection, malignant"],
 'GI160': [0.25, "Gastrointestinal tract ( esophagus to anus) - resection, benign"],
 'GI170': [0.5, "Gastrointestinal tract (esophagus to rectum) - surgical biopsies (i.e. for polyps): DISCRETE LESION"],
 'GI180': [0.25, "Gastrointestinal tract (esophagus to rectum) - surgical biopsies (i.e. for polyps): LARGE POLYP (multi block resection)"],
 'GI190': [1, "Gastrointestinal tract (esophagus to anus) - surgical biopsies (i.e. for polyps): HIGH GRADE DYSPLASIA OR CARCINOMA"],
 'GI200': [0.5, "Gastrointestinal tract (esophagus to anus) - surgical biopsies (i.e. for polyps): ANUS"],
 'GI210': [0.125, "Hemorrhoids: GROSS ONLY"],
 'GI220': [0.25, "Hemorrhoids: GROSS & MICRO"],
 'GI230': [5, "Liver biopsy/wedge resection, for medical conditions, includes pretransplant and transplant"],
 'GI240': [1, "Liver for metastases or mass lesion: BIOPSY"],
 'GI250': [0.25, "Liver for metastases or mass lesion: WEDGE BIOPSY"],
 'GI260': [0.25, "Liver resection"],
 'GI270': [5, "Liver, explant"],
 'GI280': [1, "Pancreas - core biopsy"],
 'GI290': [0.25, "Pancreas - segmental or total resection, benign"],
 'GI300': [0.25, "Pancreas - segmental or total resection, malignant"],
 'GI310': [1, "Peritoneal biopsy"],
 'GI320': [0.5, "Pilonidal sinus/cyst"],
 'GI330': [0.25, "Stoma - enterostomy, ileostomy, colostomy, etc. and donuts"],
 'GI340': [0.25, "Vermiform appendix - incidental with no pathology"],
 'GI350': [0.25, "Vermiform appendix - neoplastic"],
 'GI360': [0.5, "Vermiform appendix - nonneoplastic"],
 'GY100': [0.5, "Bartholin's gland (abscess/cyst), paratubal cyst, peritoneum for endometriosis"],
 'GY110A': [1, "Cervix - biopsy or curetting: BENIGN"],
 'GY110B': [0.25, "Cervix - biopsy or curetting: BENIGN"],
 'GY120A': [1, "Cervix - biopsy or curetting: (PRE-) MALIGNANT"],
 'GY120B': [0.25, "Cervix - biopsy or curetting: (PRE-) MALIGNANT"],
 'GY130': [0.25, "Cervix - cone/LEEP biopsy: BENIGN"],
 'GY135': [0.25, "Cervix – trachelectomy: SIMPLE (e.g. completion hysterectomy)"],
 'GY140': [0.25, "Cervix - cone/LEEP biopsy: (PRE-) MALIGNANT"],
 'GY145': [0.25, "Cervix – trachelectomy: RADICAL (MALIGNANT)"],
 'GY150A': [1, "Endometrial biopsy/curetting: BENIGN"],
 'GY150B': [0.25, "Endometrial biopsy/curetting: BENIGN"],
 'GY160A': [1, "Endometrial biopsy/curetting: (PRE-) MALIGNANT"],
 'GY160B': [0.25, "Endometrial biopsy/curetting: (PRE-) MALIGNANT"],
 'GY170': [1, "Fallopian tube - biopsy"],
 'GY180': [0.25, "Fallopian tube resection, benign"],
 'GY190': [0.25, "Fallopian tubes - sterilization"],
 'GY200': [0.25, "Fallopian tubes or contents - ectopic pregnancy"],
 'GY210': [0.25, "Hysterectomy +/- adnexa – benign conditions"],
 'GY220': [0.25, "Hysterectomy +/- adnexa - malignant condition with or without nodes, with or without staging laparotomy:"],
 'GY230': [0.25, "Leiomyoma(s) – myomectomy"],
 'GY240': [0.25, "Molar pregnancy"],
 'GY250': [0.25, "Ovary with/without tubes, benign"],
 'GY290': [0.25, "Placenta, gross & micro"],
 'GY300': [0.25, "Products of conception, missed/spontaneous"],
 'GY310': [0.125, "Products of conception, therapeutic (family planning): GROSS ONLY"],
 'GY320': [0.5, "Products of conception, therapeutic (family planning): GROSS & MICRO"],
 'GY330': [0.25, "Ovary (with or without tube) OR fallopian tube tumour: BORDERLINE"],
 'GY340': [0.25, "Ovary (with or without tube) OR fallopian tube tumour: INTESTINAL MUCINOUS TUMOUR"],
 'GY350': [0.25, "Ovary (with or without tube) OR fallopian tube tumour: MALIGNANT"],
 'GY360': [0.25, "Vagina repair (plastic)"],
 'GY370': [0.25, "Vulva/vagina: MALIGNANT"],
 'GY380': [0.25, "Vulva/vagina: BENIGN or PRE-MALIGNANT"],
 'GY390': [1, "Vulva/vagina/perineal - biopsy"],
 'GY400': [0.25, "Pelvic Exenteration"],
 'HN100': [0.125, "Adenoids/tonsils: GROSS ONLY"],
 'HN110': [0.5, "Adenoids/tonsils: GROSS & MICRO"],
 'HN120': [0.25, "Adenoid/tonsils - malignant resection without nodes"],
 'HN130': [0.5, "Branchial cleft cyst"],
 'HN140': [0.5, "Cholesteatoma"],
 'HN150': [0.25, "ENT (laryngeal, trachea, tongue etc) - partial/ total resection with unilateral neck nodes dissection, malignant: Including neck dissection"],
 'HN160': [1, "Larynx - biopsy"],
 'HN170': [0.25, "Larynx - partial or total resection, non-malignant"],
 'HN180': [0.5, "Mucus retention cyst -salivary/oral"],
 'HN190': [0.5, "Nasal/sinonasal polyps - inflammatory or allergic"],
 'HN200': [0.125, "Nasal cartilage: GROSS ONLY"],
 'HN210': [0.25, "Nasal cartilage: GROSS & MICRO"],
 'HN220': [0.25, "Odontogenic tumour resection"],
 'HN230': [1, "Odontogenic/dental cyst"],
 'HN240': [1, "Oral, nasal sinus, nose, tongue & ENT, mucosal biopsy: BENIGN"],
 'HN250': [1, "Oral, nasal sinus, nose, tongue & ENT, mucosal biopsy: (PRE-)MALIGNANT"],
 'HN260A': [1, "Paranasal sinus - biopsy/curetting: BENIGN"],
 'HN260B': [0.25, "Paranasal sinus - biopsy/curetting: BENIGN"],
 'HN270A': [1, "Paranasal sinus - biopsy/curetting: (PRE-) MALIGNANT"],
 'HN270B': [0.25, "Paranasal sinus - biopsy/curetting: (PRE-) MALIGNANT"],
 'HN280': [1, "Pharynx – biopsy: BENIGN"],
 'HN290': [1, "Pharynx – biopsy: (PRE-)MALIGNANT"],
 'HN300': [1, "Salivary gland biopsy: BENIGN"],
 'HN310': [1, "Salivary gland biopsy: (PRE-)MALIGNANT"],
 'HN320': [0.25, "Salivary gland resection: BENIGN"],
 'HN330': [0.25, "Salivary gland resection: MALIGNANT"],
 'HN340': [0.125, "Teeth - gross only"],
 'HN350': [0.5, "Thyroglossal duct/cyst"],
 'HN360': [1, "Tongue biopsy: BENIGN"],
 'HN370': [1, "Tongue biopsy: (PRE-)MALIGNANT"],
 'HN380': [0.25, "Tongue resection: BENIGN"],
 'HN390': [0.25, "Tongue resection: (PRE-)MALIGNANT"],
 'HE100': [3, "Bone marrow, for metastasis, aspiration and biopsy"],
 'HE110': [2, "Bone marrow, for metastasis: BIOPSY"],
 'HE120': [1, "Bone marrow, for metastasis: ASPIRATION"],
 'HE130': [6, "Bone marrow, for hematolymphoid condition, biopsy and aspiration"],
 'HE140': [4, "Bone marrow, for hematolymphoid: BIOPSY"],
 'HE150': [2, "Bone marrow, for hematolymphoid: ASPIRATION"],
 'HE160': [3, "Bone marrow biopsy and/or aspiration - to perform the procedure"],
 'HE170': [1, "Peripheral blood smear"],
 'HE180': [5, "Extranodal lymphoma, biopsy: SKIN"],
 'HE190': [5, "Extranodal lymphoma, biopsy: NON-CUTANEOUS"],
 'HE200': [1, "Lymph node - non-hematological , core or excisional biopsy: BENIGN"],
 'HE210': [1, "Lymph node - non-hematological , core or excisional biopsy: METASTATIC"],
 'HE220': [5, "Lymph node - hematolymphoid neoplasm or atypical lymphoid proliferation, core or excisional biopsy"],
 'HE230': [5, "Surgical specimens (colectomy, Whipple, spleen etc.) – lymphoma"],
 'HE240': [0.25, "Mediastinal mass/tumour, resection"],
 'HE250': [0.5, "Spleen: TRAUMA"],
 'HE260': [0.25, "Spleen: UNDERLYING PATHOLOGY (NON-LYMPHOPROLIFERATIVE)"],
 'HE270': [5, "Spleen: LYMPHOPROLIFERATIVE"],
 'HE280': [0.25, "Thymus - tumour resection"],
 'FS1': [3, "First specimen - includes 1 frozen section/imprint cytology/scrape cytology/MOHs"],
 'FS2': [1, "If more than 1 frozen section/imprint cytology/scrape cytology"],
 'FS3': [2, "Additional specimen(s) after the first specimen, on the same case"],
 'GU100': [0.125, "Hydrocele sac: GROSS ONLY"],
 'GU110': [0.5, "Hydrocele sac: GROSS & MICRO"],
 'GU120': [0.25, "Penis resection, benign"],
 'GU130A': [1, "Prostate - needle core biopsies"],
 'GU130B': [0.25, "Prostate - needle core biopsies"],
 'GU140': [0.25, "Prostate - prostatectomy, benign"],
 'GU150': [0.25, "Prostate - prostatectomy, malignant"],
 'GU160A': [1, "Prostate - TURP"],
 'GU160B': [0.25, "Prostate - TURP"],
 'GU170': [0.25, "Radical penis resection for malignant conditions"],
 'GU180': [0.5, "Spermogram after vasectomy"],
 'GU190': [1, "Spermogram for fertility"],
 'GU200': [0.25, "Testes, orchiectomy, malignant"],
 'GU210': [0.25, "Testes, orchiectomy, benign"],
 'GU220': [0.25, "Testes, orchiectomy for carcinoma of prostate"],
 'GU230': [1, "Testicular biopsy, all conditions except for infertility"],
 'GU240': [5, "Testicular biopsy, for infertility (medical)"],
 'GU250': [0.25, "Testis - appendix with no pathology"],
 'GU260': [0.25, "Testis, appendage with pathology"],
 'GU270': [0.5, "Testis, spermatocele"],
 'GU280': [0.25, "Testis, varicocele"],
 'GU290': [0.25, "Vas deferens for sterilization"],
 'GU300': [0.5, "Vas deferens, non-sterilization"],
 'MI100': [0.5, "Abscess"],
 'MI110': [5, "All transplant biopsies (all organs from all systems)"],
 'MI130': [0.125, "Calculus (stone), foreign body"],
 'MI140A': [0.125, "Hernia sacs: GROSS ONLY"],
 'MI140B': [0.25, "Hernia sacs: GROSS & MICRO"],
 'MI140C': [0.25, "Hernia sacs: PATHOLOGY FOUND"],
 'MI150': [0.5, "Material passed per vagina or other orifices"],
 'MI160': [1, "Mesothelium, other than pleural - biopsy/tissue"],
 'MI170': [0.125, "No tissue in the container and no sections are taken"],
 'MI180': [0.25, "Omentum"],
 'MI190': [0.125, "Foreign body: GROSS ONLY"],
 'MI200': [0.25, "Foreign body: GROSS & MICRO"],
 'MI210': [1, "Retroperitoneal biopsy"],
 'MILN100': [0.25, "Lymph node - regional resection per side of body"],
 'MILN110': [1, "Lymph node - sentinel nodes alone: FIRST 3 BLOCKS"],
 'MILN120': [0.25, "Lymph node - sentinel nodes alone: EACH ADDITIONAL BLOCK"],
 'NE100': [5, "Brain biopsy for medical reasons (dementia, infectious disorders, etc)"],
 'NE110': [1, "Brain biopsy for metastatic lesion"],
 'NE120': [1, "Brain biopsy for primary brain tumour"],
 'NE130': [1, "Brain cyst"],
 'NE140': [0.125, "Brain/meninges – trauma: GROSS ONLY"],
 'NE150': [0.25, "Brain/meninges – trauma: GROSS & MICRO"],
 'NE160': [0.25, "Brain/meninges - tumour resection: MORE THAN 3 BLOCKS"],
 'NE165': [1, "Brain/meninges - tumour resection: 3 BLOCKS OR LESS"],
 'NE170': [0.25, "CNS, spinal cord, nerve - tumour resection: MORE THAN 3 BLOCKS"],
 'NE175': [1, "CNS, spinal cord, nerve - tumour resection: 3 BLOCKS OR LESS"],
 'NE180': [5, "Muscle biopsy, metabolic and medical conditions"],
 'NE190': [5, "Nerve - biopsy"],
 'NE200': [0.25, "Nerve, confirm nerve (vagus, sympathectomy, ganglions)"],
 'OR100': [5, "Bone, biopsy(ies) or curetting for primary bone tumour"],
 'OR110': [0.25, "Amputation, extremity, benign and nontraumatic condition: GROSS ONLY"],
 'OR120': [1, "Amputation, extremity, benign and nontraumatic condition: GROSS & MICRO"],
 'OR130': [0.25, "Amputation, finger and toes, benign and non-traumatic: GROSS ONLY"],
 'OR140': [1, "Amputation, finger and toes, benign and non-traumatic: GROSS & MICRO"],
 'OR150': [0.25, "Amputation, finger and toes, malignant"],
 'OR160': [0.125, "Amputation, finger and toes, traumatic: GROSS ONLY"],
 'OR170': [0.5, "Amputation, finger and toes, traumatic: GROSS & MICRO"],
 'OR180': [0.125, "Amputation, whole extremities, traumatic: GROSS ONLY"],
 'OR190': [1, "Amputation, whole extremities, traumatic: GROSS & MICRO"],
 'OR200': [0.25, "Amputation/disarticulation, extremity, malignant condition"],
 'OR210': [0.5, "Bone - exostosis"],
 'OR220': [5, "Bone biopsy for medical and metabolic disorders"],
 'OR230': [1, "Bone core biopsies - metastatic tumour and pathologic fracture"],
 'OR240A': [1, "Bone curetting/reaming for metastatic carcinoma"],
 'OR240B': [0.25, "Bone curetting/reaming for metastatic carcinoma"],
 'OR250': [0.5, "Bone fragments requiring histology"],
 'OR260': [0.125, "Bone, femoral head, knee, others - benign condition: GROSS ONLY"],
 'OR270': [0.5, "Bone, femoral head, knee, others - benign condition: GROSS & MICRO"],
 'OR280': [0.25, "Bone, primary bone tumour - radical resection"],
 'OR290': [0.125, "Intervertebral disc: GROSS ONLY"],
 'OR300': [0.25, "Intervertebral disc: GROSS & MICRO"],
 'OR310': [0.25, "Joint, bursa"],
 'OR320': [0.125, "Joint, cartilage and shavings: GROSS ONLY"],
 'OR330': [0.25, "Joint, cartilage and shavings: GROSS & MICRO"],
 'OR340': [0.125, "Joint, loose body: GROSS ONLY"],
 'OR350': [0.25, "Joint, loose body: GROSS & MICRO"],
 'OR360': [0.125, "Joint, meniscus: GROSS ONLY"],
 'OR370': [0.25, "Joint, meniscus: GROSS & MICRO"],
 'OR380': [0.5, "Joint, synovium cyst"],
 'OR390': [0.125, "Rib, incidental: GROSS ONLY"],
 'OR400': [0.25, "Rib, incidental: GROSS & MICRO"],
 'OR410': [1, "Synovial biopsy"],
 'QA190': [0.125, "Correlation studies (total agreement)"],
 'QA200': [0.25, "Correlation studies (minor disagreement)"],
 'QA210': [3, "Correlation studies (major disagreement)"],
 'RE100': [0.25, "Lung - resection (segmental, lobe, total), benign conditions"],
 'RE110': [0.25, "Lung - resection (segmental, lobe, total), malignant conditions - radical"],
 'RE120': [0.25, "Lung wedge biopsy for medical conditions"],
 'RE130': [0.25, "Lung wedge resection for tumours: BENIGN"],
 'RE140': [0.25, "Lung wedge resection for tumours: (PRE-) MALIGNANT"],
 'RE150': [5, "Lung explant"],
 'RE160': [1, "Pleural biopsy"],
 'RE170': [1, "Respiratory tract (trachea to lung) - biopsy (e.g. transbronchial)"],
 'RE180': [1, "Respiratory tract (trachea to lung) - core biopsy for neoplastic conditions"],
 'RE190': [5, "Respiratory tract (trachea to lung), core biopsy for medical conditions"],
 'RE200': [1, "Mediastinal or Thymic biopsy"],
 'SK100': [0.5, "Skin biopsies (< 2 cm), basal cell and squamous cell carcinoma"],
 'SK110': [0.25, "Skin excision for cosmetic reason"],
 'SK120': [1, "Skin, atypical melanocytic nevus and melanoma in situ"],
 'SK130': [3, "Skin biopsy for alopecia (using multiple transverse sections protocol)"],
 'SK140': [0.25, "Skin excision of malignant neoplasm: SKIN EXCISION, see comment for additional codes to enter when nodes included"],
 'SK150': [0.25, "Skin, large excisions (non-cosmetic)"],
 'SK160': [0.5, "Skin (<2 cm), neoplasms, benign"],
 'SK160B': [0.5, "Skin (<2 cm), neoplasms, benign - multiple fibroepithelial in same container"],
 'SK160C': [1, "Skin (<2 cm), neoplasms, benign – skin adnexal tumours or benign cutaneous"],
 'SK170': [1, "Skin (<2cm), neoplasms, malignant - except basal and squamous cell carcinoma"],
 'SK180': [1, "Skin (<2cm), non-neoplastic conditions"],
 'SK190': [1, "Skin (<2 cm)adnexal tumour and benign cutaneous infiltrates"],
 'SK200': [0.5, "Nail clippings"],
 'ST100': [0.5, "Carpal tunnel tissue"],
 'ST110': [0.25, "Deeper lipomatous lesions"],
 'ST120': [0.5, "Fibromatosis - palmar/plantar/others"],
 'ST130': [0.25, "Ganglion cyst"],
 'ST140A': [1, "Soft tissue tumour benign and malignant not requiring radiologic correlation: BIOPSY/CORE BIOPSY/CURETTINGS"],
 'ST140B': [0.25, "Soft tissue tumour benign and malignant not requiring radiologic correlation: BIOPSY/CORE BIOPSY/CURETTINGS"],
 'ST150': [0.25, "Soft tissue tumour benign and malignant not requiring radiologic correlation: EXCISION"],
 'ST160': [5, "Soft tissue tumour requiring radiologic correlation: BIOPSY/CORE BIOPSY/ CURETTINGS"],
 'ST170': [5, "Soft tissue tumour requiring radiologic correlation: EXCISION"],
 'ST180': [0.5, "Soft tissue, debridement"],
 'ST190': [0.25, "Soft tissue, malignant - radical surgery"],
 'GU310': [0.25, "Kidney - partial or total nephrectomy, malignant (includes ureteric lesions)"],
 'GU320': [0.25, "Kidney - partial or total nephrectomy, non-malignant (includes ureteric lesions)"],
 'GU330': [5, "Kidney biopsy (medical)"],
 'GU340A': [1, "Kidney core biopsy (surgical - i.e. for tumour)"],
 'GU340B': [1, "Kidney core biopsy (surgical - i.e. for tumour)"],
 'GU350': [5, "Kidney, explant"],
 'GU360': [1, "Ureter/urethra/urinary bladder - biopsies"],
 'GU370': [0.25, "Ureter/urethra/urinary bladder - partial or total resections for benign conditions"],
 'GU380': [0.25, "Urinary bladder - partial or total resection, malignant (includes urethra lesions)"],
 'GU390': [0.25, "Radical cystoprostatctomy"],
 'GU400A': [1, "Urinary bladder - transurethral resections"],
 'GU400B': [0.25, "Urinary bladder - transurethral resections"],
 'ADD': [0.25, "Additional tissue blocks"],
 'LEV': [0.125, "For every level or deeper after reviewing the routine slides"],
 'IHC': [0.125, "Diagnostic and non-quantitative, excluding controls"],
 'IHCQ': [0.5, "Quantitative IHC for predictive, prognostic purposes, excluding controls"],
 'SS': [0.125, "Non-routine special stains, excluding controls (except Warthin Starry, ZN or Fite)"],
 'SSM': [0.5, "Warthin Starry, ZN or Fite, excluding controls"],
 'IF': [0.25, "Immunofluorescence, excluding controls"],
 'REP': [0.5, "For reading, interpreting and integrating special results done by other department or person"],
 'FISH': [2, "For reading, counting and interpretation of the slide, excluding repeats"],
 'FLOW': [2, "For reviewing the print outs and issuing the original flow cytometry report"],
 'MOL': [0.5, "For receiving pictures/data, interpreting and producing a report"],
 'SYN': [3, "For each distinct tumour per part requiring a synoptic (see rule 5) or for upgrade to a synoptic"],
}

code_df = pd.DataFrame.from_dict(
    code_dict, orient='index', columns=['Value', 'Description']
).reset_index().rename(columns={'index': 'Code'})


def validate_codes(code_quantity):
    """Returns 'SUCCESS' or an error string naming the invalid code."""
    tokens = [t.split("/", 1)[0] for t in code_quantity.replace(",", "").split() if t]
    for code in tokens:
        if code not in code_dict:
            return f"Code/Quantity: '{code}' is not in the Billing Code Dictionary"
    return "SUCCESS"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("SQL_File.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS case_info "
            "(CaseID PRIMARYKEY text, Part text, Code_Quantity text, Pathologist text, DateTime text)"
        )
        self.conn.commit()

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception:
            pass

    def insert(self, case_id, part, code_quantity, pathologist, date_time):
        self.cursor.execute(
            "INSERT INTO case_info VALUES (?, ?, ?, ?, ?)",
            (case_id, part, code_quantity, pathologist, date_time)
        )
        self.conn.commit()

    def update(self, case_id, part, code_quantity, pathologist, date_time):
        self.cursor.execute(
            "UPDATE case_info SET Code_Quantity = ?, Pathologist = ?, DateTime = ? "
            "WHERE CaseID = ? AND Part = ?",
            (code_quantity, pathologist, date_time, case_id, part)
        )
        self.conn.commit()

    def search(self, case_id, part):
        self.cursor.execute(
            "SELECT * FROM case_info WHERE CaseID = ? AND Part = ?", (case_id, part)
        )
        return self.cursor.fetchall()

    def delete(self, case_id, part):
        self.cursor.execute(
            "DELETE FROM case_info WHERE CaseID = ? AND Part = ?", (case_id, part)
        )
        self.conn.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM case_info")
        return self.cursor.fetchall()


class TableView:
    """Generic read-only table window. col_widths is a dict of {column_name: pixel_width}."""
    def __init__(self, title, columns, data, col_widths):
        window = tkinter.Tk()
        window.wm_title(title)

        tree = tkinter.ttk.Treeview(window)
        tree.grid(pady=15, column=1, row=1)
        tree["show"] = "headings"
        tree["columns"] = columns

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=col_widths[col])

        for record in data:
            tree.insert('', 'end', values=record)

        window.mainloop()


class CaseLocatorWindow:
    """Prompts for CaseID and Part, then calls on_confirm(case_id, part)."""
    def __init__(self, action_label, on_confirm):
        self.on_confirm = on_confirm
        self.window = tkinter.Tk()
        self.window.wm_title(f"{action_label} Data")

        self.case_id = tkinter.StringVar()
        self.part = tkinter.StringVar()

        tkinter.Label(self.window, text=f"Enter CaseID and Part to {action_label.lower()}", width=35).grid(pady=20, row=1, column=2)
        tkinter.Label(self.window, text="CaseID", width=10).grid(pady=5, row=2, column=1)
        tkinter.Label(self.window, text="Part", width=10).grid(pady=5, row=3, column=1)

        self.case_id_entry = tkinter.Entry(self.window, width=10, textvariable=self.case_id)
        self.part_entry = tkinter.Entry(self.window, width=10, textvariable=self.part)
        self.case_id_entry.grid(pady=5, row=2, column=3)
        self.part_entry.grid(pady=5, row=3, column=3)

        tkinter.Button(
            self.window, width=20, text=action_label,
            command=lambda: self.on_confirm(self.case_id_entry.get(), self.part_entry.get())
        ).grid(pady=15, padx=5, column=2, row=4)


CASE_INFO_COLUMNS = ("CaseID", "Part", "Code_Quantity", "Pathologist", "DateTime")
CASE_INFO_WIDTHS = {col: 135 for col in CASE_INFO_COLUMNS}


class InsertWindow:
    def __init__(self):
        self.db = Database()
        self.window = tkinter.Tk()
        self.window.wm_title("Insert Data")

        self.case_id = tkinter.StringVar()
        self.part = tkinter.StringVar()
        self.code_quantity = tkinter.StringVar()
        self.pathologist = tkinter.StringVar()

        tkinter.Label(self.window, text="Case ID", width=25).grid(pady=5, column=1, row=1)
        tkinter.Label(self.window, text="Part", width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, text="Code/Quantity", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, text="Pathologist", width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, text="Date & Time", width=25).grid(pady=5, column=1, row=5)
        self.date_time_label = tkinter.Label(self.window, text=self._now(), width=25)
        self.date_time_label.grid(pady=5, column=3, row=5)

        self.case_id_entry = tkinter.Entry(self.window, width=25, textvariable=self.case_id)
        self.part_entry = tkinter.Entry(self.window, width=25, textvariable=self.part)
        self.code_quantity_entry = tkinter.Entry(self.window, width=25, textvariable=self.code_quantity)
        self.pathologist_entry = tkinter.Entry(self.window, width=25, textvariable=self.pathologist)

        self.case_id_entry.grid(pady=5, column=3, row=1)
        self.part_entry.grid(pady=5, column=3, row=2)
        self.code_quantity_entry.grid(pady=5, column=3, row=3)
        self.pathologist_entry.grid(pady=5, column=3, row=4)

        tkinter.Button(self.window, width=20, text="Insert", command=self.on_insert).grid(pady=15, padx=5, column=1, row=10)
        tkinter.Button(self.window, width=20, text="New Case", command=self.on_reset).grid(pady=15, padx=5, column=2, row=10)
        tkinter.Button(self.window, width=20, text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3, row=10)

        self.window.mainloop()

    def _now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d,%H:%M")

    def on_insert(self):
        result = validate_codes(self.code_quantity_entry.get())
        if result != "SUCCESS":
            tkinter.messagebox.showerror("Value Error", "Invalid input in field " + result)
            return
        ts = self._now()
        self.db.insert(
            self.case_id_entry.get(), self.part_entry.get(),
            self.code_quantity_entry.get(), self.pathologist_entry.get(), ts
        )
        tkinter.messagebox.showinfo("Inserted Data", "Successfully inserted the above data in the database")
        self.part_entry.delete(0, tkinter.END)
        self.code_quantity_entry.delete(0, tkinter.END)
        self.date_time_label.config(text=ts)

    def on_reset(self):
        for entry in (self.case_id_entry, self.part_entry, self.code_quantity_entry):
            entry.delete(0, tkinter.END)
        self.date_time_label.config(text=self._now())


class UpdateWindow:
    def __init__(self, case_id, part):
        self.db = Database()
        self.case_id = case_id
        self.part = part

        self.window = tkinter.Tk()
        self.window.wm_title("Update Data")

        self.code_quantity = tkinter.StringVar()
        self.pathologist = tkinter.StringVar()

        tkinter.Label(self.window, text="CaseID", width=25).grid(pady=5, column=1, row=1)
        tkinter.Label(self.window, text=case_id, width=25).grid(pady=5, column=3, row=1)
        tkinter.Label(self.window, text="Part", width=25).grid(pady=5, column=1, row=2)
        tkinter.Label(self.window, text=part, width=25).grid(pady=5, column=3, row=2)
        tkinter.Label(self.window, text="Code/Quantity", width=25).grid(pady=5, column=1, row=3)
        tkinter.Label(self.window, text="Pathologist", width=25).grid(pady=5, column=1, row=4)
        tkinter.Label(self.window, text="Date & Time", width=25).grid(pady=5, column=1, row=5)
        tkinter.Label(self.window, text=datetime.datetime.now().strftime("%Y-%m-%d,%H:%M"), width=25).grid(pady=5, column=3, row=5)

        existing = self.db.search(case_id, part)
        if existing:
            tkinter.Label(self.window, text=existing[0][2], width=25).grid(pady=5, column=2, row=3)
            tkinter.Label(self.window, text=existing[0][3], width=25).grid(pady=5, column=2, row=4)
            tkinter.Label(self.window, text=existing[0][4], width=25).grid(pady=5, column=2, row=5)

        self.code_quantity_entry = tkinter.Entry(self.window, width=25, textvariable=self.code_quantity)
        self.pathologist_entry = tkinter.Entry(self.window, width=25, textvariable=self.pathologist)
        self.code_quantity_entry.grid(pady=5, column=3, row=3)
        self.pathologist_entry.grid(pady=5, column=3, row=4)

        tkinter.Button(self.window, width=20, text="Update", command=self.on_update).grid(pady=15, padx=5, column=1, row=10)
        tkinter.Button(self.window, width=20, text="Reset", command=self.on_reset).grid(pady=15, padx=5, column=2, row=10)
        tkinter.Button(self.window, width=20, text="Close", command=self.window.destroy).grid(pady=15, padx=5, column=3, row=10)

        self.window.mainloop()

    def on_update(self):
        result = validate_codes(self.code_quantity_entry.get())
        if result != "SUCCESS":
            tkinter.messagebox.showerror("Value Error", "Invalid input in field " + result)
            return
        self.db.update(
            self.case_id, self.part,
            self.code_quantity_entry.get(), self.pathologist_entry.get(),
            datetime.datetime.now().strftime("%Y-%m-%d,%H:%M")
        )
        tkinter.messagebox.showinfo("Updated Data", "Successfully updated the above data in the database")

    def on_reset(self):
        self.code_quantity_entry.delete(0, tkinter.END)


class SaveFile:
    def __init__(self):
        conn = sqlite3.connect("SQL_File.db")
        df = pd.read_sql_query("SELECT * FROM case_info", conn)
        conn.close()

        if df.empty:
            tkinter.messagebox.showinfo("No Data", "No data available to save")
            return

        path = self._prompt_save_path()
        if not path:
            return

        df = self._compute_units(df)
        mode = 'a' if os.path.isfile(path) else 'w'
        df.to_csv(path, mode=mode, index=False, header=(mode == 'w'))
        tkinter.messagebox.showinfo("Data Exported", f"Your data has been exported to {os.path.basename(path)} successfully.")

        conn = sqlite3.connect("SQL_File.db")
        conn.execute("DELETE FROM case_info")
        conn.commit()
        conn.close()

        if os.path.isfile("SQL_File.db"):
            os.remove("SQL_File.db")

    def _prompt_save_path(self):
        now = datetime.datetime.now()
        quarter = (now.month - 1) // 3 + 1
        prefix = f"Q{quarter}_{now.year}_"

        raw = filedialog.asksaveasfilename(
            initialdir=os.getcwd(), title="Save CSV",
            filetypes=(("CSV File", "*.csv"), ("All Files", "*.*"))
        )
        if not raw:
            return None

        name = os.path.basename(raw)
        if not name.endswith('.csv'):
            name += '.csv'
        return os.path.join(os.path.dirname(raw), prefix + name)

    def _compute_units(self, df):
        df['Code_Quantity'] = df['Code_Quantity'].str.replace(r'\s+', '', regex=True).str.rstrip(',')

        rows = df.Code_Quantity.str.split(',', expand=True).stack().str.strip().reset_index(level=1, drop=True)
        df = df.drop('Code_Quantity', axis=1).join(
            pd.concat([rows], axis=1, keys=['Code_Quantity'])
        ).reset_index(drop=True)

        df[['Code', 'Quantity']] = df.Code_Quantity.str.split("/", expand=True)
        df = df.drop('Code_Quantity', axis=1)
        df = df[['CaseID', 'Part', 'Code', 'Quantity', 'Pathologist', 'DateTime']]

        obj_cols = df.select_dtypes('object').columns
        df[obj_cols] = df[obj_cols].apply(pd.to_numeric, errors='ignore')
        obj_cols = df.select_dtypes('object').columns
        df[obj_cols] = df[obj_cols].astype('category')

        df['Units Worked'] = df.apply(
            lambda row: row['Quantity'] * code_dict[row['Code']][0], axis=1
        )
        return df


class HomePage:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("Pathologist Workload Information System")

        tkinter.Label(self.window, text="Home Page", width=100).grid(pady=20, column=1, row=1)

        buttons = [
            ("Insert",                  self.on_insert),
            ("Update",                  self.on_update),
            ("Search",                  self.on_search),
            ("Delete",                  self.on_delete),
            ("Display",                 self.on_display),
            ("Billing Code Dictionary", self.on_billing_codes),
            ("Save Quarterly Workload", self.on_save_workload),
        ]
        for row, (label, command) in enumerate(buttons, start=2):
            tkinter.Button(self.window, width=20, text=label, command=command).grid(pady=15, column=1, row=row)

        tkinter.Button(self.window, width=20, text="Exit", command=self.window.destroy).grid(pady=15, column=1, row=10)

        self.window.mainloop()

    def on_insert(self):
        InsertWindow()

    def on_update(self):
        self.locator = CaseLocatorWindow("Update", lambda c, p: UpdateWindow(c, p))

    def on_search(self):
        def show_results(case_id, part):
            data = Database().search(case_id, part)
            TableView("Search Results", CASE_INFO_COLUMNS, data, CASE_INFO_WIDTHS)
        self.locator = CaseLocatorWindow("Search", show_results)

    def on_delete(self):
        def do_delete(case_id, part):
            Database().delete(case_id, part)
            tkinter.messagebox.showinfo("Deleted Data", "Successfully deleted the selected data in the database")
        self.locator = CaseLocatorWindow("Delete", do_delete)

    def on_display(self):
        TableView("Database View", CASE_INFO_COLUMNS, Database().display(), CASE_INFO_WIDTHS)

    def on_billing_codes(self):
        data = list(code_df.itertuples(index=False, name=None))
        TableView("Billing Code Dictionary", ("Code", "Value", "Description"), data,
                  {"Code": 220, "Value": 220, "Description": 550})

    def on_save_workload(self):
        SaveFile()


HomePage()
