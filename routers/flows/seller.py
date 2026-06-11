from helpers.whatsapp_client import send_button, send_list, send_text
from helpers.session import update_session, get_session
from routers.flows.buyer import LOCATIONS, SUB_TYPES, PROPERTY_TYPE_LABELS


async def start_seller_flow(phone: str):
    await send_button(
        to=phone,
        body=(
            "Great! Let's list your property 🏠\n\n"
            "We'll collect a few details and our team will get your listing live.\n\n"
            "What *type* of property are you listing?"
        ),
        buttons=["🏘 Residential", "🏢 Commercial", "🌾 Agricultural"],
        header="📋 Post Your Property"
    )
    update_session(phone, {"flow": "seller", "step": "property_type"})


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
        body=f"Got it! Now select the *{label}* property type:",
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
            f"Nice! Listing a *{row_title}* 🏠\n\n"
            "📍 Where is the property located?"
        ),
        button_label="Select Area",
        sections=sections,
        header="📍 Property Location"
    )
    update_session(phone, {"step": "location"})


async def handle_location(phone: str, row_id: str, row_title: str):
    update_session(phone, {"location": row_id, "location_label": row_title})

    await send_text(
        phone,
        (
            f"Perfect! *{row_title}* selected 📍\n\n"
            "💰 What is your *asking price?*\n\n"
            "Just type it — for example:\n"
            "• _45 lakhs_\n"
            "• _1.2 crore_\n"
            "• _85,00,000_"
        )
    )
    update_session(phone, {"step": "price"})


async def handle_price(phone: str, text: str):
    update_session(phone, {"price": text})

    await send_text(
        phone,
        (
            "Got it! 💰\n\n"
            "📝 Now give us a *brief description* of your property.\n\n"
            "Include details like:\n"
            "• Number of bedrooms / floors\n"
            "• Area in sqft\n"
            "• Age of property\n"
            "• Any key features\n\n"
            "_Example: 3BHK flat, 1400 sqft, 5 years old, 3rd floor, parking included_"
        )
    )
    update_session(phone, {"step": "description"})


async def handle_description(phone: str, text: str):
    update_session(phone, {"description": text})
    session = get_session(phone)
    _save_listing(phone, session)

    sub_type = session.get("sub_type_label", "Property")
    location = session.get("location_label", "Hyderabad")
    price = session.get("price", "")

    await send_button(
        to=phone,
        body=(
            "✅ *Your listing has been submitted!*\n\n"
            f"🏷 *Type:* {sub_type}\n"
            f"📍 *Location:* {location}\n"
            f"💰 *Price:* {price}\n\n"
            "Our team will review and *publish your listing within 24 hours* 🎉\n\n"
            "We'll notify you once it's live!"
        ),
        buttons=["🏠 Main Menu", "➕ Add Another"],
        header="🎉 Listing Submitted!"
    )
    update_session(phone, {"step": "post_listing"})


def _save_listing(phone: str, session: dict):
    from database import SessionLocal
    from models.db import WALead, LeadType

    db = SessionLocal()
    try:
        lead = WALead(
            phone_number=phone,
            lead_type=LeadType.seller,
            data={
                "property_type": session.get("property_type_label"),
                "sub_type": session.get("sub_type_label"),
                "location": session.get("location_label"),
                "price": session.get("price"),
                "description": session.get("description"),
            }
        )
        db.add(lead)
        db.commit()
    finally:
        db.close()
