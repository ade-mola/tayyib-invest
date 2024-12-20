import os

from dotenv import load_dotenv


load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_PROMPT = """Provide comprehensive analysis of {} from multiple perspectives:
1. Shariah Compliance Assessment
2. Financial Health Overview
3. Potential Ethical Concerns
4. Recommendations for Islamic Investors
Context:
- Latest financial report date: {}
- Market Cap: ${}
- Is Business Activity Halal: {}
- Debt-Market Cap Ratio: {}%
- Non-Halal Income Ratio: {}%
- Cash-Market Cap ratio: {}%
- Liquidity Ratio: {}%
Analyze considering AAOIFI Shari’ah Standard No. (21) and other Islamic financial standards.
"""
