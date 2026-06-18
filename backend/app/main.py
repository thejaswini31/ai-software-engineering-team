from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base, User
from .schemas import UserCreate
from .auth import hash_password
from .schemas import LoginRequest
from .auth import verify_password
from .security import create_access_token
from .dependencies import get_current_user
from fastapi import UploadFile
from fastapi import File
from .pdf_service import (
    extract_text_from_pdf
)
import shutil
from .chunk_service import create_chunks
from .embedding_service import (
    create_embedding
)
from .vector_service import store_chunk
from .vector_service import search_chunks
from .ollama_service import ask_llm
from .models import Base, User, ChatHistory
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Software Engineering Team"
    }


@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User Registered Successfully"
    }

@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return {
            "message": "Invalid email or password"
        }

    password_valid = verify_password(
        login_data.password,
        user.password
    )

    if not password_valid:
        return {
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile")
def profile(
    current_user=Depends(
        get_current_user
    )
):

    if not current_user:

        return {
            "message": "Not Authenticated"
        }

    return {
        "message": "Access Granted",
        "user": current_user
    }

@app.post("/upload")
def upload_file(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }

@app.post("/chunk-pdf")
def chunk_pdf(
    filename: str
):

    file_path = f"uploads/{filename}"

    text = extract_text_from_pdf(
        file_path
    )

    chunks = create_chunks(text)

    return {
        "total_chunks": len(chunks),
        "chunks": chunks
    }

@app.post("/generate-embedding")
def generate_embedding(
    text: str
):

    embedding = create_embedding(
        text
    )

    return {
        "dimensions": len(embedding),
        "embedding": embedding[:10]
    }

@app.post("/store-pdf")
def store_pdf(
    filename: str
):

    file_path = f"uploads/{filename}"

    text = extract_text_from_pdf(
        file_path
    )

    chunks = create_chunks(text)

    for i, chunk in enumerate(chunks):

        embedding = create_embedding(
            chunk
        )

        store_chunk(
            chunk,
            embedding,
            i
        )

    return {
        "message": "Stored successfully",
        "chunks": len(chunks)
    }

@app.post("/search")
def search(
    question: str
):

    query_embedding = create_embedding(
        question
    )

    results = search_chunks(
        query_embedding
    )

    return results

@app.post("/chat")
def chat(
    question: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    query_embedding = create_embedding(
        question
    )

    results = search_chunks(
        query_embedding
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    answer = ask_llm(prompt)

    chat = ChatHistory(
    user_id=current_user["user_id"],
    question=question,
    answer=answer
)
    db.add(chat)
    db.commit()

    return {
    "question": question,
    "answer": answer
}

@app.get("/chat-history")
def get_chat_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = db.query(
    ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user["user_id"]
    ).all()

    return chats

@app.post("/generate-documentation")
def generate_documentation(
    code: str
):

    prompt = f"""
Generate professional
documentation for:

{code}
"""

    answer = ask_llm(prompt)

    return {
        "documentation": answer
    }

@app.post("/generate-sql")
def generate_sql(
    requirement: str
):

    prompt = f"""
Generate SQL query:

{requirement}
"""

    answer = ask_llm(prompt)

    return answer

@app.post("/interview-question")
def interview_question(
    topic: str
):

    prompt = f"""
Generate interview questions
for {topic}
"""

    answer = ask_llm(prompt)

    return answer

@app.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total_users = db.query(
        User
    ).count()

    total_chats = db.query(
        ChatHistory
    ).count()

    total_documents = len(
        search_chunks(
            create_embedding("test")
        )["ids"][0]
    )

    return {
        "total_users": total_users,
        "total_chats": total_chats,
        "total_documents": total_documents
    }

@app.post("/generate-code")
def generate_code(
    requirement: str
):

    prompt = f"""
Generate complete production-ready code.

Requirement:
{requirement}
"""

    answer = ask_llm(prompt)

    return {
        "generated_code": answer
    }

@app.post("/fix-code")
def fix_code(
    code: str
):

    prompt = f"""
Find bugs and fix this code.

Code:
{code}

Return corrected code only.
"""

    answer = ask_llm(prompt)

    return {
        "fixed_code": answer
    }

@app.post("/explain-code")
def explain_code(
    code: str
):

    prompt = f"""
Explain this code line by line.

Code:
{code}
"""

    answer = ask_llm(prompt)

    return {
        "explanation": answer
    }

@app.post("/summarize-pdf")
def summarize_pdf(
    filename: str
):

    file_path = f"uploads/{filename}"

    text = extract_text_from_pdf(
        file_path
    )

    prompt = f"""
Summarize this document:

{text[:5000]}
"""

    answer = ask_llm(prompt)

    return {
        "summary": answer
    }
    
@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    return user

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    user.name = user_data.name
    user.email = user_data.email

    db.commit()

    db.refresh(user)

    return user


@app.post("/read-pdf")
def read_pdf(
    filename: str
):

    file_path = f"uploads/{filename}"

    text = extract_text_from_pdf(
        file_path
    )

    return {
        "text": text
    }