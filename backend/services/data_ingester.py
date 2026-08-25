import json
import os
import glob
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client and embedding model
chroma_client = chromadb.PersistentClient(path="./chroma_db")
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_collection():
    return chroma_client.get_or_create_collection("nirma_knowledge")

def _ingest_faculty(data: dict, collection):
    """Parse the real faculty.json structure with leadership, faculty, and placement_cell_contacts arrays."""
    documents = []
    metadatas = []
    ids = []

    # Leadership
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

    # Faculty (HoDs and regular faculty)
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
        metadatas.append({
            "source_file": "faculty.json",
            "category": "faculty",
            "department": person.get("department", ""),
            "entity_name": person.get("name", "")
        })
        ids.append(f"faculty_{idx}")

    # Placement cell contacts
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

def _ingest_placements(data: dict, collection):
    """Parse the real placements.json with btech_year_wise array, top_recruiters, and mtech notes."""
    documents = []
    metadatas = []
    ids = []

    # Year-wise BTech placement data
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
            parts.append(f"Companies (5-year cumulative): {year_data['companies_visited_last_5_years_cumulative']}.")
        if year_data.get("offers_extended"):
            parts.append(f"Offers Extended: {year_data['offers_extended']}.")

        # Placement percentages
        pct = year_data.get("placement_percentage") or year_data.get("placement_percentage_range")
        if pct:
            parts.append(f"Overall Placement Rate: {pct}.")

        branch_pct = year_data.get("placement_percentage_by_branch", {})
        if branch_pct:
            branch_strs = [f"{branch}: {pct}%" for branch, pct in branch_pct.items()]
            parts.append(f"Branch-wise Placement: {', '.join(branch_strs)}.")

        if year_data.get("students_opted_higher_studies"):
            parts.append(f"Students opting for higher studies: {year_data['students_opted_higher_studies']}.")

        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "All", "entity_name": f"Placements {year}"})
        ids.append(f"placement_{year.replace('-', '_').replace(' ', '_')}")

    # Top recruiters
    recruiters = data.get("top_recruiters_mentioned", [])
    if recruiters:
        text = f"Top recruiters at Nirma University ITNU: {', '.join(recruiters)}."
        documents.append(text)
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "All", "entity_name": "Top Recruiters"})
        ids.append("top_recruiters")

    # MTech/MCA placement notes
    for idx, note in enumerate(data.get("mtech_mca_notes", [])):
        documents.append(f"MTech/MCA Placement: {note}")
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "PG Programs", "entity_name": f"PG Placement Note {idx}"})
        ids.append(f"mtech_note_{idx}")

    # CSE department note
    cse_note = data.get("cse_department_note")
    if cse_note:
        documents.append(f"CSE Department Placement Info: {cse_note}")
        metadatas.append({"source_file": "placements.json", "category": "placement", "department": "CSE", "entity_name": "CSE Placement Note"})
        ids.append("cse_placement_note")

    return documents, metadatas, ids

def _ingest_fees(data: dict, collection):
    """Parse the real fees.json with btech_2026_27, mtech_mca_approx, and NRI data."""
    documents = []
    metadatas = []
    ids = []

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

    # MTech/MCA fees
    mtech = data.get("mtech_mca_approx", {})
    if mtech:
        parts = ["MTech/MCA Fee Structure at Nirma University ITNU."]
        if mtech.get("tuition_per_semester_inr"):
            parts.append(f"Tuition: ₹{mtech['tuition_per_semester_inr']}+ per semester.")
        if mtech.get("gate_scholarship"):
            parts.append(f"GATE Scholarship: Available ({mtech['gate_scholarship']}).")
        if mtech.get("hostel_on_campus"):
            parts.append("On-campus hostel available for PG students.")

        text = " ".join(parts)
        documents.append(text)
        metadatas.append({"source_file": "fees.json", "category": "fees", "department": "PG Programs", "entity_name": "MTech/MCA Fees"})
        ids.append("fees_mtech_mca")

    return documents, metadatas, ids

def _ingest_campus_map(data: dict, collection):
    """Parse the real campus_map.json with buildings array."""
    documents = []
    metadatas = []
    ids = []

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
        metadatas.append({
            "source_file": "campus_map.json",
            "category": "campus",
            "department": building.get("category", ""),
            "entity_name": building.get("name", "")
        })
        ids.append(f"building_{building.get('id', idx)}")

    # Navigation notes
    nav_notes = data.get("navigation_notes", [])
    if nav_notes:
        text = "Nirma University Campus Navigation: " + " ".join(nav_notes)
        documents.append(text)
        metadatas.append({"source_file": "campus_map.json", "category": "campus", "department": "navigation", "entity_name": "Navigation Info"})
        ids.append("campus_navigation")

    return documents, metadatas, ids

def ingest_file(file_path: str):
    """Ingest a single JSON file into ChromaDB with proper parsing based on file type."""
    collection = get_collection()
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filename = os.path.basename(file_path)
    documents, metadatas, ids = [], [], []

    if filename == "faculty.json":
        documents, metadatas, ids = _ingest_faculty(data, collection)
    elif filename == "placements.json":
        documents, metadatas, ids = _ingest_placements(data, collection)
    elif filename == "fees.json":
        documents, metadatas, ids = _ingest_fees(data, collection)
    elif filename == "campus_map.json":
        documents, metadatas, ids = _ingest_campus_map(data, collection)

    if documents:
        print(f"  → Ingesting {len(documents)} chunks from {filename}")
        embeddings = model.encode(documents).tolist()
        collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

def ingest_all():
    """Re-ingest all JSON files from the data directory. Deletes and rebuilds the collection."""
    data_dir = os.getenv("DATA_DIR", "/Users/jaimin/FAQ CHATBOT/files/")
    print(f"\n🔄 Starting full data ingestion from: {data_dir}")

    # Recreate collection
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
    """Return current vector store statistics."""
    try:
        collection = get_collection()
        return {"vectors_count": collection.count()}
    except Exception:
        return {"vectors_count": 0}
