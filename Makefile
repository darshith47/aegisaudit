# ==============================================================================
# AegisAudit Platform Automation Makefile
# ==============================================================================

.PHONY: help up down test lint format demo seed clean

help:
	@echo "AegisAudit Management Commands:"
	@echo "  make up      - Build and start full stack via Docker Compose"
	@echo "  make down    - Stop all running containers and volumes"
	@echo "  make test    - Run automated backend test suite with Pytest"
	@echo "  make lint    - Run code quality linters (Ruff, Black, MyPy)"
	@echo "  make format  - Auto-format backend code with Black and Ruff"
	@echo "  make demo    - Start stack, seed demo accounts, and show login info"
	@echo "  make seed    - Seed local database with demo accounts (Admin/Auditor/Viewer)"
	@echo "  make clean   - Remove cache files, logs, and build artifacts"

up:
	@echo "[*] Launching AegisAudit services..."
	docker compose up --build -d
	@echo "[+] Services online: Dashboard: http://localhost:3000 | API Docs: http://localhost:8000/docs"

down:
	@echo "[*] Stopping AegisAudit services..."
	docker compose down

test:
	@echo "[*] Running backend test suite..."
	cd backend && pytest -v --cov=app --cov-report=term-missing

lint:
	@echo "[*] Running Ruff linter..."
	cd backend && ruff check .
	@echo "[*] Checking code formatting with Black..."
	cd backend && black --check .
	@echo "[*] Checking static typing with MyPy..."
	cd backend && mypy app

format:
	@echo "[*] Formatting code with Black and Ruff..."
	cd backend && ruff check --fix .
	cd backend && black .

seed:
	@echo "[*] Seeding demo accounts and authorized scope..."
	cd backend && python scripts/seed.py

demo: up
	@echo "[*] Waiting for backend API to be healthy..."
	@sleep 5 || true
	@echo "[*] Seeding demonstration accounts in container..."
	docker compose exec -T backend python scripts/seed.py || cd backend && python scripts/seed.py
	@echo ""
	@echo "======================================================="
	@echo "  AegisAudit Ready for Demonstration!"
	@echo "======================================================="
	@echo "  1. Open Dashboard:  http://localhost:3000"
	@echo "  2. Log In as Admin: admin / DemoAdmin2026!"
	@echo "  3. Log In as Auditor: auditor / DemoAuditor2026!"
	@echo "  4. Log In as Viewer:  viewer / DemoViewer2026!"
	@echo "======================================================="

clean:
	@echo "[*] Cleaning caches and temporary artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f backend/.coverage backend/coverage.xml 2>/dev/null || true
