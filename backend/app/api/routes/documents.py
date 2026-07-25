from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.api.deps import get_db, get_current_user, require_role
from app.schemas.document import DocumentRead
from app.services.document_service import create_document

router = APIRouter()


@router.post("", response_model=DocumentRead, dependencies=[Depends(require_role("admin"))])
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> DocumentRead:
    try:
        return create_document(db, uploader_id=current_user.id, title=title, file=file)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from None


@router.get("", response_model=list[DocumentRead], dependencies=[Depends(require_role("admin"))])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentRead]:
    from app.models.document import Document
    from app.models.user import User

    stmt = (
        select(Document)
        .options(selectinload(Document.uploaded_by_user).selectinload(User.role))
        .order_by(Document.created_at.desc())
    )
    return list(db.scalars(stmt).all())
