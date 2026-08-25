import json
import os
import glob
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Resolve storage relative to this repository so local and deployed runs use the same data.
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = REPO_ROOT / "files"
chroma_client = chromadb.PersistentClient(path=str(REPO_ROOT / "backend" / "chroma_db"))
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_collection():
    return chroma_client.get_or_create_collection("nirma_knowledge")

# ──────────────────────────────────────────────
#  FACULTY.JSON
# ──────────────────────────────────────────────
def _ingest_faculty(data: dict):
    documents, metadatas, ids = [], [], []

    for idx, person in enumerate(data.get("leadership", [])):
        text = (
            f"Leadership: {person.get('name', '')}. "
            f"Designation: {person.get('designation', '')}. "
            f"Qualification: {person.get('qualification', '')}. "
            f"Specialization: {person.get('specialization', '')}."
        )
        if person.get("linkedin"):
            text += f" LinkedIn: {person['linkedin']}."
        documents.append(text)
        metadatas.append({"source_file": "faculty.json", "category": "faculty", "department": "Leadership", "entity_name": person.get("name", "")})
        ids.append(f"leadership_{idx}")

    for idx, person in enumerate(data.get("faculty", [])):
        text = (
            f"Faculty: {person.get('name', '')}. "
            f"Designation: {person.get('designation', '')}. "
            f"Department: {person.get('department', '')}. "
            f"Qualification: {person.get('qualification', '')}. "
            f"Specialization: {person.get('specialization', '')}."
        )
        if person.get("orcid"):
            text += f" ORCID: {person['orcid']}."
        if person.get("linkedin"):
            text += f" LinkedIn: {person['linkedin']}."
        documents.append(text)
        metadatas.append({"source_file": "faculty.json", "category": "faculty", "department": person.get("department", ""), "entity_name": person.get("name", "")})
        ids.append(f"faculty_{idx}")

    for idx, person in enumerate(data.get("placement_cell_contacts", [])):
        text = (
            f"Placement Cell Contact: {person.get('name', '')}. "
            f"Role: {person.get('role', '')}."
        )
        if person.get("email"):
            text += f" Email: {person['email']}."
        documents.append(text)
        metadatas.append({"source_file": "faculty.json", "category": "placement_cell", "department": "Placement Cell", "entity_name": person.get("name", "")})
        ids.append(f"placement_contact_{idx}")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  PLACEMENTS.JSON
# ──────────────────────────────────────────────
def _ingest_placements(data: dict):
    documents, metadatas, ids = [], [], []

    for idx, year_data in enumerate(data.get("btech_year_wise", [])):
        year = year_data.get("year", f"unknown_{idx}")
        parts = [f"Placement Year: {year}."]
        if year_data.get("highest_package_lpa"):
            parts.append(f"Highest Package: ₹{year_data['highest_package_lpa']} LPA.")
        if year_data.get("highest_recruiter"):
            parts.append(f"Highest Recruiter: {year_data['highest_recruiter']}.")
        if year_data.get("average_package_lpa"):
            parts.append(f"Average Package: ₹{year_data['average_package_lpa']} LPA.")
        if year_data.get("highest_branch"):
            parts.append(f"Highest Branch: {year_data['highest_branch']}.")
        if year_data.get("companies_visited"):
            parts.append(f"Companies Visited: {year_data['companies_visited']}.")
        if year_data.get("companies_visited_last_5_years_cumulative"):
            parts.append(f"Companies (5-yr cumulative): {year_data['companies_visited_last_5_years_cumulative']}.")
        if year_data.get("offers_extended"):
            parts.append(f"Offers Extended: {year_data['offers_extended']}.")
        pct = year_data.get("placement_percentage") or year_data.get("placement_percentage_range")
        if pct:
            parts.append(f"Overall Placement Rate: {pct}.")
        branch_pct = year_data.get("placement_percentage_by_branch", {})
        if branch_pct:
            branch_strs = [f"{b}: {p}%" for b, p in branch_pct.items()]
            parts.append(f"Branch-wise Placement: {', '.join(branch_strs)}.")
        if year_data.get("students_opted_higher_studies"):
            parts.append(f"Students opting for higher studies: {year_data['students_opted_higher_studies']}.")

        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "All", "entity_name": f"Placements {year}"})
        ids.append(f"placement_{year.replace('-', '_').replace(' ', '_')}")

    recruiters = data.get("top_recruiters_mentioned", [])
    if recruiters:
        documents.append(f"Top recruiters at Nirma University ITNU: {', '.join(recruiters)}.")
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "All", "entity_name": "Top Recruiters"})
        ids.append("top_recruiters")

    for idx, note in enumerate(data.get("mtech_mca_notes", [])):
        documents.append(f"MTech/MCA Placement: {note}")
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "PG Programs", "entity_name": f"PG Note {idx}"})
        ids.append(f"mtech_note_{idx}")

    cse_note = data.get("cse_department_note")
    if cse_note:
        documents.append(f"CSE Department Placement Info: {cse_note}")
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "CSE", "entity_name": "CSE Placement Note"})
        ids.append("cse_placement_note")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  FEES.JSON
# ──────────────────────────────────────────────
def _ingest_fees(data: dict):
    documents, metadatas, ids = [], [], []

    btech = data.get("btech_2026_27", {})
    if btech:
        parts = ["BTech Fee Structure AY 2026-27 at Nirma University ITNU."]
        if btech.get("tuition_fee_per_annum_inr"):
            parts.append(f"Tuition Fee: ₹{btech['tuition_fee_per_annum_inr']:,} per annum.")
        if btech.get("tuition_fee_4_years_inr"):
            parts.append(f"Total 4-year tuition: ₹{btech['tuition_fee_4_years_inr']:,}.")
        if btech.get("security_deposit_refundable_inr"):
            parts.append(f"Security Deposit (refundable): ₹{btech['security_deposit_refundable_inr']:,}.")
        if btech.get("total_first_year_cost_inr_approx"):
            parts.append(f"First Year Total (approx): ₹{btech['total_first_year_cost_inr_approx']:,}.")
        if btech.get("total_4_year_academic_fee_inr_approx"):
            parts.append(f"Total 4-year Academic Fee (approx): ₹{btech['total_4_year_academic_fee_inr_approx']:,}.")
        nri = btech.get("nri_category", {})
        if nri:
            parts.append(f"NRI Category: Tuition ${nri.get('tuition_per_annum_usd', 'N/A')} USD/year, Other fees ₹{nri.get('other_fees_inr', 'N/A')}.")
        app_fee = btech.get("application_fee_inr", {})
        if app_fee:
            parts.append(f"Application Fee: Gujarat Board ₹{app_fee.get('gujarat_board', 'N/A')}, Outside Gujarat ₹{app_fee.get('outside_gujarat_board', 'N/A')}.")
        hostel = btech.get("hostel")
        if hostel:
            parts.append(f"Hostel: {hostel}")
        categories = btech.get("categories", [])
        if categories:
            parts.append(f"Admission Categories: {', '.join(categories)}.")
        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "fees.json", "category": "fees", "department": "BTech", "entity_name": "BTech Fees 2026-27"})
        ids.append("fees_btech_2026_27")

    mtech = data.get("mtech_mca_approx", {})
    if mtech:
        parts = ["MTech/MCA Fee Structure at Nirma University ITNU."]
        if mtech.get("tuition_per_semester_inr"):
            parts.append(f"Tuition: ₹{mtech['tuition_per_semester_inr']}+ per semester.")
        if mtech.get("gate_scholarship"):
            parts.append(f"GATE Scholarship: Available.")
        if mtech.get("hostel_on_campus"):
            parts.append("On-campus hostel available for PG students.")
        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "fees.json", "category": "fees", "department": "PG Programs", "entity_name": "MTech/MCA Fees"})
        ids.append("fees_mtech_mca")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  CAMPUS_MAP.JSON
# ──────────────────────────────────────────────
def _ingest_campus_map(data: dict):
    documents, metadatas, ids = [], [], []

    for idx, building in enumerate(data.get("buildings", [])):
        parts = [f"Campus Building: {building.get('name', '')}."]
        if building.get("category"):
            parts.append(f"Category: {building['category']}.")
        if building.get("description"):
            parts.append(f"Description: {building['description']}")
        if building.get("departments"):
            parts.append(f"Departments: {', '.join(building['departments'])}.")
        if building.get("facilities"):
            parts.append(f"Facilities: {', '.join(building['facilities'])}.")
        if building.get("working_hours"):
            parts.append(f"Working Hours: {building['working_hours']}.")
        if building.get("contacts"):
            parts.append(f"Contacts: {', '.join(building['contacts'])}.")
        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "campus_map.json", "category": "campus", "department": building.get("category", ""), "entity_name": building.get("name", "")})
        ids.append(f"building_{building.get('id', idx)}")

    nav_notes = data.get("navigation_notes", [])
    if nav_notes:
        text = "Nirma University Campus Navigation: " + " ".join(nav_notes)
        documents.append(text)
        metadatas.append({"source_file": "campus_map.json", "category": "campus", "department": "navigation", "entity_name": "Navigation Info"})
        ids.append("campus_navigation")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  SCHOLARSHIPS DATASET
# ──────────────────────────────────────────────
def _ingest_scholarships(data: dict):
    documents, metadatas, ids = [], [], []

    # University profile
    profile = data.get("university_profile", {})
    if profile:
        parts = [
            f"Nirma University Profile: {profile.get('type', '')}.",
            f"Established: {profile.get('established_year', '')}.",
            f"Accreditation: {profile.get('accreditation', '')}.",
            f"Campus Size: {profile.get('campus_size', '')}.",
            f"Location: {profile.get('location_description', '')}.",
            f"Address: {profile.get('postal_address', '')}.",
            f"Website: {profile.get('website', '')}.",
            f"Admissions Portal: {profile.get('admissions_portal', '')}.",
        ]
        institutes = profile.get("constituent_institutes", [])
        if institutes:
            parts.append(f"Constituent Institutes: {'; '.join(institutes)}.")
        documents.append(" ".join(parts))
        metadatas.append({"source_file": "nirma_university_scholarships_dataset.json", "category": "university_profile", "department": "All", "entity_name": "University Profile"})
        ids.append("uni_profile")

    # GPS reference distances
    gps = data.get("gps_data", {})
    ref_dists = gps.get("reference_distances", [])
    for idx, rd in enumerate(ref_dists):
        parts = [f"Distance from {rd.get('from', '')} to Nirma University:"]
        if rd.get("driving_km_approx"):
            parts.append(f"Driving distance: ~{rd['driving_km_approx']} km.")
        if rd.get("typical_drive_time_min"):
            parts.append(f"Drive time: ~{rd['typical_drive_time_min']} minutes.")
        documents.append(" ".join(parts))
        metadatas.append({"source_file": "nirma_university_scholarships_dataset.json", "category": "location", "department": "All", "entity_name": f"Distance from {rd.get('from', '')}"})
        ids.append(f"ref_distance_{idx}")

    # Scholarships
    for idx, sch in enumerate(data.get("scholarships", [])):
        parts = [f"Scholarship: {sch.get('category', '')}."]
        if sch.get("program"):
            parts.append(f"Program: {sch['program']}.")
        if sch.get("basis"):
            parts.append(f"Basis: {sch['basis']}.")
        if sch.get("benefit"):
            parts.append(f"Benefit: {sch['benefit']}.")
        if sch.get("benefit_range"):
            parts.append(f"Benefit Range: {sch['benefit_range']}.")
        if sch.get("income_limit"):
            parts.append(f"Income Limit: {sch['income_limit']}.")
        if sch.get("eligibility"):
            parts.append(f"Eligibility: {sch['eligibility']}.")
        if sch.get("eligibility_examples"):
            parts.append(f"Eligibility Examples: {'; '.join(sch['eligibility_examples'])}.")
        if sch.get("renewal_conditions"):
            parts.append(f"Renewal Conditions: {'; '.join(sch['renewal_conditions'])}.")
        if sch.get("note"):
            parts.append(f"Note: {sch['note']}")
        if sch.get("not_eligible"):
            parts.append(f"Not Eligible: {'; '.join(sch['not_eligible'])}.")
        documents.append(" ".join(parts))
        metadatas.append({"source_file": "nirma_university_scholarships_dataset.json", "category": "scholarship", "department": sch.get("program", ""), "entity_name": sch.get("category", f"Scholarship {idx}")})
        ids.append(f"scholarship_{sch.get('id', idx)}")

    # Contacts/FAQ
    for idx, contact in enumerate(data.get("contacts_and_faq", [])):
        parts = []
        if contact.get("question"):
            parts.append(f"Q: {contact['question']}")
        if contact.get("answer"):
            parts.append(f"A: {contact['answer']}")
        if contact.get("topic"):
            parts.append(f"Topic: {contact['topic']}.")
        if parts:
            documents.append(" ".join(parts))
            metadatas.append({"source_file": "nirma_university_scholarships_dataset.json", "category": "faq", "department": "All", "entity_name": contact.get("topic", f"FAQ {idx}")})
            ids.append(f"scholarship_faq_{idx}")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  GPS NAVIGATION DATASET
# ──────────────────────────────────────────────
def _ingest_gps_navigation(data: dict):
    documents, metadatas, ids = [], [], []

    # Campus overview
    overview = data.get("campus_overview", {})
    if overview:
        text = (
            f"Nirma University Campus: {overview.get('address', '')}. "
            f"Size: {overview.get('campus_size_acres', '')} acres. "
            f"GPS Center: {overview.get('center_latitude', '')}, {overview.get('center_longitude', '')}."
        )
        documents.append(text)
        metadatas.append({"source_file": "nirma_university_gps_navigation.json", "category": "campus", "department": "All", "entity_name": "Campus Overview"})
        ids.append("gps_campus_overview")

    # Buildings with real GPS
    for idx, building in enumerate(data.get("buildings", [])):
        parts = [f"Building: {building.get('name', '')}."]
        if building.get("type"):
            parts.append(f"Type: {building['type']}.")
        parts.append(f"GPS: {building.get('latitude', '')}, {building.get('longitude', '')}.")
        if building.get("website"):
            parts.append(f"Website: {building['website']}.")
        if building.get("phone"):
            parts.append(f"Phone: {building['phone']}.")
        if building.get("rating"):
            parts.append(f"Rating: {building['rating']}/5.")
        if building.get("hours"):
            hours = building["hours"]
            hour_parts = [f"{k}: {v}" for k, v in hours.items()]
            parts.append(f"Hours: {', '.join(hour_parts)}.")
        if building.get("notes"):
            parts.append(f"Note: {building['notes']}.")
        documents.append(" ".join(parts))
        metadatas.append({"source_file": "nirma_university_gps_navigation.json", "category": "campus", "department": building.get("type", ""), "entity_name": building.get("name", "")})
        ids.append(f"gps_building_{building.get('id', idx)}")

    # Pairwise navigation routes
    nav = data.get("pairwise_building_navigation", {})
    for idx, route in enumerate(nav.get("routes", [])):
        text = (
            f"Walking distance from {route.get('from', '')} to {route.get('to', '')}: "
            f"{route.get('straight_line_distance_m', '?')}m straight-line, "
            f"estimated walk time: {route.get('estimated_walk_time_min', '?')} minutes."
        )
        documents.append(text)
        metadatas.append({"source_file": "nirma_university_gps_navigation.json", "category": "navigation", "department": "All", "entity_name": f"Route: {route.get('from', '')} → {route.get('to', '')}"})
        ids.append(f"gps_route_{idx}")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  ACADEMIC CALENDARS
# ──────────────────────────────────────────────
def _ingest_academic_calendars(data: dict):
    documents, metadatas, ids = [], [], []

    for idx, inst in enumerate(data.get("institutes", [])):
        inst_name = inst.get("institute", f"Institute {idx}")
        programmes = inst.get("programmes_covered", [])
        calendar_page = inst.get("calendar_page", "")

        # Current cycle documents
        for doc_idx, doc in enumerate(inst.get("current_cycle_documents", [])):
            text = (
                f"Academic Calendar: {doc.get('title', '')}. "
                f"Institute: {inst_name}. "
                f"Programme: {doc.get('programme', '')}. "
                f"Term: {doc.get('term', '')}. "
                f"Download: {doc.get('url', '')}."
            )
            documents.append(text)
            metadatas.append({"source_file": "nirma_university_academic_calendars.json", "category": "academic_calendar", "department": inst_name, "entity_name": doc.get("title", "")})
            ids.append(f"calendar_{idx}_{doc_idx}")

        # Institute summary
        if programmes:
            text = (
                f"Academic Calendar for {inst_name}. "
                f"Programmes covered: {', '.join(programmes)}. "
                f"Calendar page: {calendar_page}. "
                f"Data source: {inst.get('data_source', 'unknown')}."
            )
            documents.append(text)
            metadatas.append({"source_file": "nirma_university_academic_calendars.json", "category": "academic_calendar", "department": inst_name, "entity_name": f"{inst_name} Calendar Info"})
            ids.append(f"calendar_summary_{idx}")

    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  GENERIC HANDLER (fallback for unknown JSON)
# ──────────────────────────────────────────────
def _ingest_generic(data: dict, filename: str):
    """Recursively flatten any unknown JSON into text chunks."""
    documents, metadatas, ids = [], [], []

    def flatten(obj, prefix="", depth=0):
        if depth > 5:
            return
        if isinstance(obj, dict):
            for key, val in obj.items():
                flatten(val, f"{prefix}{key}: ", depth + 1)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, dict):
                    # Each dict item in a list = 1 chunk
                    text_parts = []
                    for k, v in item.items():
                        if isinstance(v, (str, int, float, bool)):
                            text_parts.append(f"{k}: {v}")
                        elif isinstance(v, list):
                            text_parts.append(f"{k}: {', '.join(str(x) for x in v[:10])}")
                    if text_parts:
                        documents.append(f"{prefix.strip()} " + ". ".join(text_parts))
                        metadatas.append({"source_file": filename, "category": "general", "department": "All", "entity_name": f"{prefix.strip()} item {i}"})
                        ids.append(f"generic_{filename}_{len(documents)}")
                elif isinstance(item, str) and len(item) > 20:
                    documents.append(f"{prefix.strip()} {item}")
                    metadatas.append({"source_file": filename, "category": "general", "department": "All", "entity_name": f"{prefix.strip()} item {i}"})
                    ids.append(f"generic_{filename}_{len(documents)}")
        elif isinstance(obj, str) and len(obj) > 30:
            documents.append(f"{prefix.strip()} {obj}")
            metadatas.append({"source_file": filename, "category": "general", "department": "All", "entity_name": prefix.strip()})
            ids.append(f"generic_{filename}_{len(documents)}")

    flatten(data)
    return documents, metadatas, ids

# ──────────────────────────────────────────────
#  MAIN INGESTION
# ──────────────────────────────────────────────
# Map filenames to their specific handlers
FILE_HANDLERS = {
    "faculty.json": _ingest_faculty,
    "placements.json": _ingest_placements,
    "fees.json": _ingest_fees,
    "campus_map.json": _ingest_campus_map,
    "nirma_university_scholarships_dataset.json": _ingest_scholarships,
    "nirma_university_gps_navigation.json": _ingest_gps_navigation,
    "nirma_university_academic_calendars.json": _ingest_academic_calendars,
}


def ingest_file(file_path: str):
    """Ingest a single JSON file into ChromaDB."""
    collection = get_collection()
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filename = os.path.basename(file_path)

    handler = FILE_HANDLERS.get(filename)
    if handler:
        documents, metadatas, ids = handler(data)
    else:
        # Generic fallback for any new JSON files
        documents, metadatas, ids = _ingest_generic(data, filename)

    if documents:
        print(f"  → Ingesting {len(documents)} chunks from {filename}")
        embeddings = model.encode(documents).tolist()
        collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)
    else:
        print(f"  → No ingestible chunks found in {filename}")


def ingest_all():
    """Re-ingest all JSON files. Deletes and rebuilds the collection."""
    data_dir = os.getenv("DATA_DIR", str(DEFAULT_DATA_DIR))
    print(f"\n🔄 Starting full data ingestion from: {data_dir}")

    try:
        chroma_client.delete_collection("nirma_knowledge")
        print("  → Cleared existing collection")
    except Exception:
        pass

    ingested = 0
    for file_path in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        basename = os.path.basename(file_path)
        if basename.startswith("_"):
            print(f"  → Skipping schema file: {basename}")
            continue
        print(f"  → Processing: {basename}")
        ingest_file(file_path)
        ingested += 1

    stats = get_stats()
    print(f"✅ Ingestion complete: {ingested} files → {stats['vectors_count']} vectors\n")


def get_stats():
    try:
        collection = get_collection()
        return {"vectors_count": collection.count()}
    except Exception:
        return {"vectors_count": 0}
