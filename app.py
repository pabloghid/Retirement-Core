from fastapi import FastAPI
from models import Session, User, Portfolio, PortfolioPositions
from schemas import *

app = FastAPI(
    title="API Principal Aposentadoria",
    version="1.0.0",
)

@app.get("/users", tags=["users"], response_model=list[UserSchema])
def read_users():
    session = Session()
    users = session.query(User).all()
    return [user.to_dict() for user in users]

@app.get("/users/{user_id}", tags=["users"], response_model=UserSchema | dict)
def read_user(user_id: int):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return user.to_dict()
    return {}

@app.post("/users", tags=["users"])
def create_user(payload: UserSchema):
    try:
        session = Session()
        new_user = User(
            name=payload.name,
            email=payload.email,
            age=payload.age,
            risk_profile=payload.risk_profile
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.to_dict()
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return {"error": "Falha ao criar usuário"}

@app.put("/users/{user_id}", tags=["users"])
def update_user(user_id: int, payload: UserSchema):
    try:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "Usuário não encontrado"}
        user.name = payload.name
        user.email = payload.email
        user.age = payload.age
        user.risk_profile = payload.risk_profile
        session.commit()
        return user.to_dict()
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return {"error": "Falha ao atualizar usuário"}

@app.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int):
    try:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "Usuário não encontrado"}
        session.delete(user)
        session.commit()
        return {"message": "Usuário deletado com sucesso"}
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return {"error": "Falha ao deletar usuário"}

@app.get("/users/{user_id}/portfolio", tags=["portfolio"])
def read_user_portfolio(user_id: int):
    session = Session()
    portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
    if portfolio:
        return portfolio.to_dict()
    return {"error": "Portfólio não encontrado"}

@app.post("/users/{user_id}/portfolio", tags=["portfolio"])
def create_user_portfolio(user_id: int, total_allocation: float):
    try:
        session = Session()
        new_portfolio = Portfolio(
            user_id=user_id,
            total_allocation=total_allocation
        )
        session.add(new_portfolio)
        session.commit()
        session.refresh(new_portfolio)
        return new_portfolio.to_dict()
    except Exception as e:
        print(f"Erro ao criar portfólio: {e}")
        return {"error": "Falha ao criar portfólio"}
    
@app.put("/users/{user_id}/portfolio", tags=["portfolio"])
def update_user_portfolio(user_id: int, total_allocation: float):
    try:
        session = Session()
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            return {"error": "Portfólio não encontrado"}
        portfolio.total_allocation = total_allocation
        session.commit()
        return portfolio.to_dict()
    except Exception as e:
        print(f"Erro ao atualizar portfólio: {e}")
        return {"error": "Falha ao atualizar portfólio"}
    
@app.delete("/users/{user_id}/portfolio", tags=["portfolio"])
def delete_user_portfolio(user_id: int):
    try:
        session = Session()
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            return {"error": "Portfólio não encontrado"}
        session.delete(portfolio)
        session.commit()
        return {"message": "Portfólio deletado com sucesso"}
    except Exception as e:
        print(f"Erro ao deletar portfólio: {e}")
        return {"error": "Falha ao deletar portfólio"}
    
@app.post("/users/{user_id}/portfolio/positions", tags=["portfolio"])
def add_portfolio_position(user_id: int, asset: str, percentage: float):
    try:
        session = Session()
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            return {"error": "Portfólio não encontrado"}
        new_position = PortfolioPositions(
            portfolio_id=portfolio.id,
            asset=asset,
            percentage=percentage
        )
        session.add(new_position)
        session.commit()
        session.refresh(new_position)
        return new_position.to_dict()
    except Exception as e:
        print(f"Erro ao adicionar posição ao portfólio: {e}")
        return {"error": "Falha ao adicionar posição ao portfólio"}