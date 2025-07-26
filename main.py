import os
import groq
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Corrected, more direct imports
import models
import schema as schemas  # since your file is named schema.py, not schemas.py
from database import engine, get_db


# This command creates the database tables from your models if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Conversational AI Service",
    description="Backend service for the conversational AI agent.",
    version="1.0.0"
)

try:
    groq_client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Failed to initialize Groq client: {e}")
    groq_client = None

@app.post("/api/chat", response_model=schemas.ChatResponse)
def chat_handler(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    """
    Main endpoint to handle chat conversations.
    """
    session_id = request.session_id

    # If no session_id is provided, create a new User and a new Session
    if not session_id:
        new_user = models.User()
        db.add(new_user)
        db.flush()

        new_session = models.Session(user_id=new_user.id)
        db.add(new_session)
        db.commit()
        session_id = new_session.id
    else:
        # If a session_id is provided, check if it's valid
        session = db.query(models.Session).filter(models.Session.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")
    
    # Save the user's message to the database
    user_message = models.Message(
        session_id=session_id,
        sender="user",
        content=request.message
    )
    db.add(user_message)
    db.commit()

    # For now, we return a simple, hardcoded response.
    db_messages = db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.timestamp.asc()).all()
    
    # 2. Format messages for the Groq API
    conversation_history = [
        {"role": msg.sender, "content": msg.content} for msg in db_messages
    ]

    # 3. Call the Groq LLM
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=conversation_history,
            model="llama3-8b-8192", # A fast and capable model
        )
        ai_reply = chat_completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LLM: {str(e)}")

    # 4. Save the REAL AI response to the database
    ai_message = models.Message(
        session_id=session_id,
        sender="ai",
        content=ai_reply
    )
    db.add(ai_message)
    db.commit()

    return schemas.ChatResponse(reply=ai_reply, session_id=session_id)
   
    # Save the AI's (hardcoded) response to the database
   