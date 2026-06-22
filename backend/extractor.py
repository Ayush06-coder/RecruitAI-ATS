import re
import spacy
nlp = spacy.load("en_core_web_sm")

# ========== SYNONYMS ==========
SYNONYMS = {
    "ML": "Machine Learning", "DL": "Deep Learning", "AI": "Artificial Intelligence",
    "NLP": "Natural Language Processing", "CV": "Computer Vision", "LLM": "Large Language Model",
    "RAG": "Retrieval-Augmented Generation", "RL": "Reinforcement Learning",
    "JS": "JavaScript", "TS": "TypeScript", "Py": "Python",
    "K8s": "Kubernetes", "CI/CD": "Continuous Integration/Continuous Deployment",
    "IaC": "Infrastructure as Code", "SRE": "Site Reliability Engineering",
    "MLOps": "Machine Learning Operations", "DevOps": "Development Operations",
    "DataOps": "Data Operations", "GitOps": "Git Operations",
    "VPC": "Virtual Private Cloud", "IAM": "Identity and Access Management",
    "SSO": "Single Sign-On", "MFA": "Multi-Factor Authentication",
    "OAuth": "Open Authorization", "JWT": "JSON Web Token",
    "SSL": "Secure Sockets Layer", "TLS": "Transport Layer Security",
    "API": "Application Programming Interface", "SDK": "Software Development Kit",
    "CLI": "Command Line Interface", "GUI": "Graphical User Interface",
    "UI": "User Interface", "UX": "User Experience",
    "CDN": "Content Delivery Network", "DNS": "Domain Name System",
    "VPN": "Virtual Private Network", "WAF": "Web Application Firewall",
    "DDoS": "Distributed Denial of Service", "IDS": "Intrusion Detection System",
    "IPS": "Intrusion Prevention System", "SIEM": "Security Information and Event Management",
    "EDR": "Endpoint Detection and Response", "XDR": "Extended Detection and Response",
    "DLP": "Data Loss Prevention", "CASB": "Cloud Access Security Broker",
    "SASE": "Secure Access Service Edge", "ZTNA": "Zero Trust Network Access",
    "SD-WAN": "Software-Defined Wide Area Network", "SDN": "Software-Defined Networking",
    "GPU": "Graphics Processing Unit", "CPU": "Central Processing Unit",
    "TPU": "Tensor Processing Unit", "FPGA": "Field-Programmable Gate Array",
    "REST": "Representational State Transfer", "SOAP": "Simple Object Access Protocol",
    "JSON": "JavaScript Object Notation", "XML": "eXtensible Markup Language",
    "YAML": "YAML Ain't Markup Language", "CSV": "Comma-Separated Values",
    "HTML": "HyperText Markup Language", "CSS": "Cascading Style Sheets",
    "DOM": "Document Object Model", "OCR": "Optical Character Recognition",
    "WebRTC": "Web Real-Time Communication", "HLS": "HTTP Live Streaming",
    "AR": "Augmented Reality", "VR": "Virtual Reality", "MR": "Mixed Reality",
    "XR": "Extended Reality", "IoT": "Internet of Things",
    "IIoT": "Industrial Internet of Things", "NFC": "Near Field Communication",
    "RFID": "Radio-Frequency Identification", "GPS": "Global Positioning System",
    "GIS": "Geographic Information System", "LTE": "Long-Term Evolution",
    "NAS": "Network Attached Storage", "SAN": "Storage Area Network",
    "SSD": "Solid State Drive", "HDD": "Hard Disk Drive",
    "TDD": "Test-Driven Development", "BDD": "Behavior-Driven Development",
    "DDD": "Domain-Driven Design", "OOP": "Object-Oriented Programming",
    "DRY": "Don't Repeat Yourself", "KISS": "Keep It Simple Stupid",
    "YAGNI": "You Aren't Gonna Need It", "SOLID": "SOLID Principles",
    "ACID": "Atomicity Consistency Isolation Durability",
    "BASE": "Basically Available Soft state Eventual consistency",
    "OKR": "Objectives and Key Results", "RPA": "Robotic Process Automation",
    "ERP": "Enterprise Resource Planning", "CRM": "Customer Relationship Management",
    "CMS": "Content Management System", "LMS": "Learning Management System",
    "SCM": "Supply Chain Management", "PLM": "Product Lifecycle Management",
    "MDM": "Master Data Management", "CDP": "Customer Data Platform",
    "DMP": "Data Management Platform", "BPM": "Business Process Management",
    "RACI": "Responsible Accountable Consulted Informed",
    "SWOT": "Strengths Weaknesses Opportunities Threats",
    "SMART": "Specific Measurable Achievable Relevant Time-bound",
}

# Build reverse mapping: full form -> abbreviation
REV_SYN = {v.lower(): k for k, v in SYNONYMS.items()}

def _expand(skill):
    """Get all forms of a skill (abbreviation + full form)."""
    s = skill.strip()
    sl = s.lower()
    forms = {sl}
    if s in SYNONYMS:
        forms.add(SYNONYMS[s].lower())
    if sl in REV_SYN:
        forms.add(REV_SYN[sl].lower())
    return forms

def _has_match(skill, text):
    """Check if skill or any synonym matches in text."""
    text_lower = text.lower()
    for form in _expand(skill):
        if re.search(r'\b' + re.escape(form) + r'\b', text_lower):
            return True
    return False

# ========== BASIC EXTRACTORS ==========
def extract_email(text):
    m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return m.group() if m else "Email not found"

def extract_phone(text):
    m = re.search(r"\+?\d[\d\s\-]{8,15}", text)
    return m.group() if m else "Phone number not found"

def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    job_words = {"developer","engineer","analyst","manager","consultant","designer",
                 "architect","lead","intern","trainee","assistant","scientist",
                 "officer","head","director","specialist","coordinator","administrator",
                 "supervisor","technician","operator","executive","associate",
                 "freelance","contractor","web","data","product","junior","senior",
                 "frontend","backend","fullstack","full-stack","full","stack","software"}
    headings = {"resume","cv","curriculum","vitae","profile","summary","education",
                "experience","skills","objective","contact","references","professional"}

    # Two consecutive uppercase single words
    for i in range(min(10, len(lines)-1)):
        w1, w2 = lines[i], lines[i+1]
        if (w1.isupper() and w2.isupper() and len(w1.split())==1 and len(w2.split())==1
            and w1.title() not in headings and w2.title() not in headings
            and w1.lower() not in job_words and w2.lower() not in job_words):
            return f"{w1} {w2}".title()

    # spaCy NER
    doc = nlp(" ".join(l.title() if l.isupper() else l for l in lines[:10]))
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            words = ent.text.split()
            clean = []
            for w in words:
                wc = w.strip().lower().rstrip(",.:;-|")
                if wc in job_words or any(j in wc for j in ["developer","engineer","analyst","manager","designer","consultant","architect","intern","trainee","assistant"]):
                    break
                clean.append(w)
            if len(clean) >= 2 and clean[-1].lower().rstrip(",.:;-|") not in job_words:
                return " ".join(clean)
    return "Name not found"

# ========== SKILLS ==========
SKILLS_LIST = [
    "Python","Java","C","C++","C#","JavaScript","TypeScript","R","Swift","Kotlin",
    "Go","Rust","PHP","Ruby","Scala","HTML","CSS","SQL","NoSQL","Bash","Shell",
    "Perl","Lua","Groovy","Objective-C","MATLAB","Julia","Dart","VBA",
    "React","Angular","Vue","Next.js","Nuxt.js","Svelte","Node.js","Express.js",
    "Django","Flask","FastAPI","Spring Boot","Ruby on Rails","Laravel","ASP.NET",
    "jQuery","Bootstrap","Tailwind CSS","Material UI","HTMX","Alpine.js","Preact",
    "Gatsby","Three.js","D3.js","Chart.js","WebGL",
    "MySQL","PostgreSQL","MongoDB","SQLite","Redis","Cassandra","CouchDB","Neo4j",
    "DynamoDB","Cosmos DB","InfluxDB","TimescaleDB","ClickHouse","Snowflake",
    "BigQuery","Redshift","Athena","Presto","Trino","Druid","Oracle","SQL Server",
    "MariaDB","CockroachDB","FaunaDB","Supabase","Firebase","Prisma","TypeORM",
    "Sequelize","Hibernate","Entity Framework","Dapper","Mongoose",
    "AWS","Azure","GCP","Google Cloud","IBM Cloud","DigitalOcean","Linode",
    "Heroku","Vercel","Netlify","Cloudflare","Docker","Kubernetes","Helm",
    "Terraform","Ansible","Chef","Puppet","SaltStack","Pulumi","Vagrant","Nomad",
    "Consul","Vault","Jenkins","GitLab CI","GitHub Actions","CircleCI","Travis CI",
    "Drone","ArgoCD","Spinnaker","Flux","Tekton","AWS CodePipeline","Azure DevOps",
    "Google Cloud Build","Nginx","Apache","Tomcat","HAProxy","Traefik","Envoy",
    "Istio","Linkerd","Prometheus","Grafana","Datadog","New Relic","Dynatrace",
    "Splunk","ELK Stack","Fluentd","Logstash","PagerDuty","Opsgenie","ServiceNow",
    "Machine Learning","Deep Learning","NLP","Natural Language Processing",
    "Computer Vision","TensorFlow","PyTorch","Keras","Scikit-learn","scikit-learn",
    "XGBoost","LightGBM","CatBoost","Pandas","NumPy","SciPy","Matplotlib","Seaborn",
    "Plotly","Bokeh","Altair","Dask","Modin","Vaex","Polars","Ray","Spark",
    "Apache Spark","PySpark","Hadoop","Hive","Impala","Pig","Kafka","Airflow",
    "Prefect","Dagster","Luigi","NiFi","MLflow","Kubeflow","DVC","Weights & Biases",
    "Neptune","Optuna","Hyperopt","Featuretools","TSFresh","Prophet","ARIMA",
    "SARIMA","LSTM","GRU","Transformer","BERT","RoBERTa","DeBERTa","XLNet",
    "ALBERT","ELECTRA","DistilBERT","GPT","GPT-2","GPT-3","GPT-4","GPT-3.5",
    "LLaMA","Mistral","Claude","Gemini","PaLM","T5","BART","Stable Diffusion",
    "Midjourney","DALL-E","Whisper","TTS","Coqui","OpenCV","Pillow","NLTK",
    "spaCy","Gensim","TextBlob","Hugging Face","OpenAI","Anthropic","LangChain",
    "LlamaIndex","CrewAI","AutoGen","Pinecone","Weaviate","Chroma","Milvus",
    "Qdrant","FAISS","ONNX","TensorRT","OpenVINO","CUDA","cuDNN","ROCm",
    "OpenCL","Vulkan","Metal","RAPIDS","CuDF","CuML","CuGraph","Numba",
    "Statsmodels","Pingouin","A/B Testing","Hypothesis Testing","Statistical Modeling",
    "Regression","Classification","Clustering","Dimensionality Reduction",
    "Ensemble Methods","Random Forest","Gradient Boosting","SVM","Naive Bayes",
    "KNN","K-Means","DBSCAN","PCA","t-SNE","UMAP","Cross-validation",
    "Grid Search","Random Search","Feature Engineering","Feature Selection",
    "Data Preprocessing","Data Cleaning","Data Wrangling","Data Mining",
    "Data Visualization","EDA","Exploratory Data Analysis","Time Series Analysis",
    "Survival Analysis","Anomaly Detection","Fraud Detection",
    "Recommendation Systems","Collaborative Filtering","Content-Based Filtering",
    "Reinforcement Learning","Q-Learning","Deep Q-Network","Policy Gradient",
    "Actor-Critic","PPO","A3C","SAC","TD3","Generative AI","GANs","VAE",
    "Diffusion Models","Flow Models","Multi-modal AI","Vision-Language Models",
    "Large Language Models","Prompt Engineering","Retrieval-Augmented Generation",
    "Fine-tuning","LoRA","QLoRA","PEFT","Adapter Tuning","Quantization",
    "Pruning","Knowledge Distillation","Model Compression","MLOps","Model Monitoring",
    "Data Drift","Concept Drift","Feature Store","Feast","Tecton",
    "Delta Lake","Apache Iceberg","Hudi","Lakehouse","Data Warehouse","Data Lake",
    "Data Mesh","Data Fabric","ETL","ELT","Data Pipeline","Stream Processing",
    "Batch Processing","Apache Beam","Dataflow","Glue","AWS Glue",
    "Azure Data Factory","dbt","Data Build Tool","Great Expectations","Soda Core",
    "Power BI","Tableau","Looker","Metabase","Superset","Redash","QuickSight",
    "Data Studio","ThoughtSpot","Sisense","Domo","MicroStrategy","Qlik Sense",
    "Excel","Google Sheets","Pandas","Plotly","Dash",
    "React Native","Flutter","Swift","Kotlin","Xamarin","Ionic","Cordova",
    "NativeScript","Capacitor","Expo","Android","iOS","Android Studio","Xcode",
    "CocoaPods","Gradle","Maven","Fastlane","OneSignal","ARKit","ARCore",
    "Unity","Unreal Engine","Godot","Blender","Cinema 4D","Maya","3ds Max",
    "ZBrush","Houdini","Shader Programming","HLSL","GLSL","Physics Engine",
    "Box2D","Bullet Physics","PhysX","Networking","Multiplayer","Photon",
    "Game AI","Pathfinding","Behavior Trees","State Machines",
    "Penetration Testing","Ethical Hacking","Red Team","Blue Team","Purple Team",
    "Threat Modeling","STRIDE","PASTA","Incident Response","Digital Forensics",
    "Malware Analysis","Reverse Engineering","Binary Exploitation",
    "Web Exploitation","Cryptography","PKI","IPSec","SOC 2","ISO 27001",
    "GDPR","CCPA","HIPAA","PCI DSS","NIST","CIS Controls","OWASP","SANS",
    "Zero Trust","Defense in Depth","Least Privilege","RBAC","ABAC","PBAC",
    "HashiCorp Vault","AWS KMS","Azure Key Vault","Secrets Management",
    "Identity Management","Blockchain","Ethereum","Solidity","Hyperledger",
    "Polygon","Arbitrum","Optimism","zkSync","StarkNet","Cosmos","Polkadot",
    "Avalanche","Solana","Cardano","IPFS","Filecoin","Chainlink","The Graph",
    "Uniswap","Aave","OpenZeppelin","Hardhat","Truffle","Foundry","Ethers.js",
    "Web3.js","Web3.py","ERC-20","ERC-721","ERC-1155","DeFi","NFT","DAO",
    "Zero-Knowledge Proofs","zk-SNARKs","zk-STARKs","Rollups",
    "Unit Testing","Integration Testing","E2E Testing","Regression Testing",
    "Load Testing","Stress Testing","Performance Testing","Security Testing",
    "TDD","Test-Driven Development","BDD","Behavior-Driven Development",
    "Jest","Mocha","Chai","Cypress","Playwright","Selenium","Appium","Detox",
    "JUnit","TestNG","PyTest","Mocking","Stubbing","Code Coverage",
    "SonarQube","JaCoCo","Coverage.py","Mutation Testing","Fuzzing",
    "JMeter","Gatling","Locust","k6","Postman","Insomnia","Swagger","OpenAPI",
    "WireMock","Git","GitHub","GitLab","Bitbucket","Azure DevOps","SVN",
    "Mercurial","Git Flow","GitHub Flow","Code Review","Pull Requests",
    "Conventional Commits","Semantic Versioning","Git Hooks","Pre-commit",
    "Linux","Ubuntu","CentOS","RHEL","Debian","Fedora","Arch Linux",
    "Alpine Linux","Windows","macOS","Unix","Bash","Zsh","PowerShell",
    "System Administration","Systemd","Cron","Kernel","Device Drivers",
    "Embedded Systems","RTOS","Virtualization","VMware","VirtualBox","KVM",
    "Xen","Hyper-V","Proxmox","QEMU","Libvirt",
    "TCP/IP","HTTP","HTTPS","HTTP/2","HTTP/3","QUIC","WebSocket","gRPC",
    "REST API","GraphQL","SOAP","Message Queue","RabbitMQ","Apache Kafka",
    "ActiveMQ","ZeroMQ","Redis","Memcached","Celery","RQ","WebRTC","RTMP",
    "SDN","NFV","5G","IoT","Edge Computing","Serverless","FaaS","PaaS",
    "IaaS","SaaS","Multi-tenancy","Hybrid Cloud","Multi-cloud",
    "Agile","Scrum","Kanban","Lean","XP","Extreme Programming","SAFe",
    "Waterfall","DevOps","DevSecOps","GitOps","DataOps","AIOps",
    "SRE","Site Reliability Engineering","Chaos Engineering","Observability",
    "Monitoring","Tracing","Logging","CI/CD","Continuous Integration",
    "Continuous Deployment","Continuous Delivery","Infrastructure as Code",
    "Configuration Management","Immutable Infrastructure","Blue-Green Deployment",
    "Canary Deployment","Feature Flags","A/B Testing","Multivariate Testing",
    "Design Thinking","OKRs","KPIs","Product Management","Project Management",
    "Risk Management","Disaster Recovery","Business Continuity",
    "High Availability","Fault Tolerance","Load Balancing","Auto-scaling",
    "Data Structures","Algorithms","OOP","Object-Oriented Programming",
    "Functional Programming","Procedural Programming","Design Patterns",
    "SOLID","DRY","KISS","YAGNI","Clean Code","Clean Architecture",
    "Hexagonal Architecture","Onion Architecture","Layered Architecture",
    "Microservices","Event Sourcing","CQRS","Saga Pattern","Outbox Pattern",
    "Circuit Breaker","Retry Pattern","Bulkhead","Timeout","Idempotency",
    "Optimistic Locking","Pessimistic Locking","MVCC","ACID","BASE",
    "CAP Theorem","PACELC","Sharding","Partitioning","Replication",
    "Federation","Denormalization","Indexing","Query Optimization",
    "Connection Pooling","Caching Strategies","Cache Invalidation",
    "Rate Limiting","Throttling","Backpressure","Load Shedding",
    "Accessibility","WCAG","ARIA","Internationalization","i18n","Localization",
    "l10n","SEO","Search Engine Optimization","Web Analytics","Google Analytics",
    "Mixpanel","Amplitude","Growth Hacking","Conversion Rate Optimization",
    "User Onboarding","Retention","Churn Analysis","Customer Journey",
    "Funnel Analysis","Cohort Analysis","Predictive Analytics",
    "Prescriptive Analytics","Descriptive Analytics","Real-time Analytics",
    "Streaming Analytics","Batch Analytics","Data Governance","Data Quality",
    "Data Lineage","Data Catalog","Master Data Management","Customer 360",
    "Data Privacy","Data Security","Data Ethics","Responsible AI",
    "Fairness","Bias Detection","Explainability","Interpretability",
    "Model Governance","AI Governance","AI Risk Management",
    "Communication","Leadership","Teamwork","Collaboration","Problem Solving",
    "Critical Thinking","Analytical Thinking","Creativity","Innovation",
    "Adaptability","Time Management","Organization","Prioritization",
    "Attention to Detail","Self-Motivated","Proactive","Mentoring","Coaching",
    "Cross-functional Collaboration","Stakeholder Communication",
    "Presentation Skills","Technical Writing","Documentation",
    "Conflict Resolution","Negotiation","Emotional Intelligence",
    "Remote Work","Distributed Teams",
]

def extract_skills(text):
    found = set()
    # Method 1: predefined list
    for skill in SKILLS_LIST:
        pat = re.escape(skill) if (" " in skill or "/" in skill or "-" in skill) else r'\b' + re.escape(skill) + r'\b'
        if re.search(pat, text, re.IGNORECASE):
            found.add(skill)
    # Method 2: dynamic from skills section
    lines = text.split("\n")
    in_skills = False
    for line in lines:
        ls = line.strip().lower()
        if any(k in ls for k in ["technical skills","core skills","key skills","skills","proficiencies"]):
            if len(ls.split()) <= 4:
                in_skills = True
                continue
        if in_skills and any(k in ls for k in ["experience","education","projects","certifications","summary"]):
            if len(ls.split()) <= 4:
                in_skills = False
                continue
        if in_skills:
            clean = re.sub(r'^[\w\s/&]+:\s*', '', line)
            for item in re.split(r'[,|;|/]', clean):
                item = item.strip()
                if 1 <= len(item.split()) <= 4 and len(item) >= 2 and not any(c in item for c in [".","!","?"]):
                    found.add(item)
    # Method 3: table format
    for line in lines:
        m = re.match(r'^[\w\s/&]+:\s*(.+)$', line.strip())
        if m:
            for item in re.split(r'[,|;|/]', m.group(1)):
                item = item.strip()
                if 1 <= len(item.split()) <= 4 and len(item) >= 2 and not any(c in item for c in [".","!","?"]):
                    found.add(item)
    return sorted(list(found)) if found else ["No skills found"]

# ========== EDUCATION ==========
EDU_KEYS = ["b.tech","m.tech","btech","mtech","b.e","m.e","b.sc","m.sc","bsc","msc",
            "bca","mca","bba","mba","bachelor","master","phd","doctorate","diploma",
            "b.com","m.com","b.a","m.a","high school","secondary","senior secondary"]
UNI_KEYS = ["university","college","institute","iit","nit","bits","amity","vit",
            "manipal","school of","academy","polytechnic","technical","engineering"]

def extract_education(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    edu_lines = []
    in_edu = False
    for line in lines:
        ll = line.lower()
        if any(k in ll for k in ["education","qualification","academic"]):
            in_edu = True
            continue
        if in_edu and any(k in ll for k in ["experience","skills","projects","certifications","summary","objective"]):
            break
        if in_edu:
            edu_lines.append(line)
    found = [l for l in edu_lines if any(k in l.lower() for k in EDU_KEYS + UNI_KEYS)]
    return found if found else ["Education not found"]

# ========== EXPERIENCE ==========
ROLE_WORDS = {"engineer","developer","analyst","manager","consultant","designer",
              "architect","lead","intern","trainee","assistant","scientist",
              "officer","head","director","specialist","coordinator","administrator",
              "supervisor","technician","operator","executive","associate","freelance","contractor"}
COMPANY_WORDS = {"technologies","solutions","systems","services","consulting",
                 "software","tech","labs","pvt","ltd","inc","limited","corp",
                 "group","studio","company","corporation","industries","ventures",
                 "partners","global","digital","innovations","enterprises","networks","media","cloud"}

def extract_experience(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    section_kws = ["work experience","professional experience","experience","employment",
                   "work history","career history","professional background","employment history","job history"]
    stop_kws = ["education","academic","qualification","degree","skills","technical skills",
                "core skills","key skills","projects","certifications","achievements",
                "publications","languages","interests","hobbies","references","summary","objective","profile"]

    def is_header(line, kws):
        lc = line.lower().replace("**","").replace("*","").strip()
        for kw in kws:
            if kw in lc and len(lc.split()) <= 6:
                if not any(c in lc for c in [".",":"] if c not in kw.split()):
                    return True
                if line.isupper() or line.istitle() or "**" in line or len(lc.split()) <= 3:
                    return True
        return False

    def has_date(line):
        dp = [r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',
              r'\b\d{4}\s*[-–—]\s*(present|current|now|today|\d{4})\b',
              r'\b\d{1,2}/\d{4}\s*[-–—]\s*(present|current|now|\d{1,2}/\d{4})\b',
              r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
              r'\b\d{4}\s*[-–—]\s*\d{4}\b',r'\b\d{4}\s+to\s+(present|current|\d{4})\b',
              r'\b\d{4}\s*[-–—]\s*\b',r'\b(present|current)\b']
        for p in dp:
            if re.search(p, line.lower(), re.IGNORECASE):
                return True
        return False

    def is_bullet(line):
        bs = ["•","-","*","►","→","⇒",">","◦","▪","▫","●","○","‣","⁃","◆"]
        return any(line.strip().startswith(b) for b in bs) or re.match(r'^[\s]*[•\-*►→⇒>◦▪▫●○‣⁃◆]\s*', line.strip())

    def is_role(line):
        return any(w in line.lower().replace("**","").replace("*","") for w in ROLE_WORDS)

    def is_company(line):
        return any(w in line.lower().replace("**","").replace("*","") for w in COMPANY_WORDS)

    def is_cont(line):
        lc = line.strip()
        return bool(lc) and (lc[0].islower() or (len(lc) < 40 and not lc.endswith(('.','!','?',':',';'))))

    def clean(line):
        return line.replace("**","").replace("*","").strip()

    # Find section
    start = -1
    for i, l in enumerate(lines):
        if is_header(l, section_kws):
            start = i
            break
    if start == -1:
        for i, l in enumerate(lines):
            lc = l.lower().replace("**","").replace("*","").strip()
            if any(k in lc for k in section_kws) and len(lc.split()) <= 4:
                start = i
                break
    if start == -1:
        return [l for l in lines if has_date(l) and (is_role(l) or is_company(l) or len(l.split()) <= 10)] or ["Experience not found"]

    # Find end
    end = len(lines)
    for i in range(start+1, len(lines)):
        if is_header(lines[i], stop_kws):
            end = i
            break

    raw = lines[start+1:end]
    if not raw:
        return ["Experience not found"]

    # Merge continuation lines
    merged = []
    for line in raw:
        if merged and is_cont(line) and not is_bullet(line):
            prev = merged[-1]
            if not prev.endswith(('.','!','?',':',';',' )',']','}')):
                merged[-1] = prev + " " + line
                continue
        merged.append(line)

    # Group entries
    entries = []
    curr = []
    for line in merged:
        cl = clean(line)
        if not cl:
            if curr:
                entries.append("\n".join(curr))
                curr = []
            continue
        hd = has_date(line)
        ir = is_role(line)
        ic = is_company(line)
        ib = is_bullet(line)
        wc = len(cl.split())
        ac = line.isupper() and wc <= 6
        ne = False
        if hd and ir and not ib:
            ne = True
        elif hd and wc <= 8 and not ib and not ic:
            ne = True
        elif ac and not ib:
            ne = True
        elif ir and ic and not ib:
            ne = True
        elif ir and wc <= 5 and not ib and not hd:
            if curr and len(curr) > 1:
                ne = True
        if ne and curr:
            if len(curr) == 1 and is_company(curr[0]) and not has_date(curr[0]):
                curr.append(line)
            else:
                entries.append("\n".join(curr))
                curr = [line]
        elif ne:
            curr = [line]
        elif curr:
            curr.append(line)
        else:
            curr = [line]
    if curr:
        entries.append("\n".join(curr))

    # Merge orphans
    merged_e = []
    for e in entries:
        el = e.split("\n")
        if len(el) <= 2 and not has_date(e) and not is_role(e):
            if merged_e:
                merged_e[-1] = merged_e[-1] + "\n" + e
                continue
        merged_e.append(e)

    valid = []
    for e in merged_e:
        ce = clean(e)
        if len(ce) < 15:
            continue
        if any(kw == ce.lower() for kw in section_kws):
            continue
        nb = [l for l in e.split("\n") if not is_bullet(l) and len(l.strip()) > 3]
        if not nb:
            continue
        valid.append(e)

    if valid:
        return valid
    fb = [clean(l) for l in raw if len(clean(l)) > 10]
    return fb if fb else ["Experience not found"]

# ========== CERTIFICATIONS ==========
CERTS_LIST = [
    "AWS Certified Solutions Architect","AWS Certified Developer",
    "AWS Certified SysOps Administrator","AWS Certified","Google Cloud Professional",
    "Google Cloud","Microsoft Azure","Azure Administrator","Azure Fundamentals",
    "PMP","Certified Scrum Master","Scrum Master","Scrum","CPA","CFA",
    "CISSP","CompTIA Security+","CompTIA Network+","CompTIA A+",
    "Oracle Certified Professional","Oracle Certified","Oracle",
    "Salesforce Certified Administrator","Salesforce Certified","Salesforce",
    "HubSpot Inbound","HubSpot","TensorFlow Developer Certificate",
    "TensorFlow Developer","CKA","CKAD","CCNA","CCNP","ITIL",
    "Six Sigma Green Belt","Six Sigma","PHR","SHRM-CP",
    "AWS Certified DevOps Engineer","AWS Certified Data Analytics",
    "AWS Certified Machine Learning","AWS Certified Security",
    "Google Cloud Professional Data Engineer",
    "Google Cloud Professional Cloud Architect",
    "Google Cloud Professional Cloud DevOps Engineer",
    "Azure Solutions Architect","Azure DevOps Engineer",
    "Azure Data Engineer","Azure AI Engineer",
    "HashiCorp Certified: Terraform Associate",
    "HashiCorp Certified: Vault Associate",
    "HashiCorp Certified: Consul Associate",
    "Certified Kubernetes Administrator",
    "Certified Kubernetes Application Developer",
    "Linux Foundation Certified System Administrator",
    "Red Hat Certified Engineer","Red Hat Certified System Administrator",
    "VMware Certified Professional",
    "Cisco Certified Network Associate","Cisco Certified Network Professional",
    "Certified Information Systems Security Professional",
    "Certified Ethical Hacker","Offensive Security Certified Professional",
    "GIAC Security Essentials","GIAC Certified Incident Handler",
]

def extract_certifications(text):
    found = []
    for cert in CERTS_LIST:
        if re.search(r'\b' + re.escape(cert) + r'\b', text, re.IGNORECASE):
            found.append(cert)
    return found if found else ["No certifications found"]

# ========== MATCHING ==========
def match_candidate(candidate_skills, jd_text, candidate_experience="", candidate_certifications="", job_title=""):
    jd_skills = extract_skills(jd_text)
    jd_skills = [s for s in jd_skills if s != "No skills found"]

    matched_skills = []
    missing_skills = []
    for skill in jd_skills:
        if _has_match(skill, candidate_skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_skills = len(jd_skills)
    skills_score = round((len(matched_skills) / total_skills) * 100) if total_skills > 0 else 0

    job_title_words = [w for w in re.split(r"[\s,/-]+", job_title.strip()) if len(w) >= 2]
    exp_keywords = list(dict.fromkeys(jd_skills + job_title_words))
    exp_text = candidate_experience if candidate_experience else ""

    matched_exp = []
    for kw in exp_keywords:
        if _has_match(kw, exp_text):
            matched_exp.append(kw)

    total_exp = len(exp_keywords)
    experience_score = round((len(matched_exp) / total_exp) * 100) if total_exp > 0 else 0

    jd_certs = extract_certifications(jd_text)
    jd_certs = [c for c in jd_certs if c != "No certifications found"]
    certs_text = candidate_certifications if candidate_certifications else ""

    matched_certs = []
    for cert in jd_certs:
        if _has_match(cert, certs_text):
            matched_certs.append(cert)

    total_certs = len(jd_certs)
    certifications_score = round((len(matched_certs) / total_certs) * 100) if total_certs > 0 else 0

    score = round((skills_score * 0.60) + (experience_score * 0.25) + (certifications_score * 0.15))

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_experience": matched_exp,
        "matched_certifications": matched_certs,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "certifications_score": certifications_score,
    }