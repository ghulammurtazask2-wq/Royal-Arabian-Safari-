"""
Royal Arabian Safari — complete price list extracted from arabiansafariroyal.com
All prices are per car (private 4x4) unless noted.
"""

SERVICES = {
    # ── DESERT SAFARIS ──────────────────────────────────────────────────────
    "desert_safari_dubai": {
        "name": "Desert Safari Dubai (Family / Standard)",
        "price_aed": 799,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/family-desert-safari-dubai/",
        "includes": [
            "Private 4×4 with experienced driver",
            "Dune bashing",
            "Sandboarding (AED 35 included)",
            "Camel ride (short, free)",
            "BBQ dinner at Bedouin camp",
            "Belly dance & Tanoura show",
            "Hotel pickup & drop-off",
        ],
        "note": "Up to 6 guests. Children free.",
    },
    "vip_desert_safari_dubai": {
        "name": "VIP Desert Safari Dubai",
        "price_aed": 999,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/vip-desert-safari-dubai/",
        "includes": [
            "Private VIP camp with dedicated seating",
            "Premium BBQ dinner",
            "Dune bashing",
            "Sandboarding & camel ride",
            "Live entertainment",
            "Hotel pickup & drop-off",
        ],
        "note": "Best for special occasions.",
    },
    "sunrise_desert_safari_dubai": {
        "name": "Sunrise Desert Safari Dubai",
        "price_aed_from": 799,
        "price_aed_to": 999,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/sunrise-desert-safari-dubai/",
        "includes": ["Early morning pickup", "Sunrise dune bashing", "Breakfast in the desert"],
        "note": "Early morning experience — departs before sunrise.",
    },
    "romantic_desert_safari_dubai": {
        "name": "Romantic Desert Safari Dubai",
        "price_aed": 899,
        "unit": "for two",
        "url": "https://www.arabiansafariroyal.com/romantic-desert-safari-dubai/",
        "includes": ["Private setup for two", "Candle-lit dinner", "Rose petals & decoration", "Dune bashing"],
        "note": "Perfect for couples & honeymoons.",
    },
    "corporate_desert_safari_dubai": {
        "name": "Corporate Desert Safari Dubai",
        "price_aed": 799,
        "price_per_seat_aed": 50,
        "unit": "per car (or AED 50/seat for large groups)",
        "url": "https://www.arabiansafariroyal.com/corporate-desert-safari-dubai/",
        "includes": ["Multiple vehicles for large groups", "Team activities", "BBQ dinner"],
        "note": "Call for group pricing on 10+ pax.",
    },
    "abu_dhabi_desert_safari": {
        "name": "Abu Dhabi Desert Safari",
        "price_aed_from": 35,
        "unit": "per person (seat in shared vehicle)",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-desert-safari-tours/",
        "includes": [
            "Dune bashing",
            "Camel ride",
            "BBQ dinner",
            "Live entertainment",
        ],
        "note": "Private car also available from AED 799. Children free, no deposit, cancel free up to 12 hours.",
    },

    # ── CITY TOURS ───────────────────────────────────────────────────────────
    "dubai_city_tour": {
        "name": "Dubai City Tour",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/dubai-city-tour/",
        "includes": ["Burj Khalifa area", "Old Dubai (Al Fahidi)", "Gold & Spice Souks", "Palm Jumeirah", "Hotel pickup"],
        "note": "Private 4×4. Up to 6 guests. Children free.",
    },
    "full_day_dubai_city_tour": {
        "name": "Full-Day Dubai City Tour (8 hours)",
        "price_aed": 899,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/full-day-dubai-city-tour/",
        "includes": ["8 hours", "Old & New Dubai", "Private 4×4 with driver", "Hotel pickup"],
        "note": "Best for first-timers wanting full coverage.",
    },
    "abu_dhabi_city_tour": {
        "name": "Abu Dhabi City Tour",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-city-tour/",
        "includes": [
            "Sheikh Zayed Grand Mosque (access pass booked for you)",
            "Corniche",
            "Qasr Al Watan area",
            "Hotel pickup from Dubai or Abu Dhabi",
        ],
        "note": "Children free. Cancel free to 12 hours.",
    },
    "full_day_abu_dhabi_city_tour": {
        "name": "Full-Day Abu Dhabi City Tour",
        "price_aed": 899,
        "unit": "per car (up to 6 guests)",
        "url": "https://www.arabiansafariroyal.com/full-day-abu-dhabi-city-tour/",
        "includes": ["Full day inside Qasr Al Watan or Louvre Abu Dhabi", "Grand Mosque", "Hotel pickup"],
        "note": "WhatsApp: +971 58 228 2683",
    },
    "old_dubai_city_tour": {
        "name": "Old Dubai City Tour",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/old-dubai-city-tour/",
        "includes": ["Al Fahidi wind towers", "Creek abra ride", "Gold Souk", "Spice Souk"],
        "note": "Half-day experience.",
    },
    "abu_dhabi_city_tour_from_dubai": {
        "name": "Abu Dhabi City Tour from Dubai",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-city-tour-from-dubai/",
        "includes": ["Tolls & fuel included", "Mosque access pass", "Hotel pickup from Dubai"],
        "note": "Free cancellation to 12 hours.",
    },

    # ── NIGHT TOURS ──────────────────────────────────────────────────────────
    "dubai_night_tour": {
        "name": "Dubai Night Tour",
        "price_aed": 699,
        "price_usd": 190,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/dubai-night-tour/",
        "includes": ["Burj Khalifa light show", "Dubai Fountain", "JBR Marina", "Gold Souk at night"],
        "note": "Perfect for evening arrivals.",
    },
    "abu_dhabi_night_layover_tour": {
        "name": "Abu Dhabi Night Layover Tour",
        "price_aed": 899,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-night-layover-tour/",
        "includes": ["Grand Mosque night visit", "Corniche at night", "Hotel / cruise drop-off"],
        "note": "Night-specific — includes mosque evening timings.",
    },

    # ── LAYOVER & STOPOVER TOURS ─────────────────────────────────────────────
    "dubai_airport_layover_tour": {
        "name": "Dubai Airport Layover Tour",
        "price_aed": 699,
        "price_usd": 190,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/dubai-airport-layover-tour/",
        "includes": ["Flight tracked", "Bags in car", "Back 3 hours before departure"],
        "note": "Only if you have 5+ usable hours after immigration.",
    },
    "abu_dhabi_layover_tour": {
        "name": "Abu Dhabi Layover Tour",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-layover-tour/",
        "includes": ["Timed to your flight", "Flight tracked", "Back 3 hours before departure"],
        "note": "Under 5 hours — stay in the airport.",
    },
    "dubai_stopover_tour": {
        "name": "Dubai Stopover Tour",
        "price_aed": 699,
        "price_usd": 190,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/dubai-stopover-tour/",
    },

    # ── TRANSFERS ────────────────────────────────────────────────────────────
    "dubai_airport_transfer": {
        "name": "Dubai Airport Transfer",
        "price_aed": 799,
        "unit": "per car (fixed)",
        "url": "https://www.arabiansafariroyal.com/dubai-airport-transfer/",
        "includes": ["Meet & greet", "Flight tracked", "Hotel drop-off"],
    },
    "abu_dhabi_airport_transfer": {
        "name": "Abu Dhabi Airport Transfer",
        "price_note": "Fixed price — WhatsApp for exact quote",
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-airport-transfer/",
        "includes": ["Meet & greet in arrivals", "Driver waits"],
        "note": "AUH taxi is AED 74–80; our transfer is fixed price with meet & greet.",
    },
    "desert_safari_from_dubai_airport": {
        "name": "Desert Safari from Dubai Airport",
        "price_aed": 799,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/desert-safari-from-dubai-airport/",
    },
    "car_with_driver_dubai": {
        "name": "Car with Driver Dubai (Hourly)",
        "price_aed_sedan": 250,
        "price_aed_land_cruiser": 350,
        "unit": "per hour",
        "url": "https://www.arabiansafariroyal.com/car-with-driver-dubai/",
        "includes": ["Tolls, fuel, parking & child seats included"],
    },
    "car_with_driver_abu_dhabi": {
        "name": "Car with Driver Abu Dhabi (Hourly)",
        "price_note": "Similar to Dubai — WhatsApp for rates",
        "url": "https://www.arabiansafariroyal.com/car-with-driver-in-abu-dhabi/",
    },

    # ── SPECIALTY TOURS ──────────────────────────────────────────────────────
    "dubai_to_hatta_tour": {
        "name": "Dubai to Hatta Tour",
        "price_aed": 1199,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/dubai-to-hatta-tour/",
        "includes": ["Hatta Dam", "Mountain pools", "Heritage village"],
    },
    "sheikh_zayed_mosque_tour": {
        "name": "Sheikh Zayed Grand Mosque Tour",
        "price_aed": 699,
        "unit": "per car",
        "url": "https://www.arabiansafariroyal.com/sheikh-zayed-grand-mosque-tour/",
        "includes": ["Access pass booked in advance", "Dress code briefed", "Driver waits", "Hotel pickup"],
        "note": "Mosque entry is free. Private car from AED 699.",
    },
    "abu_dhabi_city_tour_baps": {
        "name": "Abu Dhabi City Tour with BAPS Temple",
        "price_note": "Per car — WhatsApp for exact price",
        "url": "https://www.arabiansafariroyal.com/abu-dhabi-city-tour-with-baps-temple/",
        "includes": ["BAPS Hindu Mandir registration done in advance", "Per car — children free"],
    },

    # ── ADD-ONS ──────────────────────────────────────────────────────────────
    "bbq_dinner": {
        "name": "BBQ Dinner (Desert Safari Add-on)",
        "price_aed": 35,
        "unit": "per person",
    },
    "dune_bashing": {
        "name": "Dune Bashing",
        "price_aed": 50,
        "unit": "per person",
    },
    "sandboarding": {
        "name": "Sandboarding",
        "price_aed": 35,
        "unit": "per person (usually included)",
    },
    "camel_ride_short": {
        "name": "Camel Ride (Short)",
        "price_aed": 0,
        "unit": "free — included in safari",
    },
    "camel_ride_long": {
        "name": "Camel Ride (Long)",
        "price_aed": 300,
        "unit": "per ride",
        "url": "https://www.arabiansafariroyal.com/camel-ride-dubai/",
    },
}

BOOKING_POLICIES = """
• All tours priced PER CAR, not per person — up to 6 guests per vehicle.
• Children FREE on all private tours.
• NO deposit required to book.
• FREE cancellation up to 12 hours before pickup.
• No credit card fees.
• Hotel pickup & drop-off included on all tours.
• Tolls, fuel & parking included.
• We track your flight for airport pickups.
"""

WHATSAPP_NUMBER = "+971582282683"
OWNER_WHATSAPP = "+971582282683"  # Owner's notification number

WEBSITE = "https://www.arabiansafariroyal.com"

QUICK_PRICE_SUMMARY = """
🏜️ *Royal Arabian Safari — Price Summary*

*Desert Safaris (Dubai)*
• Standard/Family Safari — AED 799/car
• VIP Safari — AED 999/car
• Sunrise Safari — AED 799–999/car
• Romantic Safari — AED 899 (for 2)
• Corporate — AED 799/car or AED 50/seat

*Desert Safari (Abu Dhabi)*
• Shared seat — from AED 35/person
• Private car — AED 799/car

*City Tours*
• Dubai City Tour — AED 699/car
• Full Day Dubai Tour (8h) — AED 899/car
• Old Dubai Tour — AED 699/car
• Abu Dhabi City Tour — AED 699/car
• Full Day Abu Dhabi Tour — AED 899/car
• Abu Dhabi Tour from Dubai — AED 699/car

*Night & Layover Tours*
• Dubai Night Tour — AED 699/car
• Dubai Airport Layover Tour — AED 699/car
• Abu Dhabi Layover Tour — AED 699/car
• Abu Dhabi Night Tour — AED 899/car

*Specialty*
• Dubai to Hatta Tour — AED 1,199/car
• Sheikh Zayed Mosque Tour — AED 699/car

*Transfers*
• Dubai Airport Transfer — AED 799/car
• Car with Driver — AED 250–350/hr

✅ All prices per car • Children free • No deposit • Cancel free 12h before
"""
