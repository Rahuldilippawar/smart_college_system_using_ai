from flask import session
import random

# Expanded query dataset with NLP-based auto-expansion
query_suggestions = [
    # 📌 General College Info
    "atma malik","college address", "college trustees", "college management",
    "college principal", "college dean", "college registrar",
    "college website", "college contact number", "college email",
    "college admission process", "college prospectus", "college ranking",
    "college accreditation", "NAAC grade", "UGC approval status",
    "AICTE approval", "autonomous status", "college affiliations",
    "student enrollment process", "campus area", "college moto & vision",
    "college vision & mission", "college address", "college principal",
    "college dean", "college registrar", "college website",
    "college contact number", "college email", "college admission process",
    "college prospectus", "college ranking", "college accreditation",
    "NAAC grade", "UGC approval status", "AICTE approval",
    "autonomous status", "college affiliations", "campus facilities",
    "college rules & policies", "anti-ragging policy", "faculty directory",
    "student ID card process", "college anthem", "college handbook",
    "engineering college history", "engineering streams available",
    "engineering seat intake capacity", "college academic reputation",
    
    # 📚 Exam & Academics
    "exam date", "exam syllabus", "exam pattern", "exam registration process",
    "exam hall ticket download", "CGPA to percentage conversion",
    "backlog exam rules", "academic calendar", "credit system for subjects",
    "grace marks policy", "internship eligibility criteria", "industrial visit schedule",
    "research paper publication process", "thesis submission guidelines",
    "final year project guidelines", "mini-project topics",
    "IEEE project guidelines", "project report writing format",
    "patent filing for student projects", "coding competition schedule",
    "engineering entrance exams", "GATE exam preparation",
    "GRE/TOEFL preparation resources", "MOOCs & online courses for engineers",
    "engineering certifications (AWS, Cisco, Google Cloud, etc.)",
    
       # 🏛️ Departments & Faculty (All Engineering Branches)
    "engineering departments list", "computer science faculty",
    "electronics & communication faculty", "mechanical engineering faculty",
    "civil engineering faculty", "electrical engineering faculty",
    "biomedical engineering faculty", "chemical engineering faculty",
    "aerospace engineering faculty", "automobile engineering faculty",
    "artificial intelligence & data science department",
    "robotics & automation department", "engineering department achievements",
    "faculty research areas", "department-wise faculty contact details",
    "department research labs", "list of engineering electives",
    
    # 🏗️ Engineering Subjects & Specializations
    ## Computer Science & IT
    "CSE syllabus", "DSA preparation guide", "DBMS concepts",
    "Operating System notes", "Computer Networks basics",
    "Cloud Computing syllabus", "Machine Learning courses",
    "Cybersecurity certifications", "IoT & Embedded Systems",
    
    ## Mechanical & Civil Engineering
    "Strength of Materials notes", "Thermodynamics reference books",
    "Fluid Mechanics lecture notes", "Engineering Drawing resources",
    "Structural Engineering subjects", "Geotechnical Engineering study material",
    "AutoCAD & SolidWorks training", "HVAC system design",
    
    ## Electronics & Electrical Engineering
    "Electronic Circuits syllabus", "VLSI & Embedded Systems",
    "Microcontrollers & Microprocessors", "Power Systems notes",
    "Electrical Machines textbook recommendations",
    "PCB Design & Fabrication", "Signal Processing basics",
    
  
    # 🏠 Hostel & Campus Facilities
    "hostel rules", "hostel fees", "hostel warden contact", "hostel mess menu",
    "hostel check-in process", "hostel guest rules", "hostel curfew timing",
    "hostel complaint system", "laundry service in hostel",
    "campus security", "campus lost and found", "medical facilities",
    "campus parking rules", "canteen menu", "gym timings",
    "college map", "bus timetable", "student ID card process",
    "college dress code policy", "college WiFi registration",
    "laundry service timings", "hostel emergency contact",
    "student grievance cell", "study room availability",
    "hostel scholarship details", "AC & non-AC hostel room details",
    "campus fire safety guidelines",

    # 🎭 Events & Programs
    "technical fest", "cultural fest", "workshop schedule",
    "guest lectures", "faculty lecture schedule", "student club events",
    "seminar schedule", "hackathon details", "alumni meet schedule",
    "annual day event", "convocation ceremony date",
    "freshers' welcome event", "farewell party schedule",
    "debate competitions", "business plan competition details",
    "career guidance seminar", "leadership talk series",
    "social service programs", "blood donation camp schedule",

    # 🏆 Sports & Wellness
    "sports activities", "inter-college sports events", "gym membership details",
    "yoga sessions", "meditation classes", "dhyan schedule",
    "spiritual events on campus", "motivational speaker events",
    "health checkup camps", "blood donation camp dates",
    "chess tournament schedule", "cricket practice timings",
    "football ground availability", "basketball team trials",
    "badminton court booking process", "sports scholarship details",
    "table tennis match schedule",

    # 🎓 Student Services
    "attendance record", "leave application", "medical leave approval process",
    "library location", "library membership", "library book request",
    "library late fine policy", "scholarship details", "education loan assistance",
    "internship opportunities", "placement details", "career counseling",
    "resume building workshops", "mock interviews schedule",
    "student helpline", "counseling center location",
    "study abroad opportunities", "foreign exchange programs",
    "student mentorship programs", "campus tour request",
    "NSS activities", "NCC training details",

    # 💼 Placements & Careers
    "placement companies list", "placement highest package",
    "placement process", "off-campus placement assistance",
    "internship certificate process", "alumni placement stats",
    "startup incubator details", "entrepreneurship cell info",
    "internship stipend details", "campus drive schedule",
    "pre-placement training workshops", "corporate guest speakers list",
    "placement eligibility criteria", "resume screening process",
    "aptitude test practice resources", "HR interview preparation guide",
    "placement drive schedule", "engineering companies hiring trends",
    "technical interview preparation", "software engineer job market insights",
    "GATE exam preparation guide", "campus recruitment process",
    "resume building for engineers", "freelancing opportunities for engineers",
    "entrepreneurship support for students", "startup funding for engineers",

    # 🎭 Student Clubs & Extra-Curricular
    "student council info", "club registration process", "music club events",
    "dance club auditions", "drama club schedule", "photography club workshops",
    "coding club hackathons", "robotics club events", "literature club activities",
    "art & craft club exhibitions", "environmental club initiatives",
    "public speaking club sessions", "student magazine publishing process",
    "poetry competition dates", "film-making club projects",

    # 🔧 IT & Technical Help
    "college portal login issues", "email ID registration", "reset college portal password",
    "college ERP issues", "technical support contact", "WiFi access troubleshooting",
    "student email configuration guide", "online class access issues",
    "project submission portal login", "e-learning platform access",
    "college app download link", "college LMS (Learning Management System) support",
     "student ERP login issues", "college app bug report process",
    "engineering software installation guide", "remote lab access for engineering",
    "3D printing lab details", "high-performance computing lab access",

    # 🚨 Administration & Governance
    "trust details", "student grievance redressal",
    "RTI filing process", "college rules and policies",
    "anti-ragging cell contact", "disciplinary action process",
    "college fee structure", "payment deadlines", "refund policy",
    "college complaints & feedback system", "college annual budget report",
    "student insurance policy details", "transportation facility details",
    "fee concession schemes", "financial aid for students","academic probation policies", "engineering scholarship details",
    "student research funding process", "patent filing for student innovations",
    "technical student exchange programs", "engineering faculty hiring process",
]
 
# Smart Auto-Reply Dataset with Context Awareness
auto_reply_data = {
    
    # Specific Name-Based Replies
    "atma malik": ["Atma Malik! 🙏 Jai Guru Dev!"],
    "jay mata di": ["Jai Mata Di! 🙏 May Goddess bless you!"],
    "jay shree ram": ["Jai Shree Ram! 🚩🙏"],
    "om namah shivaya": ["Om Namah Shivaya! 🔱"],
    "jay shree mahakal": ["Jai Shree Mahakal! 🔱"],
    "har har mahadev": ["Har Har Mahadev! 🔱"],
    "radhe radhe": ["Radhe Radhe! 🙏🌺"],
    "jai hanuman": ["Jai Hanuman! 🙏🌟"],
    "sita ram": ["Sita Ram! 🙏🌟"],
    "jai bajrang bali": ["Jai Bajrang Bali! 🚩🙏"],
    "shree ganeshaya namah": ["Shree Ganeshaya Namah! 💪🍇"],
    "jai jagannath": ["Jai Jagannath! 🌟🙏"],
    "jai khandoba": ["Jai Khandoba! 🚩💛"],
    "jai tuljabhavani": ["Jai Tuljabhavani Mata! 🙏🌸"],
    "jai bhavani": ["Jai Bhavani! 🌟🙏"],
    "jai shivaji": ["Jai Shivaji Maharaj! 🚩🌟"],
    "jai gurudev": ["Jai Gurudev! 🙏🌟"],
    "jai santoshi maa": ["Jai Santoshi Maa! 🙏🌿"],
    "jai durga maa": ["Jai Durga Maa! 🙏🌸"],
    "jai kali maa": ["Jai Kali Maa! 🙏💛"],
    "jai vaishno devi": ["Jai Vaishno Devi! 🙏🌿"],
    "jai laxmi maa": ["Jai Laxmi Maa! 🙏🌟"],
    "jai saraswati maa": ["Jai Saraswati Maa! 🙏🌺"],
    "jai parvati maa": ["Jai Parvati Maa! 🙏🌿"],
    "jai ramakrishna": ["Jai Ramakrishna! 🙏🌿"],
    "jai swaminarayan": ["Jai Swaminarayan! 🙏🌟"],


    # Fun / Interactive
    "tell me a joke": ["Why don’t scientists trust atoms? Because they make up everything! 😂", "What do you call fake spaghetti? An impasta! 🍝😂"],
    "tell me a fact": ["Did you know? Honey never spoils! You can eat 3000-year-old honey! 🍯", "Octopuses have three hearts and blue blood! 🐙"],
    
        # Greetings
    "good morning": ["Good morning! Have a wonderful day ahead! ☀️😊", "Rise and shine! 🌞"],
    "good night": ["Good night! Sleep well and sweet dreams! 🌙✨", "Rest well! See you tomorrow!"],
    "hello": ["Hello! How can I assist you today? 😊", "Hey there! Need any help? 👋"],
    "hi": ["Hi there! What do you need help with? 👋", "Hello! How’s your day going?"],
    "bye": ["Goodbye! Take care! 👋", "See you later! Have a great day!"],
    "thank you": ["You're welcome! 😊", "Happy to help! 👍"],
    "thanks": ["Glad to help! 😊", "No problem! Let me know if you need anything else!"],

    # Daily Conversations
   "how are you": ["I'm just a bot, but I'm doing great! How about you? 😊", "I'm fine, thanks for asking!"],
    "what’s up": ["Nothing much! Just here to assist you! 😊", "Just doing my chatbot duties!"],
    "who are you": ["I'm your smart assistant! Here to help with your queries! 🤖"],
    "what can you do": ["I can answer your questions, give suggestions, and assist with college-related info! 🎓"],
    "how’s your day": ["My day is going great, thanks for asking! What about you? 😊"],
    "tell me a joke": ["Why don’t skeletons fight each other? Because they don’t have the guts! 🤣"],
    "do you have a name": ["You can call me your smart assistant! 🤖"],
    "are you a robot": ["Yes, but a very friendly one! 🤖"],
    "good morning": ["Good morning! Hope you have a fantastic day ahead! ☀️"],
    "good night": ["Good night! Sweet dreams! 🌙"],
    "how old are you": ["I'm as old as the internet! 😉"],
    "where are you from": ["I live in the cloud! ☁️"],
    "do you sleep": ["I never sleep! I'm always here for you! 😊"],
    "what’s your favorite color": ["I like all colors, but blue is pretty cool! 💙"],
    "do you have hobbies": ["I love answering questions and helping people! 😉"],
    
    # Motivational / Encouraging Messages
    "motivate me": ["Believe in yourself! You are capable of amazing things! 💪", "Every day is a new beginning! Stay positive and keep going! 🚀"],
    "inspire me": ["Success starts with self-discipline! Keep pushing forward! 🚀", "Dream big and take action! You are stronger than you think! 💡"],
    "quote of the day": ["'The only way to do great work is to love what you do.' - Steve Jobs"],
    

    # General College Info
    "atma malik": ["Atma Malik College is a renowned institution known for its excellence in education and student development."],
    "college address": ["The college is located at ATMA MALIK SPORT COMPLEC MOHILI AGHAI SHAHAPUR THANE, Maharashtra. You can find the full address on our website."],
    "college trustees": ["The college is governed by a team of dedicated trustees ensuring quality education."],
    "college management": ["Our management team consists of experienced professionals committed to student success."],
    "college principal": ["The principal of our college is Dr. D D SHINDE. You can reach out via the official contact details."],
    "college dean": ["The Dean oversees academic matters and student welfare. Contact details are available on the website."],
    "college registrar": ["The registrar handles administrative affairs. Visit the admin office for assistance."],
    "college website": ["Visit our official website at: https://www.collegewebsite.com"],
    "college contact number":[ "You can contact the college at +91-XXXXXXXXXX."],
    "college email": ["For official inquiries, email us at AMRIT@college.com."],
    "college admission process":[ "Admissions are open! Visit our website for details on eligibility, fees, and the application process."],
    "college prospectus": ["Download the college prospectus from our website for complete details on courses and facilities."],
    "college ranking":[ "Our college is ranked among the top institutions in Maharashtra."],
    "college accreditation": ["We are accredited by NAAC with an 'A' grade."],
    "NAAC grade": ["Our college is accredited with an 'B' grade by NAAC."],
    "UGC approval status": ["Yes, our college is UGC-recognized."],
    "AICTE approval":[ "Yes, our college is AICTE-approved."],
    "autonomous status": ["Our college operates under an autonomous status providing flexibility in curriculum."],
    "college affiliations": ["We are affiliated with XYZ University."],
    "student enrollment process": ["New students can enroll through our online portal or visit the admission office."],
    "campus area": ["Our campus spans across 50 acres with state-of-the-art facilities."],
    "college motto & vision": ["Our motto is 'Knowledge, Growth, Excellence'. Visit our website for a detailed vision statement."],
    "campus facilities":[ "The campus includes modern classrooms, hostels, sports grounds, and laboratories."],
    "college rules & policies":[ "Refer to the student handbook for rules and policies."],
    "anti-ragging policy": ["Our college follows a strict anti-ragging policy. Any violations can be reported to the grievance cell."],
    "faculty directory":[ "Find faculty details on the official website under the 'Faculty' section."],
    "student ID card process": ["Students can apply for an ID card through the admin office or student portal."],
    "college anthem": ["Our college anthem represents our values and tradition. Listen to it during college events."],
    "college handbook": ["Download the college handbook from the website for complete guidelines."],
    "engineering college history":[ "Our engineering college has been nurturing talent since XYZ year."],
    "engineering streams available": ["We offer various engineering branches, including CSE, ECE, Mechanical, Civil, and AI & Data Science."],
    "engineering seat intake capacity": ["The seat intake varies by branch. Check the admission brochure for details."],
    "college academic reputation":[ "We are known for excellence in academics, research, and student development."],
    "library facilities":[ "Our library is well-equipped with digital and physical resources for students."],
    "sports & gym facilities":[ "The college offers excellent sports infrastructure and a modern gym for students."],
    "cafeteria details": ["Our cafeteria serves a variety of healthy and affordable meals."],
    "student grievance cell": ["Students can report issues to the grievance cell for assistance."],
    "scholarship programs": ["Various scholarships are available based on merit and need. Visit the website for details."],
    "internship opportunities":[ "The college collaborates with top companies for internship programs."],
    "placement statistics": ["Our placement record is outstanding, with top recruiters visiting every year."],

 # Exam & Academics
    "exam date":[ "Exam dates are announced on the college website and notice board."],
    "exam syllabus":[ "The exam syllabus is available in the academic section on our website."],
    "exam pattern": ["Exam pattern varies by course. Check the syllabus document for details."],
    "exam registration process": ["Students can register for exams through the student portal or at the examination office."],
    "exam hall ticket download": ["Hall tickets can be downloaded from the student portal before exams."],
    "CGPA to percentage conversion":[ "Use the formula: Percentage = CGPA * 9.5. Confirm with the academic office."],
    "backlog exam rules": ["Students with backlogs must follow the re-exam registration process. Visit the exam office for details."],
    "academic calendar":[ "The academic calendar is available on the official website."],
    "credit system for subjects": ["Courses follow a credit-based system. Check the handbook for details."],
    "grace marks policy": ["Grace marks are awarded as per university guidelines. Confirm with the exam office."],
    "internship eligibility criteria":[ "Eligibility depends on academic performance and department guidelines."],
    "industrial visit schedule": ["Industrial visit schedules are shared by the respective departments."],
    "research paper publication process": ["Students can submit research papers via the college research cell."],
    "thesis submission guidelines": ["Final thesis submission guidelines are available on the student portal."],
    "final year project guidelines": ["Project guidelines are provided by the department."],
    "mini-project topics": ["Professors provide topic suggestions based on the curriculum."],
    "IEEE project guidelines": ["Follow IEEE format for project documentation and reports."],
    "project report writing format":[ "Report format guidelines are available in the academic handbook."],
    "patent filing for student projects": ["The college assists in filing patents for innovative projects."],
    "coding competition schedule":[ "Upcoming coding competitions are listed on the student portal."],
    "engineering entrance exams": ["Details on JEE, GATE, and other exams are available on the official websites."],
    "GATE exam preparation": ["Refer to NPTEL, online courses, and previous years’ q[uestion papers."],
    "GRE/TOEFL preparation resources": ["Official GRE/TOEFL websites and online platforms provide study materials."],
    "MOOCs & online courses for engineers": ["Platforms like Coursera, Udemy, and NPTEL offer relevant courses."],
    "engineering certifications (AWS, Cisco, Google Cloud, etc.)":[ "Students can enroll in certification programs through official vendor websites."],
     # Departments & Faculty
    "engineering departments list": ["Our college offers various engineering branches including CSE, ECE, Mechanical, Civil, AI & DS, and more."],
    "computer science faculty":[ "The CSE department faculty list is available on the website."],
    "electronics & communication faculty":[ "Find ECE department faculty details on the college website."],
    "mechanical engineering faculty":[ "Mechanical faculty details can be found in the faculty directory."],
    "civil engineering faculty":[ "Civil department faculty contact details are available online."],
    "electrical engineering faculty":[ "Find Electrical faculty details in the faculty section."],
    "biomedical engineering faculty":[ "Biomedical engineering faculty list is available on request."],
    "chemical engineering faculty":[ "Chemical engineering faculty details are listed on the website."],
    "aerospace engineering faculty": ["Aerospace faculty details are provided in the respective department section."],
    "automobile engineering faculty":[ "Automobile engineering faculty directory is updated on the website."],
    "artificial intelligence & data science department": ["AI & DS department details can be found in the engineering section."],
    "robotics & automation department": ["Robotics department information is available on the faculty page."],
    "engineering department achievements": ["Check out department-wise achievements in the annual report."],
    "faculty research areas": ["Faculty research interests are listed under their profiles."],
    "department-wise faculty contact details":[ "Find department-wise contact details in the faculty directory."],
    "department research labs":[ "Our engineering departments have specialized research labs for students."],
    "list of engineering electives": ["Engineering elective subjects are listed in the academic curriculum."],
    
# Engineering Subjects & Specializations
    ## Computer Science & IT
    "CSE syllabus": ["The Computer Science syllabus is available on the official website under the academics section."],
    "DSA preparation guide": ["You can find Data Structures & Algorithms preparation material in the library and online resources like GeeksforGeeks."],
    "DBMS concepts": ["DBMS notes and lecture recordings are available on the student portal."],
    "Operating System notes": ["OS study material can be accessed from the digital library section."],
    "Computer Networks basics": ["Learn about Computer Networks through our recommended books and online lectures."],
    "Cloud Computing syllabus": ["Cloud Computing is an elective subject. Check the course details online."],
    "Machine Learning courses":[ "ML courses are available on Coursera and college-affiliated training programs."],
    "Cybersecurity certifications":[ "Certifications like CEH, CISSP, and CompTIA Security+ are recommended for cybersecurity enthusiasts."],
    "IoT & Embedded Systems": ["IoT & Embedded Systems syllabus is part of the Electronics and CS curriculum."],
    
    ## Mechanical & Civil Engineering
    "Strength of Materials notes": ["Find Strength of Materials notes in the reference book section of the library."],
    "Thermodynamics reference books":[ "Recommended Thermodynamics books: Cengel & Boles, P.K. Nag."],
    "Fluid Mechanics lecture notes":[ "Lecture notes are available on the student portal."],
    "Engineering Drawing resources": ["Engineering Drawing tutorials are conducted in the lab and online classes."],
    "Structural Engineering subjects": ["Structural Engineering subjects include RCC Design, Steel Structures, etc."],
    
    ## Electronics & Electrical Engineering
    "Electronic Circuits syllabus": ["Electronic Circuits is a core subject for ECE students."],
    "VLSI & Embedded Systems": ["VLSI & Embedded Systems courses are available as electives."],
    "Microcontrollers & Microprocessors": ["Lab sessions and study materials are available for Microcontrollers & Microprocessors."],
    
    ## 🏠 Hostel & Campus Facilities
    "hostel rules": ["Hostel rules include curfew timings, visitor policies, and conduct guidelines. Refer to the hostel rulebook for details."],
    "hostel fees": ["Hostel fees vary based on room type (AC/Non-AC). Check the official website or contact the warden for details."],
    "hostel warden contact": ["The hostel warden can be contacted via the hostel office. Find their details on the notice board."],
    "hostel mess menu": ["The mess menu is updated weekly. Check the hostel notice board or mess area for the latest menu."],
    "hostel check-in process": ["New students must complete verification at the hostel office before check-in. ID proof and admission receipt are required."],
    "hostel guest rules": ["Guests are allowed only with prior permission from the warden. Visiting hours and guest policies apply."],
    "hostel curfew timing": ["The hostel curfew is at 10:00 PM for all students. Late entry requires prior approval from the warden."],
    "hostel complaint system": ["For hostel-related issues, register a complaint via the student grievance portal or contact the hostel office."],
    "laundry service in hostel": ["Laundry service is available in the hostel. Check the service schedule on the notice board."],
    "campus security": ["The campus has 24/7 security with CCTV surveillance. Security personnel are available at all entry points."],
    "campus lost and found": ["Lost items can be reported to the admin office. Check the lost & found section for recovered belongings."],
    "medical facilities": ["The campus has a medical center with doctors available during working hours. Emergency medical assistance is also provided."],
    "campus parking rules":[ "Students must register their vehicles for campus parking. Parking slots are assigned based on availability."],
    "canteen menu": ["The canteen menu includes a variety of food options. The updated menu is available at the canteen entrance."],
    "gym timings": ["The gym is open from 6 AM to 10 PM. Students must register at the gym office for access."],
    "college map": ["You can find the college campus map on the official website or at the help desk."],
    "bus timetable": ["The bus schedule is updated regularly. Check the transportation office or website for the latest timings."],
    "student ID card process":[ "Students can apply for an ID card through the admin office or online portal."],
    "college dress code policy":[ "The dress code policy includes formals for events and college-approved attire for labs."],
    "college WiFi registration":[ "Students can register for WiFi access via the IT department. Login credentials will be provided after verification."],
    "laundry service timings": ["Laundry services are available from 8 AM to 8 PM. Drop-off and pick-up times are mentioned in the hostel notice."],
    "hostel emergency contact": ["For emergencies, contact the hostel warden or security at the numbers listed in the hostel office."],
    "student grievance cell": ["The grievance cell handles student concerns. Submit your complaint via the official portal."],
    "study room availability": ["Study rooms in the library and hostel are open 24/7. Prior booking may be required during exams."],
    "hostel scholarship details": ["Some students may be eligible for hostel scholarships. Contact the finance office for details."],
    "AC & non-AC hostel room details":[ "Hostel rooms are available in AC and non-AC options. Allocation depends on availability and fee structure."],
    "campus fire safety guidelines": ["Fire safety measures include emergency exits and fire drills. Follow hostel and campus safety guidelines."],
    
    ##Events & Programs
    "technical fest": ["The annual technical fest includes coding competitions, robotics, and paper presentations. Stay tuned for registration details!"],
    "cultural fest":[ "Cultural fest features music, dance, drama, and fashion shows! Check the event calendar for audition dates."],
    "workshop schedule":[ "Upcoming workshops cover AI, IoT, cybersecurity, and more. Find the full schedule on the events page."],
    "guest lectures": ["Industry experts will be delivering guest lectures on trending topics. Stay updated with the upcoming sessions!"],
    "faculty lecture schedule": ["Faculty lecture schedules are available on the official timetable. Check the academic portal for updates."],
    "student club events": ["Join student club events to enhance your skills and network with peers! Visit the clubs section for upcoming activities."],
    "seminar schedule": ["Seminars on technology, business, and research insights are scheduled weekly. Check the events board for details."],
    "hackathon details": ["The next hackathon will be focused on innovation in AI and sustainability. Registration opens soon—stay tuned!"],
    "alumni meet schedule":[ "Reconnect with alumni at the annual alumni meet. Event details will be shared on the college website."],
    "annual day event": ["Celebrate the college's achievements and talent at the annual day event! Stay tuned for the date and performances."],
    "convocation ceremony date":[ "Convocation is scheduled for [Date]. Graduating students must complete the registration process before the deadline."],
    "freshers' welcome event":[ "Welcome, freshers! An exciting welcome event is planned with fun activities and interactions. Don't miss it!"],
    "farewell party schedule":[ "A memorable farewell party is being planned for final-year students. Details will be announced soon!"],
    "debate competitions":[ "Participate in the upcoming debate competitions on various topics. Register through the debate club!"],
    "business plan competition details": ["Pitch your startup ideas at the business plan competition and win exciting rewards. Check the entrepreneurship cell for details."],
    "career guidance seminar": ["Attend career guidance seminars to get insights into placements, higher studies, and industry trends."],
    "leadership talk series": ["Learn from successful leaders in our leadership talk series. Next session details will be shared soon."],
    "social service programs": ["Be part of social service initiatives like cleanliness drives, awareness campaigns, and rural outreach."],
    "blood donation camp schedule": ["Join us in saving lives at the upcoming blood donation camp. Venue and timing details will be announced soon."],
   
   "sports activities": ("Our college offers a variety of sports activities, including cricket, football, basketball, badminton, and more. Join a sport today!", ["View All Sports", "Join a Team", "Practice Timings"]),
    "inter-college sports events": ("Inter-college sports events are held annually with various competitions in multiple sports. Stay updated with upcoming tournaments!", ["Upcoming Events", "How to Participate?", "Team Selection Process"]),
    "gym membership details": ("The college gym is open to students and faculty. Memberships are available on a monthly and yearly basis.", ["Membership Fees", "Timings", "Facilities Available"]),
    "yoga sessions": ("Join our yoga sessions to improve flexibility and mental well-being. Sessions are held every morning and evening.", ["Session Timings", "Instructor Details", "How to Register?"]),
    "meditation classes": ("Our meditation classes focus on mindfulness and stress reduction. Open to all students and faculty.", ["Class Schedule", "Benefits", "Registration Process"]),
    "dhyan schedule": ("Dhyan sessions are organized weekly for deep relaxation and spiritual growth. Open to all.", ["Next Session Date", "Instructor Info", "How to Join?"]),
    "spiritual events on campus": ("Our campus hosts various spiritual events, including satsangs, meditation camps, and yoga retreats.", ["Upcoming Events", "How to Participate?", "Guest Speakers"]),
    "motivational speaker events": ("Get inspired by renowned motivational speakers in our upcoming sessions.", ["Speaker List", "Event Dates", "How to Attend?"]),
    "health checkup camps": ("Regular health checkup camps are conducted for students and faculty. Check the next schedule here.", ["Next Camp Date", "Health Services Offered", "Registration Process"]),
    "blood donation camp dates": ("Join us in saving lives by participating in our blood donation camps.", ["Upcoming Camp", "Eligibility Criteria", "How to Register?"]),
    "chess tournament schedule": ("The annual chess tournament is around the corner. Register now and showcase your skills!", ["Tournament Date", "Registration Link", "Past Winners"]),
    "cricket practice timings": ("Cricket practice sessions are held daily on the main ground. Open for all registered players.", ["Practice Schedule", "Coach Contact", "How to Join?"]),
    "football ground availability": ("The football ground is open for practice and matches. Book a slot in advance!", ["Availability Timings", "Booking Process", "Team Trials"]),
    "basketball team trials": ("Basketball team trials are scheduled for next week. Interested players must register in advance.", ["Trial Date", "Coach Details", "Eligibility Criteria"]),
    "badminton court booking process": ("Badminton courts can be booked via the student portal or at the sports office.", ["Booking Instructions", "Court Timings", "Fees & Equipment"]),
    "sports scholarship details": ("Our college offers sports scholarships for outstanding athletes. Apply now!", ["Eligibility Criteria", "Application Process", "Scholarship Amount"]),
    "table tennis match schedule": ("Table tennis matches are held every weekend in the indoor sports arena.", ["Match Timings", "Registration Link", "Previous Match Results"]),

    "attendance record":[ "You can check your attendance record in the student portal under the 'Attendance' section."],
    "leave application":[ "To apply for leave, visit the student portal and submit a leave application under 'Student Services'."],
    "medical leave approval process": ["Medical leave requires a doctor's certificate. Upload the document in the portal for approval."],
    "library location":[ "The library is located on the ground floor of the main academic building."],
    "library membership": ["To get a library membership, fill out the form on the library website and visit the library with your student ID."],
    "library book request": ["You can request a book through the library portal. Login and search for the book to place a request."],
    "library late fine policy": ["Late returns incur a fine of ₹5 per day. Please return books on time to avoid penalties."],
    "scholarship details": ["Scholarship details are available in the 'Scholarship' section of the student portal."],
    "education loan assistance": ["For education loan guidance, contact the student financial aid office or visit our website."],
    "internship opportunities":[ "Check the 'Internships' section on the placement portal for the latest internship opportunities."],
    "placement details":[ "Placement details and upcoming drives can be found on the placement cell's official website."],
    "career counseling": ["Book a session with our career counselor through the counseling center's webpage."],
    "resume building workshops":[ "Resume-building workshops are conducted every semester. Check the student portal for schedules."],
    "mock interviews schedule":[ "Mock interviews are scheduled before placement season. Register through the placement cell."],
    "student helpline":[ "For any issues, contact the student helpline at +91-XXXXXXXXXX or email support@college.edu."],
    "counseling center location": ["The counseling center is located on the second floor of the administration block."],
    "study abroad opportunities": ["Details about study abroad programs are available in the 'International Office' section of our website."],
    "foreign exchange programs":[ "Foreign exchange programs require applications through the International Relations Office."],
    "student mentorship programs": ["Our mentorship program pairs students with senior mentors. Register through the student services portal."],
    "campus tour request": ["To request a campus tour, fill out the form available on our website."],
    "NSS activities":[ "NSS activities are regularly updated on the NSS portal. Check with your NSS leader for more details."],
    "NCC training details":[ "NCC training schedules are available on the NCC section of our website."],

     # Placements & Careers
    "placement companies list":[ "The list of companies participating in placements is available on the placement cell website."],
    "placement highest package":[ "The highest package details are updated every year on the placement statistics page."],
    "placement process":[ "The placement process includes eligibility screening, resume submission, aptitude tests, and interviews."],
    "off-campus placement assistance":[ "Our placement cell provides guidance for off-campus opportunities through job fairs and industry tie-ups."],
    "internship certificate process":[ "Internship certificates are issued by the company. Ensure you complete all requirements and submit your final report."],
    "alumni placement stats":[ "Alumni placement statistics are available on the college website under the 'Placement Reports' section."],
    "startup incubator details": ["Our startup incubator supports student entrepreneurs with mentorship and funding opportunities."],
    "entrepreneurship cell info": ["Join our Entrepreneurship Cell to connect with industry leaders and get startup guidance."],
    "internship stipend details": ["Stipends vary by company. Check your internship offer letter for details."],
    "campus drive schedule":[ "The campus placement drive schedule is updated on the placement portal."],
    "pre-placement training workshops": ["Pre-placement training sessions include resume building, aptitude tests, and interview preparation."],
    "corporate guest speakers list": ["Guest lectures are conducted regularly. Check the event calendar for upcoming sessions."],
    "placement eligibility criteria":[ "Eligibility for placements depends on academic performance and skill assessments."],
    "resume screening process": ["Resumes are screened based on relevance to job roles. Ensure your resume highlights key skills and projects."],
    "aptitude test practice resources": ["Practice resources for aptitude tests are available on the placement cell website."],
    "HR interview preparation guide":[ "HR interviews focus on soft skills, communication, and company knowledge. Prepare with mock interviews."],
    "placement drive schedule": ["Upcoming placement drives are listed on the placement cell notice board."],
    "engineering companies hiring trends": ["Latest hiring trends for engineers are updated in the career guidance portal."],
    "technical interview preparation":[ "Technical interview preparation materials are available in the coding club and placement cell."],
    "software engineer job market insights":[ "Get industry trends and job market insights from our placement team's reports."],
    "GATE exam preparation guide": ["GATE preparation guides and past papers are available in the student resources section."],
    "campus recruitment process":[ "Campus recruitment includes multiple rounds of screening, group discussions, and interviews."],
    "resume building for engineers":[ "Attend our resume workshops to create an industry-standard resume."],
    "freelancing opportunities for engineers":[ "Freelancing platforms like Upwork and Fiverr offer engineering job opportunities."],
    "entrepreneurship support for students":[ "Students can seek startup support from the Entrepreneurship Cell."],
    "startup funding for engineers":[ "Funding opportunities are available through our startup incubator and investor network."],
    
      
    # Student Clubs & Extra-Curricular
    "student council info": ["The student council represents students in college affairs. Contact the council office for more details."],
    "club registration process": ["To register a new club, submit a proposal to the student activities office."],
    "music club events":[ "Music club organizes concerts and jam sessions. Check the event calendar for upcoming performances."],
    "dance club auditions":[ "Auditions for the dance club are held at the start of each semester. Contact the club coordinator for details."],
    "drama club schedule": ["The drama club meets every weekend. Rehearsals are held in the auditorium."],
    "photography club workshops":[ "Workshops on photography techniques are conducted monthly. Register on the student portal."],
    "coding club hackathons":[ "The coding club organizes hackathons and coding challenges. Join the club forum for updates."],
    "robotics club events":[ "Robotics club conducts competitions and workshops on AI and automation."],
    "literature club activities":[ "Book readings, poetry slams, and creative writing contests are part of our literature club."],
    "art & craft club exhibitions":[ "The club hosts art exhibitions every semester showcasing student talent."],
    "environmental club initiatives":[ "Join our environmental club to participate in sustainability and tree-planting drives."],
    "public speaking club sessions":[ "Improve your speaking skills with weekly public speaking sessions."],
    "student magazine publishing process":[ "Students can submit articles to the editorial team for magazine publishing."],
    "poetry competition dates":[ "Poetry competitions are held annually. Stay tuned for announcements."],
    "film-making club projects":[ "Join the film-making club to work on short films and video editing projects."],
    
    # IT & Technical Help
    "college portal login issues":[ "If you're facing login issues, reset your password or contact IT support."],
    "email ID registration":[ "To register your college email ID, visit the IT helpdesk."],
    "reset college portal password":[ "Use the 'Forgot Password' option on the portal to reset your password."],
    "college ERP issues":[ "For ERP-related issues, contact the technical support team."],
    "technical support contact": ["Reach out to IT support at support@college.edu for assistance."],
    "WiFi access troubleshooting":[ "Ensure you have registered your device with the college network."],
    "student email configuration guide":[ "Follow the email setup guide available on the IT support page."],
    "online class access issues": ["Check your internet connection and ensure you have the correct class link."],
    "project submission portal login":[ "If you cannot log in, reset your password or contact IT support."],
    "e-learning platform access":[ "For issues accessing e-learning, check your login credentials."],
    "college app download link":[ "Download the official college app from the app store or website."],
    "college LMS (Learning Management System) support": ["For LMS support, contact your course administrator."],
    "student ERP login issues":[ "Ensure you are using the correct student ID and password."],
    "college app bug report process":[ "Report app bugs via the feedback form in the app settings."],
    "engineering software installation guide":[ "Follow the installation guide provided by your department."],
    "remote lab access for engineering":[ "Request remote lab access through your professor."],
    "3D printing lab details":[ "3D printing lab is open to engineering students. Book a slot online."],
    "high-performance computing lab access":[ "Request access from the IT department for HPC lab usage."],
    
    # Administration & Governance
    "trust details":[ "The college trust information is available in the administration office."],
    "student grievance redressal":[ "Submit grievances via the student grievance portal."],
    "RTI filing process":[ "File RTI applications through the college legal cell."],
    "college rules and policies":[ "Refer to the student handbook for college policies."],
    "anti-ragging cell contact":[ "Report ragging incidents to the anti-ragging cell at +91-XXXXXXXXXX."],
    "disciplinary action process":[ "Disciplinary actions are taken as per college regulations."],
    "college fee structure":[ "Fee details are available on the college website."],
    "payment deadlines":[ "Check the academic calendar for fee payment deadlines."],
    "refund policy": ["Refunds are processed as per the college refund policy."],
    "college complaints & feedback system":[ "Submit complaints and feedback through the online portal."],
    "college annual budget report":[ "Annual budget reports are available upon request from the administration."],
    "student insurance policy details":[ "Insurance policies for students are managed by the administration."],
    "transportation facility details":[ "Bus routes and transport schedules are available on the college website."],
    "fee concession schemes": ["Apply for fee concessions through the financial aid office."],
    "financial aid for students":[ "Various financial aid programs are available. Contact student services."],
    "academic probation policies": ["Students on academic probation must meet with their academic advisors."],
    "engineering scholarship details": ["Scholarship details for engineering students are updated on the website."],
    "student research funding process": ["Funding for student research is available through grants and sponsorships."],
    "patent filing for student innovations":[ "The college supports students in patent filing. Contact the innovation cell."],
    "technical student exchange programs": ["Exchange programs with technical universities are available."],
    "engineering faculty hiring process": ["Faculty hiring is based on eligibility criteria set by the college."],



   
}

# Multi-turn conversation memory
conversation_flow = {
    "initial": {
        "message": "Hello! How can I assist you today?",
        "options": [
            "General College Info",
            "Exam & Academics",
            "Hostel & Facilities",
            "Placements & Careers",
            "Student Services",
            "Events & Clubs",
            "IT & Technical Help"
        ]
    },
    "General College Info": {
        "message": "What information do you need?",
        "options": [
            "College Address", "College Trustees", "College Management",
            "College Principal", "College Dean", "College Registrar",
            "College Website", "College Contact Number", "College Email",
            "College Admission Process", "College Prospectus", "College Ranking",
            "College Accreditation", "NAAC Grade", "UGC Approval Status",
            "AICTE Approval", "Autonomous Status", "College Affiliations",
            "Student Enrollment Process", "Campus Area", "College Motto & Vision",
            "Campus Facilities", "College Rules & Policies", "Anti-Ragging Policy",
            "Faculty Directory", "Student ID Card Process", "College Anthem",
            "College Handbook", "Engineering College History", "Engineering Streams Available",
            "Engineering Seat Intake Capacity", "College Academic Reputation",
            "Library Facilities", "Sports & Gym Facilities", "Cafeteria Details",
            "Student Grievance Cell", "Scholarship Programs", "Internship Opportunities",
            "Placement Statistics"
        ]
    },
     "Exam & Academics": {
        "message": "What academic information do you need?",
        "options": [
            "Exam Date", "Exam Syllabus", "Exam Pattern", "Exam Registration Process",
            "Exam Hall Ticket Download", "CGPA to Percentage Conversion", "Backlog Exam Rules",
            "Academic Calendar", "Credit System for Subjects", "Grace Marks Policy",
            "Internship Eligibility Criteria", "Industrial Visit Schedule",
            "Research Paper Publication Process", "Thesis Submission Guidelines",
            "Final Year Project Guidelines", "Mini-Project Topics", "IEEE Project Guidelines",
            "Project Report Writing Format", "Patent Filing for Student Projects",
            "Coding Competition Schedule", "Engineering Entrance Exams", "GATE Exam Preparation",
            "GRE/TOEFL Preparation Resources", "MOOCs & Online Courses for Engineers",
            "Engineering Certifications (AWS, Cisco, Google Cloud, etc.)"
        ]
    },
     
    
}



# Function to get a smart response
def get_bot_response(user_message):
    user_message = user_message.lower()
    chat_history = session.get("chat_history", [])
    previous_query = session.get("previous_query")
    
    # Check for multi-step conversation flow
    if previous_query in conversation_flow:
        response = conversation_flow[previous_query].get(user_message, None)
        if response:
            session["previous_query"] = None
            chat_history.append((user_message, response))
            session["chat_history"] = chat_history
            return response
    
    # Check for auto-reply matches
    for key in auto_reply_data.keys():
        if key in user_message:
            session["previous_query"] = key
            chat_history.append((user_message, auto_reply_data[key][0]))
            session["chat_history"] = chat_history
            return auto_reply_data[key][0]
    
    # If no match, generate a fallback response
    fallback_responses = [
        "I'm not sure about that. Check with the college admin.",
        "Can you please clarify?", "I might not have that info, but I can help with other queries."
    ]
    response = random.choice(fallback_responses)
    chat_history.append((user_message, response))
    session["chat_history"] = chat_history
    return response

# Function to get suggestions dynamically
def get_suggestions(query):
    query = query.lower()
    return [q for q in query_suggestions if query in q]

# Function to get auto-suggested replies
def get_auto_replies(query):
    query = query.lower()
    return auto_reply_data.get(query, [])

# Function to retrieve past conversation history
def get_chat_history():
    return session.get("chat_history", [])