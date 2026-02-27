from sqlalchemy import create_engine, Column, String, Integer, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import POSTGRES_URL, SQLITE_URL
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    city = Column(String)
    occupation = Column(String)
    field = Column(String)

# Fallback Logic: Try Postgres, use SQLite if it fails
try:
    engine = create_engine(POSTGRES_URL, connect_args={'connect_timeout': 2})
    engine.connect()
    logger.info("Connected to PostgreSQL successfully.")
except Exception as e:
    logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite.")
    engine = create_engine(SQLITE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine, Column, String, Integer, and_, or_, text

def init_db():
    Base.metadata.create_all(bind=engine)
    if engine.name == 'postgresql':
        with engine.begin() as conn:
            # 1. Add tsvector column
            conn.execute(text("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS search_vector tsvector"))
            # 2. Add GIN Index
            conn.execute(text("CREATE INDEX IF NOT EXISTS jobs_search_idx ON jobs USING GIN (search_vector)"))
            # 3. Update existing records
            conn.execute(text("""
                UPDATE jobs SET search_vector = 
                to_tsvector('english', coalesce(occupation,'') || ' ' || coalesce(field,'') || ' ' || coalesce(city,'') || ' ' || coalesce(country,''))
                WHERE search_vector IS NULL
            """))
            # 4. Create trigger to keep it updated automatically
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
                BEGIN
                    NEW.search_vector := to_tsvector('english', coalesce(NEW.occupation,'') || ' ' || coalesce(NEW.field,'') || ' ' || coalesce(NEW.city,'') || ' ' || coalesce(NEW.country,''));
                    RETURN NEW;
                END
                $$ LANGUAGE plpgsql;
            """))
            conn.execute(text("""
                DROP TRIGGER IF EXISTS tsvectorupdate ON jobs;
                CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
                ON jobs FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();
            """))

def search_pg(params: dict):
    db = SessionLocal()
    query = db.query(Job)
    
    # If no searchable params are provided, return empty
    searchable_keys = ["country", "city", "occupation", "field"]
    search_params = {}
    for k in searchable_keys:
        val = params.get(k)
        if val:
            if isinstance(val, list):
                if len(val) > 0:
                    search_params[k] = val
            else:
                search_params[k] = val
    
    if not search_params:
        db.close()
        return [], ""

    # Implement AND logic for different fields, but OR logic within lists of synonyms
    filters = []
    
    for key in ["country", "city", "occupation", "field"]:
        if search_params.get(key):
            val = search_params[key]
            
            # Use postgres specific robust full-text search combined with ILIKE
            if engine.name == 'postgresql':
                if isinstance(val, list):
                    field_filters = []
                    for i, syn in enumerate(val):
                        # Unique Parameter binding to prevent SQL injection & param name clashes
                        pname = f"tsquery_{key}_{i}"
                        # Check vector but ALSO check the column explicitly for higher precision
                        field_filters.append(and_(
                            text(f"search_vector @@ plainto_tsquery('english', :{pname})").bindparams(**{pname: syn}),
                            getattr(Job, key).ilike(f"%{syn}%")
                        ))
                    filters.append(or_(*field_filters))
                else:
                    pname = f"tsquery_{key}_single"
                    filters.append(and_(
                        text(f"search_vector @@ plainto_tsquery('english', :{pname})").bindparams(**{pname: val}),
                        getattr(Job, key).ilike(f"%{val}%")
                    ))
            else:
                # SQLite vanilla fallback
                if isinstance(val, list):
                    field_filters = [getattr(Job, key).ilike(f"%{syn}%") for syn in val]
                    filters.append(or_(*field_filters))
                else:
                    filters.append(getattr(Job, key).ilike(f"%{val}%"))
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Capture the SQL query
    try:
        raw_sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    except Exception:
        raw_sql = str(query.statement)

    results = query.all()
    db.close()
    
    data = [
        {
            "country": job.country,
            "city": job.city,
            "occupation": job.occupation,
            "field": job.field
        } for job in results
    ]
    return data, raw_sql
