from typing import Literal

AllowedLocationTypes = Literal[
    "Park",
    "park",
    "Meadow",
    "meadow",
    "Fenced meadow",
    "fenced meadow",
    "Beach",
    "beach",
    "Other",
    "other",
]
AllowedLocationSizes = Literal[
    "Mini",
    "mini",
    "Small",
    "small",
    "Medium",
    "medium",
    "Large",
    "large",
    "Giant",
    "giant",
]
AllowedPetEnergies = Literal[1, 2, 3, 4, 5]
AllowedPetSizes = Literal[
    "Mini",
    "mini",
    "Small",
    "small",
    "Medium",
    "medium",
    "Large",
    "large",
    "Giant",
    "giant",
]
AllowedReviewGrades = Literal[1, 2, 3, 4, 5]
AllowedTagColors = Literal[
    "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
]
