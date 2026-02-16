from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from app.api.analyze import router as analyze_router
from app.api.validate import router as validate_router

app = FastAPI(
    title="Audit Intelligence Engine",
    description="""
    Advanced audit analysis platform for comprehensive compliance and risk assessment.
    
    ## Features
    
    * **Comprehensive Analysis**: Multi-dimensional audit metrics including compliance, risk, and financial impact
    * **Data Validation**: Pre-analysis validation and data quality checks
    * **Smart Insights**: AI-powered recommendations and priority actions
    * **Risk Categorization**: Automated high/medium/low risk classification
    * **Financial Impact**: Budget analysis and risk quantification
    * **Red Flag Detection**: Automatic identification of critical issues
    
    ## Usage
    
    1. Upload your Excel file using `/api/analyze` endpoint
    2. Validate data quality with `/api/validate` endpoint
    3. Preview data with `/api/preview` endpoint
    """,
    version="2.0.0",
    contact={
        "name": "Audit Intelligence Team",
        "email": "support@auditintel.com",
    },
    license_info={
        "name": "MIT",
    }
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])
app.include_router(validate_router, prefix="/api", tags=["Validation"])


@app.get("/")
async def root():
    """
    Root endpoint - API health check and information
    """
    return {
        "app": "Audit Intelligence Engine",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "analysis": "/api/analyze",
            "validation": "/api/validate",
            "preview": "/api/preview",
            "required_columns": "/api/columns/required",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "audit-intelligence-engine"
    }

