# Pages métier (référencement). Exécuté dans build.py avant PAGES.

REF_BY_IMG = {r[0]: r for r in REFS}
CUR_BY_TITLE = {c[2]: c for c in CURRENT}

ACTIVITES = [
 dict(
  title_en='Drinking water and sewer networks in Guadeloupe and Saint-Martin | TMI', desc_en='Laying and renewal of drinking water mains, sewers and stormwater networks, service connections and boreholes in Guadeloupe and Saint-Martin.',
  eid='reseaux', slug='reseaux-eau-potable-assainissement-guadeloupe.html',
  hero='ref-petit-canal-aep', side='2026-quai-aep',
  nav=("Réseaux d'eau et assainissement", "Water and sewer networks"),
  title="Réseaux d'eau potable et d'assainissement en Guadeloupe | TMI",
  desc="Pose et renouvellement de réseaux d'eau potable (AEP), d'eaux usées et d'eaux pluviales, branchements et forages en Guadeloupe et à Saint-Martin.",
  h1=("Réseaux d'eau potable et d'assainissement en Guadeloupe et à Saint-Martin", "Drinking water and sewer networks in Guadeloupe and Saint-Martin"),
  lead=("Adduction d'eau potable, eaux usées, eaux pluviales, branchements et forages : nous construisons et renouvelons les réseaux qui alimentent les deux îles.",
        "Drinking water supply, wastewater, stormwater, connections and boreholes: we build and renew the networks that serve both islands."),
  intro=[
   ("Fuites, coupures, canalisations anciennes ou sous-dimensionnées : la Guadeloupe et Saint-Martin mènent un effort important de renouvellement de leurs réseaux d'eau. TMI réalise ces travaux pour les syndicats et établissements publics de l'eau, le Conseil départemental, les communes, le Grand Port Maritime et les aménageurs, de l'ouverture de la tranchée à la mise en service.",
    "Leaks, supply cuts, old or undersized pipes: Guadeloupe and Saint-Martin are making a major effort to renew their water networks. TMI carries out this work for water authorities and utilities, the Departmental Council, towns, the Port Authority and developers, from trench opening to commissioning."),
   ("Nous posons les canalisations d'adduction et de distribution d'eau potable (AEP), les collecteurs d'eaux usées et d'eaux pluviales, les branchements avec leurs coffrets de comptage, ainsi que les regards, chambres de vannes et ouvrages annexes. Les travaux sont phasés par tronçons pour maintenir la desserte des abonnés et limiter la gêne pour les riverains.",
    "We lay drinking water supply and distribution mains, wastewater and stormwater sewers, service connections with meter boxes, plus manholes, valve chambers and ancillary structures. Work is phased section by section to keep customers supplied and limit disruption for residents."),
   ("Chaque réseau est contrôlé avant sa mise en service : essais de pression et désinfection pour l'eau potable, essais d'étanchéité et inspection pour l'assainissement. La réfection de chaussée qui suit la tranchée est assurée par notre propre atelier d'enrobés, sans intervenant supplémentaire.",
    "Every network is tested before commissioning: pressure tests and disinfection for drinking water, leak tests and inspection for sewers. Road reinstatement after trenching is done by our own asphalt crew, with no extra contractor."),
  ],
  pillars=[("Préparation", "Preparation", "Études d'exécution, détection des réseaux existants, plan de phasage et information des riverains.", "Detailed design, detection of existing utilities, phasing plan and information for residents."),
           ("Pose et essais", "Laying and testing", "Pose au laser, compactage contrôlé, essais de pression, désinfection et mise en eau.", "Laser-guided laying, controlled compaction, pressure testing, disinfection and commissioning."),
           ("Réfection intégrée", "Integrated reinstatement", "Remblaiement et réfection de chaussée en enrobé par nos propres équipes.", "Backfilling and asphalt reinstatement by our own crews.")],
  refs=['ref-petit-canal-aep'],
  current=["Reprise de l'adduction d'eau potable du quai 6", "Renouvellement d'eau potable et création d'un réseau d'eaux usées",
           'Travaux de renouvellement du réseau AEP de Sainte-Anne, impasse Vallier',
           'Travaux de renouvellement du réseau AEP de Saint-François, tranche 1 : secteurs de Bragelogne et Saint-Charles',
           "Forages pour la ressource en eau potable"],
  faq=[
   ("Pour quels maîtres d'ouvrage intervenez-vous ?", "Which clients do you work for?",
    "Principalement des maîtres d'ouvrage publics : SMGEAG, Conseil départemental de la Guadeloupe, Grand Port Maritime de la Guadeloupe, établissements publics de l'eau. Nous étudions aussi les demandes d'aménageurs, d'entreprises et de propriétaires privés via notre formulaire de contact.",
    "Mainly public clients: SMGEAG, the Guadeloupe Departmental Council, the Guadeloupe Port Authority and public water utilities. We also consider requests from developers, businesses and private owners through our contact form."),
   ("Réalisez-vous les branchements d'eau et d'assainissement ?", "Do you build water and sewer connections?",
    "Oui. À Petit-Canal, secteur Cornet, nous avons réalisé 450 branchements avec coffrets de comptage, en plus de 6 km de réseau d'eau potable et 6 km de réseau d'eaux usées.",
    "Yes. In the Cornet area of Petit-Canal we built 450 connections with meter boxes, alongside 6 km of drinking water mains and 6 km of sewers."),
   ("Intervenez-vous à Saint-Martin ?", "Do you work in Saint-Martin?",
    "Oui. Nous y réalisons actuellement le renouvellement d'un réseau d'eau potable et la création d'un réseau d'eaux usées pour l'établissement public de l'eau.",
    "Yes. We are currently renewing a drinking water main and building a new sewer network there for the public water utility."),
   ("Qui refait la route après les travaux de réseau ?", "Who resurfaces the road after pipe works?",
    "Nos équipes. TMI dispose de son propre atelier d'enrobés (raboteuses, finisseurs, compacteurs), ce qui permet d'enchaîner la réfection de chaussée sans attendre une autre entreprise.",
    "Our own crews. TMI has its own asphalt plant and crew (milling machines, pavers, rollers), so road reinstatement follows straight on without waiting for another contractor."),
  ]),
 dict(
  title_en='Asphalt paving and roadworks in Guadeloupe and Saint-Martin | TMI', desc_en='Milling, asphalt paving and road resurfacing in Guadeloupe and Saint-Martin, day and night, with our own crew: roads, ports, car parks, local streets.',
  eid='routes', slug='enrobes-voirie-guadeloupe-saint-martin.html',
  hero='ref-colombier', side='materiel-finisseur',
  nav=("Enrobés et travaux routiers", "Asphalt and roadworks"),
  title="Enrobés et travaux routiers en Guadeloupe et à Saint-Martin | TMI",
  desc="Rabotage, enrobés et réfection de chaussée en Guadeloupe et à Saint-Martin, de jour comme de nuit, avec notre propre atelier : routes, ports, parkings, voies communales.",
  h1=("Enrobés et réfection de chaussée en Guadeloupe et à Saint-Martin", "Asphalt paving and road resurfacing in Guadeloupe and Saint-Martin"),
  lead=("Rabotage, mise en œuvre et compactage d'enrobés avec notre propre atelier, sur les routes, les ports, les parkings et les voies communales.",
        "Milling, paving and compaction with our own crew and plant, on roads, ports, car parks and local streets."),
  intro=[
   ("La chaussée est l'ouvrage que chacun utilise tous les jours. TMI dispose d'un atelier d'enrobés intégré : deux raboteuses, deux finisseurs grande et petite largeur, cinq compacteurs et une bouille à émulsion. Cette autonomie nous permet de mobiliser rapidement une équipe complète et de tenir des fenêtres d'intervention courtes.",
    "Roads are the infrastructure everyone uses every day. TMI has an integrated asphalt crew: two milling machines, wide and narrow pavers, five rollers and an emulsion sprayer. Being self-sufficient lets us mobilise a full team quickly and work within short time windows."),
   ("Nous réalisons le rabotage, les couches d'accrochage, la mise en œuvre en pleine largeur ou par bandes et le compactage, sur les axes principaux comme sur les voies communales, les zones portuaires, les parkings et les voies privées. Lorsque la circulation l'impose, nous travaillons de nuit pour rendre la voie aux usagers le matin.",
    "We carry out milling, tack coats, full-width or strip paving and compaction, on main roads and local streets, port areas, car parks and private roads. When traffic requires it we work at night so the road is open again in the morning."),
   ("À Saint-Martin, nous avons mis en œuvre 600 tonnes rue de Hollande, 500 tonnes à Friar's Bay et 320 tonnes rue Colombier, puis livré en 2026 la phase 2 de Friar's Bay, la route de Bellevue, le carrefour de Pic Paradis et une réfection de voirie en centre-ville. En Guadeloupe, nous réalisons la réfection en enrobé multisite du Grand Port Maritime.",
    "In Saint-Martin we laid 600 tonnes on Rue de Hollande, 500 tonnes at Friar's Bay and 320 tonnes on Rue Colombier, then delivered Friar's Bay phase 2, Bellevue road, the Pic Paradis junction and a town-centre resurfacing in 2026. In Guadeloupe we are resurfacing several sites of the Port Authority."),
  ],
  pillars=[("Atelier intégré", "In-house crew", "Raboteuses, finisseurs et compacteurs en propre : pas de dépendance à un sous-traitant.", "Our own milling machines, pavers and rollers: no reliance on subcontractors."),
           ("Travail de nuit", "Night work", "Interventions de nuit et par phases pour maintenir la circulation.", "Night and phased work to keep traffic moving."),
           ("Deux îles", "Two islands", "Équipes et matériel mobilisés en Guadeloupe comme à Saint-Martin.", "Crews and equipment deployed in Guadeloupe and Saint-Martin.")],
  refs=['ref-rue-de-hollande', 'ref-friars-bay', 'ref-colombier', 'ref-froston', 'ref-vieux-habitants-pont'],
  current=['Réfection en enrobé multisite du port', "Réfection en enrobé de la route de Friar's Bay, phase 2",
           "Reprises de chaussée en enrobé, route de Bellevue", "Réfection en enrobé du carrefour de Pic Paradis", 'Réfection de voirie en centre-ville'],
  faq=[
   ("Pouvez-vous travailler de nuit ?", "Can you work at night?",
    "Oui. Sur les axes fréquentés, nous intervenons de nuit et par phases pour limiter la gêne et rendre la chaussée à la circulation le matin.",
    "Yes. On busy roads we work at night and in phases to limit disruption and reopen the road in the morning."),
   ("Réalisez-vous des parkings et des voies privées ?", "Do you pave car parks and private roads?",
    "Oui. En plus des routes et des zones portuaires, nous réalisons des parkings, des cours et des voies de circulation pour des entreprises et des propriétaires privés. Décrivez votre besoin dans le formulaire de contact.",
    "Yes. Besides roads and port areas, we pave car parks, yards and access roads for businesses and private owners. Describe your needs in the contact form."),
   ("Quel matériel utilisez-vous ?", "What equipment do you use?",
    "Deux raboteuses XCMG (1,00 et 1,50 m), deux finisseurs XCMG couvrant de 0,50 à 7,50 m, cinq compacteurs et une bouille à émulsion de 2 000 litres.",
    "Two XCMG milling machines (1.00 and 1.50 m), two XCMG pavers covering 0.50 to 7.50 m, five rollers and a 2,000-litre emulsion sprayer."),
   ("Intervenez-vous à Saint-Martin ?", "Do you work in Saint-Martin?",
    "Oui, régulièrement : rue de Hollande, Friar's Bay, rue Colombier, Froston, route de Bellevue, Pic Paradis et centre-ville de Marigot.",
    "Yes, regularly: Rue de Hollande, Friar's Bay, Rue Colombier, Froston, Bellevue road, Pic Paradis and Marigot town centre."),
  ]),
 dict(
  title_en='Earthworks and utilities (VRD) in Guadeloupe and Saint-Martin | TMI', desc_en='Roads and utilities, earthworks, pavements, verges, stormwater drainage and urban works in Guadeloupe and Saint-Martin, including emergency response.',
  eid='vrd', slug='vrd-terrassement-guadeloupe.html',
  hero='ref-vieux-fort-amenagement', side='materiel-pelle-roues',
  nav=("VRD et terrassement", "Utilities and earthworks"),
  title="VRD et terrassement en Guadeloupe | TMI Travaux Modernes Ingénierie",
  desc="Voirie et réseaux divers (VRD), terrassement, trottoirs, accotements, eaux pluviales et aménagements urbains en Guadeloupe et à Saint-Martin, y compris en urgence.",
  h1=("VRD et terrassement en Guadeloupe et à Saint-Martin", "Utilities and earthworks in Guadeloupe and Saint-Martin"),
  lead=("Terrassement, voirie, réseaux divers, trottoirs et eaux pluviales : nous aménageons et sécurisons les espaces publics, les zones d'activité et les résidences.",
        "Earthworks, roads, utilities, pavements and stormwater: we develop and secure public spaces, business zones and housing estates."),
  intro=[
   ("Les travaux de voirie et réseaux divers (VRD) regroupent tout ce qui rend un terrain ou un espace public utilisable : terrassement, voies, trottoirs, accotements, réseaux d'eaux pluviales, fourreaux et réseaux secs, éclairage et signalisation. TMI les réalise pour les collectivités, les aménageurs, les bailleurs sociaux et le Grand Port Maritime.",
    "Roads and utilities works cover everything that makes a site or public space usable: earthworks, roads, pavements, verges, stormwater drainage, ducts and dry utilities, lighting and signage. TMI carries them out for local authorities, developers, social landlords and the Port Authority."),
   ("Notre parc de terrassement compte huit mini-pelles, des pelles de 6 à 15 tonnes, deux pelles sur pneus de 16 tonnes, deux tractopelles et sept camions bennes. Il nous permet de traiter aussi bien les fouilles en milieu urbain contraint que les grands volumes d'un aménagement de zone.",
    "Our earthworks fleet includes eight mini excavators, 6 to 15 tonne excavators, two 16 tonne wheeled excavators, two backhoe loaders and seven dump trucks. It handles both tight urban excavations and the large volumes of an area development."),
   ("En 2026, nous réalisons les VRD du quai 12 du port, l'aménagement d'un secteur pour une société publique d'aménagement, les VRD de la résidence Legitimus pour la SIKOA et une aire de covoiturage à Vieux-Habitants. Nous intervenons aussi en urgence après intempérie, comme à Saint-Claude après un éboulement sur la route de la Soufrière.",
    "In 2026 we are building the roads and utilities of Quay 12 at the port, an area development for a public development company, the external works of the Legitimus residence for SIKOA and a park-and-ride in Vieux-Habitants. We also respond to emergencies after storms, as in Saint-Claude after a landslide on the Soufrière road."),
  ],
  pillars=[("Terrassement", "Earthworks", "Décapage, déblais, remblais, plateformes et fouilles en milieu contraint.", "Stripping, cut and fill, platforms and excavation in tight spaces."),
           ("Voirie et réseaux", "Roads and utilities", "Chaussées, trottoirs, accotements béton, eaux pluviales et réseaux secs.", "Carriageways, pavements, concrete verges, stormwater and dry utilities."),
           ("Urgences", "Emergencies", "Mobilisation rapide après éboulement ou intempérie pour sécuriser et rétablir.", "Rapid response after landslides or storms to secure and restore.")],
  refs=['ref-vieux-fort-amenagement', 'ref-capesterre', 'ref-soufriere-urgence'],
  current=["Voirie et réseaux divers du quai 12", "Aménagement d'un secteur : terrassement, voirie, réseaux",
           "Voirie et réseaux divers de la résidence Legitimus", "Création d'une aire de covoiturage"],
  faq=[
   ("Que comprennent des travaux de VRD ?", "What do roads and utilities works include?",
    "Le terrassement, la création des voies et trottoirs, les réseaux d'eaux pluviales et d'eaux usées, les réseaux secs (fourreaux pour électricité et télécoms), l'éclairage et la signalisation. Nous pouvons prendre en charge l'ensemble ou un lot.",
    "Earthworks, roads and pavements, stormwater and sewer networks, dry utilities (ducts for power and telecoms), lighting and signage. We can take on the whole package or a single lot."),
   ("Intervenez-vous en urgence ?", "Do you handle emergency works?",
    "Oui. Après un éboulement sur la route de la Soufrière à Saint-Claude, nous avons terrassé, sécurisé les abords et créé un caniveau bétonné d'environ 60 m pour le Département.",
    "Yes. After a landslide on the Soufrière road in Saint-Claude, we carried out earthworks, secured the area and built a concrete gutter about 60 m long for the Department."),
   ("Travaillez-vous pour les aménageurs et les bailleurs ?", "Do you work for developers and landlords?",
    "Oui : société publique d'aménagement, SIKOA, Grand Port Maritime, communes. Les entreprises et les particuliers peuvent également nous soumettre leur projet via le formulaire de contact.",
    "Yes: public development companies, SIKOA, the Port Authority and towns. Businesses and individuals can also send us their project through the contact form."),
  ]),
 dict(
  title_en='Special foundations and seismic strengthening in Guadeloupe | TMI', desc_en='Micropiles, soil-nailed walls, retaining walls, shotcrete, slope stabilisation and seismic strengthening of buildings in Guadeloupe and Saint-Martin.',
  eid='speciaux', slug='fondations-speciales-parasismique-guadeloupe.html',
  hero='ref-bergevin-parasismique', side='materiel-foreuse',
  nav=("Fondations spéciales et parasismique", "Special foundations and seismic"),
  title="Fondations spéciales et renforcement parasismique en Guadeloupe | TMI",
  desc="Micropieux, parois clouées, murs de soutènement, béton projeté, confortement de talus et renforcement parasismique de bâtiments en Guadeloupe et à Saint-Martin.",
  h1=("Fondations spéciales et renforcement parasismique en Guadeloupe", "Special foundations and seismic strengthening in Guadeloupe"),
  lead=("Micropieux, parois clouées, soutènements, béton projeté et renforcement parasismique : des solutions adaptées aux sols et au risque sismique des Antilles.",
        "Micropiles, soil-nailed walls, retaining structures, shotcrete and seismic strengthening: solutions suited to the soils and seismic risk of the Caribbean."),
  intro=[
   ("La Guadeloupe est classée en zone de sismicité 5, le niveau le plus élevé en France. Beaucoup de bâtiments existants, logements sociaux et équipements publics, doivent être renforcés, et les ouvrages neufs reposent souvent sur des sols qui imposent des fondations profondes. TMI met en œuvre ces techniques avec ses propres foreuses et ses propres équipes.",
    "Guadeloupe is rated seismic zone 5, the highest level in France. Many existing buildings, social housing and public facilities need strengthening, and new structures often stand on ground that calls for deep foundations. TMI delivers these techniques with its own drilling rigs and crews."),
   ("Nous réalisons des micropieux, des parois clouées, des murs de soutènement, du béton projeté, des confortements de talus et le renforcement parasismique de bâtiments occupés ou vacants. À la résidence Bergevin, à Pointe-à-Pitre, nous avons mis en œuvre 384 micropieux et des voiles en béton armé d'environ 15 m de hauteur.",
    "We build micropiles, soil-nailed walls, retaining walls, shotcrete, slope stabilisation and seismic strengthening of occupied or vacant buildings. At the Bergevin residence in Pointe-à-Pitre we installed 384 micropiles and reinforced concrete walls about 15 m high."),
   ("En 2026, nous conduisons pour la SIKOA le confortement parasismique de la résidence Legitimus ainsi que la démolition, le gros œuvre et les fondations spéciales de 206 logements à Rivière Salée.",
    "In 2026 we are carrying out for SIKOA the seismic strengthening of the Legitimus residence and the demolition, structural work and special foundations of 206 homes in Rivière Salée."),
  ],
  pillars=[("Foreuses en propre", "Our own rigs", "Comacchio MC8 HT, XCMG XLS4 et ensembles Marini, centrale d'injection et gunitage.", "Comacchio MC8 HT, XCMG XLS4 and Marini units, grouting plant and shotcrete."),
           ("Sites occupés", "Occupied sites", "Phasage et sécurisation pour travailler dans des résidences habitées.", "Phasing and safety measures for work in occupied residences."),
           ("Sols difficiles", "Difficult ground", "Fondations profondes, soutènements et talus en terrain pentu ou instable.", "Deep foundations, retaining structures and slopes on steep or unstable ground.")],
  refs=['ref-bergevin-parasismique', 'ref-vieux-fort-talus', 'ref-gosier-fondations', 'ref-saint-martin-soutenement'],
  current=["Confortement parasismique de la résidence Legitimus", "Démolition, gros œuvre et fondations spéciales : 206 logements de Rivière Salée"],
  faq=[
   ("Qu'est-ce qu'un micropieu ?", "What is a micropile?",
    "Un pieu de petit diamètre foré puis armé et injecté de coulis, qui transmet les charges d'un ouvrage vers un sol plus résistant en profondeur. Il convient aux accès restreints et au renforcement de bâtiments existants.",
    "A small-diameter pile that is drilled, reinforced and grouted, transferring loads to stronger ground at depth. It suits restricted access and the strengthening of existing buildings."),
   ("Pourquoi renforcer un bâtiment existant ?", "Why strengthen an existing building?",
    "En zone de sismicité 5, de nombreux bâtiments construits avant les règles parasismiques actuelles doivent être confortés pour protéger leurs occupants. Le renforcement associe souvent micropieux, voiles en béton armé et reprises de structure.",
    "In seismic zone 5, many buildings built before current seismic codes need strengthening to protect occupants. The work often combines micropiles, reinforced concrete walls and structural repairs."),
   ("Disposez-vous de vos propres foreuses ?", "Do you have your own drilling rigs?",
    "Oui : foreuses Comacchio MC8 HT et XCMG XLS4, ensembles Marini, centrale d'injection, unités de gunitage et compresseurs jusqu'à 24 m³.",
    "Yes: Comacchio MC8 HT and XCMG XLS4 rigs, Marini units, a grouting plant, shotcrete units and compressors up to 24 m³."),
  ]),
 dict(
  title_en='Building, structural work and civil engineering in Guadeloupe | TMI', desc_en='Construction, heavy refurbishment, structural work and reinforced concrete for public facilities, housing and technical buildings in Guadeloupe and Saint-Martin.',
  eid='batiment', slug='batiment-genie-civil-guadeloupe.html',
  hero='ref-vieux-habitants-class', side='ref-vieux-habitants-creche',
  nav=("Bâtiment et génie civil", "Building and civil engineering"),
  title="Bâtiment, gros œuvre et génie civil en Guadeloupe | TMI",
  desc="Construction, réhabilitation lourde, gros œuvre et béton armé pour les équipements publics, le logement et les bâtiments techniques en Guadeloupe et à Saint-Martin.",
  h1=("Bâtiment, gros œuvre et génie civil en Guadeloupe", "Building, structural work and civil engineering in Guadeloupe"),
  lead=("Construction neuve, réhabilitation lourde, gros œuvre et béton armé pour les équipements publics, le logement et les bâtiments techniques.",
        "New construction, heavy rehabilitation, structural work and reinforced concrete for public facilities, housing and technical buildings."),
  intro=[
   ("TMI intervient sur les bâtiments publics, les logements collectifs et les bâtiments techniques, en construction neuve comme en réhabilitation. Nous réalisons le gros œuvre et les structures en béton armé, et coordonnons l'ensemble des corps d'état lorsque l'opération le demande.",
    "TMI works on public buildings, multi-unit housing and technical buildings, both new and refurbished. We carry out structural work and reinforced concrete, and coordinate all trades when the project requires it."),
   ("À Vieux-Habitants, nous avons reconstruit et réhabilité la crèche municipale et réaménagé le bâtiment du CLASS, avec reprise de toiture et mise en conformité. Ces chantiers ont été conduits en cinq mois chacun pour une remise en service rapide.",
    "In Vieux-Habitants we rebuilt and rehabilitated the municipal nursery and refurbished the CLASS building, including roof renovation and compliance upgrades. Each project took five months, for a quick return to service."),
   ("En 2026, nous construisons un bâtiment public pour la Ville du Moule et le hangar du centre technique municipal d'Anse-Bertrand, et réalisons pour la SIKOA la démolition et le gros œuvre de 206 logements à Rivière Salée.",
    "In 2026 we are building a public building for the Town of Le Moule and the municipal technical centre shed in Anse-Bertrand, and carrying out demolition and structural work for 206 homes in Rivière Salée for SIKOA."),
  ],
  pillars=[("Gros œuvre", "Structural work", "Fondations, voiles, dalles et structures en béton armé, avec pompe à béton en propre.", "Foundations, walls, slabs and reinforced concrete structures, with our own concrete pump."),
           ("Réhabilitation", "Rehabilitation", "Reprise de structure, toiture et mise en conformité de bâtiments existants.", "Structural repairs, roofing and compliance upgrades of existing buildings."),
           ("Tous corps d'état", "All trades", "Coordination des lots jusqu'à la livraison et la remise en service.", "Coordination of all trades through to handover.")],
  refs=['ref-vieux-habitants-class', 'ref-vieux-habitants-creche'],
  current=["Construction d'un bâtiment public", "Hangar d'un centre technique municipal",
           "Démolition, gros œuvre et fondations spéciales : 206 logements de Rivière Salée"],
  faq=[
   ("Intervenez-vous en tous corps d'état ?", "Do you work as an all-trades contractor?",
    "Oui. Nous réalisons le gros œuvre et coordonnons les autres corps d'état, comme pour la crèche et le CLASS de Vieux-Habitants.",
    "Yes. We carry out the structural work and coordinate the other trades, as for the nursery and the CLASS building in Vieux-Habitants."),
   ("Construisez-vous des bâtiments neufs ?", "Do you build new buildings?",
    "Oui : en 2026, un bâtiment public au Moule et un hangar de centre technique municipal à Anse-Bertrand.",
    "Yes: in 2026, a public building in Le Moule and a municipal technical centre shed in Anse-Bertrand."),
   ("Pour qui travaillez-vous ?", "Who do you work for?",
    "Communes, bailleurs sociaux comme la SIKOA, collectivités et entreprises. Toute demande peut nous être adressée par le formulaire de contact.",
    "Towns, social landlords such as SIKOA, local authorities and businesses. Any request can be sent through our contact form."),
  ]),
]
ACT_BY_EID = {x['eid']: x for x in ACTIVITES}

def page_activite(act):
    def render():
        url = BASE + act['slug']
        h1fr, h1en = act['h1']; nfr, nen = act['nav']
        def ld_for(lang):
            u = url_for(act['slug'], lang); en = lang == 'en'
            return [
              {"@context": "https://schema.org", "@type": "Service", "name": h1en if en else h1fr, "serviceType": nen if en else nfr, "url": u,
               "description": act['desc_en'] if en else act['desc'], "areaServed": ["Guadeloupe", "Saint-Martin"], "inLanguage": lang,
               "provider": {"@type": "GeneralContractor", "name": "TMI Travaux Modernes Ingénierie", "url": BASE, "email": EMAIL}},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home" if en else "Accueil", "item": url_for('index.html', lang)},
                {"@type": "ListItem", "position": 2, "name": "Expertise" if en else "Expertises", "item": url_for('expertises.html', lang)},
                {"@type": "ListItem", "position": 3, "name": nen if en else nfr, "item": u}]},
              {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": [
                {"@type": "Question", "name": qe if en else qf, "acceptedAnswer": {"@type": "Answer", "text": re_ if en else rf}} for qf, qe, rf, re_ in act['faq']]},
            ]
        h = head(act['slug'], act['title'], act['desc'], extra_ld=ld_for('fr'), nav_page='expertises.html',
                 title_en=act['title_en'], desc_en=act['desc_en'], extra_ld_en=ld_for('en'))
        exp = next(e for e in EXPERTISES if e[0] == act['eid'])
        subs, mfr, men = exp[6], exp[7], exp[8]
        subl = ''.join(f'<li data-en="{a(se)}">{esc(sf)}</li>' for sf, se in subs)
        intro = ''.join(T(fr, en, 'p') for fr, en in act['intro'])
        pillars = ''.join(f'<div class="pillar">{T(tf, te, "h3")}{T(df, de, "p")}</div>' for tf, te, df, de in act['pillars'])
        cards = ''.join(card(REF_BY_IMG[k], link=CH_SLUG[k]) for k in act['refs'])
        rows = ''.join(crow(CUR_BY_TITLE[t], CH_2026[t][0] if t in CH_2026 else None) for t in act['current'])
        faq = ''.join(f'<details class="faq">{T(qf, qe, "summary")}{T(rf, re_, "p")}</details>' for qf, qe, rf, re_ in act['faq'])
        others = ''.join(f'<li><a href="{x["slug"]}" data-en="{a(x["nav"][1])}">{esc(x["nav"][0])}</a></li>' for x in ACTIVITES if x is not act)
        body = f'''<section class="phero">
  {pic(act['hero'], '', '', lazy=False, prio=True, sizes='100vw')}
  <div class="wrap">
    <p class="crumbs"><a href="index.html" data-en="Home">Accueil</a> / <a href="expertises.html" data-en="Expertise">Expertises</a> / {T(nfr, nen)}</p>
    {T(h1fr, h1en, 'h1')}
    {T(act['lead'][0], act['lead'][1], 'p', 'lead')}
  </div>
</section>
<section class="sect"><div class="wrap split top">
  <div class="prose">
    {T("Notre savoir-faire", "What we do", 'p', 'kicker')}
    {intro}
  </div>
  <div>
    <div class="exp-photo">{pic(act['side'], nfr, nen, sizes='(max-width:900px) 100vw, 560px')}</div>
    <ul class="sublist">{subl}</ul>
    <div class="exp-refs"><strong data-en="Dedicated equipment">Matériel dédié</strong>{T(mfr, men)} <a class="link" href="materiel.html" data-en="See the fleet">Voir le parc</a></div>
  </div>
</div></section>
<section class="sect tint"><div class="wrap"><div class="pillars p3">{pillars}</div></div></section>
<section class="sect" id="references"><div class="wrap">
  <div class="sect-head">
    <div>{T("Références", "References", 'p', 'kicker')}{T("Chantiers réalisés et en cours", "Completed and ongoing projects", 'h2')}</div>
    {T("Une sélection d'opérations conduites par nos équipes pour des maîtres d'ouvrage publics de Guadeloupe et de Saint-Martin.", "A selection of projects carried out by our crews for public clients in Guadeloupe and Saint-Martin.", 'p', 'lead')}
  </div>
  <div class="cards">{cards}</div>
  <ul class="crows">
    <li class="crow head" aria-hidden="true"><span data-en="Trade">Métier</span><span data-en="Project">Opération</span><span data-en="Client">Maître d'ouvrage</span><span data-en="Area">Territoire</span><span data-en="Amount">Montant</span><span data-en="Status">Statut</span></li>
    {rows}
  </ul>
</div></section>
<section class="sect tint"><div class="wrap split top">
  <div>{T("Questions fréquentes", "Frequently asked questions", 'p', 'kicker')}{T("Vos questions sur ce métier", "Your questions about this trade", 'h2')}</div>
  <div class="faqs">{faq}</div>
</div></section>
<section class="sect"><div class="wrap cta-row">
  <div>
    {T("Un projet, une consultation, une question ?", "A project, a tender, a question?", 'h2')}
    {T("Collectivités, maîtres d'œuvre, entreprises ou particuliers : décrivez votre besoin, nous revenons vers vous.", "Public bodies, engineers, businesses or individuals: describe your needs and we will get back to you.", 'p', style='margin-top:1rem;color:var(--gris)')}
  </div>
  <div class="actions"><a class="btn" href="contact.html" data-en="Write to us">Nous écrire</a></div>
</div></section>
<section class="sect" style="padding-top:0"><div class="wrap">
  {T("Nos autres expertises", "Our other areas of expertise", 'p', 'kicker')}
  <ul class="other-acts">{others}</ul>
</div></section>
'''
        return h + body + FOOT
    return render

for _act in ACTIVITES:
    PAGES_EXTRA[_act['slug']] = page_activite(_act)

# ---------------------------------------------------------------- Fiches chantier
# Vidéos (chantiers d'enrobé uniquement) : renseigner l'identifiant YouTube, ex. 'chantier-enrobe-friars-bay-saint-martin.html': 'dQw4w9WgXcQ'
# Le bloc vidéo n'apparaît sur la fiche que lorsqu'un identifiant est renseigné.
VIDEOS = {}

def video_block(vid, tfr, ten):
    thumb = f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
    return f'''<div class="wrap ch-video">
  {T("Le chantier en vidéo", "The project on video", 'h2', style='margin-bottom:1.5rem')}
  <button type="button" class="yt" data-yt="{vid}" aria-label="Lire la vidéo : {a(tfr)}" data-en-label="Play the video: {a(ten)}">
    <img src="{thumb}" alt="" loading="lazy" width="480" height="360"><span class="yt-play" aria-hidden="true"></span>
  </button>
</div>'''
CH_SLUG = {
 'ref-petit-canal-aep': 'chantier-aep-assainissement-cornet-petit-canal.html',
 'ref-rue-de-hollande': 'chantier-enrobe-rue-de-hollande-marigot.html',
 'ref-friars-bay': 'chantier-enrobe-friars-bay-saint-martin.html',
 'ref-colombier': 'chantier-enrobe-rue-colombier-saint-martin.html',
 'ref-froston': 'chantier-enrobe-froston-saint-martin.html',
 'ref-vieux-habitants-pont': 'chantier-pont-de-vanier-vieux-habitants.html',
 'ref-vieux-fort-amenagement': 'chantier-amenagement-securisation-vieux-fort.html',
 'ref-capesterre': 'chantier-amenagement-voirie-capesterre-belle-eau.html',
 'ref-soufriere-urgence': 'chantier-travaux-urgence-soufriere-saint-claude.html',
 'ref-bergevin-parasismique': 'chantier-renforcement-parasismique-bergevin-pointe-a-pitre.html',
 'ref-vieux-fort-talus': 'chantier-confortement-talus-vieux-fort.html',
 'ref-gosier-fondations': 'chantier-micropieux-belle-plaine-le-gosier.html',
 'ref-saint-martin-soutenement': 'chantier-mur-soutenement-spring-saint-martin.html',
 'ref-vieux-habitants-class': 'chantier-rehabilitation-class-vieux-habitants.html',
 'ref-vieux-habitants-creche': 'chantier-creche-vieux-habitants.html',
}
# chantiers 2026 avec photos : titre -> (slug, photos, description fr, en)
CH_2026 = {
 "Reprise de l'adduction d'eau potable du quai 6": ('chantier-aep-quai-6-port-guadeloupe.html', ['2026-quai-aep'],
   "Reprise du réseau d'adduction d'eau potable qui dessert le quai 6 du Grand Port Maritime de la Guadeloupe, en site portuaire en exploitation.",
   "Renewal of the drinking water supply network serving Quay 6 of the Guadeloupe Port Authority, on an operating port site."),
 "Confortement parasismique de la résidence Legitimus": ('chantier-confortement-parasismique-legitimus.html', ['2026-residence-parasismique'],
   "Confortement parasismique de la résidence Legitimus pour la SIKOA : renforcement de la structure existante pour améliorer son comportement en cas de séisme.",
   "Seismic strengthening of the Legitimus residence for SIKOA: reinforcing the existing structure to improve its behaviour in an earthquake."),
}
REF_ACT = {k: act for act in ACTIVITES for k in act['refs']}
CUR_ACT = {t: act for act in ACTIVITES for t in act['current']}

def page_chantier(act, slug, title, place, moa, dur, amt_txt, status, desc, photos, cat):
    def render():
        tfr, ten = title; nfr, nen = act['nav']; cfr, cen = CATS[cat]
        def ld_for(lang):
            en = lang == 'en'
            return [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home" if en else "Accueil", "item": url_for('index.html', lang)},
                {"@type": "ListItem", "position": 2, "name": nen if en else nfr, "item": url_for(act['slug'], lang)},
                {"@type": "ListItem", "position": 3, "name": ten if en else tfr, "item": url_for(slug, lang)}]}]
        h = head(slug, f"{tfr}, {place} | TMI", f"{desc[0]} Maître d'ouvrage : {moa[0]}.", extra_ld=ld_for('fr'), nav_page='realisations.html',
                 title_en=f"{ten}, {place} | TMI", desc_en=f"{desc[1]} Client: {moa[1]}.", extra_ld_en=ld_for('en'))
        rows = [("Maître d'ouvrage", "Client", T(moa[0], moa[1])), ("Lieu", "Location", esc(place)), ("Métier", "Trade", T(cfr, cen))]
        if dur: rows.append(("Durée", "Duration", T(dur[0], dur[1])))
        if amt_txt: rows.append(("Montant", "Amount", fmt_ht(amt_txt[1]) if amt_txt[0] == 'ht' else fmt_eur(amt_txt[1])))
        rows.append(("Statut", "Status", T(status[0], status[1])))
        fiche = ''.join(f'<div><dt data-en="{a(e)}">{esc(f)}</dt><dd>{v}</dd></div>' for f, e, v in rows)
        gal = ''.join(f'<figure class="ch-photo">{pic(p, tfr, ten, sizes="(max-width:700px) 100vw, 600px")}</figure>' for p in photos[1:])
        others = [card(REF_BY_IMG[k], link=CH_SLUG[k]) for k in act['refs'] if CH_SLUG[k] != slug][:3]
        oth = (f'''<section class="sect tint"><div class="wrap">
  {T("Autres chantiers du métier", "Other projects in this trade", 'h2', style='margin-bottom:2rem')}
  <div class="cards">{''.join(others)}</div>
</div></section>''' if others else '')
        body = f'''<section class="phero">
  {pic(photos[0], '', '', lazy=False, prio=True, sizes='100vw')}
  <div class="wrap">
    <p class="crumbs"><a href="index.html" data-en="Home">Accueil</a> / <a href="{act['slug']}" data-en="{a(nen)}">{esc(nfr)}</a> / {T("Chantier", "Project")}</p>
    {T(tfr, ten, 'h1')}
    <p class="lead">{esc(place)}</p>
  </div>
</section>
<section class="sect"><div class="wrap split top">
  <div class="prose">
    {T("L'opération", "The project", 'p', 'kicker')}
    {T(desc[0], desc[1], 'p')}
    {T("Ce chantier a été conduit par nos propres équipes, avec notre matériel. Il illustre notre métier :", "This project was carried out by our own crews with our own equipment. It is an example of our work in:", 'p')}
    <p><a class="link" href="{act['slug']}" data-en="{a(nen)}">{esc(nfr)}</a></p>
  </div>
  <dl class="ch-fiche">{fiche}</dl>
</div>
{f'<div class="wrap ch-gal">{gal}</div>' if gal else ''}
{video_block(VIDEOS[slug], tfr, ten) if (act['eid'] == 'routes' and slug in VIDEOS) else ''}
</section>
{oth}
<section class="sect"><div class="wrap cta-row">
  <div>
    {T("Un projet comparable ?", "A similar project?", 'h2')}
    {T("Collectivités, maîtres d'œuvre, entreprises ou particuliers : décrivez votre besoin, nous revenons vers vous.", "Public bodies, engineers, businesses or individuals: describe your needs and we will get back to you.", 'p', style='margin-top:1rem;color:var(--gris)')}
  </div>
  <div class="actions"><a class="btn" href="contact.html" data-en="Write to us">Nous écrire</a><a class="btn line" href="{act['slug']}#references" data-en="All projects in this trade">Tous les chantiers du métier</a></div>
</div></section>
'''
        return h + body + FOOT
    return render

for _k, _slug in CH_SLUG.items():
    r = REF_BY_IMG[_k]
    img, cat, tfr, ten, place, moa, dur, amt, dfr, den = r
    PAGES_EXTRA[_slug] = page_chantier(REF_ACT[_k], _slug, (tfr, ten), place, moa, dur, ('ttc', amt), ('Livré en 2025', 'Delivered in 2025'), (dfr, den), [img], cat)
for _t, (_slug, _ph, _dfr, _den) in CH_2026.items():
    c = CUR_BY_TITLE[_t]
    cat, st, tfr, ten, moa, terr, *_ = c
    PAGES_EXTRA[_slug] = page_chantier(CUR_ACT[_t], _slug, (tfr, ten), terr, moa, None, ('ht', AMOUNTS[tfr]), st, (_dfr, _den), _ph, cat)
