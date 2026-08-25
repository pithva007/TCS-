# NirmaAI — College Intelligence & FAQ Chatbot
## Hackathon Data Collection & MVP Specification

> **Goal:** Build a practical, industry-oriented college AI assistant using the data that is actually available to us.
>
> **Important:** We do **not** need registration/transaction data, student behavioral data, or sensitive personal data. The MVP will focus on public/institutional college information, RAG-based answers, personalized recommendations from static student-profile data (if available), and useful analytics.

---

# 1. Final MVP Scope

The system should cover these core areas:

1. 🏫 **Campus & Facilities**
2. 👨‍🏫 **Faculty**
3. 📚 **Syllabus & Courses**
4. 💰 **Fees**
5. 🎉 **Events**
6. ⏰ **Deadlines**
7. 💼 **Placements & Companies**
8. 🎓 **Departments & Programs**
9. 🏆 **Clubs, Societies & Student Activities**
10. 📖 **Library & Academic Resources**
11. 🎒 **Scholarships / Financial Aid**
12. 🚌 **Hostel / Transportation / Campus Services** — only if data is available
13. ❓ **General College FAQs**
14. 🤖 **AI Recommendations**
15. 📊 **Admin Analytics**
16. 🧠 **AI-generated insights from chatbot queries**

The first 7 are the **must-have** categories.

The remaining categories are optional and should only be added if reliable data is available.

---

# 2. What We Are NOT Building

Because time is very limited, DO NOT spend time building:

- ❌ Online registration
- ❌ Fee payment
- ❌ Exam registration
- ❌ Attendance management
- ❌ Real-time ERP integration
- ❌ Real student marks
- ❌ Personal student records
- ❌ Real-time placement portal integration
- ❌ Complex computer vision features
- ❌ Full mobile application
- ❌ 3D campus
- ❌ Complex agentic automation

These can be mentioned under **Future Scope**.

---

# 3. Main Product Idea

## NirmaAI — Intelligent University Assistant

The chatbot is only one part of the system.

The complete system should provide:

```text
Student
   ↓
Ask a question
   ↓
AI identifies the topic
   ↓
Searches official college knowledge
   ↓
Retrieves relevant information
   ↓
LLM generates answer
   ↓
Shows source + confidence
   ↓
Logs anonymous query
   ↓
Analytics identify popular topics
```

Example:

> "Who teaches Operating Systems?"

The system searches faculty + syllabus data and answers with the relevant faculty information.

Example:

> "What subjects are there in CSE Semester 7?"

The system searches syllabus data.

Example:

> "What was TCS placement package last year?"

The system searches the placement dataset/document and clearly states the year/source.

---

# 4. DATA WE NEED

## Priority Levels

### 🔴 P0 — Absolutely Required
Collect these first.

### 🟠 P1 — Highly Recommended
Collect if available.

### 🟢 P2 — Optional
Only collect if time remains.

---

# 5. 🏫 CAMPUS & FACILITIES

## Priority: 🔴 P0

We need information about the physical campus and major facilities.

### Data Required

- Campus name
- Campus address
- Campus description
- Buildings
- Departments/buildings
- Labs
- Library
- Sports facilities
- Cafeteria
- Medical/first-aid facilities
- Auditorium
- Seminar halls
- Parking
- Wi-Fi facilities
- Student activity areas
- Important offices
- Working hours
- Contact information
- Location/block information
- Facility description

### Preferred Format

CSV:

```csv
facility_id,name,category,building,location,description,working_hours,contact
F001,Central Library,Library,Main Block,Ground Floor,University central library,8 AM - 8 PM,library@example.com
F002,Computer Lab 1,Laboratory,CSE Block,First Floor,CSE programming laboratory,9 AM - 5 PM,
```

### If you already have a PDF/website

Give us:

```text
campus_information.pdf
```

or the original webpage/document.

---

# 6. 👨‍🏫 FACULTY

## Priority: 🔴 P0

This is one of the most important datasets.

### Data Required

- Faculty ID
- Faculty name
- Department
- Designation
- Qualification
- Specialization
- Subjects taught
- Research interests
- Office/room
- Email
- Phone — only if officially public
- Profile URL — if available

### Preferred CSV

```csv
faculty_id,name,department,designation,qualification,specialization,subjects,email,office,profile_url
F001,Dr. ABC,CSE,Professor,PhD,Machine Learning,"ML, AI",abc@example.com,CSE-201,https://example.com
```

### Important

Do NOT provide private phone numbers or personal information.

Use only officially published faculty information.

---

# 7. 📚 SYLLABUS & COURSES

## Priority: 🔴 P0

This should be a major part of the chatbot.

### Data Required

For every course:

- Program
- Department
- Semester
- Course code
- Course name
- Credits
- Course type
- Prerequisites
- Units/modules
- Topics
- Faculty — if available
- Lab/theory
- Elective/core
- Course description

### Preferred CSV

```csv
program,department,semester,course_code,course_name,credits,type,description
BTech,CSE,7,CS701,Machine Learning,4,Core,"Introduction to machine learning"
BTech,CSE,7,CS702,Cloud Computing,3,Elective,"Cloud architecture and services"
```

### Units can be separate

```csv
course_code,unit_no,unit_title,topics
CS701,1,Introduction,"ML basics, supervised learning"
CS701,2,Regression,"Linear regression, logistic regression"
CS701,3,Classification,"Decision tree, KNN, SVM"
```

### Best source

If the university already has official syllabus PDFs, give us the PDFs.

We can extract the information.

---

# 8. 💰 FEES

## Priority: 🔴 P0

Collect only official fee information.

### Data Required

- Program
- Academic year
- Semester/year
- Tuition fee
- Examination fee
- Hostel fee
- Other mandatory fees
- One-time fees
- Refundable deposit
- Total approximate fee
- Category if applicable
- Source document/date

### Preferred CSV

```csv
program,academic_year,semester,fee_type,amount,description,source
BTech CSE,2026-27,7,Tuition,XXXXX,Semester tuition fee,Fee Structure 2026
BTech CSE,2026-27,7,Exam,XXXXX,Examination fee,Fee Structure 2026
```

### Important

Always include the **academic year**.

Fees change, so the chatbot should never present old fees as current fees.

---

# 9. 🎉 EVENTS

## Priority: 🔴 P0

Events can include:

- Technical events
- Hackathons
- Cultural events
- Sports
- Seminars
- Workshops
- Guest lectures
- Conferences
- Club events
- Competitions
- Placement events

### Data Required

- Event name
- Event category
- Date
- Start time
- End time
- Venue
- Organizer
- Department/club
- Description
- Eligibility
- Registration link — if available
- Contact
- Status

### Preferred CSV

```csv
event_id,event_name,category,date,time,venue,organizer,department,description,eligibility,registration_link
E001,AI Workshop,Workshop,2026-09-10,10:00 AM,CSE Auditorium,CSI,CSE,"Hands-on AI workshop","CSE students",https://example.com
```

---

# 10. ⏰ DEADLINES

## Priority: 🔴 P0

We don't need registration-system data.

We only need **known institutional deadlines**.

Examples:

- Scholarship application deadline
- Internship application deadline
- Placement registration deadline
- Competition deadline
- Event registration deadline
- Assignment/project deadline — only if officially available
- Academic submission deadline
- Application deadlines
- Club recruitment deadline

### Data Required

```csv
deadline_id,title,category,date,department,description,source,status
D001,Scholarship Application,Scholarship,2026-09-05,University,"Last date for scholarship application","Notice 2026","Upcoming"
D002,TCS Campus Drive,Placement,2026-09-10,CSE,"Registration closes","Placement Cell","Upcoming"
```

### Important

Do not invent deadlines.

If a date is unknown, leave it blank.

---

# 11. 💼 PLACEMENTS & COMPANIES

## Priority: 🔴 P0

This can become one of our strongest features.

We need historical placement information where officially available.

### University-level placement data

Collect:

- Academic year
- Number of students placed
- Placement percentage
- Highest package
- Average package
- Median package — if available
- Number of companies
- Major recruiters
- Internship statistics — if available

### Preferred CSV

```csv
academic_year,students_placed,placement_percentage,highest_package,average_package,median_package,total_companies,source
2025-26,XXX,XX%,XX LPA,XX LPA,XX LPA,XXX,Placement Report 2025-26
```

---

# 12. COMPANY-WISE PLACEMENT DATA

## Priority: 🔴 P0

This is especially useful for questions like:

> "What was TCS's placement package?"

> "Which companies recruited CSE students?"

> "What roles did Deloitte offer?"

### Data Required

```csv
company,academic_year,department,role,students_selected,package,package_type,location,eligibility,source
TCS,2025-26,CSE,Software Engineer,XX,XX LPA,CTC,India,"As per placement criteria",Placement Report
```

### If exact values are not available

Use:

```text
Not Available
```

Do NOT estimate.

---

# 13. COMPANY KNOWLEDGE

## Priority: 🟠 P1

For major recruiters, create:

```csv
company,industry,roles,skills,eligibility,selection_process,previous_recruitment_years,source
TCS,IT Services,"Software Engineer","C++,Java,DSA,SQL","As per official criteria","Online test + interview","2024,2025,2026","Official/Placement source"
```

The chatbot can then answer:

> "What skills should I prepare for TCS?"

But clearly distinguish:

- **Official university information**
- **General AI recommendation**

---

# 14. 🎓 DEPARTMENTS & PROGRAMS

## Priority: 🟠 P1

### Data Required

- Department
- Programs
- Degrees
- Duration
- Specializations
- HOD
- Department description
- Contact
- Website
- Facilities
- Research areas

### CSV

```csv
department,program,degree,duration,specialization,hod,description,website
CSE,Computer Science Engineering,BTech,4 years,,Dr. XYZ,"...",https://example.com
```

---

# 15. 🏆 CLUBS & SOCIETIES

## Priority: 🟠 P1

This can make the student assistant much more useful.

### Data Required

- Club name
- Category
- Description
- Department
- Faculty coordinator
- Student coordinator
- Activities
- Recruitment period
- Contact
- Social link
- Website

### CSV

```csv
club_name,category,department,description,faculty_coordinator,activities,contact,website
CSI,Technical,CSE,"Computer society","Dr. XYZ","Hackathons, workshops",csi@example.com,https://example.com
```

---

# 16. 📖 LIBRARY

## Priority: 🟠 P1

Collect:

- Opening hours
- Rules
- Membership rules
- Borrowing limits
- Fine rules
- Digital resources
- Contact
- Location
- Important services

This can mostly be a PDF/document.

Example questions:

> "How many books can I borrow?"

> "When is the library open?"

> "What are the library rules?"

---

# 17. 🎓 SCHOLARSHIPS / FINANCIAL AID

## Priority: 🟠 P1

Collect:

- Scholarship name
- Eligibility
- Required documents
- Amount
- Deadline
- Application method
- Category
- Official source

### CSV

```csv
scholarship,eligibility,amount,documents,deadline,application_method,source
Scholarship A,"Eligibility criteria",XXXXX,"Income certificate, ID",2026-09-05,"Online","Official Notice"
```

---

# 18. 🏠 HOSTEL / TRANSPORT / CAMPUS SERVICES

## Priority: 🟢 P2

Only collect if easily available.

### Hostel

- Hostel names
- Capacity
- Fees
- Facilities
- Rules
- Timings
- Contact

### Transport

- Routes
- Stops
- Timings
- Fees
- Contact

Do not spend much time here if data collection is difficult.

---

# 19. ❓ GENERAL FAQ

## Priority: 🔴 P0

Create a small curated FAQ dataset.

Examples:

- How do I contact the examination cell?
- Where is the library?
- Who is the CSE HOD?
- What programs are offered?
- What are the library timings?
- What clubs are available?
- What placement companies visit?
- Where can I find the syllabus?
- What are the campus facilities?
- Where is the placement cell?

### CSV

```csv
question,answer,category,department,source
"Where is the central library?","Main campus, Ground Floor","Campus","University","Official Campus Information"
```

---

# 20. 📄 DOCUMENTS WE SHOULD COLLECT

If you can get PDFs, these are extremely valuable.

## 🔴 Must Have

```text
01_academic_information.pdf
02_syllabus.pdf
03_fee_structure.pdf
04_placement_report.pdf
05_faculty_directory.pdf
06_events.pdf
07_deadlines_notices.pdf
08_campus_facilities.pdf
```

## 🟠 Good to Have

```text
09_scholarship_guidelines.pdf
10_library_rules.pdf
11_club_directory.pdf
12_department_information.pdf
13_hostel_information.pdf
14_transport_information.pdf
```

**Do not convert PDFs into manually typed data unless necessary. Give us the original PDFs.**

---

# 21. BEST WAY TO GIVE THE DATA TO THE DEVELOPMENT TEAM

## Option A — BEST

Give original documents:

```text
/data/documents/

academic_calendar.pdf
syllabus.pdf
fee_structure.pdf
placement_report.pdf
faculty.pdf
campus.pdf
library_rules.pdf
scholarships.pdf
```

This allows the RAG pipeline to process the documents directly.

---

## Option B — Structured Data

For tabular information, use CSV.

```text
/data/csv/

faculty.csv
courses.csv
fees.csv
events.csv
deadlines.csv
placements.csv
companies.csv
departments.csv
clubs.csv
scholarships.csv
facilities.csv
faq.csv
```

---

# 22. DO NOT SEND DATA AS SCREENSHOTS IF YOU HAVE THE ORIGINAL FILE

### Bad

```text
WhatsApp screenshot
Screenshot of Excel
Screenshot of website
Photo of PDF
```

### Better

```text
PDF
Excel
CSV
DOCX
TXT
Official webpage
```

Screenshots are only a last resort.

---

# 23. Excel Format Is Also Fine

If CSV is inconvenient, give us one Excel file:

```text
NirmaAI_Data.xlsx
```

with sheets:

```text
Sheet 1 → Faculty
Sheet 2 → Courses
Sheet 3 → Fees
Sheet 4 → Events
Sheet 5 → Deadlines
Sheet 6 → Placements
Sheet 7 → Companies
Sheet 8 → Departments
Sheet 9 → Clubs
Sheet 10 → Scholarships
Sheet 11 → Facilities
Sheet 12 → FAQ
```

This is probably the **easiest format for your team** if someone is manually collecting data.

---

# 24. If You Have Website Links

You can also provide a simple text file:

```text
sources.txt

Campus:
https://...

Faculty:
https://...

Syllabus:
https://...

Fees:
https://...

Placements:
https://...

Events:
https://...

Departments:
https://...
```

The team can then process the relevant information.

---

# 25. Recommended Final Data Folder

Give the development team this structure:

```text
NirmaAI_Data/
│
├── documents/
│   ├── campus.pdf
│   ├── syllabus.pdf
│   ├── fees.pdf
│   ├── placement_report.pdf
│   ├── faculty.pdf
│   ├── library.pdf
│   └── scholarship.pdf
│
├── csv/
│   ├── faculty.csv
│   ├── courses.csv
│   ├── fees.csv
│   ├── events.csv
│   ├── deadlines.csv
│   ├── placements.csv
│   ├── companies.csv
│   ├── departments.csv
│   ├── clubs.csv
│   ├── scholarships.csv
│   ├── facilities.csv
│   └── faq.csv
│
└── sources.txt
```

---

# 26. IMPORTANT: SOURCE + DATE FOR EVERY DATASET

Every piece of important information should have:

```text
Source
Date / Academic Year
```

Example:

```text
Source: Nirma University Placement Report
Academic Year: 2025-26
```

This allows the chatbot to say:

> "According to the 2025-26 placement report..."

instead of presenting potentially outdated information as fact.

---

# 27. AI ANSWER FORMAT

The chatbot should ideally answer like this:

```text
Answer:
TCS recruited students for Software Engineer-related roles
during the 2025-26 placement cycle.

Placement Information:
• Package: XX LPA
• Role: Software Engineer
• Department: CSE
• Academic Year: 2025-26

Source:
Placement Report 2025-26

Confidence:
94%
```

If the information isn't available:

```text
I couldn't find verified information about this in the
university knowledge base.

I don't want to guess or provide unverified information.
```

This is an important **anti-hallucination feature**.

---

# 28. OUT-OF-THE-BOX FEATURES WE CAN BUILD FROM THIS DATA

Even without registration/student behavioral data, we can still build interesting features.

## 1. 🎯 Student Career Match

Student enters:

```text
Skills:
C++
DSA
Machine Learning

Interests:
AI
Software Development
```

AI recommends:

```text
Best-fit companies
Relevant placement roles
Relevant university events
Relevant courses
Skills to improve
```

---

## 2. 🔮 "What Should I Focus On?"

Student asks:

> "I want to prepare for TCS. What should I focus on?"

System combines:

```text
Company information
+
Previous placement information
+
Student skills
+
Courses
```

and generates a preparation roadmap.

---

## 3. 🧭 "Find My Path"

Student says:

> "I want to become an AI engineer."

System maps:

```text
Goal
 ↓
Required skills
 ↓
Relevant university courses
 ↓
Faculty
 ↓
Clubs
 ↓
Events
 ↓
Projects
 ↓
Relevant recruiters
```

This could become one of your strongest student-facing features.

---

# 29. AI CAMPUS SEARCH

Instead of only asking questions, provide:

### "Search the University"

Student enters:

> `Machine Learning`

System returns:

```text
📚 Courses
Machine Learning

👨‍🏫 Faculty
Dr. XYZ
Dr. ABC

🎉 Events
AI Workshop

🏆 Clubs
CSI

💼 Companies
Companies hiring ML-related roles

📄 Documents
ML syllabus
```

This is much more powerful than a normal FAQ chatbot.

---

# 30. UNIVERSAL CAMPUS ANSWER

If someone asks:

> "Tell me everything about Machine Learning at Nirma."

The AI can combine:

```text
Course
+
Syllabus
+
Faculty
+
Events
+
Clubs
+
Placement relevance
+
Recommended skills
```

and generate a complete answer.

This is where RAG + structured data becomes powerful.

---

# 31. ADMIN ANALYTICS WITHOUT PRIVATE STUDENT DATA

We can safely analyze chatbot interactions.

Store only:

```text
timestamp
query
topic
response_time
confidence
feedback
```

Avoid storing unnecessary personal information.

Then show:

```text
Most Asked Topics

Placements       32%
Syllabus         24%
Faculty          15%
Fees             11%
Events            9%
Campus            6%
Other             3%
```

---

# 32. AI INSIGHTS

From those queries, the system can generate:

> **Insight 1**
>
> Placement-related questions are the most frequent category.

> **Insight 2**
>
> Students frequently ask about company-specific placement information.

> **Insight 3**
>
> Syllabus-related queries are concentrated around final-year courses.

> **Recommendation**
>
> Create a dedicated placement preparation knowledge section.

This does not require registration data.

---

# 33. FINAL MVP ARCHITECTURE

```text
                         NirmaAI
                            │
            ┌───────────────┼────────────────┐
            │               │                │
        STUDENT          AI ENGINE          ADMIN
            │               │                │
            │          ┌────┴────┐           │
            │          │         │           │
         Chatbot      RAG    Recommendations Analytics
            │          │         │           │
            │          │         │           │
            └──────────┼─────────┼───────────┘
                       │
                UNIVERSITY DATA
                       │
        ┌──────────────┼───────────────┐
        │              │               │
      PDFs            CSV            Excel
        │              │               │
        └──────────────┼───────────────┘
                       │
                  Data Pipeline
                       │
              ┌────────┴────────┐
              │                 │
          Vector DB          SQL DB
          ChromaDB           SQLite
              │                 │
              └────────┬────────┘
                       │
                     Ollama
                       │
                      LLM
```

---

# 34. PRIORITY ORDER — VERY IMPORTANT

Because you said you have **very little time**, collect data in exactly this order:

## 🔴 PHASE 1 — Collect Immediately

```text
[ ] Campus information
[ ] Faculty
[ ] Syllabus
[ ] Fees
[ ] Events
[ ] Deadlines
[ ] Placement report
[ ] Company-wise placement information
[ ] Basic FAQ
```

## 🟠 PHASE 2 — If available

```text
[ ] Departments
[ ] Clubs
[ ] Library
[ ] Scholarships
[ ] Company information
```

## 🟢 PHASE 3 — Only if time remains

```text
[ ] Hostel
[ ] Transportation
[ ] Extra facilities
[ ] Additional historical data
```

---

# 35. THE ONE FILE I WANT FROM YOU

If you are extremely short on time, the easiest approach is:

```text
NirmaAI_Data.xlsx
```

Create these sheets:

```text
1. Faculty
2. Courses
3. Fees
4. Events
5. Deadlines
6. Placements
7. Companies
8. Departments
9. Clubs
10. Facilities
11. Scholarships
12. FAQ
```

And separately provide:

```text
NirmaAI_Documents/

PDF files
```

That is enough to start.

---

# 36. Minimum Data Required to Start Development

If you can only collect a small amount, give us:

```text
1. Faculty PDF/Excel
2. Syllabus PDF
3. Fee PDF
4. Placement Report PDF
5. Campus information
6. 10-20 events
7. 10-20 deadlines
8. 20-50 FAQs
9. List of departments
10. List of major facilities
```

**Do not wait for perfect data.**

A smaller amount of clean, verified data is much better than a huge amount of messy data.

---

# 37. Final Product Vision

The final system should feel like:

> ## "ChatGPT for the entire university."

But with a major difference:

> **It doesn't know everything from the internet. It knows the university's verified knowledge and can connect information across campus, academics, faculty, events, fees, deadlines, and placements.**

A student can ask:

> "Who teaches ML?"

> "What is in ML syllabus?"

> "When is the next AI event?"

> "Which companies hire for AI roles?"

> "What skills should I learn?"

> "What should I prepare for TCS?"

And the AI can connect all of those pieces.

---

# 38. ONE-LINE HACKATHON PITCH

> **NirmaAI is an AI-powered university intelligence platform that turns scattered campus information into one trusted conversational interface, connecting academics, faculty, campus life, events, deadlines, fees, and career opportunities while generating personalized student recommendations and actionable institutional insights.**

---

# 39. DATA COLLECTION RULE

### Give us data in this priority:

**Original PDF > Excel > CSV > DOCX/TXT > Official URL > Screenshot**

And always provide:

**Source + Academic Year/Date**

for information that can change.

---

# 40. DO NOT WASTE TIME

Do not spend hours manually converting every PDF into CSV.

If you already have:

```text
syllabus.pdf
placement_report.pdf
faculty.pdf
fee_structure.pdf
```

**just give the original PDFs.**

The development pipeline can handle:

```text
PDF
 ↓
Text extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
RAG
 ↓
Ollama
 ↓
Answer
```

For naturally structured data such as events, fees, faculty lists, and placement tables, CSV/Excel is preferable.
