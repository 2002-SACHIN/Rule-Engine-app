from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import SessionLocal, engine
from .core_logic import create_rule, combine_rules, evaluate_rule

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rules/", response_model=schemas.Rule)
def create_new_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    return create_rule(db, rule.rule_string, rule.name, rule.description)

@app.post("/rules/combine/", response_model=schemas.Rule)
def combine_existing_rules(rule_combine: schemas.RuleCombine, db: Session = Depends(get_db)):
    return combine_rules(db, rule_combine.rule_ids, rule_combine.new_rule_name)

@app.post("/rules/{rule_id}/evaluate/", response_model=schemas.RuleEvaluationResult)
def evaluate_existing_rule(rule_id: int, data: schemas.UserData, db: Session = Depends(get_db)):
    result = evaluate_rule(db, rule_id, data.dict())
    return {"result": result}

@app.get("/rules/", response_model=List[schemas.Rule])
def get_all_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = db.query(models.Rule).offset(skip).limit(limit).all()
    return rules

@app.get("/rules/{rule_id}", response_model=schemas.Rule)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule

@app.put("/rules/{rule_id}", response_model=schemas.Rule)
def update_rule(rule_id: int, rule: schemas.RuleUpdate, db: Session = Depends(get_db)):
    db_rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    for var, value in vars(rule).items():
        setattr(db_rule, var, value) if value else None
    db.commit()
    db.refresh(db_rule)
    return db_rule

@app.delete("/rules/{rule_id}", response_model=schemas.RuleDeletion)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = db.query(models.Rule).filter(models.Rule.id == rule_id).first()
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    db.delete(db_rule)
    db.commit()
    return {"success": True, "message": f"Rule {rule_id} has been deleted"}
