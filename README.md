# BookAroundMe - Local Book Exchange Platform

A peer-to-peer book-sharing platform built with React, Flask, and SQLite that ensures safety and privacy through local centers.

## 📚 Project Overview

**BookAroundMe** solves the safety and privacy issues of traditional P2P marketplaces by introducing **local centers** where users meet to exchange books instead of meeting strangers.

### Key Features (Planned)
- 🔒 Safe exchanges at verified local centers
- 📍 Find books near you with location-based search
- 👥 Three distinct user roles: General Users, Center Admins, Master Admins
- 🚀 Real-time book request tracking with state machine workflow
- 📊 Automated return date countdowns and analytics

## 🛠️ Tech Stack

- **Frontend:** React.js with Tailwind CSS
- **Backend:** Python Flask with SQLAlchemy ORM
- **Database:** SQLite (easily upgradable to PostgreSQL/MySQL)
- **Authentication:** Google OAuth 2.0
- **API:** RESTful architecture with Blueprints

## 📁 Project Structure

```
bookaroundyou/
├── backend/
│   ├── app/
│   │   ├── blueprints/
│   │   │   ├── auth.py          # Authentication routes
│   │   │   ├── books.py         # Book management routes
│   │   │   ├── centers.py       # Local center routes
│   │   │   └── admin.py         # Admin routes
│   │   ├── models/
│   │   │   └── models.py        # SQLAlchemy ORM models
│   │   ├── utils/               # Helper functions
│   │   └── __init__.py          # App factory
│   ├── config.py                # Configuration
│   ├── run.py                   # Entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variables template
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/          # Reusable React components
    │   ├── pages/              # Page components
    │   ├── services/           # API service calls
    │   ├── context/            # React Context (Auth, etc)
    │   ├── utils/              # Utility functions
    │   ├── App.js
    │   └── index.js
    ├── package.json
    ├── tailwind.config.js
    └── postcss.config.js
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd bookaroundyou/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google OAuth credentials
   ```

5. **Initialize database:**
   ```bash
   python -c "from app import create_app; app = create_app(); print('DB initialized')"
   ```

6. **Run the server:**
   ```bash
   python run.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd bookaroundyou/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   App runs on `http://localhost:3000`

## 📋 Feature Roadmap

### Phase 1: Foundation ✅
- [x] Backend structure with Flask Blueprints
- [x] SQLAlchemy ORM models
- [x] Frontend React setup with routing
- [x] Database schema with state machine

### Phase 2: Authentication 🔄
- [ ] Google OAuth 2.0 login
- [ ] Session management
- [ ] Role-based access control

### Phase 3: Core Features
- [ ] Book CRUD operations
- [ ] Search & filter by location/genre/language
- [ ] Book request workflow
- [ ] Local center confirmations

### Phase 4: Advanced Features
- [ ] Real-time notifications
- [ ] Admin dashboard
- [ ] Analytics
- [ ] Content moderation

## 🔄 The Book Handover Workflow

```
1. Match & Intent
   Borrower requests book → Lender confirms availability

2. The Drop-off
   Lender drops at center → Center admin confirms receipt

3. The Handover
   Borrower picks up → Center admin confirms handover

4. The Countdown
   System auto-calculates return date (e.g., 14 days)
   Both parties see countdown

5. Return & Completion
   Borrower returns to center → Center confirms return
```

## 🧪 Testing

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

## 📝 API Documentation

All API endpoints are prefixed with `/api/`:

- `/api/auth/` - Authentication endpoints
- `/api/books/` - Book management
- `/api/centers/` - Local center operations
- `/api/admin/` - Admin operations

See individual route files for detailed documentation.

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Built with ❤️ for book lovers and local communities.
