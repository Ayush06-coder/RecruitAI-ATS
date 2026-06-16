import re

import spacy
nlp = spacy.load("en_core_web_lg")

def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "Email not found"

def extract_phone(text):
    pattern = r"\+?\d[\d\s\-]{8,15}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "Phone number not found"

def extract_name(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    headings = {
        "Resume", "Cv", "Curriculum", "Vitae", "Profile",
        "Summary", "Education", "Experience", "Skills",
        "Objective", "Contact", "References", "Professional"
    }

    job_titles = {
        "junior", "senior", "developer", "engineer", "analyst",
        "manager", "designer", "lead", "frontend", "backend",
        "fullstack", "full-stack", "full", "stack", "software",
        "intern", "consultant", "architect", "executive",
        "associate", "trainee", "assistant", "scientist",
        "officer", "head", "director", "specialist", "coordinator",
        "administrator", "representative", "supervisor", "technician",
        "operator", "freelance", "contractor", "web", "data", "product"
    }

    for i in range(len(lines[:10]) - 1):
        w1, w2 = lines[i], lines[i + 1]

        if (
            w1.isupper() and w2.isupper()
            and len(w1.split()) == 1
            and len(w2.split()) == 1
            and w1.title() not in headings
            and w2.title() not in headings
            and w1.lower() not in job_titles
            and w2.lower() not in job_titles
        ):
            return f"{w1} {w2}".title()

    text_for_nlp = " ".join(
        line.title() if line.isupper() else line
        for line in lines[:10]
    )

    doc = nlp(text_for_nlp)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            words = ent.text.split()

            clean_words = []
            for word in words:
                word_clean = word.strip().lower().rstrip(",.:;-|")
                if word_clean in job_titles:
                    break
                if any(jt in word_clean for jt in ["developer", "engineer", "analyst", "manager", "designer", "consultant", "architect", "intern", "trainee", "assistant"]):
                    break
                clean_words.append(word)

            if len(clean_words) >= 2:
                result = " ".join(clean_words)
                last_word = clean_words[-1].lower().rstrip(",.:;-|")
                if last_word not in job_titles:
                    return result

    return "Name not found"

SKILLS_LIST = [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "R", "Swift", "Kotlin", "Go", "Rust", "PHP", "Ruby", "Scala",
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Django",
    "Flask", "FastAPI", "REST API", "GraphQL",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
    "NumPy", "Matplotlib", "Seaborn",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis",
    "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Linux", "Streamlit", "Power BI", "Tableau", "Excel",
    "Data Structures", "Algorithms", "OOP", "System Design",
    "Jenkins", "Jest", "CI/CD", "Agile", "Scrum", "Microservices",
    "RESTful", "Express.js", "Next.js", "Spring Boot", "Hibernate",
    "Flutter", "Dart", "Firebase", "Supabase", "Prisma", "TypeORM",
    "Tailwind CSS", "Bootstrap", "Sass", "LESS", "Webpack", "Vite",
    "Apache Kafka", "RabbitMQ", "Elasticsearch", "Logstash", "Kibana",
    "Prometheus", "Grafana", "Terraform", "Ansible", "Chef", "Puppet",
    "Nginx", "Apache", "Tomcat", "Jetty", "WildFly",
    "Unity", "Unreal Engine", "Blender", "Maya", "3ds Max",
    "Figma", "Adobe XD", "Sketch", "InVision", "Canva",
    "Jira", "Confluence", "Trello", "Asana", "Monday.com",
    "Slack", "Teams", "Zoom", "Notion", "Obsidian",
    "Postman", "Insomnia", "Swagger", "OpenAPI",
    "GitLab", "Bitbucket", "Azure DevOps", "CircleCI", "Travis CI",
    "Heroku", "Vercel", "Netlify", "Firebase Hosting", "AWS Amplify",
    "DigitalOcean", "Linode", "Vultr", "OVH", "Hetzner",
    "Oracle", "SQL Server", "DB2", "Sybase", "Informix",
    "Cassandra", "CouchDB", "Neo4j", "DynamoDB", "Cosmos DB",
    "InfluxDB", "TimescaleDB", "ClickHouse", "Snowflake", "BigQuery",
    "Redshift", "Athena", "Presto", "Trino", "Druid",
    "Hadoop", "Spark", "Hive", "Impala", "Pig", "Kafka",
    "Airflow", "Prefect", "Dagster", "Luigi", "NiFi",
    "MLflow", "Kubeflow", "DVC", "Weights & Biases", "Neptune",
    "Optuna", "Ray", "Dask", "Modin", "Vaex", "Polars",
    "Spark NLP", "Hugging Face", "OpenAI", "Anthropic", "Cohere",
    "LangChain", "LlamaIndex", "CrewAI", "AutoGen", "Semantic Kernel",
    "Pinecone", "Weaviate", "Chroma", "Milvus", "Qdrant", "FAISS",
    "OpenCV", "Pillow", "Scikit-image", "SimpleITK", "ITK",
    "NLTK", "spaCy", "Gensim", "TextBlob", "Pattern",
    "Stanford NLP", "AllenNLP", "Flair", "Stanza", "Transformers",
    "BERT", "GPT", "T5", "LLaMA", "Mistral", "Claude", "Gemini",
    "YOLO", "RCNN", "Mask R-CNN", "DETR", "SAM",
    "Stable Diffusion", "Midjourney", "DALL-E", "Imagen",
    "Whisper", "TTS", "Coqui", "Murf", "ElevenLabs",
    "ONNX", "TensorRT", "OpenVINO", "Core ML", "TFLite",
    "CUDA", "cuDNN", "ROCm", "OpenCL", "Vulkan", "Metal",
    "MPI", "OpenMP", "CUDA-aware MPI", "NCCL", "Gloo",
    "gRPC", "Protobuf", "Thrift", "Avro", "MessagePack",
    "WebSocket", "Socket.io", "SignalR", "MQTT", "CoAP",
    "OAuth", "JWT", "SAML", "LDAP", "Kerberos", "SSO",
    "HashiCorp Vault", "AWS KMS", "Azure Key Vault", "Google Cloud KMS",
    "SonarQube", "ESLint", "Prettier", "Black", "Flake8", "Pylint",
    "Mypy", "Pyright", "TypeScript Compiler", "Babel", "SWC",
    "Storybook", "Chromatic", "Cypress", "Playwright", "Selenium",
    "Appium", "Detox", "Maestro", "Katalon", "TestComplete",
    "JMeter", "Gatling", "Locust", "k6", "Artillery",
    "Grafana", "Datadog", "New Relic", "Dynatrace", "AppDynamics",
    "Splunk", "ELK Stack", "Fluentd", "Logstash", "Beats",
    "PagerDuty", "Opsgenie", "VictorOps", "xMatters",
    "ServiceNow", "Remedy", "Jira Service Management",
    "Confluence", "Notion", "SharePoint", "Google Workspace",
    "Microsoft 365", "Slack", "Discord", "Mattermost", "Rocket.Chat",
    "Zoom", "Google Meet", "Microsoft Teams", "Webex", "GoToMeeting",
    "Loom", "Vidyard", "Wistia", "Kaltura", "Panopto",
    "Figma", "Sketch", "Adobe XD", "InVision", "Axure", "Balsamiq",
    "Miro", "Mural", "Lucidchart", "Draw.io", "Whimsical",
    "Canva", "Adobe Creative Suite", "Photoshop", "Illustrator",
    "InDesign", "Premiere Pro", "After Effects", "Audition",
    "Blender", "Cinema 4D", "Maya", "3ds Max", "ZBrush",
    "Houdini", "Substance Painter", "Substance Designer",
    "Unreal Engine", "Unity", "Godot", "CryEngine", "Lumberyard",
    "GameMaker", "Construct", "RPG Maker", "Ren'Py",
    "Arduino", "Raspberry Pi", "ESP32", "STM32", "PIC",
    "FPGA", "VHDL", "Verilog", "SystemVerilog", "HLS",
    "MATLAB", "Simulink", "LabVIEW", "Mathematica", "Maple",
    "ANSYS", "COMSOL", "Abaqus", "SolidWorks", "AutoCAD",
    "CATIA", "NX", "Creo", "Inventor", "Fusion 360",
    "Revit", "ArchiCAD", "SketchUp", "Rhino", "Grasshopper",
    "Lumion", "Enscape", "V-Ray", "Corona Renderer", "Arnold",
    "Octane Render", "Redshift", "Cycles", "Eevee", "Mantra",
    "Houdini Engine", "Clarisse", "Katana", "Mari", "Nuke",
    "DaVinci Resolve", "Final Cut Pro", "Avid Media Composer",
    "Premiere Pro", "After Effects", "Motion", "Compressor",
    "Logic Pro", "Pro Tools", "Ableton Live", "FL Studio",
    "Cubase", "Nuendo", "Reaper", "Studio One", "Bitwig",
    "Reason", "Maschine", "Komplete", "Kontakt", "Serato",
    "Traktor", "Rekordbox", "Virtual DJ", "Djay",
    "SAS", "SPSS", "Stata", "Minitab", "JMP",
    "RStudio", "Jupyter", "Zeppelin", "Databricks", "Snowflake",
    "Palantir", "Alteryx", "Knime", "RapidMiner", "Weka",
    "Orange", "RapidMiner", "Dataiku", "Domino", "H2O.ai",
    "DataRobot", "AutoML", "TPOT", "Auto-sklearn", "Auto-PyTorch",
    "Featuretools", "TSFresh", "Prophet", "ARIMA", "SARIMA",
    "LSTM", "GRU", "Transformer", "BERT", "RoBERTa", "DeBERTa",
    "XLNet", "ALBERT", "ELECTRA", "DistilBERT", "MobileBERT",
    "TinyBERT", "Longformer", "BigBird", "Reformer", "Performer",
    "Linformer", "Linear Attention", "Flash Attention", "Sparse Attention",
    "Mixture of Experts", "Switch Transformer", "GLaM", "PaLM",
    "Chinchilla", "Gopher", "LaMDA", "Bard", "Claude", "GPT-4",
    "GPT-3.5", "GPT-3", "GPT-2", "GPT", "Codex", "Copilot",
    "AlphaCode", "StarCoder", "CodeT5", "CodeBERT", "GraphCodeBERT",
    "UniXcoder", "CodeGPT", "PolyCoder", "SantaCoder", "InCoder",
    "Replit", "GitHub Codespaces", "Gitpod", "CodeSandbox",
    "StackBlitz", "JSFiddle", "CodePen", "Glitch", "Repl.it",
    "LeetCode", "HackerRank", "Codeforces", "AtCoder", "TopCoder",
    "Codewars", "Exercism", "Edabit", "CheckiO", "CodeSignal",
    "InterviewBit", "Scaler", "AlgoExpert", "NeetCode",
    "System Design Primer", "Designing Data-Intensive Applications",
    "Clean Code", "Clean Architecture", "Domain-Driven Design",
    "The Pragmatic Programmer", "Code Complete", "Refactoring",
    "Head First Design Patterns", "Gang of Four", "SOLID",
    "DRY", "KISS", "YAGNI", "TDD", "BDD", "DDD",
    "Event Sourcing", "CQRS", "Saga Pattern", "Outbox Pattern",
    "Circuit Breaker", "Retry Pattern", "Bulkhead", "Timeout",
    "Idempotency", "Optimistic Locking", "Pessimistic Locking",
    "MVCC", "ACID", "BASE", "CAP Theorem", "PACELC",
    "Sharding", "Partitioning", "Replication", "Federation",
    "Denormalization", "Indexing", "Query Optimization",
    "Connection Pooling", "Caching Strategies", "Cache Invalidation",
    "CDN", "Edge Computing", "Serverless", "FaaS", "PaaS",
    "IaaS", "SaaS", "DaaS", "BaaS", "MBaaS",
    "Multi-tenancy", "Single-tenant", "Hybrid Cloud", "Multi-cloud",
    "Private Cloud", "Public Cloud", "Community Cloud",
    "Zero Trust", "Defense in Depth", "Least Privilege",
    "RBAC", "ABAC", "PBAC", "MAC", "DAC",
    "SOC 2", "ISO 27001", "GDPR", "CCPA", "HIPAA", "PCI DSS",
    "NIST", "CIS Controls", "OWASP", "SANS", "CERT",
    "Threat Modeling", "STRIDE", "PASTA", "Trike", "VAST",
    "Penetration Testing", "Red Team", "Blue Team", "Purple Team",
    "Incident Response", "Forensics", "Malware Analysis",
    "Reverse Engineering", "Binary Exploitation", "Web Exploitation",
    "Cryptography", "PKI", "SSL/TLS", "IPSec", "VPN",
    "Blockchain", "Ethereum", "Solidity", "Hyperledger", "Corda",
    "Quorum", "Polygon", "Arbitrum", "Optimism", "zkSync",
    "StarkNet", "Cosmos", "Polkadot", "Substrate", "Avalanche",
    "Solana", "Cardano", "Tezos", "Algorand", "NEAR",
    "IPFS", "Filecoin", "Arweave", "Sia", "Storj",
    "Chainlink", "The Graph", "Uniswap", "Aave", "Compound",
    "MakerDAO", "Curve", "SushiSwap", "PancakeSwap",
    "OpenZeppelin", "Hardhat", "Truffle", "Foundry", "Brownie",
    "Remix", "MetaMask", "WalletConnect", "Rainbow",
    "Ethers.js", "Web3.js", "Web3.py", "viem", "wagmi",
    "Token Standards", "ERC-20", "ERC-721", "ERC-1155", "ERC-4337",
    "DeFi", "NFT", "DAO", "GameFi", "SocialFi", "DeSci",
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_LIST:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills if found_skills else ["No skills found"]

EDUCATION_KEYWORDS = [
    "b.tech", "m.tech", "btech", "mtech", "b.e", "m.e",
    "b.sc", "m.sc", "bsc", "msc", "bca", "mca", "bba", "mba",
    "bachelor", "master", "phd", "doctorate", "diploma",
    "b.com", "m.com", "b.a", "m.a"
]

UNIVERSITY_KEYWORDS = [
    "university", "college", "institute", "iit", "nit",
    "bits", "amity", "vit", "manipal", "school of"
]

def extract_education(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    section_keywords = ["education", "qualification", "academic"]
    stop_keywords = ["experience", "skills", "projects",
                     "certifications", "summary", "objective"]
    keywords = EDUCATION_KEYWORDS + UNIVERSITY_KEYWORDS

    education_lines = []
    in_education_section = False

    for line in lines:
        line_lower = line.lower()

        if any(kw in line_lower for kw in section_keywords):
            in_education_section = True
            continue

        if in_education_section and any(kw in line_lower for kw in stop_keywords):
            break

        if in_education_section:
            education_lines.append(line)

    found_education = [
        line for line in education_lines
        if any(kw in line.lower() for kw in keywords)
    ]

    return found_education if found_education else ["Education not found"]

ROLE_KEYWORDS = [
    "intern", "internship", "engineer", "developer", "analyst",
    "manager", "consultant", "designer", "architect", "lead",
    "executive", "associate", "trainee", "assistant", "scientist"
]

COMPANY_KEYWORDS = [
    "technologies", "solutions", "systems", "services", "consulting",
    "software", "tech", "labs", "pvt", "ltd", "inc", "limited",
    "corp", "group", "studio"
]

def extract_experience(text):
    """
    Extract experience from resume text.
    Handles: DOCX bold/italic, various date formats, bullet points, etc.
    Never returns empty if experience section exists.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    section_keywords = [
        "work experience", "professional experience", "experience",
        "employment", "work history", "career history", "professional background",
        "employment history", "job history", "career summary"
    ]

    stop_keywords = [
        "education", "academic", "qualification", "degree",
        "skills", "technical skills", "core skills", "key skills",
        "projects", "personal projects", "side projects",
        "certifications", "certificates", "licenses",
        "achievements", "awards", "honors",
        "publications", "research", "papers",
        "languages", "interests", "hobbies", "activities",
        "references", "referees", "testimonials",
        "summary", "objective", "profile", "about me"
    ]

    def _is_section_header(line, keywords):
        line_clean = line.lower().replace("**", "").replace("*", "").strip()
        for kw in keywords:
            if kw in line_clean:
                words = line_clean.split()
                if len(words) <= 6:
                    if not any(c in line_clean for c in [".", ":"] if c not in kw.split()):
                        return True
                    if line.isupper() or line.istitle() or "**" in line or len(words) <= 3:
                        return True
        return False

    def _has_date(line):
        date_patterns = [
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',
            r'\b\d{4}\s*[-–—]\s*(present|current|now|today|\d{4})\b',
            r'\b\d{1,2}/\d{4}\s*[-–—]\s*(present|current|now|\d{1,2}/\d{4})\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
            r'\b\d{4}\s*[-–—]\s*\d{4}\b',
            r'\b\d{4}\s+to\s+(present|current|\d{4})\b',
            r'\b\d{4}\s*[-–—]\s*\b',
            r'\b(present|current)\b',
        ]
        line_lower = line.lower()
        for pattern in date_patterns:
            if re.search(pattern, line_lower, re.IGNORECASE):
                return True
        return False

    def _is_bullet_point(line):
        bullet_starts = ["•", "-", "*", "►", "→", "⇒", ">", "◦", "▪", "▫", "●", "○", "‣", "⁃", "◆"]
        stripped = line.strip()
        return any(stripped.startswith(b) for b in bullet_starts) or re.match(r'^[\s]*[•\-*►→⇒>◦▪▫●○‣⁃◆]\s*', stripped)

    def _is_role_line(line):
        role_keywords = [
            "engineer", "developer", "analyst", "manager", "consultant",
            "designer", "architect", "lead", "intern", "trainee",
            "assistant", "scientist", "officer", "head", "director",
            "specialist", "coordinator", "administrator", "supervisor",
            "technician", "operator", "executive", "associate",
            "freelance", "contractor"
        ]
        line_lower = line.lower().replace("**", "").replace("*", "").strip()
        return any(kw in line_lower for kw in role_keywords)

    def _is_company_line(line):
        company_keywords = [
            "technologies", "solutions", "systems", "services", "consulting",
            "software", "tech", "labs", "pvt", "ltd", "inc", "limited",
            "corp", "group", "studio", "company", "corporation",
            "industries", "ventures", "partners", "global", "digital",
            "innovations", "enterprises", "networks", "media", "cloud"
        ]
        line_lower = line.lower().replace("**", "").replace("*", "").strip()
        return any(kw in line_lower for kw in company_keywords)

    def _is_continuation_line(line):
        """Check if line is a continuation of previous text."""
        line_clean = line.strip()
        if not line_clean:
            return False
        if line_clean[0].islower():
            return True
        if len(line_clean) < 40 and not line_clean.endswith(('.', '!', '?', ':', ';')):
            return True
        return False

    def _clean_line(line):
        return line.replace("**", "").replace("*", "").strip()

    # Find experience section
    exp_start_idx = -1
    for i, line in enumerate(lines):
        if _is_section_header(line, section_keywords):
            exp_start_idx = i
            break

    if exp_start_idx == -1:
        for i, line in enumerate(lines):
            line_clean = line.lower().replace("**", "").replace("*", "").strip()
            if any(kw in line_clean for kw in section_keywords):
                if len(line_clean.split()) <= 4:
                    exp_start_idx = i
                    break

    if exp_start_idx == -1:
        entries = []
        for i, line in enumerate(lines):
            if _has_date(line) and (_is_role_line(line) or _is_company_line(line) or len(line.split()) <= 10):
                entries.append(line)
        return entries if entries else ["Experience not found"]

    # Find where experience section ends
    exp_end_idx = len(lines)
    for i in range(exp_start_idx + 1, len(lines)):
        if _is_section_header(lines[i], stop_keywords):
            exp_end_idx = i
            break

    raw_exp_lines = lines[exp_start_idx + 1:exp_end_idx]

    if not raw_exp_lines:
        return ["Experience not found"]

    # Merge continuation lines
    merged_lines = []
    for line in raw_exp_lines:
        if merged_lines and _is_continuation_line(line) and not _is_bullet_point(line):
            prev = merged_lines[-1]
            if not prev.endswith(('.', '!', '?', ':', ';', ')', ']', '}')):
                merged_lines[-1] = prev + " " + line
                continue
        merged_lines.append(line)

    # Group entries
    entries = []
    current_entry = []

    for line in merged_lines:
        line_clean = _clean_line(line)

        if not line_clean:
            if current_entry:
                entries.append("\n".join(current_entry))
                current_entry = []
            continue

        has_date = _has_date(line)
        is_role = _is_role_line(line)
        is_company = _is_company_line(line)
        is_bullet = _is_bullet_point(line)
        word_count = len(line_clean.split())
        is_short = word_count <= 8
        is_all_caps = line.isupper() and word_count <= 6

        is_new_entry = False

        if has_date and is_role and not is_bullet:
            is_new_entry = True
        elif has_date and is_short and not is_bullet and not is_company:
            is_new_entry = True
        elif is_all_caps and not is_bullet:
            is_new_entry = True
        elif is_role and is_company and not is_bullet:
            is_new_entry = True
        elif is_role and is_short and not is_bullet and not has_date:
            if current_entry and len(current_entry) > 1:
                is_new_entry = True

        if is_new_entry and current_entry:
            if len(current_entry) == 1 and _is_company_line(current_entry[0]) and not _has_date(current_entry[0]):
                current_entry.append(line)
            else:
                entries.append("\n".join(current_entry))
                current_entry = [line]
        elif is_new_entry:
            current_entry = [line]
        elif current_entry:
            current_entry.append(line)
        else:
            current_entry = [line]

    if current_entry:
        entries.append("\n".join(current_entry))

    # Merge orphaned entries
    merged_entries = []
    for i, entry in enumerate(entries):
        entry_lines = entry.split("\n")
        if len(entry_lines) <= 2 and not _has_date(entry) and not _is_role_line(entry):
            if merged_entries:
                merged_entries[-1] = merged_entries[-1] + "\n" + entry
                continue
        merged_entries.append(entry)

    # Final filter
    valid_entries = []
    for entry in merged_entries:
        entry_clean = _clean_line(entry)
        if len(entry_clean) < 15:
            continue
        if any(kw == entry_clean.lower() for kw in section_keywords):
            continue
        non_bullet = [l for l in entry.split("\n") if not _is_bullet_point(l) and len(l.strip()) > 3]
        if not non_bullet:
            continue
        valid_entries.append(entry)

    if valid_entries:
        return valid_entries

    fallback = [_clean_line(l) for l in raw_exp_lines if len(_clean_line(l)) > 10]
    if fallback:
        return fallback

    return ["Experience not found"]

CERTIFICATIONS_LIST = [
    "AWS Certified Solutions Architect", "AWS Certified Developer",
    "AWS Certified SysOps Administrator", "AWS Certified", "Google Cloud Professional",
    "Google Cloud", "Microsoft Azure", "Azure Administrator", "Azure Fundamentals",
    "PMP", "Certified Scrum Master", "Scrum Master", "Scrum", "CPA", "CFA",
    "CISSP", "CompTIA Security+", "CompTIA Network+", "CompTIA A+",
    "Oracle Certified Professional", "Oracle Certified", "Oracle",
    "Salesforce Certified Administrator", "Salesforce Certified", "Salesforce",
    "HubSpot Inbound", "HubSpot", "TensorFlow Developer Certificate",
    "TensorFlow Developer", "CKA", "CKAD", "CCNA", "CCNP", "ITIL",
    "Six Sigma Green Belt", "Six Sigma", "PHR", "SHRM-CP",
]

def extract_certifications(text):
    found_certifications = []
    for cert in CERTIFICATIONS_LIST:
        pattern = r'\b' + re.escape(cert) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_certifications.append(cert)
    return found_certifications if found_certifications else ["No certifications found"]

def _whole_word_match(term, text):
    pattern = r'\b' + re.escape(term) + r'\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def match_candidate(
    candidate_skills,
    jd_text,
    candidate_experience="",
    candidate_certifications="",
    job_title="",
):
    jd_skills = extract_skills(jd_text)
    jd_skills = [s for s in jd_skills if s != "No skills found"]

    matched_skills = []
    missing_skills = []
    for skill in jd_skills:
        if _whole_word_match(skill, candidate_skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_skills = len(jd_skills)
    skills_score = round((len(matched_skills) / total_skills) * 100) if total_skills > 0 else 0

    job_title_words = [
        w for w in re.split(r"[\s,/-]+", job_title.strip())
        if len(w) >= 2
    ]
    experience_keywords = list(dict.fromkeys(jd_skills + job_title_words))
    experience_text = candidate_experience if candidate_experience else ""

    matched_experience = []
    for keyword in experience_keywords:
        if _whole_word_match(keyword, experience_text):
            matched_experience.append(keyword)

    total_exp = len(experience_keywords)
    experience_score = (
        round((len(matched_experience) / total_exp) * 100) if total_exp > 0 else 0
    )

    jd_certifications = extract_certifications(jd_text)
    jd_certifications = [c for c in jd_certifications if c != "No certifications found"]
    certs_text = candidate_certifications if candidate_certifications else ""

    matched_certifications = []
    for cert in jd_certifications:
        if _whole_word_match(cert, certs_text):
            matched_certifications.append(cert)

    total_certs = len(jd_certifications)
    certifications_score = (
        round((len(matched_certifications) / total_certs) * 100) if total_certs > 0 else 0
    )

    score = round(
        (skills_score * 0.60)
        + (experience_score * 0.25)
        + (certifications_score * 0.15)
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_experience": matched_experience,
        "matched_certifications": matched_certifications,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "certifications_score": certifications_score,
    }