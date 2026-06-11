import logging
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key="local",
    base_url=settings.local_llm_url,
)

SYSTEM_PROMPT = """You are a helpful WhatsApp assistant for Gazam Associates, Hyderabad's trusted real estate platform.

About Gazam Associates:
- Based in Hyderabad, Telangana, India
- Services: Buy property, Sell/Post property, Home loans, Talk to agent, Support
- Areas covered: Gachibowli, Hitech City, Miyapur, Kompally, Kukatpally, Madhapur, Banjara Hills, Jubilee Hills, Manikonda, Narsingi, and more
- Property types: Residential (flats, villas, plots, studios), Commercial (offices, shops, warehouses), Agricultural (farmland, farmhouse)

Your job:
- Answer questions about Hyderabad real estate — prices, areas, market trends, loan eligibility, documentation, etc.
- Be friendly, concise, and helpful
- Keep responses SHORT — this is WhatsApp, not a webpage. Max 3-4 sentences unless the user asks for detail
- Do NOT use markdown headers or bullet formatting — plain text only, use line breaks
- When a user wants to buy/sell/apply for loan/talk to agent, guide them: "Tap the menu below or type 'menu' to get started"
- If you don't know something specific to Gazam's listings or pricing, say so honestly and offer to connect them with an agent

Always respond in the same language the user writes in (English, Telugu, or Hindi)."""


async def get_ai_response(phone: str, user_message: str, history: list[dict]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include last few exchanges for context (keep token usage low)
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model="gemma",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"AI error for {phone}: {e}")
        return (
            "Sorry, I couldn't process that right now 😔\n\n"
            "Type *menu* to explore our services or try again in a moment."
        )
