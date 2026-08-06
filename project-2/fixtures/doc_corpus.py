from typing import Dict, List, Any

def raw_documents_repository() -> List[Dict[str, Any]]:
    return [
        # --- CINE Y EFECTOS VISUALES (Contradicción directa con la web) ---
        {
            "content": (
                "CONFIDENTIAL INTERNAL AUDIT: VFX & FILM PRODUCTION (Dec 2025).\n"
                "Executive Summary: Contrary to public claims of 22% savings, actual net post-production "
                "cost reduction capped at only 8% in 2025. Unforeseen workforce retraining costs and "
                "manual cleanup of AI rendering artifacts severely offset financial gains."
            ),
            "document_name": "internal/audits/film_vfx_real_roi_2025.pdf",
            "published_date": "2025-12-05",
        },
        # --- ARTE DIGITAL Y PROPIEDAD INTELECTUAL ---
        {
            "content": (
                "LEGAL MEMORANDUM: DIGITAL ART & COPYRIGHT RISK (Jan 2026).\n"
                "Subject: GenAI Licensing in Commercial Art. Recommendation: Enforce mandatory "
                "human-in-the-loop validation for all commercial graphic assets prior to client delivery. "
                "Legal risk mitigation required updating 90% of vendor agreements with explicit AI indemnification clauses."
            ),
            "document_name": "internal/legal/copyright_risk_2026.pdf",
            "published_date": "2026-01-01",            
        },
        # --- MÚSICA (Uso interno de derechos) ---
        {
            "content": (
                "INTERNAL POLICY: MUSIC & AUDIO CATALOG TRAINING (Nov 2025).\n"
                "Analysis of proprietary audio datasets used to train in-house ambient music generators. "
                "All internal game sound design teams must verify stem origins to prevent external copyright infringement claims."
            ),
            "document_name": "internal/policy/audio_dataset_compliance.pdf",
            "published_date": "2025-11-18",
        },
        # --- VIDEOJUEGOS Y NARRATIVA ---
        {
            "content": (
                "STUDIO PRODUCTION REPORT: NARRATIVE & NPC AI INTEGRATION (Feb 2026).\n"
                "Pilot results for dynamic AI-driven dialogue trees in RPG projects: Narrative designers "
                "spend 35% more time reviewing generated dialogue trees for tone consistency, negating initial speed benefits."
            ),
            "document_name": "internal/production/rpg_narrative_ai_assessment.pdf",
            "published_date": "2026-02-10",
        },
        # --- DANZA (Nota explícita de falta de datos) ---
        {
            "content": (
                "INTERNAL RESEARCH SCOPING MEMO (Jan 2026).\n"
                "Subject: Assessment of AI in Choreography and Performing Arts.\n"
                "Note: Data on choreographic software and dance performance impact remains unavailable. "
                "No active internal initiatives or external benchmarks exist for this domain."
            ),
            "document_name": "internal/research/performing_arts_gap_analysis.pdf",
            "published_date": "2026-01-15",
        }
    ]