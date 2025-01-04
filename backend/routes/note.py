from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from backend.dependencies import get_auth_user
from backend.models.note import Note
from backend.schemas.note import NoteRequest, NoteResponse

note_router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_auth_user)])


@note_router.get("", response_model=list[NoteResponse])
async def get_all():
    """Endpoint to get all notes."""
    try:
        notes = await Note.find_all().to_list()
        return notes
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while retrieving the notes"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@note_router.post("")
async def create(note_request: NoteRequest):
    """Endpoint to create a note."""
    try:
        note = await Note.find_one({"title": note_request.title})
        if note:
            return JSONResponse(
                content={"message": "Note already exists"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        await Note.add(note_request.model_dump())
        return JSONResponse(
            content={"message": "Note created successfully"},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while creating the note"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@note_router.get("/{note_id}", response_model=NoteResponse)
async def get(note_id: str):
    """Endpoint to get a note."""
    try:
        note = await Note.get_by_id(note_id)
        if not note:
            return JSONResponse(
                content={"message": "Note not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return NoteResponse(**note.model_dump())
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while retrieving the note"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@note_router.put("/{note_id}")
async def update(note_id: str, note_request: NoteRequest):
    """Endpoint to update a note."""
    try:
        note = await Note.get_by_id(note_id)
        if not note:
            return JSONResponse(
                content={"message": "Note not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await Note.update_data(note, note_request.model_dump())
        return JSONResponse(
            content={"message": "Note updated successfully"},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while updating the note"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@note_router.delete("/{note_id}")
async def delete(note_id: str):
    """Endpoint to delete a note."""
    try:
        note = await Note.get_by_id(note_id)
        if not note:
            return JSONResponse(
                content={"message": "Note not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await note.delete()
        return JSONResponse(
            content={"message": "Note deleted successfully"},
            status_code=status.HTTP_200_OK,
        )
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while deleting the note"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
