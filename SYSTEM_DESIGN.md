# System Design

## Overview
- FastAPI backend handles authentication, RBAC, tasks, documents, semantic search, and analytics.
- React frontend provides a single dashboard for admin and user workflows.
- MySQL stores relational data; FAISS stores vector indexes for semantic retrieval.

## Core Data Model
- `roles`: admin and user roles.
- `users`: references `roles`.
- `tasks`: references creator and assignee users.
- `documents`: stores upload metadata and extracted text.
- `document_chunks`: stores chunked document text for vector search.
- `activity_logs`: tracks login, uploads, searches, and task updates.

## AI Search Flow
1. Admin uploads a `.txt` or `.pdf` document.
2. Backend extracts text and splits it into chunks.
3. Chunks are embedded locally using `sentence-transformers`.
4. Embeddings are stored in FAISS with chunk metadata.
5. User submits a semantic query.
6. Query text is embedded and matched against the vector index.
7. Matching chunks are returned with similarity scores.

## Security
- JWT access tokens protect all non-auth endpoints.
- Role checks enforce admin-only actions for uploads, analytics, and task creation.
- Users can only complete their assigned tasks unless they are admin.

## API Surface
- `POST /auth/login`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}/status`
- `POST /documents`
- `GET /documents`
- `POST /search`
- `GET /analytics`
