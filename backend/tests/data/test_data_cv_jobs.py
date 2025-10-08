from models import ParsedCV, Project, Experience, Suggestion, Education, JobApplication, JobRequirements
from storage import storage
# Alice - Frontend Developer
Alice_base_cv = ParsedCV(
    name="Alice Johnson",
    email="alice.johnson@email.com",
    location="New York, NY",
    phone="+1 555-0123",
    job_title="Full Stack Developer",
    bio="Experienced software developer with 5 years of experience in web development. Passionate about creating efficient and scalable applications.",
    skills=["JavaScript", "React", "Node.js", "Python", "PostgreSQL", "Docker"],
    languages=["English - Native", "Spanish - B2"],
    projects=[
        Project(
            title="E-commerce Platform",
            tools="React, Node.js, MongoDB",
            description=[
                "Built complete e-commerce solution",
                "Implemented payment processing",
                "Created admin dashboard"
            ],
            link="https://github.com/alice/ecommerce"
        ),
        Project(
            title="Task Management App",
            tools="Vue.js, Express, MySQL",
            description=[
                "Developed real-time collaboration features",
                "Integrated email notifications",
                "Optimized database queries"
            ],
            link="https://github.com/alice/taskapp"
        )
    ],
    experience=[
        Experience(
            title="Full Stack Developer",
            company="Tech Solutions Inc",
            date="2021 - Present",
            description=[
                "Developed web applications using React and Node.js",
                "Collaborated with design team on UI/UX improvements",
                "Implemented automated testing with Jest",
                "Reduced page load time by 40%"
            ]
        ),
        Experience(
            title="Junior Developer",
            company="StartupXYZ",
            date="2019 - 2021",
            description=[
                "Built RESTful APIs",
                "Worked with MongoDB and Express",
                "Participated in code reviews"
            ]
        )
    ],
    education=[
        Education(
            degree="Bachelor of Science",
            field="Computer Science",
            school_name="State University",
            date="2015 - 2019"
        )
    ]
)

Alice_job = JobApplication(
    job_id="550e8400-e29b-41d4-a716",
    user_id="Alice",
    job_requirements=JobRequirements(
        job_title="Senior React Developer",
        company="InnovateTech",
        key_skills=["React", "TypeScript", "GraphQL", "AWS"],
        important_keywords=["scalable", "performance", "modern web", "microservices"],
        responsibilities=[
            "Lead frontend development",
            "Mentor junior developers",
            "Architect scalable solutions"
        ],
        company_values=["innovation", "continuous learning", "collaboration"],
        tone="technical"
    ),
    suggestions=[
        Suggestion(
            type="update_field",
            section="job_title",
            current_value="Full Stack Developer",
            suggested_value="Senior React Developer",
            reason="Match job posting title for better ATS alignment",
            status="accepted"
        ),
        Suggestion(
            type="rewrite",
            section="bio",
            current_value="Experienced software developer with 5 years of experience in web development. Passionate about creating efficient and scalable applications.",
            suggested_value="Senior React developer with 5 years of experience building scalable web applications. Specialized in modern frontend architecture and performance optimization.",
            reason="Emphasize React expertise and scalability keywords from job posting",
            status="modified",
            final_value="Senior React developer with 5+ years of experience building high-performance, scalable web applications. Expert in modern frontend architecture with focus on React ecosystem."
        ),
        Suggestion(
            type="rewrite",
            section="experience",
            target_item_index=0,
            target_field="description",
            target_field_index=0,
            current_value="Developed web applications using React and Node.js",
            suggested_value="Architected and developed scalable web applications using React, focusing on performance optimization and modern best practices",
            reason="Add scalability and performance keywords",
            status="accepted"
        ),
        Suggestion(
            type="rewrite",
            section="experience",
            target_item_index=0,
            target_field="description",
            target_field_index=1,
            current_value="Collaborated with design team on UI/UX improvements",
            suggested_value="Led cross-functional collaboration with design team to deliver exceptional user experiences",
            reason="Show leadership alignment with Senior role",
            status="rejected"
        )
    ],
    status="modified",
    analysis_model="full"
)

# Bob - Backend Engineer
Bob_base_cv = ParsedCV(
    name="Bob Martinez",
    email="bob.martinez@protonmail.com",
    location="Austin, TX",
    phone="+1 555-9876",
    job_title="Backend Engineer",
    bio="Backend engineer with strong focus on API design and database optimization. Experience with microservices architecture.",
    skills=["Python", "Django", "PostgreSQL", "Redis", "Docker", "AWS"],
    languages=["English - Native", "Portuguese - C1"],
    projects=[
        Project(
            title="Payment Processing System",
            tools="Python, FastAPI, Stripe API",
            description=[
                "Designed secure payment processing pipeline",
                "Integrated multiple payment providers",
                "Handled 10k+ transactions daily"
            ],
            link="https://github.com/bob/payment-system"
        )
    ],
    experience=[
        Experience(
            title="Backend Engineer",
            company="FinTech Corp",
            date="2020 - Present",
            description=[
                "Built RESTful APIs using Django REST Framework",
                "Optimized database queries reducing response time by 60%",
                "Implemented caching with Redis",
                "Deployed applications on AWS"
            ]
        ),
        Experience(
            title="Software Developer",
            company="WebApp Solutions",
            date="2018 - 2020",
            description=[
                "Developed backend services",
                "Worked with PostgreSQL databases",
                "Created automated tests"
            ]
        )
    ],
    education=[
        Education(
            degree="Bachelor of Engineering",
            field="Software Engineering",
            school_name="Tech Institute",
            date="2014 - 2018"
        )
    ]
)

Bob_job = JobApplication(
    job_id="abc-def-123-456",
    user_id="Bob",
    job_requirements=JobRequirements(
        job_title="Senior Python Developer",
        company="DataFlow Systems",
        key_skills=["Python", "FastAPI", "Microservices", "Kubernetes", "PostgreSQL"],
        important_keywords=["high-performance", "distributed systems", "scalability", "cloud-native"],
        responsibilities=[
            "Design microservices architecture",
            "Optimize system performance",
            "Lead technical initiatives"
        ],
        company_values=["technical excellence", "innovation", "teamwork"],
        tone="technical"
    ),
    suggestions=[
        Suggestion(
            type="update_field",
            section="job_title",
            current_value="Backend Engineer",
            suggested_value="Senior Python Developer",
            reason="Exact match with job posting title",
            status="accepted"
        ),
        Suggestion(
            type="rewrite",
            section="bio",
            current_value="Backend engineer with strong focus on API design and database optimization. Experience with microservices architecture.",
            suggested_value="Senior Python developer specializing in high-performance microservices and distributed systems. Expert in building scalable cloud-native applications.",
            reason="Incorporate job keywords: high-performance, microservices, scalable, cloud-native",
            status="accepted"
        ),
        Suggestion(
            type="rewrite",
            section="experience",
            target_item_index=0,
            target_field="description",
            target_field_index=0,
            current_value="Built RESTful APIs using Django REST Framework",
            suggested_value="Designed and built high-performance RESTful microservices using Python and FastAPI",
            reason="Emphasize FastAPI and microservices from job requirements",
            status="modified",
            final_value="Architected and built high-performance RESTful microservices using Python, FastAPI, and distributed systems patterns"
        )
    ],
    status="ready",
    analysis_model="full"
)

# Carol - Data Scientist
Carol_base_cv = ParsedCV(
    name="Carol Chen",
    email="carol.chen@gmail.com",
    location="San Francisco, CA",
    phone="+1 555-4567",
    job_title="Data Scientist",
    bio="Data scientist with expertise in machine learning and statistical analysis. Experienced in building predictive models.",
    skills=["Python", "TensorFlow", "Pandas", "SQL", "Scikit-learn", "Jupyter"],
    languages=["English - Native", "Mandarin - Native"],
    projects=[
        Project(
            title="Customer Churn Prediction",
            tools="Python, TensorFlow, Pandas",
            description=[
                "Built ML model to predict customer churn",
                "Achieved 85% accuracy",
                "Deployed model to production"
            ],
            link=None
        ),
        Project(
            title="Sales Forecasting System",
            tools="Python, Scikit-learn, SQL",
            description=[
                "Created time-series forecasting model",
                "Integrated with business intelligence tools",
                "Improved forecast accuracy by 30%"
            ],
            link="https://github.com/carol/sales-forecast"
        )
    ],
    experience=[
        Experience(
            title="Data Scientist",
            company="Analytics Hub",
            date="2021 - Present",
            description=[
                "Developed machine learning models for business insights",
                "Conducted statistical analysis on large datasets",
                "Collaborated with stakeholders to define requirements",
                "Presented findings to executive team"
            ]
        ),
        Experience(
            title="Data Analyst",
            company="Marketing Solutions",
            date="2019 - 2021",
            description=[
                "Analyzed customer behavior data",
                "Created dashboards and reports",
                "Performed A/B testing"
            ]
        )
    ],
    education=[
        Education(
            degree="Master of Science",
            field="Data Science",
            school_name="University of California",
            date="2017 - 2019"
        ),
        Education(
            degree="Bachelor of Science",
            field="Mathematics",
            school_name="State College",
            date="2013 - 2017"
        )
    ]
)

Carol_job = JobApplication(
    job_id="xyz-789-ghi-012",
    user_id="Carol",
    job_requirements=JobRequirements(
        job_title="Senior ML Engineer",
        company="AI Innovations Lab",
        key_skills=["Python", "TensorFlow", "PyTorch", "MLOps", "Kubernetes"],
        important_keywords=["deep learning", "production ML", "scalable", "real-time inference"],
        responsibilities=[
            "Design ML infrastructure",
            "Deploy models to production",
            "Optimize model performance"
        ],
        company_values=["innovation", "research-driven", "collaboration"],
        tone="technical"
    ),
    suggestions=[
        Suggestion(
            type="update_field",
            section="job_title",
            current_value="Data Scientist",
            suggested_value="Senior ML Engineer",
            reason="Match job title exactly",
            status="pending"
        ),
        Suggestion(
            type="rewrite",
            section="bio",
            current_value="Data scientist with expertise in machine learning and statistical analysis. Experienced in building predictive models.",
            suggested_value="Senior ML Engineer specializing in production ML systems and deep learning. Expert in building scalable, real-time inference pipelines.",
            reason="Emphasize production ML, deep learning, scalability keywords",
            status="pending"
        ),
        Suggestion(
            type="rewrite",
            section="experience",
            target_item_index=0,
            target_field="description",
            target_field_index=0,
            current_value="Developed machine learning models for business insights",
            suggested_value="Designed and deployed production-grade machine learning systems with real-time inference capabilities",
            reason="Add production ML and real-time keywords",
            status="pending"
        ),
        Suggestion(
            type="rewrite",
            section="projects",
            target_item_index=0,
            target_field="description",
            target_field_index=2,
            current_value="Deployed model to production",
            suggested_value="Deployed scalable ML model to production using MLOps best practices and containerization",
            reason="Add MLOps and scalability keywords",
            status="pending"
        )
    ],
    status="pending",
    analysis_model="full"
)

# # Zapisz wszystkie do storage
storage.save_base_cv("Alice", Alice_base_cv)
storage.save_job_application("Alice", Alice_job.job_id, Alice_job)

storage.save_base_cv("Bob", Bob_base_cv)
storage.save_job_application("Bob", Bob_job.job_id, Bob_job)

storage.save_base_cv("Carol", Carol_base_cv)
storage.save_job_application("Carol", Carol_job.job_id, Carol_job)

# print("✅ Saved 3 users with base CVs and job applications!")