# NB - Some staff members may be incorrectly positioned and may not directly report in to those indicated in the chart below, e.g. Nick Smith, Will Widen, Jordan Downes-Soares

from collections import OrderedDict

org_chart = {
    "Rob Stone": OrderedDict(
        [
            ("Position", "CEO"),
            ("City", "London"),
            ("e-mail", "rob.stone@onclusive.com"),
            ("skills", []),
            ("languages", ["English"]),
            (
                "Direct_Reports",
                {
                    "Patrick Liang": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "SVP Engineering & Tech"),
                            ("City", "San Francisco"),
                            ("e-mail", "patrick@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            ("Direct_Reports", {}),
                        ]
                    ),
                    "Judy Luk-Smit": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "SVP Product"),
                            ("City", "San Francisco"),
                            ("e-mail", "judy@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            (
                                "Direct_Reports",
                                {
                                    "Elodie Guessard": OrderedDict(
                                        [
                                            ("Reports_to", "Judy Luk-Smit"),
                                            (
                                                "Position",
                                                "Director of Product Management",
                                            ),
                                            ("City", "Paris"),
                                            ("e-mail", "elodie.guessard@onclusive.com"),
                                            ("skills", []),
                                            ("languages", ["French", "English"]),
                                            (
                                                "Direct_Reports",
                                                {
                                                    "Charlotte Hammond": OrderedDict(
                                                        [
                                                            (
                                                                "Reports_to",
                                                                "Elodie Guessard",
                                                            ),
                                                            (
                                                                "Position",
                                                                "Product Manager",
                                                            ),
                                                            ("City", "London"),
                                                            (
                                                                "e-mail",
                                                                "charlotte.hammond@onclusive.com",
                                                            ),
                                                            ("skills", []),
                                                            ("languages", ["English"]),
                                                            ("Direct_Reports", {}),
                                                        ]
                                                    )
                                                },
                                            ),
                                        ]
                                    )
                                },
                            ),
                        ]
                    ),
                    "Nick Smith": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "Vice President Global Vendor Management"),
                            ("City", "London"),
                            ("e-mail", "nick.smith@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            ("Direct_Reports", {}),
                        ]
                    ),
                    "Will Widen": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "Global Head of External Content"),
                            ("City", "London"),
                            ("e-mail", "will.widen@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            (
                                "Direct_Reports",
                                {
                                    "Eddie Shinks": OrderedDict(
                                        [
                                            ("Reports_to", "Will Widen"),
                                            (
                                                "Position",
                                                "Service Fulfilment Executive",
                                            ),
                                            ("City", "London"),
                                            ("e-mail", "eddie.shinks@onclusive.com"),
                                            ("skills", []),
                                            ("languages", ["English"]),
                                            ("Direct_Reports", {}),
                                        ]
                                    )
                                },
                            ),
                        ]
                    ),
                    "Philip Lynch": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "SVP Insights & Consultancy"),
                            ("City", "London"),
                            ("e-mail", "philip.lynch@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            (
                                "Direct_Reports",
                                {
                                    "Arnaud Couturier": OrderedDict(
                                        [
                                            ("Reports_to", "Philip Lynch"),
                                            ("Position", "Directeur Etudes"),
                                            ("City", "Paris"),
                                            (
                                                "e-mail",
                                                "arnaud.couturier@onclusive.com",
                                            ),
                                            ("skills", []),
                                            ("languages", ["English", "French"]),
                                            ("Direct_Reports", {}),
                                        ]
                                    ),
                                    "Sonia Metché": OrderedDict(
                                        [
                                            ("Reports_to", "Philip Lynch"),
                                            ("Position", "Directrice Etudes"),
                                            ("City", "Paris"),
                                            ("e-mail", "sonia.metche@onclusive.com"),
                                            ("skills", []),
                                            ("languages", ["English", "French"]),
                                            ("Direct_Reports", {}),
                                        ]
                                    ),
                                    "Jordan Downes-Soares": OrderedDict(
                                        [
                                            ("Reports_to", "Philip Lynch"),
                                            (
                                                "Position",
                                                "Team Leader, Quality Assurance",
                                            ),
                                            ("City", "London"),
                                            (
                                                "e-mail",
                                                "jordan.downes-soares@onclusive.com",
                                            ),
                                            ("skills", []),
                                            ("languages", ["English"]),
                                            ("Direct_Reports", {}),
                                        ]
                                    ),
                                    "Lisa Travers": OrderedDict(
                                        [
                                            ("Reports_to", "Philip Lynch"),
                                            ("Position", "Head of Insight"),
                                            ("City", "London"),
                                            ("e-mail", "lisa.travers@onclusive.com"),
                                            ("skills", []),
                                            ("languages", ["English"]),
                                            (
                                                "Direct_Reports",
                                                {
                                                    "Luke Constable": OrderedDict(
                                                        [
                                                            (
                                                                "Reports_to",
                                                                "Lisa Travers",
                                                            ),
                                                            (
                                                                "Position",
                                                                "Insights Manager",
                                                            ),
                                                            ("City", "London"),
                                                            (
                                                                "e-mail",
                                                                "luke.constable@onclusive.com",
                                                            ),
                                                            ("skills", []),
                                                            ("languages", ["English"]),
                                                            (
                                                                "Direct_Reports",
                                                                {
                                                                    "Gareth Perry": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - Focus",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "gareth.perry@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Amy Blakemore": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "amy.blakemore@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Daniel Barton": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "daniel,barton@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Dhruv Sarup": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "dhruv.sarup@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "George Skinner": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "george.skinner@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                ['Power BI'],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Jade Checkley": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "jade.checkley@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Katrine Rute": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "katrina.rute@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Russian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Kevin Bartholomew": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "kevin.batholomew@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Louis Fletcher": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "louis.fletcher@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Oscar Garcia": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "oscar.garcia@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Spanish",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Zhulen Ali": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gareth Perry",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "zhulen.ali@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Bulgarian",
                                                                                                    "Turkish",
                                                                                                    "Russian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Natalie Lewis": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - International",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "natalie.lewis@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Aidan McGee": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "aidan.mcgee@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Danish",
                                                                                                    "Norwegian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Alastair Reed": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "alastair.reed@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Christopher Matthews": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Senior Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "christopher.matthews@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Emma Woodhouse": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "emma.woodhouse@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Maria Rodriguez Guia": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "maria.rodrigeuzguia@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Spanish",
                                                                                                    "Portuguese",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Matthew Leung": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "matthew.leung@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Cantonese",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                            (
                                                                                                "Notes",
                                                                                                "AKA Ming Leung",
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Paulo Faria": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "amy.blakemore@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Portuguese",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Shane Jackson": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "shane.jackson@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Sophie Nicholson": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "sophie.nicholson@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Yosephine Devina Tiurma": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "yosephinedevina.tiurma@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Zakia Arif": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Natalie Lewis",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "zakia.arif@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "James Sharpe": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - Red",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "james.sharpe@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Aby Elie": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "aby.elie@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Danish",
                                                                                                    "Norwegian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Aneek Sarkar": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "aneek.sarkar@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Danish",
                                                                                                    "Norwegian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Charlotte Boyce": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "charlotte.boyce@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Mark Greig": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "mark.greig@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Raffaela Martuccio": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "rafaella.martuccio@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Rohan Magon": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "rohan.magon@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Xue-er Su": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "James Sharpe",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "xue-er.su@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Mandarin",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Tim Staig": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - Blue",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "tim.staig@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Brian Gallagher": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "brian.gallagher@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Daniel Power": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "daniel.power@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Karim Kasem": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "karim.kasem@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Lawrence Southgate": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "lawrence.southgate@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                ['Power BI'],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Maciej Furmanczyk": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "maciej.furmanczyk@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Max Macleod": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "max.mcleod@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Miodrag Vidic": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "miodrag.vidic.su@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Serbian",
                                                                                                    "Croatian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Nicholas Michael": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "nicholas.michael@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Nuno Camara": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "nuno.camara@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Portuguese",
                                                                                                    "Spanish",
                                                                                                    "French",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Sachin Rajput": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "sachin.rajput@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Slobodan Topovic": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "slobodan.topovic@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                ['Power BI'],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English",
                                                                                                    "Serbian",
                                                                                                    "Croatian",
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Stewart Mott": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "stewart.mott@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Xue-er Su": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tim Staig",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Media Analyst",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "zakia.uddin@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Tom Millward": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - Proofing",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "tom.millward@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Alec Holt": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tom Millward",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Sub-editor",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "alec.holt@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Edward Caddy": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tom Millward",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Sub-editor",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "edward.caddy@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                    "Romy Mitchell": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Tom Millward",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Sub-editor",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "romy.mitchell@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Gabriel Dabner": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Team Leader - Presswatch",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "gabriel.dabner@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {
                                                                                    "Victor Ume": OrderedDict(
                                                                                        [
                                                                                            (
                                                                                                "Reports_to",
                                                                                                "Gabriel Dabner",
                                                                                            ),
                                                                                            (
                                                                                                "Position",
                                                                                                "Analyst - Presswatch",
                                                                                            ),
                                                                                            (
                                                                                                "City",
                                                                                                "London",
                                                                                            ),
                                                                                            (
                                                                                                "e-mail",
                                                                                                "victor.ume@onclusive.com",
                                                                                            ),
                                                                                            (
                                                                                                "skills",
                                                                                                [],
                                                                                            ),
                                                                                            (
                                                                                                "languages",
                                                                                                [
                                                                                                    "English"
                                                                                                ],
                                                                                            ),
                                                                                            (
                                                                                                "Direct_Reports",
                                                                                                {},
                                                                                            ),
                                                                                        ]
                                                                                    )
                                                                                },
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Hannah Jackson": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Operations Support Manager",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "hannah.jackson@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {},
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    "Daniel Travers": OrderedDict(
                                                                        [
                                                                            (
                                                                                "Reports_to",
                                                                                "Luke Constable",
                                                                            ),
                                                                            (
                                                                                "Position",
                                                                                "Insight Development Serior Analyst",
                                                                            ),
                                                                            (
                                                                                "City",
                                                                                "London",
                                                                            ),
                                                                            (
                                                                                "e-mail",
                                                                                "daniel.travers@onclusive.com",
                                                                            ),
                                                                            (
                                                                                "skills",
                                                                                [],
                                                                            ),
                                                                            (
                                                                                "languages",
                                                                                [
                                                                                    "English"
                                                                                ],
                                                                            ),
                                                                            (
                                                                                "Direct_Reports",
                                                                                {},
                                                                            ),
                                                                        ]
                                                                    ),
                                                                },
                                                            ),
                                                        ]
                                                    ),
                                                    "Rob Manley": OrderedDict(
                                                        [
                                                            (
                                                                "Reports_to",
                                                                "Lisa Travers",
                                                            ),
                                                            (
                                                                "Position",
                                                                "Insight Development Leader",
                                                            ),
                                                            ("City", "London"),
                                                            (
                                                                "e-mail",
                                                                "rob.manley@onclusive.com",
                                                            ),
                                                            ("skills", []),
                                                            (
                                                                "languages",
                                                                ["English", "French"],
                                                            ),
                                                            ("Direct_Reports", {}),
                                                        ]
                                                    ),
                                                },
                                            ),
                                        ]
                                    ),
                                },
                            ),
                        ]
                    ),
                    "Jason Revel": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "Program Manager"),
                            ("City", "London"),
                            ("e-mail", "jason.revel@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English"]),
                            ("Direct_Reports", {}),
                        ]
                    ),
                    "Rene-Jean Corneille": OrderedDict(
                        [
                            ("Reports_to", "Rob Stone"),
                            ("Position", "Director of Engineering (Machine Learning)"),
                            ("City", "London"),
                            ("e-mail", "rene-jean.corneille@onclusive.com"),
                            ("skills", []),
                            ("languages", ["English", "French"]),
                            ("Direct_Reports", {}),
                        ]
                    ),
                },
            ),
        ]
    )
}


# def print_positions(org_chart):
#     for name, info in org_chart.items():
#         print(f"Name: {name}\t\tPosition: {info['Position']}")
#         if 'Direct_Reports' in info:
#             print_positions(info['Direct_Reports'])

# print_positions(org_chart)


# function used once for adding 'Reports_to' key for each person

# def add_reports_to(chart, boss=None):
#     for staff, details in chart.items():
#         if boss is not None:  # if there is a boss, add 'Reports_to'
#             details = OrderedDict([('Reports_to', boss)] + list(details.items()))
#             chart[staff] = details
#         if details['Direct_Reports']:  # if there are any direct reports
#             add_reports_to(details['Direct_Reports'], staff)

#     return chart