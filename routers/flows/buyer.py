from helpers.whatsapp_client import send_button, send_list
from helpers.session import update_session, get_session

LOCATIONS = [
    ("loc_gachi",    "Gachibowli",    "IT hub, premium apartments"),
    ("loc_hitech",   "Hitech City",   "Tech corridor, great connectivity"),
    ("loc_miyapur",  "Miyapur",       "Affordable & fast growing"),
    ("loc_kompally", "Kompally",      "North Hyd, peaceful locality"),
    ("loc_kuka",     "Kukatpally",    "Well connected, family friendly"),
    ("loc_madha",    "Madhapur",      "Prime location, high demand"),
    ("loc_banjara",  "Banjara Hills", "Premium & luxury properties"),
    ("loc_jubilee",  "Jubilee Hills", "Upscale residential area"),
    ("loc_manik",    "Manikonda",     "Affordable, near IT parks"),
    ("loc_narsi",    "Narsingi",      "Emerging area, great value"),
]

BUDGETS = [
    ("budget_30",     "Under ₹30 Lakhs",  "Entry level & affordable"),
    ("budget_30_60",  "₹30L – ₹60L",      "Mid range properties"),
    ("budget_60_1cr", "₹60L – ₹1 Crore",  "Premium properties"),
    ("budget_1_2cr",  "₹1Cr – ₹2 Crore",  "Luxury segment"),
    ("budget_2cr",    "Above ₹2 Crore",    "Ultra luxury & exclusive"),
]

SUB_TYPES = {
    "btn_0": [
        ("sub_flat",   "🏢 Flat / Apartment",  "Ready to move & under construction"),
        ("sub_villa",  "🏡 Villa / Row House",  "Independent luxury living"),
        ("sub_house",  "🏠 Independent House",  "Your own standalone home"),
        ("sub_plot",   "📐 Residential Plot",   "Build your dream home"),
        ("sub_studio", "🛋 Studio Apartment",   "Compact & affordable"),
    ],
    "btn_1": [
        ("sub_office",     "🏢 Office Space",       "Ready to use workspaces"),
        ("sub_shop",       "🏪 Shop / Showroom",    "Prime retail locations"),
        ("sub_warehouse",  "🏭 Warehouse / Godown", "Storage & logistics"),
        ("sub_complot",    "📐 Commercial Plot",    "Build your business hub"),
    ],
    "btn_2": [
        ("sub_farmland",   "🌾 Farm Land",       "Agricultural land parcels"),
        ("sub_farmhouse",  "🏡 Farm House",      "Weekend getaway & investment"),
        ("sub_plantation", "🌳 Plantation Land", "Coffee, coconut & more"),
    ],
}

PROPERTY_TYPE_LABELS = {
    "btn_0": "Residential",
    "btn_1": "Commercial",
    "btn_2": "Agricultural",
}


async def start_buyer_flow(phone: str):
    await send_button(
        to=phone,
        body=(
            "Great choice! 🏠 Let's find your perfect property.\n\n"
            "First, what *type* of property are you looking for?"
        ),
        buttons=["🏘 Residential", "🏢 Commercial", "🌾 Agricultural"],
        header="🔍 Find Property"
    )
    update_session(phone, {"flow": "buyer", "step": "property_type"})


async def handle_property_type(phone: str, button_id: str):
    sub_types = SUB_TYPES.get(button_id, SUB_TYPES["btn_0"])
    label = PROPERTY_TYPE_LABELS.get(button_id, "Residential")

    update_session(phone, {"property_type": button_id, "property_type_label": label})

    sections = [{
        "title": f"{label} Types",
        "rows": [
            {"id": sid, "title": title, "description": desc}
            for sid, title, desc in sub_types
        ]
    }]

    await send_list(
        to=phone,
        body=f"Perfect! 👍 Now choose the *{label}* property type:",
        button_label="Select Type",
        sections=sections,
        header=f"🏷 {label} Properties"
    )
    update_session(phone, {"step": "sub_type"})


async def handle_sub_type(phone: str, row_id: str, row_title: str):
    update_session(phone, {"sub_type": row_id, "sub_type_label": row_title})

    sections = [{
        "title": "📍 Hyderabad Areas",
        "rows": [
            {"id": lid, "title": title, "description": desc}
            for lid, title, desc in LOCATIONS
        ]
    }]

    await send_list(
        to=phone,
        body=(
            f"Nice! Looking for *{row_title}* 🏠\n\n"
            "📍 Which area in Hyderabad are you interested in?"
        ),
        button_label="Select Area",
        sections=sections,
        header="📍 Choose Location"
    )
    update_session(phone, {"step": "location"})


async def handle_location(phone: str, row_id: str, row_title: str):
    update_session(phone, {"location": row_id, "location_label": row_title})

    sections = [{
        "title": "💰 Your Budget Range",
        "rows": [
            {"id": bid, "title": title, "description": desc}
            for bid, title, desc in BUDGETS
        ]
    }]

    await send_list(
        to=phone,
        body=(
            f"Great choice! *{row_title}* is a wonderful area 📍\n\n"
            "💰 What's your budget range?"
        ),
        button_label="Select Budget",
        sections=sections,
        header="💰 Budget Range"
    )
    update_session(phone, {"step": "budget"})


async def handle_budget(phone: str, row_id: str, row_title: str):
    update_session(phone, {"budget": row_id, "budget_label": row_title, "step": "results"})
    await send_mock_results(phone)


async def send_mock_results(phone: str):
    session = get_session(phone)
    location = session.get("location_label", "Hyderabad")
    sub_type = session.get("sub_type_label", "Property")
    budget = session.get("budget_label", "")

    # WhatsApp enforces 24-char max on list row titles
    mock_properties = [
        {
            "id": "prop_1",
            "title": "3BHK – Property #1",
            "description": f"1450 sqft, Ready to move | {budget}"
        },
        {
            "id": "prop_2",
            "title": "2BHK – Property #2",
            "description": f"1100 sqft, New launch | {budget}"
        },
        {
            "id": "prop_3",
            "title": "Premium – Property #3",
            "description": f"1800 sqft, Gated community | {budget}"
        },
    ]

    sections = [{"title": "🏠 Top Matches For You", "rows": mock_properties}]

    await send_list(
        to=phone,
        body=(
            f"🎉 Found *{len(mock_properties)} properties* matching your search!\n\n"
            f"📍 *Location:* {location}\n"
            f"🏷 *Type:* {sub_type}\n"
            f"💰 *Budget:* {budget}\n\n"
            "👇 Tap on a property to register your interest:"
        ),
        button_label="View Properties",
        sections=sections,
        header="🔍 Search Results"
    )
    update_session(phone, {"step": "enquiry"})


async def handle_enquiry(phone: str, row_id: str, row_title: str):
    session = get_session(phone)
    _save_lead(phone, session, row_id, row_title)

    await send_button(
        to=phone,
        body=(
            f"✅ *Interest registered!*\n\n"
            f"🏠 *Property:* {row_title}\n\n"
            "Our team will call you within *2 working hours* 📞\n\n"
            "What would you like to do next?"
        ),
        buttons=["🏠 Main Menu", "🔍 More Properties"],
        header="🎉 We Got Your Request!"
    )
    update_session(phone, {"step": "post_enquiry"})


def _save_lead(phone: str, session: dict, prop_id: str, prop_title: str):
    from database import SessionLocal
    from models.db import WALead, LeadType

    db = SessionLocal()
    try:
        lead = WALead(
            phone_number=phone,
            lead_type=LeadType.buyer,
            data={
                "property_id": prop_id,
                "property_title": prop_title,
                "property_type": session.get("property_type_label"),
                "sub_type": session.get("sub_type_label"),
                "location": session.get("location_label"),
                "budget": session.get("budget_label"),
            }
        )
        db.add(lead)
        db.commit()
    finally:
        db.close()
