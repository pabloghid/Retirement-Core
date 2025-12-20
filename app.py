from fastapi import FastAPI
from models import (
    Session, User, Portfolio, PortfolioPositions, UserIncome, UserExpense, ExpenseCategory
)
from schemas import *
from services.simulation import summarize_sim
import requests

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

@app.get("/users/{user_id}/portfolio/positions", tags=["portfolio"])
def read_portfolio_positions(user_id: int):
    session = Session()
    positions = session.query(PortfolioPositions).join(Portfolio).filter(Portfolio.user_id == user_id).all()
    return [position.to_dict() for position in positions]

@app.post("/users/{user_id}/portfolio/positions", tags=["portfolio"])
def add_portfolio_position(user_id: int, asset: str, amount: float, indexer: str):
    try:
        session = Session()
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            return {"error": "Portfólio não encontrado"}
        
        indexer=indexer.lower()
        if indexer not in ['ibov', 'ipca', 'selic']:
            return {"error": "Indexador inválido. Use 'ibov', 'ipca' ou 'selic'."}
        
        new_position = PortfolioPositions(
            portfolio_id=portfolio.id,
            asset=asset,
            amount=amount,
            indexer=indexer
        )
        session.add(new_position)
        session.commit()
        session.refresh(new_position)
        return new_position.to_dict()
    except Exception as e:
        print(f"Erro ao adicionar posição ao portfólio: {e}")
        return {"error": "Falha ao adicionar posição ao portfólio"}

@app.get("/users/{user_id}/incomes", tags=["finances"])
def read_user_incomes(user_id: int):
    session = Session()
    incomes = session.query(UserIncome).filter(UserIncome.user_id == user_id).all()
    return [income.to_dict() for income in incomes]

@app.post("/users/{user_id}/incomes", tags=["finances"])
def add_user_income(user_id: int, amount: float, source: str): 
    try:
        session = Session()
        new_income = UserIncome(
            user_id=user_id,
            amount=amount,
            source=source
        )
        session.add(new_income)
        session.commit()
        session.refresh(new_income)
        return new_income.to_dict()
    except Exception as e:
        print(f"Erro ao adicionar renda do usuário: {e}")
        return {"error": "Falha ao adicionar renda do usuário"}

@app.put("/users/{user_id}/incomes/{income_id}", tags=["finances"])
def update_user_income(user_id: int, income_id: int, amount: float, source: str):
    try:
        session = Session()
        income = session.query(UserIncome).filter(UserIncome.id == income_id, UserIncome.user_id == user_id).first()
        if not income:
            return {"error": "Renda não encontrada"}
        income.amount = amount
        income.source = source
        session.commit()
        return income.to_dict()
    except Exception as e:
        print(f"Erro ao atualizar renda do usuário: {e}")
        return {"error": "Falha ao atualizar renda do usuário"}

@app.delete("/users/{user_id}/incomes/{income_id}", tags=["finances"])
def delete_user_income(user_id: int, income_id: int):
    try:
        session = Session()
        income = session.query(UserIncome).filter(UserIncome.id == income_id, UserIncome.user_id == user_id).first()
        if not income:
            return {"error": "Renda não encontrada"}
        session.delete(income)
        session.commit()
        return {"message": "Renda deletada com sucesso"}
    except Exception as e:
        print(f"Erro ao deletar renda do usuário: {e}")
        return {"error": "Falha ao deletar renda do usuário"}

@app.get("/users/{user_id}/expenses", tags=["finances"])
def read_user_expenses(user_id: int):
    session = Session()
    expenses = session.query(UserExpense).filter(UserExpense.user_id == user_id).all()
    return [expense.to_dict() for expense in expenses]

@app.post("/users/{user_id}/expenses", tags=["finances"])
def add_user_expense(user_id: int, amount: float, category: str):
    try:
        session = Session()
        category_enum = None
        category = category.lower()
        try:
            category_enum = ExpenseCategory[category]
        except KeyError:
            try:
                category_enum = ExpenseCategory[category.lower()]
            except Exception:
                category_enum = ExpenseCategory.other
        new_expense = UserExpense(
            user_id=user_id,
            amount=amount,
            category=category_enum
        )
        session.add(new_expense)
        session.commit()
        session.refresh(new_expense)
        return new_expense.to_dict()
    except Exception as e:
        print(f"Erro ao adicionar despesa do usuário: {e}")
        return {"error": "Falha ao adicionar despesa do usuário"}
    
@app.put("/users/{user_id}/expenses/{expense_id}", tags=["finances"])
def update_user_expense(user_id: int, expense_id: int, amount: float, category: str):
    try:
        session = Session()
        expense = session.query(UserExpense).filter(UserExpense.id == expense_id, UserExpense.user_id == user_id).first()
        if not expense:
            return {"error": "Despesa não encontrada"}
        try:
            category_enum = ExpenseCategory[category]
        except KeyError:
            try:
                category_enum = ExpenseCategory[category.lower()]
            except Exception:
                category_enum = ExpenseCategory.other
                
        expense.amount = amount
        expense.category = category_enum

        session.commit()
        return expense.to_dict()
    except Exception as e:
        print(f"Erro ao atualizar despesa do usuário: {e}")
        return {"error": "Falha ao atualizar despesa do usuário"}

@app.delete("/users/{user_id}/expenses/{expense_id}", tags=["finances"])
def delete_user_expense(user_id: int, expense_id: int):
    try:
        session = Session()
        expense = session.query(UserExpense).filter(UserExpense.id == expense_id, UserExpense.user_id == user_id).first()
        if not expense:
            return {"error": "Despesa não encontrada"}
        session.delete(expense)
        session.commit()
        return {"message": "Despesa deletada com sucesso"}
    except Exception as e:
        print(f"Erro ao deletar despesa do usuário: {e}")
        return {"error": "Falha ao deletar despesa do usuário"}
    
@app.post("/simulate-retirement", tags=["Simulation"])
async def simulate_retirement(user_id: int, retirement_age: int):
    try:
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "Usuário não encontrado"}
        
        portfolio = session.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            return {"error": "Portfólio do usuário não encontrado"}
        
        portfolio_positions = session.query(PortfolioPositions).filter(PortfolioPositions.portfolio_id == portfolio.id).all()
        if not portfolio_positions:
            return {"error": "Posições do portfólio não encontradas"}

        portfolio_clean = []
        for position in portfolio_positions:
            portfolio_clean.append({
                "amount": position.amount,
                "asset": position.asset,
                "indexer": position.indexer
            })

        incomes = session.query(UserIncome).filter(UserIncome.user_id == user_id).all()
        expenses = session.query(UserExpense).filter(UserExpense.user_id == user_id).all()
        
        income_clean = []
        for income in incomes:
            income_clean.append({
                "amount": income.amount,
                "source": income.source
            })
            
        expenses_clean = []
        for expense in expenses:
            expenses_clean.append({
                "amount": expense.amount,
                "category": expense.category.value
            })
            
        
        payload = {
            "current_age": user.age,
            "retirement_age": retirement_age,
            "risk_profile": user.risk_profile,
            "portfolio": portfolio_clean,
            "incomes": income_clean,
            "expenses": expenses_clean
        }
        
        response = requests.post(
            "http://retirement-simulator:8001/simulate-retirement",
            json=payload
        )
        if response.status_code != 200:
            return {"error": "Failed to get simulation results"}
    
        summary = summarize_sim(response.json())
        return summary

    except Exception as e:
        print(f"Erro ao simular aposentadoria: {e}")
        return {"error": "Falha ao simular aposentadoria"}

@app.get("/economic-indicators", tags=["Simulation"])
async def get_indicators():
    try:
        response = requests.get("http://retirement-simulator:8001/indicators")
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception as e:
        print(f"Erro ao obter indicadores econômicos: {e}")
        return None

@app.post("/estimate-inss", tags=["Simulation"])
async def estimate_inss(user_id: int, years_of_contribution: int):
    try:
        user_salary = Session().query(UserIncome).filter(UserIncome.user_id == user_id and UserIncome.source == "salary").all()
        if not user_salary:
            return None

        salary = user_salary[0].amount
        payload = {
            "average_salary": salary,
            "years_contributed": years_of_contribution,
        }

        response = requests.post(
            "http://retirement-simulator:8001/estimate-inss",
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception as e:
        print(f"Erro ao estimar INSS: {e}")
        return None
    
@app.post("/estimate-real-value", tags=["Simulation"])
async def real_value(data: RealValueRequest):
    try:
        payload = {
            "current_value": data.current_value,
            "years": data.years
        }
        response = requests.post(
            "http://retirement-simulator:8001/real-value",
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            return data
        return None
    except Exception as e:
        print(f"Erro ao estimar valor real: {e}")
        return None