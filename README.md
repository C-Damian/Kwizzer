**Kwizzer 🎯**
A Kahoot-like interactive quiz platform built as a personal project to explore full-stack development with modern technologies. Think Kahoot, but simplified and customizable for studying from any content - whether it's a prompt or uploaded PDF files.

**🚀 The Vision**
Create a real-time quiz experience where:

- Hosts can generate quizzes from prompts or uploaded documents using AI
- Players join anonymously with just a game code and display name
- Everyone participates in live, timed questions with instant feedback

**🛠️ Tech Stack**

- Frontend: React (Vite) - Clean, responsive UI
- Backend: FastAPI - High-performance Python API
- Database: PostgreSQL - Reliable data persistence
- AI Integration: Google Gemini API - Dynamic question generation
- Real-time: WebSockets - Live game synchronization

**📍 Current State (In Development)**

**✅ Completed**

- Database Schema: Complete data models for games, users, questions, players, and answers
- Database Migrations: Alembic setup for version control
- Core API Structure: FastAPI foundation with health checks
- Game Creation Endpoint: Basic /game/create with database integration
- Anonymous User Support: Hosts can create games without registration

**🚧 In Progress**

- Question generation integration (AI stub ready)
- Player join and answer submission endpoints
- Real-time WebSocket implementation

*🎯 Next Steps*

- AI integration with Google Gemini API
- Frontend React components
- Live game session management
- File upload processing

**🏗️ Project Structure**

Kwizzer/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py   # API endpoints
│   │   ├── models.py # SQLAlchemy database models
│   │   ├── schemas.py# Pydantic request/response models
│   │   └── db.py     # Database connection
│   └── alembic/      # Database migrations
└── frontend/         # React (Vite) application
    └── src/          # React components

    
This is my playground for learning modern web development patterns, database design, real-time systems, and AI integration. Every feature is built with scalability and clean architecture in mind! 🎓