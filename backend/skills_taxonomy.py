"""
Curated skills taxonomy for resume parsing and job matching.
Skills are grouped by category for clustering and display.
"""

SKILLS_TAXONOMY = {
    "programming_languages": {
        "label": "Programming Languages",
        "color": "#6C63FF",
        "skills": [
            "python", "javascript", "typescript", "java", "c++", "c#", "c",
            "go", "golang", "rust", "kotlin", "swift", "scala", "ruby",
            "php", "r", "matlab", "julia", "dart", "elixir", "erlang",
            "haskell", "perl", "lua", "bash", "shell", "powershell",
            "assembly", "cobol", "fortran", "vba", "groovy", "clojure",
            "f#", "ocaml", "prolog", "solidity", "verilog", "hdl"
        ]
    },
    "web_frontend": {
        "label": "Frontend Development",
        "color": "#FF6584",
        "skills": [
            "react", "reactjs", "react.js", "vue", "vuejs", "vue.js",
            "angular", "angularjs", "svelte", "next.js", "nextjs", "nuxt",
            "gatsby", "html", "html5", "css", "css3", "sass", "scss",
            "less", "tailwindcss", "tailwind", "bootstrap", "material-ui",
            "mui", "ant design", "chakra ui", "styled components",
            "javascript", "typescript", "webpack", "vite", "babel",
            "jquery", "redux", "zustand", "mobx", "graphql", "apollo",
            "three.js", "d3.js", "chart.js", "webgl", "websockets",
            "pwa", "web components", "storybook", "jest", "cypress",
            "playwright", "vitest", "testing library"
        ]
    },
    "web_backend": {
        "label": "Backend Development",
        "color": "#43E97B",
        "skills": [
            "fastapi", "django", "flask", "express", "expressjs", "node.js",
            "nodejs", "spring", "spring boot", "laravel", "rails",
            "ruby on rails", "asp.net", ".net", "nestjs", "gin",
            "fiber", "echo", "fastify", "hapi", "koa", "graphql",
            "rest", "restful", "api design", "microservices", "grpc",
            "websockets", "oauth", "jwt", "authentication", "authorization",
            "middleware", "orm", "sqlalchemy", "prisma", "sequelize",
            "mongoose", "hibernate", "jpa", "celery", "rq"
        ]
    },
    "databases": {
        "label": "Databases",
        "color": "#F7971E",
        "skills": [
            "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle",
            "sql server", "mssql", "mariadb", "mongodb", "cassandra",
            "redis", "elasticsearch", "dynamodb", "firestore", "firebase",
            "neo4j", "couchdb", "influxdb", "timescaledb", "clickhouse",
            "snowflake", "bigquery", "redshift", "hive", "hbase",
            "database design", "schema design", "query optimization",
            "indexing", "sharding", "replication", "acid", "nosql",
            "vector database", "pinecone", "weaviate", "qdrant"
        ]
    },
    "cloud_devops": {
        "label": "Cloud & DevOps",
        "color": "#4FACFE",
        "skills": [
            "aws", "amazon web services", "azure", "gcp", "google cloud",
            "docker", "kubernetes", "k8s", "terraform", "ansible",
            "jenkins", "github actions", "gitlab ci", "circleci",
            "travis ci", "argocd", "helm", "istio", "prometheus",
            "grafana", "elk stack", "datadog", "new relic", "sentry",
            "nginx", "apache", "load balancing", "cdn", "cloudflare",
            "ci/cd", "devops", "devsecops", "infrastructure as code",
            "serverless", "lambda", "cloud functions", "heroku",
            "vercel", "netlify", "digitalocean", "linux", "unix",
            "bash scripting", "monitoring", "logging", "observability"
        ]
    },
    "machine_learning": {
        "label": "Machine Learning & AI",
        "color": "#FA709A",
        "skills": [
            "machine learning", "deep learning", "neural networks",
            "natural language processing", "nlp", "computer vision",
            "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
            "pandas", "numpy", "scipy", "matplotlib", "seaborn",
            "xgboost", "lightgbm", "catboost", "random forest",
            "linear regression", "logistic regression", "svm",
            "k-means", "clustering", "classification", "regression",
            "reinforcement learning", "generative ai", "llm",
            "large language models", "transformers", "hugging face",
            "bert", "gpt", "stable diffusion", "langchain", "llamaindex",
            "rag", "retrieval augmented generation", "vector embeddings",
            "openai api", "gemini", "claude", "mlops", "mlflow",
            "feature engineering", "model deployment", "model serving",
            "a/b testing", "data science", "statistics", "hypothesis testing",
            "time series", "anomaly detection", "recommendation systems"
        ]
    },
    "data_engineering": {
        "label": "Data Engineering",
        "color": "#30CFD0",
        "skills": [
            "apache spark", "spark", "hadoop", "kafka", "airflow",
            "dbt", "etl", "elt", "data pipeline", "data warehouse",
            "data lake", "data lakehouse", "databricks", "flink",
            "beam", "nifi", "talend", "informatica", "ssis",
            "data modeling", "dimensional modeling", "star schema",
            "data quality", "data governance", "data catalog",
            "metabase", "tableau", "power bi", "looker", "superset",
            "dask", "ray", "polars"
        ]
    },
    "mobile": {
        "label": "Mobile Development",
        "color": "#a18cd1",
        "skills": [
            "android", "ios", "react native", "flutter", "swift",
            "kotlin", "objective-c", "xamarin", "ionic", "capacitor",
            "expo", "mobile ui", "firebase", "push notifications",
            "app store", "google play", "xcode", "android studio"
        ]
    },
    "cybersecurity": {
        "label": "Cybersecurity",
        "color": "#f093fb",
        "skills": [
            "cybersecurity", "information security", "penetration testing",
            "ethical hacking", "vulnerability assessment", "soc",
            "siem", "firewall", "ids/ips", "encryption", "pki",
            "owasp", "ssl/tls", "zero trust", "identity management",
            "iam", "oauth", "saml", "mfa", "ctf", "reverse engineering",
            "malware analysis", "forensics", "compliance", "gdpr",
            "hipaa", "iso 27001", "nist", "risk assessment", "burp suite",
            "metasploit", "wireshark", "nmap", "kali linux"
        ]
    },
    "tools_productivity": {
        "label": "Tools & Productivity",
        "color": "#ffecd2",
        "skills": [
            "git", "github", "gitlab", "bitbucket", "jira", "confluence",
            "trello", "notion", "slack", "figma", "sketch", "adobe xd",
            "photoshop", "illustrator", "postman", "insomnia", "swagger",
            "vs code", "intellij", "pycharm", "vim", "neovim",
            "linux", "macos", "windows", "agile", "scrum", "kanban",
            "waterfall", "tdd", "bdd", "code review", "pair programming"
        ]
    },
    "soft_skills": {
        "label": "Soft Skills",
        "color": "#84fab0",
        "skills": [
            "leadership", "communication", "teamwork", "problem solving",
            "critical thinking", "creativity", "adaptability", "time management",
            "project management", "stakeholder management", "presentation",
            "negotiation", "mentoring", "coaching", "analytical thinking",
            "attention to detail", "self-motivated", "fast learner",
            "collaboration", "customer focus", "decision making"
        ]
    },
    "domain_expertise": {
        "label": "Domain Expertise",
        "color": "#fda085",
        "skills": [
            "fintech", "healthtech", "edtech", "e-commerce", "logistics",
            "supply chain", "banking", "insurance", "real estate",
            "healthcare", "medical", "legal", "education", "gaming",
            "media", "entertainment", "saas", "b2b", "b2c",
            "blockchain", "web3", "nft", "defi", "cryptocurrency",
            "iot", "embedded systems", "robotics", "autonomous vehicles",
            "ar", "vr", "metaverse", "quantum computing"
        ]
    }
}

# Flat lookup for fast matching
SKILL_TO_CATEGORY = {}
for cat_key, cat_data in SKILLS_TAXONOMY.items():
    for skill in cat_data["skills"]:
        SKILL_TO_CATEGORY[skill.lower()] = cat_key

# All skills as a flat set
ALL_SKILLS = set(SKILL_TO_CATEGORY.keys())
