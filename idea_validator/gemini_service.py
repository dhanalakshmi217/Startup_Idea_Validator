import os
import json
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

# System instructions to guide Gemini in generating the structured analysis
SYSTEM_INSTRUCTION = """You are an expert startup advisor, venture capitalist, and business strategist.
Your task is to analyze the user's startup idea based on the provided target audience, budget, and industry.
You MUST analyze the idea and return your complete response in structured JSON format matching the schema below.
Ensure your analysis is highly detailed, realistic, specific to the inputs, and actionable.

JSON Schema format:
{
  "swot": {
    "strengths": ["string"],
    "weaknesses": ["string"],
    "opportunities": ["string"],
    "threats": ["string"]
  },
  "competitors": {
    "competitors": [
      {
        "name": "string",
        "market_share": "string",
        "strengths": ["string"],
        "weaknesses": ["string"]
      }
    ],
    "differentiation_strategy": "string"
  },
  "business_model": {
    "value_proposition": "string",
    "customer_segments": ["string"],
    "channels": ["string"],
    "key_partners": ["string"],
    "cost_structure": ["string"]
  },
  "marketing_plan": {
    "channels": ["string"],
    "tactics": ["string"],
    "go_to_market_steps": ["string"]
  },
  "revenue_model": {
    "pricing_strategy": "string",
    "monetization_options": ["string"],
    "projected_costs": "string",
    "estimated_margins": "string"
  },
  "risks": [
    {
      "risk_name": "string",
      "impact": "High" | "Medium" | "Low",
      "mitigation_strategy": "string"
    }
  ],
  "improvements": [
    {
      "area": "string",
      "suggestion": "string"
    }
  ],
  "investor_pitch": {
    "hook": "string",
    "problem": "string",
    "solution": "string",
    "market_size": "string",
    "financial_projections": "string",
    "the_ask": "string"
  }
}
"""

def generate_validation_report(idea, target_audience, budget, industry):
    """
    Generates a startup validation report using Gemini API.
    If the API key is missing or calls fail, falls back to generating realistic mock data.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.warning("GEMINI_API_KEY is not set. Generating mock analysis report.")
        return generate_mock_report(idea, target_audience, budget, industry, mode="Demo Mode (API Key Missing)")

    try:
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash as the fast and reliable model for text tasks
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        prompt = f"""
        Analyze this startup idea:
        - Startup Idea: {idea}
        - Target Audience: {target_audience}
        - Budget: {budget}
        - Industry: {industry}
        
        Please evaluate and generate:
        1. SWOT Analysis
        2. Competitor Analysis (identify 2-3 realistic competitors)
        3. Business Model
        4. Marketing Plan
        5. Revenue Model
        6. Risks and mitigation strategies
        7. Key improvements and iterations
        8. Investor Pitch
        
        Return ONLY a JSON object matching the requested schema.
        """
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse and return JSON
        report_data = json.loads(response.text)
        report_data['generation_mode'] = "AI Generated"
        return report_data

    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}. Falling back to mock data.")
        return generate_mock_report(
            idea, target_audience, budget, industry, 
            mode=f"Demo Mode (API call failed: {str(e)[:50]}...)"
        )

def generate_mock_report(idea, target_audience, budget, industry, mode="Demo Mode"):
    """
    Generates high-quality, customized mock report data.
    Uses input fields to interpolate values so that the analysis feels genuine.
    """
    return {
        "generation_mode": mode,
        "swot": {
            "strengths": [
                f"Directly addresses the needs of {target_audience} with a tailored solution.",
                f"Optimized cost structure aligned with the starting budget of {budget}.",
                f"Leverages modern digital tools in the {industry} space for low overhead."
            ],
            "weaknesses": [
                f"Limited initial budget ({budget}) might constrain aggressive customer acquisition.",
                "Lack of established brand presence makes building initial trust harder.",
                "Heavy dependency on organic growth channels in the early stages."
            ],
            "opportunities": [
                f"Rapid expansion inside the underserved segments of {target_audience}.",
                f"Partnering with micro-influencers or niche communities focusing on {industry}.",
                "Introducing premium tiers or value-added services as user base grows."
            ],
            "threats": [
                "Established incumbents in the market copy the core feature set.",
                "Platform dependency if relying heavily on third-party APIs or social networks.",
                "Changes in consumer sentiment or regulations within the path of the startup."
            ]
        },
        "competitors": {
            "competitors": [
                {
                    "name": f"Legacy {industry} Players",
                    "market_share": "60%",
                    "strengths": ["High brand awareness", "Deep financial pockets", "Comprehensive product line"],
                    "weaknesses": ["Slow to adapt to new trends", "Not focused on target audience", "High pricing structures"]
                },
                {
                    "name": "Niche Tech Challengers",
                    "market_share": "15%",
                    "strengths": ["Modern UX", "Agile development", "Feature-rich"],
                    "weaknesses": ["Poor customer retention", "Unclear monetization model", "Fragmented focus"]
                }
            ],
            "differentiation_strategy": f"Focus strictly on {target_audience} by offering a highly simplified, cost-effective tool built specifically to solve their main pain point, bypassing the bloated feature sets of legacy {industry} competitors."
        },
        "business_model": {
            "value_proposition": f"Providing a seamless, affordable way for {target_audience} to leverage {idea} without the complexity and high cost of existing options.",
            "customer_segments": [
                f"{target_audience} looking for efficient solutions.",
                f"Early adopters in the {industry} sector.",
                "Cost-conscious customers looking for high value-to-cost ratio."
            ],
            "channels": [
                "Direct-to-consumer digital portal / app store.",
                "Content marketing, blogs, and SEO focused on the target segment.",
                "Word of mouth and community referral programs."
            ],
            "key_partners": [
                f"Infrastructure and hosting providers to support scale on a budget of {budget}.",
                "Niche content creators and community leaders.",
                f"Data or API providers specialized in {industry}."
            ],
            "cost_structure": [
                "Software development and server infrastructure maintenance.",
                "Customer support and success operations.",
                "Targeted organic and paid digital marketing campaigns."
            ]
        },
        "marketing_plan": {
            "channels": [
                "Organic Search (SEO) targeting specific buyer intent queries.",
                "Niche online communities (Reddit, Discord, LinkedIn groups).",
                "Direct cold outreach and email newsletter nurturing."
            ],
            "tactics": [
                f"Create a free utility tool related to {industry} to capture lead emails.",
                f"Publish comprehensive guides addressing how {target_audience} can solve their problems.",
                "Offer a transparent, risk-free trial option to minimize entry friction."
            ],
            "go_to_market_steps": [
                "Phase 1: Build a minimal landing page to capture early sign-ups and validate messaging.",
                "Phase 2: Launch a beta version to the first 100 users for feedback and iteration.",
                f"Phase 3: Roll out official pricing and launch community marketing campaigns targeting {target_audience}."
            ]
        },
        "revenue_model": {
            "pricing_strategy": "Value-based pricing starting with a low-tier subscription model to build customer lock-in, scaling to usage-based fees.",
            "monetization_options": [
                "Monthly SaaS / membership subscription.",
                "Pay-as-you-go usage credits.",
                "Premium add-on features and custom integrations."
            ],
            "projected_costs": f"Minimal infrastructure and licensing overhead, estimated around 15-20% of the {budget} budget annually.",
            "estimated_margins": "Expected gross margins of 75-80% once initial development phases settle."
        },
        "risks": [
            {
                "risk_name": "Low User Adoption",
                "impact": "High",
                "mitigation_strategy": "Conduct weekly user interviews, iterate quickly on feedback, and pivots features to address actual friction points."
            },
            {
                "risk_name": "Budget Depletion",
                "impact": "Medium",
                "mitigation_strategy": f"Adopt a strict bootstrapping mindset, limit headcount, and prioritize revenue-generating activities within the initial {budget} pool."
            },
            {
                "risk_name": "Technical Scalability Issues",
                "impact": "Low",
                "mitigation_strategy": "Use serverless architectures and scalable cloud solutions that grow dynamically only as user volume increases."
            }
        ],
        "improvements": [
            {
                "area": "Onboarding Friction",
                "suggestion": "Introduce a 1-click Google OAuth login and a 30-second guided wizard to let users experience core value immediately."
            },
            {
                "area": "Value Communication",
                "suggestion": f"Show visible ROI calculators directly on the dashboard reflecting time or money saved for the {target_audience}."
            }
        ],
        "investor_pitch": {
            "hook": f"For {target_audience}, finding a way to implement {idea} has always been expensive and complex. We are changing that.",
            "problem": f"Existing solutions in {industry} are built for large enterprises, creating a massive barrier for {target_audience} who lack the budget ({budget}) and technical resources to implement them.",
            "solution": f"We've built a lightweight, intuitive validator platform that automates {idea} specifically for our target users, reducing costs by 80% and setup time to under 5 minutes.",
            "market_size": f"Targeting an underserved market of millions of users globally in {industry}, with an immediate obtainable market size of $150M.",
            "financial_projections": "We project reaching $1M in Annual Recurring Revenue (ARR) within 18 months by capturing just 0.5% of our target segment.",
            "the_ask": f"We are looking for strategic advisors and an initial seed round of funding to accelerate product development and scale marketing outreach to {target_audience}."
        }
    }
