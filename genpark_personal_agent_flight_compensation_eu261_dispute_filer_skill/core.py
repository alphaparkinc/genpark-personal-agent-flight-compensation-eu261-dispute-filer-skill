# -*- coding: utf-8 -*-
"""Flight Compensation EU261 Dispute Filer Skill for GenPark Personal Agents."""
import json
from typing import Dict, Any

def evaluate_statutory_delay_compensation(flight_number: str, flight_distance_km: float, arrival_delay_minutes: int, airline_claimed_reason: str, departure_airport_iata: str = "LHR", arrival_airport_iata: str = "JFK") -> Dict[str, Any]:
    # EU261 statutory rules: Delay must exceed 3 hours (180 mins)
    is_delay_threshold_met = arrival_delay_minutes >= 180

    # Extraordinary circumstances test
    # Per ECJ Wallentin-Hermann precedent (C-549/07), technical defects and crew shortages are NOT extraordinary
    extraordinary_reasons = ["severe_weather", "air_traffic_control", "strike"]
    is_defense_valid = airline_claimed_reason in extraordinary_reasons

    # Compensation tiers
    if flight_distance_km <= 1500:
        statutory_payout_eur = 250.0
    elif flight_distance_km <= 3500:
        statutory_payout_eur = 400.0
    else:
        # Long haul > 3500km
        statutory_payout_eur = 600.0 if arrival_delay_minutes >= 240 else 300.0

    claim_valid = is_delay_threshold_met and not is_defense_valid
    payout_approved = statutory_payout_eur if claim_valid else 0.0

    if not is_delay_threshold_met:
        status = "INELIGIBLE_SUB_3_HOUR_DELAY"
        comment = f"Arrival delay ({arrival_delay_minutes}m) does not meet the statutory 180-minute minimum."
    elif is_defense_valid:
        status = "POTENTIAL_FORCE_MAJEURE_DEFENSE"
        comment = f"Airline citing '{airline_claimed_reason}' which may qualify as extraordinary circumstances under Art. 5(3)."
    else:
        status = "STATUTORY_COMPENSATION_GUARANTEED"
        comment = f"Reason '{airline_claimed_reason}' is an inherent operational risk per ECJ case law; full indemnity owed."

    return {
        "flight": flight_number.upper(),
        "route": f"{departure_airport_iata} -> {arrival_airport_iata}",
        "distance_km": flight_distance_km,
        "delay_minutes": arrival_delay_minutes,
        "airline_defense": airline_claimed_reason,
        "claim_status": status,
        "entitled_compensation_eur": payout_approved,
        "legal_basis": "Regulation (EC) No 261/2004 & ECJ Case C-549/07",
        "advisory": comment,
        "advocate": "GenPark Aviation Passenger Rights Advocate"
    }

def compile_formal_eu261_demand_letter(passenger_name: str, booking_reference: str, airline_legal_entity: str, claim_amount_eur: float) -> Dict[str, Any]:
    letter = (
        f"FORMAL STATUTORY NOTICE OF INDEMNITY DEMAND UNDER REGULATION (EC) NO 261/2004\n\n"
        f"To: {airline_legal_entity} Legal Compliance & Passenger Claims\n"
        f"Passenger: {passenger_name}\n"
        f"Booking Reference (PNR): {booking_reference}\n\n"
        f"Dear Claims Department,\n\n"
        f"Pursuant to Article 7 of Regulation (EC) No 261/2004, I hereby demand direct payment of €{claim_amount_eur:.2f} "
        f"in statutory cash compensation resulting from a material arrival delay in excess of three hours.\n\n"
        f"Please note that under binding precedent established by the European Court of Justice in Wallentin-Hermann (Case C-549/07) "
        f"and Sturgeon (Joined Cases C-402/07 and C-432/07), routine technical malfunctions, maintenance events, and internal crew shortages "
        f"do not constitute 'extraordinary circumstances' capable of exculpating the operating carrier.\n\n"
        f"I request that payment be transmitted via bank wire within fourteen (14) calendar days, failing which this matter will be "
        f"referred to the relevant National Enforcement Body (NEB) and European Small Claims Procedure without further notice.\n\n"
        f"Yours faithfully,\n{passenger_name}"
    )

    return {
        "passenger": passenger_name,
        "airline": airline_legal_entity,
        "pnr": booking_reference,
        "claim_value_eur": claim_amount_eur,
        "formal_demand_letter_text": letter,
        "enforcement_window_days": 14,
        "status": "FORMAL_LEGAL_DEMAND_READY"
    }
