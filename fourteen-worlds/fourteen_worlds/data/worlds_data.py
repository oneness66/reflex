"""Data for the fourteen worlds (lokas) of Vedic cosmology."""

# Loka-traya - The Three Planetary Systems
LOKA_TRAYA_INFO = {
    "title": "Loka-traya - The 3 Planetary Systems",
    "description": "According to the Purāṇas, this universe is called loka-traya - the three lokas (Bhūrloka, Bhuvarloka and Svarloka), or three spheres consisting of 14 planetary systems.",
    "upper_world": {
        "name": "Ūrdhvaloka (ऊर्ध्वलोक)",
        "description": "The upper world or svarga-lokas - heavenly planets above mount Meru. The celestial world, the realms of the gods or heavens."
    },
    "middle_world": {
        "name": "Madhya-loka",
        "description": "The middle planetary system, world of mortals, the realms of humans, animals and plants."
    },
    "lower_world": {
        "name": "Adhaloka (अधलोक)",
        "description": "The lower world, the subterranean heavens (Bila-Swarga), the realms of beings other than humans, like Daityas, Dānavas and Nāgas."
    },
    "reference": "SB 1.19.23"
}

# Lotus Cosmology
LOTUS_COSMOLOGY = {
    "description": "From Viṣṇu's navel, the stem of a lotus flower grows, and on that lotus flower the first creature, Brahmā, is born. Within the stem of that lotus flower are fourteen divisions of planetary systems, which are created by Brahmā.",
    "reference": "SB 3.10.8-9"
}

# Antarikṣa - Space between worlds
ANTARIKSA_INFO = {
    "name": "Antarikṣa",
    "description": "The space between Bhūrloka and Bhuvarloka. The sun is situated in the middle of the universe, in the area between Bhūrloka and Bhuvarloka, called antarikṣa (outer space).",
    "details": "Beneath Vidyādhara-loka, Cāraṇaloka and Siddhaloka, in the sky called antarikṣa, are the places of enjoyment for the Yakṣas, Rākṣasas, Piśācas, ghosts and so on.",
    "reference": "SB 5.24.5"
}

# Bila-svarga - Subterranean Heavens
BILA_SVARGA_INFO = {
    "name": "Bila-svarga",
    "description": "The heavenly subterranean worlds. The seven lower regions are called bila-svargas (subterranean heavens) and are NOT regarded as planets but as realms or dwelling places below the earth.",
    "details": "These regions are described as being more opulent than the upper regions of the universe. The life here is of pleasure, wealth and luxury, with no distress. The demon architect Māyā has constructed palaces, temples, houses, yards and hotels with jewels. There is no sunlight in the lower realms, but the darkness is dissipated by the shining of the jewels that the residents wear. There is no old age, no sweat, no disease in the lower realms.",
    "width": "The width and length of the seven lower planetary systems are calculated to be exactly the same as those of earth."
}

# Naraka - The Hellish Planets
NARAKA_INFO = {
    "name": "Naraka - 28 Hells",
    "description": "All the hellish planets are situated in the intermediate space between the three worlds and the Garbhodaka Ocean. They lie on the southern side of the universe, beneath Bhū-maṇḍala.",
    "ruler": "Yamarāja, the very powerful son of the sun-god, resides in Pitṛloka with his personal assistants (Yamadūtas) who bring sinful men to him upon their death for judgment.",
    "count": 28,
    "reference": "SB 5.26"
}

WORLDS_DATA = [
    # Upper Worlds (Svargaloka)
    {
        "id": 1,
        "name": "Satya-loka",
        "alt_name": "Brahmaloka",
        "category": "upper",
        "level": 7,
        "description": "The highest planet where Lord Brahmā resides. In Satyaloka the inhabitants are fully cognizant of Vedic wisdom, and thus the mystic cloud of material energy is cleared.",
        "details": "There is neither bereavement, nor old age nor death. There is no pain of any kind, and therefore there are no anxieties. The duration of life in Satyaloka is calculated to be 15,480,000,000,000 years.",
        "reference": "SB 2.2.27",
        "color": "#FFD700"
    },
    {
        "id": 2,
        "name": "Tapa-loka",
        "alt_name": "World of Penance",
        "category": "upper",
        "level": 6,
        "description": "The planet of those who have performed severe penances. This loka is not inundated at the time of universal devastation.",
        "details": "The distance from the sun to Tapoloka is about 1,870,400,000 miles. Above Janaloka by 80,000,000 yojanas is Tapoloka. The higher planetary systems, beginning with Maharloka, Janaloka and Tapoloka, are not inundated at the time of devastation.",
        "reference": "SB 5.1.31",
        "color": "#FFA500"
    },
    {
        "id": 3,
        "name": "Jana-loka",
        "alt_name": "World of the Wise",
        "category": "upper",
        "level": 5,
        "description": "Great saintly persons reside here after death. Wise sages who are perfect celibates perform great sacrifices to the Absolute Truth.",
        "details": "A lively discussion arose among the sages on Janaloka about the nature of the Supreme Absolute Truth. At the time of cosmic devastation, great sages transport themselves to Janaloka, being distressed by the warmth of the blazing fire.",
        "reference": "SB 10.87.9",
        "color": "#FF8C00"
    },
    {
        "id": 4,
        "name": "Mahar-loka",
        "alt_name": "World of Saints",
        "category": "upper",
        "level": 4,
        "description": "Purified saints like Bhṛgu enjoy a duration of life of 4,300,000,000 solar years. This planet is worshipable even for transcendentally situated saints.",
        "details": "One can live here even at time of partial annihilation of the universe. The annihilation begins with volcanic flames from Shesha Ananta Deva, and when the heat reaches Maharloka, residents pass to Brahmaloka.",
        "reference": "SB 2.2.24",
        "color": "#FFB347"
    },
    {
        "id": 5,
        "name": "Svar-loka",
        "alt_name": "Svargaloka - Heaven",
        "category": "upper",
        "level": 3,
        "description": "The heavenly planets including the sun and the moon, ruled by Indra. Fruitive workers elevate themselves to these planets.",
        "details": "The denizens of heaven who live in planetary systems from Svarloka cannot even see Lord Viṣṇu in Śvetadvīpa. At the end of Lord Brahmā's day, everything up to Svargaloka is inundated with water.",
        "reference": "SB 8.11.5",
        "color": "#87CEEB"
    },
    {
        "id": 6,
        "name": "Bhuvar-loka",
        "alt_name": "Atmospheric Plane",
        "category": "middle",
        "level": 2,
        "description": "The middle portion of the sky where demigods, Gandharvas, Cāraṇas, and Vidyādharas reside. This is the atmospheric region.",
        "details": "Celestial denizens known as Cāraṇas and Gandharvas, munis and damsels of heavenly planets reside here. This is part of the three primary planetary systems. The middle portion of the sky is called Bhuvarloka.",
        "reference": "SB 5.20.37",
        "color": "#98D8C8"
    },
    {
        "id": 7,
        "name": "Bhūr-loka",
        "alt_name": "Earth",
        "category": "middle",
        "level": 1,
        "description": "The earthly planetary system where human beings, animals, and plants reside. This is the world of mortals - the middle planetary system.",
        "details": "Human beings on earth are situated at the beginning of the intermediate worlds. The planetary system known as Bhū-maṇḍala resembles a lotus flower, and its seven islands resemble the whorl of that flower. Jambūdvīpa is situated in the middle.",
        "reference": "SB 5.16.5",
        "color": "#6B8E23"
    },
    
    # Lower Worlds (Pātāla)
    {
        "id": 8,
        "name": "Atala",
        "alt_name": "First Subterranean World",
        "category": "lower",
        "level": -1,
        "description": "The abode of Bala, son of Maya Dānava, who created ninety-six kinds of mystic power. Three kinds of women reside here.",
        "details": "Women here capture men and induce them to drink an intoxicating beverage made with hāṭaka (cannabis indica). This intoxicant endows great sexual prowess, and illusioned by false pride, men think themselves gods.",
        "color": "#8B4513"
    },
    {
        "id": 9,
        "name": "Vitala",
        "alt_name": "Second Subterranean World",
        "category": "lower",
        "level": -2,
        "description": "Lord Śiva and Gaurī reside here. A special kind of gold called hāṭaka is produced from the river Hāṭakī.",
        "details": "Lord Śiva engages with Bhavānī to produce living entities, and from their vital fluid the river Hāṭakī is generated. When fire drinks of this river, it produces gold called Hāṭaka, with which demons decorate themselves.",
        "color": "#704214"
    },
    {
        "id": 10,
        "name": "Sutala",
        "alt_name": "Third Subterranean World",
        "category": "lower",
        "level": -3,
        "description": "The abode of Bali Mahārāja, celebrated as the most pious king. Lord Vāmanadeva serves as his doorkeeper.",
        "details": "Bali Mahārāja was favored by Vāmanadeva for his intense devotional service. The Lord took all his possessions but was pleased and returned his kingdom, making him richer than Indra. Even now, Bali engages in devotional service here.",
        "color": "#5C4033"
    },
    {
        "id": 11,
        "name": "Talātala",
        "alt_name": "Fourth Subterranean World",
        "category": "lower",
        "level": -4,
        "description": "The abode of Maya Dānava, the master of all māyāvīs who can invoke powers of sorcery. He is protected by Lord Śiva.",
        "details": "Maya is the ācārya of sorcery. Lord Śiva once set fire to his three kingdoms but later returned them. Since that time, Maya has been protected by Lord Śiva and falsely thinks he need not fear the Sudarśana cakra.",
        "color": "#483C32"
    },
    {
        "id": 12,
        "name": "Mahātala",
        "alt_name": "Fifth Subterranean World",
        "category": "lower",
        "level": -5,
        "description": "The abode of many-hooded snakes descended from Kadrū, including Kuhaka, Takṣaka, Kāliya and Suṣeṇa.",
        "details": "The great snakes here are always disturbed by fear of Garuḍa, the carrier of Lord Viṣṇu. Although full of anxiety, some nevertheless sport with their wives, children, friends and relatives.",
        "color": "#3C3530"
    },
    {
        "id": 13,
        "name": "Rasātala",
        "alt_name": "Sixth Subterranean World",
        "category": "lower",
        "level": -6,
        "description": "The abode of demoniac sons of Diti and Danu - Paṇis, Nivāta-kavacas, Kāleyas and Hiraṇya-puravāsīs who reside in holes like snakes.",
        "details": "They are enemies of demigods, extremely powerful and cruel from birth, proud of their strength but always defeated by the Sudarśana cakra. They become very afraid when the messenger Saramā chants a particular curse.",
        "color": "#2C2416"
    },
    {
        "id": 14,
        "name": "Pātāla",
        "alt_name": "Nāgaloka - Seventh Subterranean World",
        "category": "lower",
        "level": -7,
        "description": "The lowest world where Vāsuki and demoniac serpents reside. Masters of Nāgaloka have many hoods bedecked with valuable gems.",
        "details": "Chief among the serpents is Vāsuki. Others include Śaṅkha, Kulika, Mahāśaṅkha, Śveta, Dhanañjaya, Dhṛtarāṣṭra, and Devadatta. They are extremely angry with hoods ranging from five to a thousand, and the light from their gems illuminates the entire planetary system.",
        "color": "#1A1410"
    }
]

def get_world_by_id(world_id: int):
    """Get a world by its ID."""
    for world in WORLDS_DATA:
        if world["id"] == world_id:
            return world
    return None

def get_worlds_by_category(category: str):
    """Get all worlds in a specific category."""
    return [world for world in WORLDS_DATA if world["category"] == category]

def get_upper_worlds():
    """Get all upper worlds."""
    return get_worlds_by_category("upper")

def get_middle_worlds():
    """Get all middle worlds."""
    return get_worlds_by_category("middle")

def get_lower_worlds():
    """Get all lower worlds."""
    return get_worlds_by_category("lower")
